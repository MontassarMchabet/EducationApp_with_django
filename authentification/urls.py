from django.urls import path
from .views import register, login_view,home,logout_view,InstructorsHome
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('StudentHome/', home, name='StudentHome'),
    path('InstructorsHome/', InstructorsHome, name='InstructorsHome'),
    path('logout/',logout_view, name='logout'),
    
    
]