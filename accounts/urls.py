from django.conf import settings
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



app_name = 'accounts'
urlpatterns = [
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password/password_reset_done.html', ), name='password_reset_done', ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password/password_reset_confirm.html"), name='password_reset_confirm'),
]

urlpatterns += [
    path('', views.index, name="index"),
    path('register/',views.register, name="register"),
    path('login/',views.login_view, name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('faq/', views.faq, name="faq"),
]




