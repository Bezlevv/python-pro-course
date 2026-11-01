from django.contrib import admin

from .models import Lesson, LessonProgress, Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('order', 'icon', 'title', 'slug', 'lesson_count')
    list_display_links = ('title',)
    list_editable = ('order', 'icon')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('module', 'order', 'title', 'difficulty', 'duration')
    list_display_links = ('title',)
    list_editable = ('order', 'difficulty', 'duration')
    list_filter = ('module', 'difficulty')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'summary')
    readonly_fields = ('created',)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed_at')
    list_filter = ('lesson__module',)
    search_fields = ('user__username', 'lesson__title')
