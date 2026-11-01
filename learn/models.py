from django.conf import settings
from django.db import models
from django.urls import reverse


class Module(models.Model):
    """Модуль курса (раздел)."""
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    title = models.CharField(max_length=120, verbose_name='Название')
    order = models.PositiveSmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    description = models.TextField(blank=True, verbose_name='Описание')
    icon = models.CharField(max_length=8, default='📘', verbose_name='Иконка')

    class Meta:
        ordering = ['order']
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('module_detail', args=[self.slug])

    def lesson_count(self):
        return self.lessons.count()


class Lesson(models.Model):
    """Урок: теория, задача, подсказка, разбор, викторина."""

    class Difficulty(models.TextChoices):
        BEGINNER = 'beginner', 'Начинающий'
        INTERMEDIATE = 'intermediate', 'Средний'
        ADVANCED = 'advanced', 'Продвинутый'

    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE, verbose_name='Модуль')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    title = models.CharField(max_length=160, verbose_name='Название')
    order = models.PositiveSmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    summary = models.CharField(max_length=240, blank=True, verbose_name='Краткое описание')
    duration = models.CharField(max_length=40, default='20 мин', verbose_name='Время')
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, default=Difficulty.BEGINNER, verbose_name='Сложность')
    tags = models.CharField(max_length=300, blank=True, verbose_name='Теги (через запятую)')
    theory_md = models.TextField(default='', verbose_name='Теория (Markdown)')
    task_md = models.TextField(default='', verbose_name='Задача (Markdown)')
    hint_md = models.TextField(default='', verbose_name='Подсказка (Markdown)')
    solution_md = models.TextField(default='', verbose_name='Разбор (Markdown)')
    quiz_md = models.TextField(default='', verbose_name='Викторина (Markdown)')
    expected_output_md = models.TextField(default='', verbose_name='Ожидаемый вывод')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        unique_together = [('module', 'order')]
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Синхронизирует вопросы викторины при сохранении урока."""
        super().save(*args, **kwargs)
        if self.quiz_md:
            from .utils import parse_quiz
            self.quizzes.all().delete()
            for idx, q in enumerate(parse_quiz(self.quiz_md), start=1):
                QuizQuestion.objects.create(
                    lesson=self,
                    order=idx,
                    question=q['question'],
                    options=q['options'],
                    correct_index=q['correct_index'],
                    explanation=q['explanation'],
                )

    def get_absolute_url(self):
        return reverse('lesson_detail', args=[self.module.slug, self.slug])

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def next_lesson(self):
        nxt = Lesson.objects.filter(module__order=self.module.order, order__gt=self.order) \
            .order_by('order').first()
        if nxt:
            return nxt
        return Lesson.objects.filter(module__order__gt=self.module.order) \
            .order_by('module__order', 'order').first()

    def prev_lesson(self):
        prev = Lesson.objects.filter(module__order=self.module.order, order__lt=self.order) \
            .order_by('-order').first()
        if prev:
            return prev
        return Lesson.objects.filter(module__order__lt=self.module.order) \
            .order_by('-module__order', '-order').first()


class LessonProgress(models.Model):
    """Прогресс ученика по уроку: прочитал / решил задачу."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='progress', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='progress', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Решено')
    read = models.BooleanField(default=False, verbose_name='Прочитан')

    class Meta:
        unique_together = [('user', 'lesson')]
        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогресс'


class QuizQuestion(models.Model):
    """Вопрос викторины урока."""
    lesson = models.ForeignKey(Lesson, related_name='quizzes', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)
    question = models.TextField(verbose_name='Вопрос')
    options = models.JSONField(default=list, verbose_name='Варианты')
    correct_index = models.PositiveSmallIntegerField(default=0, verbose_name='Номер верного варианта')
    explanation = models.TextField(blank=True, verbose_name='Объяснение')

    class Meta:
        ordering = ['order']
        unique_together = [('lesson', 'order')]
        verbose_name = 'Вопрос викторины'
        verbose_name_plural = 'Вопросы викторины'

    def __str__(self):
        return self.question[:60]


class Comment(models.Model):
    """Комментарий под уроком."""
    lesson = models.ForeignKey(Lesson, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lesson_comments', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user.username}: {self.text[:40]}'


class LessonNote(models.Model):
    """Личная заметка ученика к уроку."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lesson_notes', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='notes', on_delete=models.CASCADE)
    text = models.TextField(blank=True, verbose_name='Заметка')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('user', 'lesson')]
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'


class Achievement(models.Model):
    """Достижение (бейдж)."""

    class Kind(models.TextChoices):
        LESSONS_COUNT = 'lessons_count', 'Количество уроков'
        STREAK_DAYS = 'streak_days', 'Серия дней'
        MODULES_COMPLETE = 'modules_complete', 'Завершённые модули'

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=240)
    icon = models.CharField(max_length=8, default='🏅')
    kind = models.CharField(max_length=20, choices=Kind.choices)
    threshold = models.PositiveIntegerField(default=1)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.icon} {self.title}'


class UserAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='achievements', on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, related_name='holders', on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'achievement')]


class CodeAttempt(models.Model):
    """Попытка запуска кода в песочнице."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='attempts', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='attempts', on_delete=models.CASCADE)
    code = models.TextField()
    output = models.TextField(blank=True)
    passed = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
