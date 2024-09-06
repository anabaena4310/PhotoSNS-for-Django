from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, CustomUser


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


def follow_unfollow_user(request, id):
    user_id = Post.objects.get(id=id).user.id
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    if user_to_follow in request.user.following.all():
        request.user.following.remove(user_to_follow)
    else:
        request.user.following.add(user_to_follow)

    return redirect('post_detail', post_id=id)


@login_required
def following_timeline(request):
    user = request.user
    following_users = user.following.all()
    posts = Post.objects.filter(user__in=following_users).order_by('-created_at')
    return render(request, 'following_timeline.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_following = post.user in request.user.following.all()

    return render(request, 'post_detail.html', {
        'post': post,
        'is_following': is_following,
    })