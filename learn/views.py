import csv
import json
import re
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import (
    Achievement,
    CodeAttempt,
    Comment,
    Lesson,
    LessonNote,
    LessonProgress,
    Module,
    UserAchievement,
)
from .utils import (
    build_lesson_tasks,
    lesson_difficulty_label,
    normalize_output,
    render_markdown,
    run_python_code,
    split_test_cases,
)


# ---------- Вспомогательное ----------

def _module_progress(user):
    if not user.is_authenticated:
        return {}
    rows = (
        LessonProgress.objects
        .filter(user=user, completed_at__isnull=False)
        .values('lesson__module')
        .annotate(done=Count('id'))
    )
    return {row['lesson__module']: row['done'] for row in rows}


def _modules_data(user):
    progress = _module_progress(user)
    data = []
    for module in Module.objects.annotate(lesson_count=Count('lessons')):
        total = module.lesson_count
        done = progress.get(module.id, 0)
        data.append({
            'module': module,
            'total': total,
            'done': done,
            'pct': round(done / total * 100) if total else 0,
        })
    return data


def _streak(user):
    days = {
        d.date() for d in
        LessonProgress.objects.filter(user=user, completed_at__isnull=False)
        .values_list('completed_at', flat=True)
    }
    today = date.today()
    current = today if today in days else today - timedelta(days=1)
    streak = 0
    while current in days:
        streak += 1
        current -= timedelta(days=1)
    return streak


LEVELS = [
    (0, '🐣 Новичок'),
    (300, '🌱 Ученик'),
    (800, '📘 Программист'),
    (1500, '⚙️ Разработчик'),
    (2500, '🚀 Продвинутый'),
    (4000, '🧙 Эксперт'),
    (6000, '🏆 Senior'),
]


def xp_for_user(user):
    """Очки опыта: 100 за решённый урок + 50 за достижение."""
    done = LessonProgress.objects.filter(user=user, completed_at__isnull=False).count()
    ach = UserAchievement.objects.filter(user=user).count()
    return done * 100 + ach * 50


def level_info(xp):
    """Возвращает уровень по XP: имя, пороги, прогресс до следующего."""
    current_index = 0
    for i, (threshold, name) in enumerate(LEVELS):
        if xp >= threshold:
            current_index = i
    current_threshold, current_name = LEVELS[current_index]
    if current_index + 1 < len(LEVELS):
        next_threshold = LEVELS[current_index + 1][0]
        progress = round((xp - current_threshold) / (next_threshold - current_threshold) * 100) \
            if next_threshold > current_threshold else 0
        return {
            'name': current_name, 'xp': xp, 'index': current_index,
            'current_threshold': current_threshold,
            'next_threshold': next_threshold,
            'progress': progress,
        }
    return {'name': current_name, 'xp': xp, 'index': current_index,
            'current_threshold': current_threshold, 'next_threshold': None, 'progress': 100}


def _completed_modules_count(user):
    total = 0
    for module in Module.objects.annotate(cnt=Count('lessons')):
        done = LessonProgress.objects.filter(
            user=user, lesson__module=module, completed_at__isnull=False
        ).count()
        if module.cnt and done >= module.cnt:
            total += 1
    return total


def _award_achievements(user):
    """Выдаёт достижения, которые пользователь уже заслужил."""
    stats = {
        'lessons_count': LessonProgress.objects.filter(user=user, completed_at__isnull=False).count(),
        'modules_complete': _completed_modules_count(user),
        'streak_days': _streak(user),
    }
    awarded = []
    for ach in Achievement.objects.all():
        if stats.get(ach.kind, 0) >= ach.threshold and \
                not UserAchievement.objects.filter(user=user, achievement=ach).exists():
            UserAchievement.objects.create(user=user, achievement=ach)
            awarded.append(ach)
    return awarded


