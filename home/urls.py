from django.urls import path
''' from apps.home import views '''
from home import views
urlpatterns = [

    # The home page
    path('', views.members,name='index'),



]
