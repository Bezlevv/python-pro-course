from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('modules/', views.module_list, name='modules'),
    path('modules/<slug:module_slug>/', views.module_detail, name='module_detail'),
    path('modules/<slug:module_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
    path('modules/<slug:module_slug>/<slug:lesson_slug>/download/', views.download_code, name='download_code'),
    path('lessons/<int:lesson_id>/complete/', views.complete_lesson, name='complete_lesson'),
    path('lessons/<int:lesson_id>/read/', views.toggle_read, name='toggle_read'),
    path('lessons/<int:lesson_id>/run/', views.run_code, name='run_code'),
    path('lessons/<int:lesson_id>/tests/', views.check_tests, name='check_tests'),
    path('lessons/<int:lesson_id>/quiz/', views.quiz_check, name='quiz_check'),
    path('lessons/<int:lesson_id>/comment/', views.add_comment, name='add_comment'),
    path('lessons/<int:lesson_id>/note/', views.save_note, name='save_note'),
    path('search/', views.search, name='search'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('lessons/<int:lesson_id>/feedback/', views.submit_feedback, name='submit_feedback'),
    path('challenge/', views.challenge, name='challenge'),
    path('goals/', views.goals, name='goals'),
    path('reference/', views.reference, name='reference'),
    path('practice/', views.practice, name='practice'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('certificate/', views.certificate, name='certificate'),
    path('certificate/pdf/', views.certificate_pdf, name='certificate_pdf'),
    path('profile/', views.profile, name='profile'),
    path('profile/export/', views.export_progress, name='export_progress'),
    path('register/', views.register, name='register'),
]
