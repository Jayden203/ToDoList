from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .forms import RegisterForm, TaskForm, CategoryForm
from .models import Task, Category


def home(request):
    return render(request, 'tasks/home.html')


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
def analytics_view(request):
    tasks = Task.objects.filter(user=request.user)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()

    if total_tasks > 0:
        completion_rate = round((completed_tasks / total_tasks) * 100, 1)
    else:
        completion_rate = 0

    category_data = (
        Category.objects.filter(user=request.user)
        .annotate(task_count=Count('tasks'))
        .order_by('-task_count', 'name')
    )

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_rate': completion_rate,
        'category_data': category_data,
    }

    return render(request, 'tasks/analytics.html', context)