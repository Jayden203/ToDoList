from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .forms import RegisterForm, TaskForm, CategoryForm
from .models import Task, Category
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
import requests

def get_weather_description(code):
    weather_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        51: "Light drizzle",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Light snow",
        80: "Rain showers",
        95: "Thunderstorm",
    }
    return weather_map.get(code, "Unknown")

def get_weather_icon(code):
    icon_map = {
        0: "☀️",   # Clear sky
        1: "🌤️",  # Mainly clear
        2: "⛅",   # Partly cloudy
        3: "☁️",   # Overcast
        45: "🌫️",  # Fog
        48: "🌫️",  # Depositing rime fog
        51: "🌦️",  # Light drizzle
        53: "🌦️",  # Moderate drizzle
        55: "🌧️",  # Dense drizzle
        61: "🌦️",  # Light rain
        63: "🌧️",  # Moderate rain
        65: "⛈️",  # Heavy rain
        71: "❄️",   # Light snow
        73: "❄️",   # Moderate snow
        75: "❄️",   # Heavy snow
        80: "🌦️",  # Rain showers
        81: "🌧️",  # Moderate rain showers
        82: "⛈️",  # Violent rain showers
        95: "⛈️",  # Thunderstorm
    }
    return icon_map.get(code, "🌍")    

def get_weather(latitude, longitude):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,weather_code,wind_speed_10m"
    )

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        current = data.get("current", {})
        code = current.get("weather_code")

        return {
            "temperature": current.get("temperature_2m"),
            "weather_code": code,
            "description": get_weather_description(code),
            "icon": get_weather_icon(code),
            "wind_speed": current.get("wind_speed_10m"),
        }
    except requests.RequestException:
        return None

def home(request):
    london_weather = get_weather(51.5072, -0.1276)
    glasgow_weather = get_weather(55.8642, -4.2518)

    context = {
        "london_weather": london_weather,
        "glasgow_weather": glasgow_weather,
    }
    return render(request, "tasks/home.html", context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully.')
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)

    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    status = request.GET.get('status', '')
    sort_by = request.GET.get('sort', '')

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    if category_id:
        tasks = tasks.filter(category_id=category_id)

    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'pending':
        tasks = tasks.filter(completed=False)

    if sort_by == 'due_date':
        tasks = tasks.order_by('due_date', '-created_at')
    elif sort_by == 'created_at':
        tasks = tasks.order_by('-created_at')
    elif sort_by == 'title':
        tasks = tasks.order_by('title')
    else:
        tasks = tasks.order_by('completed', 'due_date', '-created_at')

    categories = Category.objects.filter(user=request.user)

    context = {
        'tasks': tasks,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_status': status,
        'selected_sort': sort_by,
    }
    return render(request, 'tasks/dashboard.html', context)


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('dashboard')
    else:
        form = TaskForm()
        form.fields['category'].queryset = Category.objects.filter(user=request.user)

    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)

    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('dashboard')

    return render(request, 'tasks/delete_task.html', {'task': task})


@login_required
def toggle_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()

    if task.completed:
        messages.success(request, 'Task marked as completed.')
    else:
        messages.success(request, 'Task marked as pending.')

    return redirect('dashboard')


@login_required
def categories_view(request):
    categories = Category.objects.filter(user=request.user).order_by('name')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully.')
            return redirect('categories')
    else:
        form = CategoryForm()

    return render(request, 'tasks/categories.html', {
        'categories': categories,
        'form': form
    })


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('categories')

    return render(request, 'tasks/delete_category.html', {'category': category})

@login_required
def analytics(request):
    tasks = Task.objects.filter(user=request.user)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()

    completion_rate = 0
    if total_tasks > 0:
        completion_rate = round((completed_tasks / total_tasks) * 100, 1)

    category_queryset = (
        tasks.values("category__name")
        .annotate(task_count=Count("id"))
        .order_by("category__name")
    )

    category_data = []
    category_labels = []
    category_counts = []

    for item in category_queryset:
        category_name = item["category__name"] or "Uncategorized"
        task_count = item["task_count"]

        category_data.append({
            "category_name": category_name,
            "task_count": task_count,
        })
        category_labels.append(category_name)
        category_counts.append(task_count)

    today = timezone.now().date()
    due_labels = []
    due_counts = []

    for i in range(7):
        day = today + timedelta(days=i)
        due_labels.append(day.strftime("%b %d"))
        due_counts.append(tasks.filter(due_date=day).count())

    context = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "completion_rate": completion_rate,
        "category_data": category_data,
        "category_labels": category_labels,
        "category_counts": category_counts,
        "due_labels": due_labels,
        "due_counts": due_counts,
    }

    return render(request, "tasks/analytics.html", context)

@login_required
@require_POST
def toggle_task_status_ajax(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()

    return JsonResponse({
        "success": True,
        "task_id": task.id,
        "completed": task.completed,
        "title": task.title,
    })