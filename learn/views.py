from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Lesson, LessonProgress, Module
from .utils import lesson_difficulty_label, render_markdown


# ---------- Вспомогательное ----------

def _module_progress(user):
    """{module_id: число пройденных уроков} для текущего пользователя."""
    if not user.is_authenticated:
        return {}
    rows = (
        LessonProgress.objects
        .filter(user=user)
        .values('lesson__module')
        .annotate(done=Count('id'))
    )
    return {row['lesson__module']: row['done'] for row in rows}


def _modules_data(user):
    """Список dict: модуль + счётчики и процент прогресса."""
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


def _lesson_ctx(request, lesson):
    """Общий контекст страницы урока."""
    done_ids = set()
    if request.user.is_authenticated:
        done_ids = set(
            LessonProgress.objects.filter(user=request.user).values_list('lesson_id', flat=True)
        )
    module_lessons = list(lesson.module.lessons.all())
    return {
        'lesson': lesson,
        'theory_html': render_markdown(lesson.theory_md),
        'task_html': render_markdown(lesson.task_md),
        'hint_html': render_markdown(lesson.hint_md),
        'solution_html': render_markdown(lesson.solution_md),
        'module_lessons': module_lessons,
        'module_lesson_ids': [l.id for l in module_lessons],
        'done_ids': done_ids,
        'difficulty_label': lesson_difficulty_label(lesson.difficulty),
        'next_lesson': lesson.next_lesson(),
        'prev_lesson': lesson.prev_lesson(),
        'is_done': lesson.id in done_ids,
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
    progress = _module_progress(request.user)
    done_ids = set()
    if request.user.is_authenticated:
        done_ids = set(
            LessonProgress.objects.filter(user=request.user, lesson__module=module)
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
    ctx = _lesson_ctx(request, lesson)
    return render(request, 'lesson_detail.html', ctx)


@require_POST
@login_required
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    if created:
        messages.success(request, f'Отлично! Урок «{lesson.title}» отмечен пройденным 🎉')
    else:
        progress.delete()
        messages.info(request, f'Отметка «{lesson.title}» снята.')
    return redirect(lesson.get_absolute_url())


def search(request):
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        results = (
            Lesson.objects.select_related('module')
            .filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(theory_md__icontains=q))
            .order_by('module__order', 'order')
        )
    return render(request, 'search.html', {'q': q, 'results': results})


@login_required
def profile(request):
    done = LessonProgress.objects.filter(user=request.user).select_related('lesson__module')
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
    return render(request, 'profile.html', {
        'data': data,
        'total_lessons': total,
        'completed': len(done),
        'pct_total': round(len(done) / total * 100) if total else 0,
        'last_done': last_done,
    })


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
