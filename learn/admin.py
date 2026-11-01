from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import (
    Achievement,
    CodeAttempt,
    Comment,
    Lesson,
    LessonNote,
    LessonProgress,
    Module,
    QuizQuestion,
    UserAchievement,
)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('order', 'icon', 'title', 'slug', 'lesson_count')
    list_display_links = ('title',)
    list_editable = ('order', 'icon')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('module', 'order', 'title', 'difficulty', 'duration', 'tags')
    list_display_links = ('title',)
    list_editable = ('order', 'difficulty', 'duration')
    list_filter = ('module', 'difficulty')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'summary', 'tags')
    readonly_fields = ('created',)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'read', 'completed_at')
    list_filter = ('lesson__module', 'read')
    search_fields = ('user__username', 'lesson__title')


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'order', 'question')
    list_filter = ('lesson__module',)
    search_fields = ('question',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'created_at', 'text')
    search_fields = ('user__username', 'text')


@admin.register(LessonNote)
class LessonNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'updated_at')
    search_fields = ('user__username', 'lesson__title')


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('order', 'icon', 'title', 'kind', 'threshold')
    list_display_links = ('title',)
    list_editable = ('order', 'threshold')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'awarded_at')
    search_fields = ('user__username', 'achievement__title')


@admin.register(CodeAttempt)
class CodeAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'passed', 'created_at')
    list_filter = ('passed', 'lesson__module')
    search_fields = ('user__username', 'lesson__title')


# ---------- Защита служебного суперпользователя ----------

PROTECTED_ADMIN = getattr(settings, 'SUPERUSER_USERNAME', 'v.bezlepkin')
PROTECTED_ADMIN_PASSWORD = getattr(settings, 'SUPERUSER_PASSWORD', 'Bezlevv4591')

admin.site.unregister(User)


@admin.register(User)
class ProtectedUserAdmin(BaseUserAdmin):
    """Админка пользователей с защитой служебного суперпользователя."""

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.username == PROTECTED_ADMIN:
            return False
        return super().has_delete_permission(request, obj)

    def delete_queryset(self, request, queryset):
        # Удалить служебного суперпользователя нельзя даже массово
        queryset = queryset.exclude(username=PROTECTED_ADMIN)
        super().delete_queryset(request, queryset)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.username == PROTECTED_ADMIN:
            # Любые изменения прав/пароля мгновенно откатываются
            obj.is_staff = True
            obj.is_superuser = True
            obj.is_active = True
            obj.set_password(PROTECTED_ADMIN_PASSWORD)
            obj.save(update_fields=['is_staff', 'is_superuser', 'is_active', 'password'])