def _lesson_ctx(request, lesson):
    done_ids = set()
    read_ids = set()
    if request.user.is_authenticated:
        progress_rows = LessonProgress.objects.filter(user=request.user)
        done_ids = set(progress_rows.filter(completed_at__isnull=False).values_list('lesson_id', flat=True))
        read_ids = set(progress_rows.filter(read=True).values_list('lesson_id', flat=True))
    module_lessons = list(lesson.module.lessons.all())
    note = ''
    if request.user.is_authenticated:
        note_obj = LessonNote.objects.filter(user=request.user, lesson=lesson).first()
        note = note_obj.text if note_obj else ''
    return {
        'lesson': lesson,
        'theory_html': render_markdown(lesson.theory_md),
        'tasks': build_lesson_tasks(lesson),
        'module_lessons': module_lessons,
        'done_ids': done_ids,
        'read_ids': read_ids,
        'difficulty_label': lesson_difficulty_label(lesson.difficulty),
        'next_lesson': lesson.next_lesson(),
        'prev_lesson': lesson.prev_lesson(),
        'is_done': lesson.id in done_ids,
        'is_read': lesson.id in read_ids,
        'tags': lesson.tag_list(),
        'quizzes': list(lesson.quizzes.all()),
        'comments': list(lesson.comments.select_related('user')),
        'note': note,
        'is_exam': lesson.is_exam,
        'has_tests': bool(lesson.test_cases_md.strip()),
        'module_done': sum(1 for l in module_lessons if l.id in done_ids),
        'module_pct': round(sum(1 for l in module_lessons if l.id in done_ids) / len(module_lessons) * 100) if module_lessons else 0,
    }


# ---------- Страницы ----------

def home(request):
    modules_data = _modules_data(request.user)
    total_lessons = Lesson.objects.count()
    completed = sum(item['done'] for item in modules_data)
    recent = Lesson.objects.select_related('module').order_by('-created')[:6]
    return render(request, 'home.html', {
        'modules_data': modules_data,
        'total_lessons': total_lessons,
        'completed': completed,
        'completed_pct': round(completed / total_lessons * 100) if total_lessons else 0,
        'recent': recent,
    })


def module_list(request):
    return render(request, 'modules.html', {'modules_data': _modules_data(request.user)})


def module_detail(request, module_slug):
    module = get_object_or_404(Module.objects.annotate(lesson_count=Count('lessons')), slug=module_slug)
    lessons = list(module.lessons.all())
    done_ids = set()
    if request.user.is_authenticated:
        done_ids = set(
            LessonProgress.objects.filter(user=request.user, lesson__module=module, completed_at__isnull=False)
            .values_list('lesson_id', flat=True)
        )
    return render(request, 'module_detail.html', {
        'module': module,
        'lessons': lessons,
        'done_ids': done_ids,
        'done_count': sum(1 for l in lessons if l.id in done_ids),
        'pct': round(sum(1 for l in lessons if l.id in done_ids) / len(lessons) * 100) if lessons else 0,
    })


def lesson_detail(request, module_slug, lesson_slug):
    module = get_object_or_404(Module, slug=module_slug)
    lesson = get_object_or_404(Lesson, module=module, slug=lesson_slug)
    return render(request, 'lesson_detail.html', _lesson_ctx(request, lesson))


@require_POST
@login_required
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    if created:
        progress.completed_at = None  # auto_now проставит время при save
        progress.save()
        awarded = _award_achievements(request.user)
        text = f'Отлично! Урок «{lesson.title}» отмечен решённым 🎉'
        if awarded:
            icons = ' '.join(a.icon for a in awarded)
            text += f' Новые достижения: {icons}'
        messages.success(request, text)
    else:
        progress.completed_at = None
        progress.save()
        messages.info(request, f'Отметка «{lesson.title}» снята.')
    return redirect(lesson.get_absolute_url())


