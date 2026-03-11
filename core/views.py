from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Doubt, Category, Branch, Subject, Answer


# 🏠 HOME PAGE
@login_required
def home(request):
    query = request.GET.get('q')

    if query:
        doubts = Doubt.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-created_at')
    else:
        doubts = Doubt.objects.all().order_by('-created_at')

    return render(request, 'home.html', {
        'doubts': doubts,
    })


# 📂 CATEGORY DOUBTS
@login_required
def category_doubts(request, pk):
    category = get_object_or_404(Category, pk=pk)
    doubts = Doubt.objects.filter(category=category).order_by('-created_at')

    return render(request, 'category_doubts.html', {
        'category': category,
        'doubts': doubts,
    })


# ❓ POST DOUBT (Only Juniors)
@login_required
def post_doubt(request):

    if request.user.user_type != "junior":
        messages.error(request, "Only Juniors can post doubts.")
        return redirect('home')

    categories = Category.objects.all()
    branches = Branch.objects.all()
    subjects = Subject.objects.all()

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        branch_id = request.POST.get('branch')
        subject_id = request.POST.get('subject')

        if not title or not description:
            messages.error(request, "Title and description are required.")
            return redirect('post_doubt')

        similar_doubts = Doubt.objects.filter(
            Q(title__icontains=title) |
            Q(description__icontains=title)
        )

        if similar_doubts.exists():
            return render(request, 'similar_doubts.html', {
                'similar_doubts': similar_doubts,
                'title': title,
                'description': description,
                'categories': categories,
                'branches': branches,
                'subjects': subjects,
            })

        category = get_object_or_404(Category, id=category_id)
        branch = get_object_or_404(Branch, id=branch_id) if branch_id else None
        subject = get_object_or_404(Subject, id=subject_id) if subject_id else None

        Doubt.objects.create(
            title=title,
            description=description,
            category=category,
            branch=branch,
            subject=subject,
            user=request.user
        )

        messages.success(request, "Doubt posted successfully!")
        return redirect('junior_dashboard')

    return render(request, 'post_doubt.html', {
        'categories': categories,
        'branches': branches,
        'subjects': subjects
    })


# 🔍 DOUBT DETAIL PAGE
@login_required
def doubt_detail(request, pk):
    doubt = get_object_or_404(Doubt, pk=pk)
    answers = Answer.objects.filter(doubt=doubt).order_by('-created_at')

    return render(request, 'doubt_detail.html', {
        'doubt': doubt,
        'answers': answers
    })


# ✍ ADD ANSWER (Only Seniors)
@login_required
def add_answer(request, pk):
    doubt = get_object_or_404(Doubt, pk=pk)

    if request.user.user_type != "senior":
        messages.error(request, "Only Seniors can answer doubts.")
        return redirect('doubt_detail', pk=pk)

    if request.method == "POST":
        content = request.POST.get('content')

        if not content:
            messages.error(request, "Answer cannot be empty.")
            return redirect('add_answer', pk=pk)

        Answer.objects.create(
            doubt=doubt,
            user=request.user,
            content=content
        )

        messages.success(request, "Answer added successfully!")
        return redirect('doubt_detail', pk=pk)

    return render(request, 'add_answer.html', {'doubt': doubt})


# 🔀 ROLE BASED REDIRECT AFTER LOGIN
@login_required
def role_redirect(request):
    user = request.user

    if user.is_superuser:
        return redirect('/admin/')

    elif user.user_type == 'junior':
        return redirect('junior_dashboard')

    elif user.user_type == 'senior':
        return redirect('senior_dashboard')

    return redirect('home')


# 👨‍🎓 JUNIOR DASHBOARD
@login_required
def junior_dashboard(request):
    doubts = Doubt.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'junior_dashboard.html', {
        'doubts': doubts
    })


# 🎓 SENIOR DASHBOARD
@login_required
def senior_dashboard(request):
    doubts = Doubt.objects.all().order_by('-created_at')

    return render(request, 'senior_dashboard.html', {
        'doubts': doubts
    })