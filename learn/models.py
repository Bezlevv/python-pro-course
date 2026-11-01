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
    """Урок: теория, задача, подсказка, разбор."""

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
    theory_md = models.TextField(default='', verbose_name='Теория (Markdown)')
    task_md = models.TextField(default='', verbose_name='Задача (Markdown)')
    hint_md = models.TextField(default='', verbose_name='Подсказка (Markdown)')
    solution_md = models.TextField(default='', verbose_name='Разбор (Markdown)')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        unique_together = [('module', 'order')]
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson_detail', args=[self.module.slug, self.slug])

    def next_lesson(self):
        """Следующий урок по порядку курса."""
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
    """Прогресс ученика по уроку."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='progress', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='progress', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('user', 'lesson')]
        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогресс'