@require_POST
@login_required
def toggle_read(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.read = not progress.read
    progress.save()
    return redirect(lesson.get_absolute_url())


@require_POST
@login_required
def check_tests(request, lesson_id):
    """Автопроверка кода по тест-кейсам урока."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    try:
        payload = json.loads(request.body or '{}')
    except ValueError:
        payload = {}
    code = payload.get('code', '')
    if not code.strip():
        return JsonResponse({'ok': False, 'error': 'Введи код для запуска'})

    cases = split_test_cases(lesson.test_cases_md)
    if not cases:
        return JsonResponse({'ok': False, 'error': 'У урока нет тест-кейсов'})

    results = []
    all_passed = True
    for case in cases:
        res = run_python_code(code, stdin_data=case['input'])
        passed = bool(res['ok']) and normalize_output(res['output']) == normalize_output(case['expected'])
        if not passed:
            all_passed = False
        results.append({
            'num': case['num'],
            'passed': passed,
            'error': res['error'],
            'output': res['output'][:4000],
            'expected': case['expected'][:1000],
            'input': case['input'][:500],
        })

    summary = '\n'.join(f'Тест {r["num"]}: {"OK" if r["passed"] else "FAIL"}' for r in results)
    CodeAttempt.objects.create(
        user=request.user, lesson=lesson, code=code,
        output=summary, passed=all_passed,
    )
    return JsonResponse({'ok': True, 'all_passed': all_passed, 'results': results})


@require_POST
@login_required
def run_code(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    try:
        payload = json.loads(request.body or '{}')
    except ValueError:
        payload = {}
    code = payload.get('code', '')
    if not code.strip():
        return JsonResponse({'ok': False, 'output': '', 'error': 'Введи код для запуска'})
    if len(code) > 20000:
        return JsonResponse({'ok': False, 'output': '', 'error': 'Код слишком длинный (максимум 20 000 символов)'})
    result = run_python_code(code)
    expected = lesson.expected_output_md.strip()
    if result.get('ok') and expected:
        result['passed'] = normalize_output(result['output']) == normalize_output(expected)
        result['verdict'] = (
            '✅ Вывод совпал с ожидаемым!'
            if result['passed'] else '❌ Вывод не совпал с ожидаемым — результат отличается.'
        )
    else:
        result['passed'] = bool(result.get('ok'))
        result['verdict'] = '' if result.get('ok') else 'Код завершился с ошибкой.'
    CodeAttempt.objects.create(
        user=request.user, lesson=lesson, code=code,
        output=result.get('output', ''), passed=result.get('passed'),
    )
    return JsonResponse(result)


@require_POST
def quiz_check(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    quizzes = list(lesson.quizzes.all())
    try:
        answers = json.loads(request.body or '{}').get('answers', [])
    except ValueError:
        answers = []
    results = []
    for i, q in enumerate(quizzes):
        user_answer = answers[i] if i < len(answers) else None
        correct = isinstance(user_answer, int) and user_answer == q.correct_index
        results.append({
            'correct': correct,
            'correct_index': q.correct_index,
            'explanation': q.explanation,
            'question': q.question,
        })
    score = sum(1 for r in results if r['correct'])
    return JsonResponse({'score': score, 'total': len(results), 'results': results})


@require_POST
@login_required
def add_comment(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    text = request.POST.get('text', '').strip()
    if text:
        Comment.objects.create(lesson=lesson, user=request.user, text=text[:3000])
        messages.success(request, 'Комментарий добавлен.')
    return redirect(lesson.get_absolute_url())


@require_POST
@login_required
def save_note(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    text = request.POST.get('text', '')
    LessonNote.objects.update_or_create(user=request.user, lesson=lesson, defaults={'text': text[:10000]})
    return JsonResponse({'ok': True})


def download_code(request, module_slug, lesson_slug):
    lesson = get_object_or_404(Lesson, module__slug=module_slug, slug=lesson_slug)
    raw = '\n'.join([lesson.theory_md, lesson.task_md, lesson.solution_md])
    blocks = re.findall(r'```python\s*\n(.*?)```', raw, re.S)
    parts = [f'# {lesson.title}', f'# Модуль: {lesson.module.title}', '', 'from __future__ import annotations', '']
    parts.extend(blocks)
    content = '\n\n'.join(parts)
    response = HttpResponse(content, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{lesson.slug}.py"'
    return response


@login_required
def export_progress(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="python_pro_progress.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow(['Модуль', 'Урок', 'Сложность', 'Прочитан', 'Решён', 'Дата решения', 'Теги'])
    rows = (
        LessonProgress.objects.filter(user=request.user)
        .select_related('lesson__module')
        .order_by('lesson__module__order', 'lesson__order')
    )
    for p in rows:
        writer.writerow([
            p.lesson.module.title,
            p.lesson.title,
            p.lesson.get_difficulty_display(),
            'да' if p.read else 'нет',
            'да' if p.completed_at else 'нет',
            p.completed_at.strftime('%d.%m.%Y %H:%M') if p.completed_at else '',
            p.lesson.tags,
        ])
    return response


def search(request):
    q = request.GET.get('q', '').strip()
    difficulty = request.GET.get('difficulty', '')
    tag = request.GET.get('tag', '')
    results = Lesson.objects.select_related('module')
    if q:
        results = results.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(theory_md__icontains=q))
    if difficulty in ('beginner', 'intermediate', 'advanced'):
        results = results.filter(difficulty=difficulty)
    if tag:
        results = results.filter(tags__icontains=tag)
    results = results.order_by('module__order', 'order')
    all_tags = sorted({t for lesson in Lesson.objects.all() for t in lesson.tag_list()})
    return render(request, 'search.html', {
        'q': q,
        'difficulty': difficulty,
        'tag': tag,
        'all_tags': all_tags,
        'results': results,
    })


@login_required
def profile(request):
    done = LessonProgress.objects.filter(user=request.user, completed_at__isnull=False).select_related('lesson__module')
    done_map = {p.lesson_id: p for p in done}
    modules = Module.objects.annotate(lesson_count=Count('lessons'))
    total = Lesson.objects.count()
    data = []
    for m in modules:
        lessons = list(m.lessons.all())
        done_in = sum(1 for l in lessons if l.id in done_map)
        data.append({
            'module': m,
            'total': len(lessons),
            'done': done_in,
            'pct': round(done_in / len(lessons) * 100) if lessons else 0,
        })
    last_done = sorted(done, key=lambda p: p.completed_at, reverse=True)[:5]
    # Активность за последние 14 дней
    start = date.today() - timedelta(days=13)
    day_counts = {}
    for p in done:
        d = p.completed_at.date()
        if d >= start:
            day_counts[d] = day_counts.get(d, 0) + 1
    activity = []
    for i in range(14):
        d = start + timedelta(days=i)
        activity.append((d.strftime('%d.%m'), day_counts.get(d, 0)))
    # Тепловая карта за год (недели × дни)
    year_start = date.today() - timedelta(days=364)
    counts = {}
    for p in done:
        d = p.completed_at.date()
        if d >= year_start:
            counts[d] = counts.get(d, 0) + 1
    monday = year_start - timedelta(days=year_start.weekday())
    weeks = []
    today = date.today()
    cur = monday
    while cur <= today:
        week = []
        for i in range(7):
            d = cur + timedelta(days=i)
            if d < year_start or d > today:
                week.append(None)
            else:
                week.append((d, counts.get(d, 0)))
        weeks.append(week)
        cur += timedelta(days=7)
    achievements = (
        UserAchievement.objects.filter(user=request.user)
        .select_related('achievement').order_by('achievement__order')
    )
    all_achievements = Achievement.objects.all()
    achieved_ids = {ua.achievement_id for ua in achievements}
    user_xp = xp_for_user(request.user)
    return render(request, 'profile.html', {
        'data': data,
        'total_lessons': total,
        'completed': len(done),
        'pct_total': round(len(done) / total * 100) if total else 0,
        'last_done': last_done,
        'streak': _streak(request.user),
        'achievements': achievements,
        'achieved_ids': achieved_ids,
        'all_achievements': all_achievements,
        'activity': activity,
        'heat': weeks,
        'xp': user_xp,
        'level': level_info(user_xp),
    })


def reference(request):
    """Страница «Справочник»: шпаргалки и глоссарий."""
    return render(request, 'reference.html')


def leaderboard(request):
    """Публичная таблица лидеров по опыту."""
    users = User.objects.annotate(
        done=Count('progress', filter=Q(progress__completed_at__isnull=False)),
        ach=Count('achievements'),
    ).order_by('-done')[:20]
    rows = []
    for u in users:
        xp = u.done * 100 + u.ach * 50
        rows.append({'user': u, 'xp': xp, 'level_name': level_info(xp)['name']})
    return render(request, 'leaderboard.html', {'rows': rows})


@login_required
def certificate(request):
    """Сертификат об окончании курса (страница)."""
    total = Lesson.objects.count()
    completed = LessonProgress.objects.filter(user=request.user, completed_at__isnull=False).count()
    if completed < total:
        messages.info(request, f'Сертификат станет доступен после прохождения всех {total} уроков. Сейчас пройдено {completed}.')
        return redirect('profile')
    return render(request, 'certificate.html', {'completed': completed, 'total': total})


@login_required
def certificate_pdf(request):
    """Сертификат об окончании курса (PDF)."""
    from datetime import date

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas as pdf_canvas

    total = Lesson.objects.count()
    completed = LessonProgress.objects.filter(user=request.user, completed_at__isnull=False).count()
    if completed < total:
        messages.info(request, f'Сертификат станет доступен после прохождения всех {total} уроков. Сейчас пройдено {completed}.')
        return redirect('profile')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pythonpro_certificate.pdf"'

    width, height = landscape(A4)
    c = pdf_canvas.Canvas(response, pagesize=landscape(A4))

    # Рамка
    c.setStrokeColor(colors.HexColor('#7c5cff'))
    c.setLineWidth(2.5)
    c.rect(14 * mm, 14 * mm, width - 28 * mm, height - 28 * mm)
    c.setStrokeColor(colors.HexColor('#22d3ee'))
    c.setLineWidth(0.75)
    c.rect(17 * mm, 17 * mm, width - 34 * mm, height - 34 * mm)

    c.setFillColor(colors.HexColor('#1a2130'))
    c.setFont('Helvetica-Bold', 44)
    c.drawCentredString(width / 2, height - 45 * mm, 'СЕРТИФИКАТ')

    c.setFont('Helvetica', 15)
    c.setFillColor(colors.HexColor('#4a5a78'))
    c.drawCentredString(width / 2, height - 54 * mm, 'подтверждает успешное прохождение курса')

    c.setFillColor(colors.HexColor('#7c5cff'))
    c.setFont('Helvetica-Bold', 34)
    c.drawCentredString(width / 2, height - 70 * mm, request.user.username)

    c.setFillColor(colors.HexColor('#222b3d'))
    c.setFont('Helvetica', 15)
    c.drawCentredString(width / 2, height - 82 * mm,
                        f'прошёл(ла) все {total} уроков курса «PythonПро» — от основ языка до продвинутых тем, проектов и деплоя.')

    c.setFont('Helvetica', 13)
    c.setFillColor(colors.HexColor('#4a5a78'))
    c.drawCentredString(width / 2, 32 * mm, f'Дата: {date.today().strftime("%d.%m.%Y")}')
    c.drawCentredString(width / 2, 24 * mm, 'PythonПро')
    c.showPage()
    c.save()
    return response


def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт создан! Теперь войдите.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
