from django.urls import path
from .views import register, login_view,home,logout_view,InstructorsHome,user_profile,update_profile,login_view2
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('login2/',login_view2 , name='login2'),
    path('StudentHome/', home, name='StudentHome'),
    path('InstructorsHome/', InstructorsHome, name='InstructorsHome'),
    path('logout/',logout_view, name='logout'),
    path('profile/', user_profile, name='user_profile'),
    path('profile/update/', update_profile, name='update_profile'),
     # Vue pour demander la réinitialisation du mot de passe
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html',
             email_template_name='password_reset_email.html',
             subject_template_name='password_reset_subject.txt',
             success_url='/password-reset/done/'
         ), 
         name='password_reset'),

    # Vue pour confirmer que l'e-mail de réinitialisation a été envoyé
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done1.html'
         ), 
         name='password_reset_done'),

    # Vue pour vérifier le lien de réinitialisation
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html',
             success_url='/reset/done/'
         ), 
         name='password_reset_confirm'),

    # Vue pour confirmer que le mot de passe a été réinitialisé
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)