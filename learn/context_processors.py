from .models import Module


def global_nav(request):
    """Доступные везде данные: модули для меню."""
    return {
        'nav_modules': Module.objects.all()[:12],
    }
