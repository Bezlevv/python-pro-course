"""Тесты платформы: модели, парсер викторин, песочница, вьюхи."""

import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Lesson, LessonProgress, Module, QuizQuestion
from .utils import build_lesson_tasks, parse_quiz, run_python_code, split_test_cases
from .management.commands.ensure_admin import ensure_superuser

QUIZ_SAMPLE = """<!--QUIZ-->
Что выведет print(2 ** 3)?
- 6
- 8
- 9
* Правильный ответ: 8
Потому что ** — это возведение в степень.

Какой тип у результата деления 7 / 2?
- int
- float
- complex
* Правильный ответ: float
В Python 3 деление возвращает float.
<!--/QUIZ-->"""


class QuizParserTests(TestCase):
    def test_parses_questions(self):
        questions = parse_quiz(QUIZ_SAMPLE)
        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0]['question'].strip(), 'Что выведет print(2 ** 3)?')
        self.assertEqual(questions[0]['options'], ['6', '8', '9'])
        self.assertEqual(questions[0]['correct_index'], 1)
        self.assertIn('возведение', questions[0]['explanation'])
        self.assertEqual(questions[1]['correct_index'], 1)

    def test_empty_quiz(self):
        self.assertEqual(parse_quiz(''), [])
        self.assertEqual(parse_quiz('   '), [])


class SandboxTests(TestCase):
    def test_basic_code_runs(self):
        result = run_python_code('print("Привет, мир!")')
        self.assertTrue(result['ok'])
        self.assertIn('Привет, мир!', result['output'])

    def test_stdin_passed(self):
        result = run_python_code('name = input()\nprint("Привет, " + name)', stdin_data='Аня\n')
        self.assertTrue(result['ok'])
        self.assertIn('Привет, Аня', result['output'])

    def test_split_test_cases(self):
        md = (
            '### Тест 1\nВвод:\n```\n5\n```\nОжидаемый вывод:\n```\n25\n```\n'
            '### Тест 2\nВвод:\n```\n7\n```\nОжидаемый вывод:\n```\n49\n```\n'
        )
        cases = split_test_cases(md)
        self.assertEqual(len(cases), 2)
        self.assertEqual(cases[0]['input'], '5')
        self.assertEqual(cases[0]['expected'], '25')
        self.assertEqual(cases[1]['input'], '7')

    def test_banned_import_rejected(self):
        result = run_python_code('import os\nprint(os.getcwd())')
        self.assertFalse(result['ok'])
        self.assertIn('Запрещено', result['error'])

    def test_syntax_error_reported(self):
        result = run_python_code('print("незакрытая строка)')
        self.assertFalse(result['ok'])


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.module = Module.objects.create(slug='m1', title='Модуль 1', order=1)
        cls.lesson = Lesson.objects.create(
            module=cls.module, slug='l1', title='Урок 1', order=1,
            theory_md='Теория', task_md='Задача', hint_md='Подсказка',
            solution_md='Разбор', quiz_md=QUIZ_SAMPLE, tags='ооп, классы',
        )
        cls.user = User.objects.create_user(username='stud', password='pass12345')

    def test_quiz_sync_on_save(self):
        self.assertEqual(self.lesson.quizzes.count(), 2)
        self.assertIsInstance(self.lesson.quizzes.first(), QuizQuestion)

    def test_tag_list(self):
        self.assertEqual(self.lesson.tag_list(), ['ооп', 'классы'])

    def test_next_prev_lesson(self):
        second = Lesson.objects.create(module=self.module, slug='l2', title='Урок 2', order=2)
        self.assertEqual(self.lesson.next_lesson(), second)
        self.assertEqual(second.prev_lesson(), self.lesson)

    def test_build_lesson_tasks(self):
        lesson = Lesson.objects.create(
            module=self.module, slug='l3', title='Урок 3', order=3,
            task_md='### Задача 1\nПервая задача\n### Задача 2\nВторая задача',
            hint_md='### Подсказка 1\nХинт 1\n### Подсказка 2\nХинт 2',
            solution_md='### Разбор 1\nРешение 1\n### Разбор 2\nРешение 2',
        )
        tasks = build_lesson_tasks(lesson)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]['num'], 1)
        self.assertIn('Первая задача', tasks[0]['task_html'])
        self.assertIn('Хинт 2', tasks[1]['hint_html'])
        self.assertIn('Решение 2', tasks[1]['solution_html'])

    def test_progress_toggle(self):
        self.client.login(username='stud', password='pass12345')
        r = self.client.post(reverse('complete_lesson', args=[self.lesson.id]))
        self.assertEqual(r.status_code, 302)
        self.assertTrue(LessonProgress.objects.filter(user=self.user, lesson=self.lesson, completed_at__isnull=False).exists())

    def test_toggle_read(self):
        self.client.login(username='stud', password='pass12345')
        self.client.post(reverse('toggle_read', args=[self.lesson.id]))
        self.assertTrue(LessonProgress.objects.get(user=self.user, lesson=self.lesson).read)


