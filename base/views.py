from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.db.models import Count, Q
from . import models
from django.contrib.auth.decorators import login_required
import random, datetime
from django.utils import timezone


#DECORATORS AND CUSTOM FUNCTIONS

def cant_be_authenticated(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return func(request,*args, **kwargs)
        else:
            return redirect(request.META.get('HTTP_REFERER', "homepage"))
    return wrapper

def must_be_ajax_and_authenticated(func):
    def wrapper(request, *args, **kwargs):
        if is_ajax(request) and request.user.is_authenticated:
            return func(request,*args, **kwargs)
        else:
            return redirect("login-page")
    return wrapper

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

#DECORATORS AND CUSTOM FUNCS END

def get_homepage(request):

    all_posts = models.Post.objects.all().annotate(rating = Count("liked_users")-Count("disliked_users"), comment_count = Count("post_comments"))
    feed_posts = []

    if request.user.is_authenticated:
        user_feed = request.user.profile.get_posts(all_posts)
        feed_posts = user_feed
    else:
        random_new_post = random.choice(all_posts.order_by("-created_date")[:15])
        random_top_post = random.choice(all_posts.order_by("-rating")[:round(len(all_posts)/100)+1])
        feed_posts = random.choices(all_posts, k=6) + [random_new_post, random_top_post]

        for post in feed_posts:
            while not feed_posts.count(post) == 1:
                feed_posts.remove(post)
                while True:
                    new = random.choice(all_posts)
                    if new not in feed_posts:
                        feed_posts.append(new)
                        break

    for post in feed_posts:
        post.best_3_comments = post.post_comments.annotate(rating=Count("liked_users")-Count("disliked_users")).order_by("-rating")[:3]
    
    context = {"posts":feed_posts, "page": "Feed"}

    return render(request, "base/index.html", context)

def get_posts_page(request):

    tag_name = request.GET.get("tag")
    #It wont throw an error if the HTTP request has no tag parameter
    tag = models.Tag.objects.filter(name=tag_name).first()
    
    date_text = request.GET.get("date")
    date = date_text if date_text in ("year", "month", "week", "day") else None

    sort_by = request.GET.get("sorting")
    sort_by = "created_date" if sort_by == "date" else sort_by
    sort_by = "?" if sort_by == "random" else sort_by

    order = "" if request.GET.get("order") == "asc" or sort_by == "?" else "-"
    # random sort throws an error if it is given with "-"  ("-?")
    
    page = int(request.GET.get("page")) if request.GET.get("page","x").isnumeric() else 1

    posts_per_page = int(request.GET.get("ppp")) if request.GET.get("ppp","x").isnumeric() else 10

    tag_filter = Q(tags__name__contains = tag.name) if tag else Q(pk__in=[]) #Always False
    date_filter = Q()

    if date:
        now = datetime.datetime.now()
        if date == "year":
            date_filter = Q(created_date__year = now.year)

        elif date == "month":
            date_filter = Q(created_date__year = now.year) & Q(created_date__month = now.month)

        elif date == "week":
            one_week_ago = datetime.datetime.today() - datetime.timedelta(days=7)
            date_filter = Q(created_date__gte=one_week_ago)

        elif date == "day":
            date_filter = Q(created_date__date=timezone.now())


    posts = models.Post.objects.filter(tag_filter&date_filter).annotate(
        rating = Count("liked_users")-Count("disliked_users"),
        comment_count = Count("post_comments"),
        vote_count = Count("liked_users")+Count("disliked_users")
        )

    
    if sort_by in ("rating", "created_date", "comment_count", "vote_count", "?"):
        posts = posts.order_by(f"{order}{sort_by}","-vote_count")
    else:
        posts = posts.order_by("-rating")
    
    
    posts = posts[(page-1)*posts_per_page:(page*posts_per_page)]

    for post in posts:
        post.best_3_comments = post.post_comments.annotate(rating=Count("liked_users")-Count("disliked_users")).order_by("-rating")[:3]

    page = f"#{tag.name} posts" if tag else "Posts"

    context = {"posts":posts, "page":page}

    return render(request, "base/posts_page.html", context)

@cant_be_authenticated
def get_register_page(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            user_profile = models.UserProfile.objects.create(user=user)
            login(request, user)
            next = request.GET.get('next') if request.GET.get('next') else "homepage"
            return redirect(next)
        else:
            messages.error(request, "Something is Wrong With Your Registration.")
            

    context = {"form":form, "page":"Register"}
    return render(request, "base/register_page.html", context)


@cant_be_authenticated
def get_login_page(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist.")
        else:
            user = authenticate(request, 
		username=username, password=password)

            if user is not None:
                login(request, user)
                next = request.GET.get('next') if request.GET.get('next') else "homepage"
 
                return redirect(next)
            else:
                messages.error(request,
		"Password does not match with username.")

    context = {"page":"Login"}
    return render(request, "base/login_page.html", context)


def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', "homepage"))


def get_user_profile_page(request, username):
    viewed_user = User.objects.get(username=username)

    filtered_related_users = []

    if viewed_user == request.user:

        related_users = []

        for followed_user in request.user.profile.following.all():
            related_users.extend(followed_user.profile.following.all())

        related_users_dict = {user:related_users.count(user) for user in related_users}
        sorted_related_users_dict = sorted(related_users_dict.items(), key=lambda x: x[1], reverse=True) 
        filtered_related_users = []

        for r_user in sorted_related_users_dict:
            if r_user[0] != request.user and r_user[0] not in request.user.profile.following.all():
                filtered_related_users.append(r_user[0])
            
            if len(filtered_related_users) == 5:
                break



    context = {"viewed_user":viewed_user, "related_users":filtered_related_users, "page": f"{viewed_user.username}'s Profile"}
    return render(request, "base/user_profile_page.html",context)


@must_be_ajax_and_authenticated
def handle_following(request, username):
    request.user.profile.handle_follow(username)
    return HttpResponse("Success.")


@must_be_ajax_and_authenticated
def like_post(request, post_id):
    post = models.Post.objects.get(id=post_id)
    request.user.profile.like(post)
    return HttpResponse("Success.")

@must_be_ajax_and_authenticated
def dislike_post(request, post_id):
    post = models.Post.objects.get(id=post_id)
    request.user.profile.dislike(post)
    return HttpResponse("Success.")

@must_be_ajax_and_authenticated
def bookmark_post(request, post_id):
    request.user.profile.bookmark_post(post_id)
    return HttpResponse("Success.")

@must_be_ajax_and_authenticated
def like_comment(request, comment_id):
    comment = models.Comment.objects.get(id=comment_id)
    request.user.profile.like(comment)
    return HttpResponse("Success.")

@must_be_ajax_and_authenticated
def dislike_comment(request, comment_id):
    comment = models.Comment.objects.get(id=comment_id)
    request.user.profile.dislike(comment)
    return HttpResponse("Success.")

@must_be_ajax_and_authenticated
def delete_comment(request, comment_id):
    comment = models.Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
        return HttpResponse("Success.")



def get_post(request, post_id):
    post = models.Post.objects.get(id=post_id)

    if request.method == "POST" and request.user.is_authenticated:
        content = request.POST.get("content")
        if len(content) > 1:
            models.Comment.objects.create(user=request.user, post=post, content=content)

    comments = models.Comment.objects.filter(post=post).annotate(rating=Count("liked_users")-Count("disliked_users")).order_by("-rating")

    context = {"post": post, "comments":comments, "page":f"{post.user}'s Post"}
    return render(request, "base/post_page.html", context)



@login_required
def get_followed_users_page(request):
    user_profile = request.user.profile
    followed_users = user_profile.following.all()
    context={"users":followed_users, "page":"Followed Users"}
    return render(request, "base/followers_and_followed_page.html", context)


@login_required
def get_follower_users_page(request):
    follower_users = [profile.user for profile in request.user.followers.all()]
    context={"users":follower_users,"page":"Follower Users"}
    return render(request, "base/followers_and_followed_page.html", context)


@login_required
def get_bookmarked_posts_page(request):
    bookmarked_posts = request.user.profile.bookmarked_posts.all()
    context={"posts":bookmarked_posts,"page":"Bookmarked Posts"}
    return render(request, "base/mini_posts_page.html", context)


@login_required
def get_liked_posts_page(request):
    liked_posts = request.user.post_likes.all()
    context={"posts":liked_posts, "page":"Liked Posts"}
    return render(request, "base/mini_posts_page.html", context)


@login_required
def get_disliked_posts_page(request):
    disliked_posts = request.user.post_dislikes.all()
    context={"posts":disliked_posts, "page": "Disliked Posts"}
    return render(request, "base/mini_posts_page.html", context)


@login_required
def get_create_post_page(request):
    
    if request.method == "POST":
        user = request.user
        raw_url = request.POST.get("url")
        description = request.POST.get("description")
        raw_tags_text = request.POST.get("tags")

        tags = raw_tags_text.strip().split()
        video_id = raw_url.partition("watch?v=")[2]

        if not video_id or not tags:
            return redirect("create-post")

        new_post = models.Post.objects.create(user=user, description=description, video_link=video_id)
        

        for tag in tags:
            tag_object, created = models.Tag.objects.get_or_create(name=tag.strip().lower())
            new_post.tags.add(tag_object)

        return redirect("post-page", new_post.id)

    context = {"page":"Share Post"}
    return render(request, "base/add_post_page.html", context)

@login_required
def get_edit_post_page(request, post_id):

    post = models.Post.objects.get(id=post_id)

    if request.user == post.user:

        if request.method == "POST":
            raw_url = request.POST.get("url")
            description = request.POST.get("description")
            raw_tags_text = request.POST.get("tags")

            video_id = raw_url.partition("watch?v=")[2]

            post.video_link = video_id
            post.description = description

            post.tags.clear()

            if raw_tags_text:

                tags = raw_tags_text.strip().split()

                for tag in tags:
                    tag_object, created = models.Tag.objects.get_or_create(name=tag.strip().lower())
                    post.tags.add(tag_object)

            post.save()

            return redirect("post-page", post_id)

        context = {"page":"Edit Post", "post":post}

        return render(request, "base/add_post_page.html", context)
    else:
        return redirect(request.META.get('HTTP_REFERER', "homepage"))

@login_required
def delete_post(request, post_id):
    
    post = models.Post.objects.get(id=post_id)

    if request.user == post.user:
        post.delete()

    return redirect("user-profile-page", request.user.username)
