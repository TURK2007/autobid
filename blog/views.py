from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from django.db.models import Q
from .models import Car

from .forms import CarForm, CommentForm, PostForm, RegisterForm
from .models import Car, Post


def home(request):
    cars = Car.objects.all().order_by("-created_at")
    return render(request, "blog/index.html", {"cars": cars})


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()

    return render(request, "blog/post_form.html", {"form": form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_form.html", {"form": form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == "POST":
        post.delete()
        return redirect("home")

    return render(request, "blog/post_confirm_delete.html", {"post": post})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by("-created_at")

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("detail", pk=post.pk)
    else:
        form = CommentForm()

    return render(
        request,
        "blog/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
        },
    )


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "blog/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")

        return render(
            request,
            "blog/login.html",
            {"error": "Неверный логин или пароль."},
        )

    return render(request, "blog/login.html")


@login_required
def sell_car(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)

        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect("/")
        else:
            print("Ошибки формы:", form.errors)
    else:
        form = CarForm()

    return render(request, "blog/sell_car.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("/")

logout_view = user_logout



from django.shortcuts import render
from .models import Car


def index(request):
    cars = Car.objects.all()
    return render(request, 'blog/index.html', {'cars': cars})

from django.db.models import Q  

def search_view(request):
    cars = Car.objects.all()

    query = request.GET.get('q')
    year = request.GET.get('year')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    if query:
        cars = cars.filter(
            Q(brand__icontains=query) | 
            Q(model__icontains=query) |
            Q(description__icontains=query)
        )

    if year:
        cars = cars.filter(year=year)

    if price_min:
        cars = cars.filter(price__gte=price_min)

    if price_max:
        cars = cars.filter(price__lte=price_max)

    return render(request, 'blog/search_results.html', {'cars': cars})