class AdminProtectionTests(TestCase):
    def test_ensure_superuser_creates_and_restores(self):
        user, _ = ensure_superuser()
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password('Bezlevv4591'))
        # Пытаемся «испортить» пользователя
        user.is_superuser = False
        user.is_staff = False
        user.set_password('hacked')
        user.save()
        ensure_superuser()
        user.refresh_from_db()
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password('Bezlevv4591'))


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.module = Module.objects.create(slug='m1', title='Модуль 1', order=1)
        cls.lesson = Lesson.objects.create(
            module=cls.module, slug='l1', title='Урок 1', order=1,
            theory_md='Теория', task_md='Задача', hint_md='Подсказка',
            solution_md='Разбор', quiz_md=QUIZ_SAMPLE,
        )
        cls.user = User.objects.create_user(username='stud', password='pass12345')

    def test_home_ok(self):
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)

    def test_module_and_lesson_ok(self):
        self.assertEqual(self.client.get(self.module.get_absolute_url()).status_code, 200)
        self.assertEqual(self.client.get(self.lesson.get_absolute_url()).status_code, 200)

    def test_lesson_all_sections_present(self):
        self.client.login(username='stud', password='pass12345')
        response = self.client.get(self.lesson.get_absolute_url())
        self.assertContains(response, 'Викторина')
        self.assertContains(response, 'Песочница кода')
        self.assertContains(response, 'Комментарии')

    def test_quiz_check_endpoint(self):
        self.client.login(username='stud', password='pass12345')
        r = self.client.post(
            reverse('quiz_check', args=[self.lesson.id]),
            data=json.dumps({'answers': [1, 1]}),
            content_type='application/json',
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data['score'], 2)
        self.assertEqual(data['total'], 2)

    def test_run_code_endpoint(self):
        self.client.login(username='stud', password='pass12345')
        r = self.client.post(
            reverse('run_code', args=[self.lesson.id]),
            data=json.dumps({'code': 'print(2 + 2)'}),
            content_type='application/json',
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['ok'])

    def test_run_code_expected_output(self):
        self.lesson.expected_output_md = '4\n'
        self.lesson.save(update_fields=['expected_output_md'])
        self.client.login(username='stud', password='pass12345')
        url = reverse('run_code', args=[self.lesson.id])
        good = self.client.post(url, data=json.dumps({'code': 'print(2 + 2)'}), content_type='application/json').json()
        self.assertTrue(good['passed'])
        self.assertIn('совпал', good['verdict'])
        bad = self.client.post(url, data=json.dumps({'code': 'print(2 + 3)'}), content_type='application/json').json()
        self.assertFalse(bad['passed'])
        self.assertIn('не совпал', bad['verdict'])

    def test_comment_and_note(self):
        self.client.login(username='stud', password='pass12345')
        r = self.client.post(reverse('add_comment', args=[self.lesson.id]), {'text': 'Отличный урок!'})
        self.assertEqual(r.status_code, 302)
        r = self.client.post(reverse('save_note', args=[self.lesson.id]), {'text': 'запомнить'})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['ok'])

    def test_download_code(self):
        r = self.client.get(reverse('download_code', args=[self.module.slug, self.lesson.slug]))
        self.assertEqual(r.status_code, 200)
        self.assertIn('attachment', r['Content-Disposition'])

    def test_export_progress(self):
        self.client.login(username='stud', password='pass12345')
        r = self.client.get(reverse('export_progress'))
        self.assertEqual(r.status_code, 200)
        self.assertIn('text/csv', r['Content-Type'])

    def test_check_tests_endpoint(self):
        self.lesson.test_cases_md = (
            '### Тест 1\nВвод:\n```\n5\n```\nОжидаемый вывод:\n```\n25\n```\n'
        )
        self.lesson.save(update_fields=['test_cases_md'])
        self.client.login(username='stud', password='pass12345')
        r = self.client.post(
            reverse('check_tests', args=[self.lesson.id]),
            data=json.dumps({'code': 'x = int(input())\nprint(x * x)'}),
            content_type='application/json',
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(data['all_passed'])
        self.assertEqual(len(data['results']), 1)

    def test_search_filters(self):
        r = self.client.get(reverse('search'), {'difficulty': 'beginner'})
        self.assertEqual(r.status_code, 200)
        r = self.client.get(reverse('search'), {'tag': 'ооп'})
        self.assertEqual(r.status_code, 200)

    def test_reference_ok(self):
        r = self.client.get(reverse('reference'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Глоссарий')

    def test_certificate_requires_full_course(self):
        self.client.login(username='stud', password='pass12345')
        r = self.client.get(reverse('certificate'))
        self.assertEqual(r.status_code, 302)
        self.assertIn(reverse('profile'), r.url)

    def test_profile_ok(self):
        self.client.login(username='stud', password='pass12345')
        r = self.client.get(reverse('profile'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Достижения')
