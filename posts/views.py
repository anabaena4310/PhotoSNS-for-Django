from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import Post, CustomUser
from django.contrib.auth.decorators import login_required
from .forms import PostForm


def home(request):
    return render(request, 'home.html')
    

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


@login_required
def following_timeline(request):
    user = request.user
    following_users = user.following.all()
    posts = Post.objects.filter(user__in=following_users).order_by('-created_at')
    return render(request, 'following_timeline.html', {'posts': posts})