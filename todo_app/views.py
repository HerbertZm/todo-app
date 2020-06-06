from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ToDoForm
from .models import ToDo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'todo_app/home.html')

def signup_user(request):
    if request.method == "GET":
        return render(request, 'todo_app/signup.html', {"form": UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_tasks')
            except IntegrityError:
                return render(request, 'todo_app/signup.html', {"form": UserCreationForm(), "error":"Username already exists"})
        else:
            return render(request, 'todo_app/signup.html', {"form": UserCreationForm(), "error":"Passwords did not match"})

def login_user(request):
    if request.method == "GET":
        return render(request, 'todo_app/login.html', {"form": AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo_app/login.html', {"form": AuthenticationForm(), "error":"Username and password do not match"})
        else:
            login(request, user)
            return redirect('current_tasks')

@login_required
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

@login_required
def create_todo(request):
    if request.method == "GET":
        return render(request, 'todo_app/create_todo.html', {"form": ToDoForm()})
    else:
        try:
            form = ToDoForm(request.POST)
            todo = form.save(commit=False)
            todo.owner = request.user
            todo.save()
            return redirect('current_tasks')
        except ValueError:
            return render(request, 'todo_app/create_todo.html', {"form": ToDoForm(), "error": "Please check you data"})

@login_required
def current_tasks(request):
    tasks = ToDo.objects.filter(owner=request.user, completed_at__isnull=True)
    return render(request, 'todo_app/current_tasks.html', {"tasks": tasks})

@login_required
def completed_tasks(request):
    tasks = ToDo.objects.filter(owner=request.user, completed_at__isnull=False).order_by('-completed_at')
    return render(request, 'todo_app/completed_tasks.html', {"tasks": tasks})

@login_required
def detail(request,task_pk):
    task = get_object_or_404(ToDo, pk=task_pk, owner=request.user)
    if request.method == "GET":
        form = ToDoForm(instance=task)
        return render(request, 'todo_app/detail.html', {'task': task, 'form': form})
    else:
        try:
            form = ToDoForm(request.POST, instance=task)
            form.save()
            return redirect('current_tasks')
        except ValueError:
            return render(request, 'todo_app/detail.html', {'task': task, 'form': form, 'error': 'Please check you data'})

@login_required
def complete_task(request, task_pk):
    task = get_object_or_404(ToDo, pk=task_pk, owner=request.user)
    if request.method == "POST":
        task.completed_at = timezone.now()
        task.save()
        return redirect('current_tasks')

@login_required
def delete_task(request, task_pk):
    task = get_object_or_404(ToDo, pk=task_pk, owner=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('current_tasks')
