"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # auth
    path('signup/', views.signup_user, name="signup_user"),
    path('logout/', views.logout_user, name="logout_user"),
    path('login/', views.login_user, name="login_user"),
    # to-do
    path('current/', views.current_tasks, name="current_tasks"),
    path('', views.home, name="home"),
    path('create/', views.create_todo, name="create_todo"),
    path('detail/<int:task_pk>', views.detail, name="detail"),
    path('detail/<int:task_pk>/complete', views.complete_task, name="complete_task"),
    path('detail/<int:task_pk>/delete', views.delete_task, name="delete_task"),
    path('completed/', views.completed_tasks, name="completed_tasks"),
]
