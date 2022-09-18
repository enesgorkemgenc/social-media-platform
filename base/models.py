from django.db import models
from django.contrib.auth.models import User
import random


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    following = models.ManyToManyField(User, blank=True, related_name="followers")
    bookmarked_posts = models.ManyToManyField("Post", blank=True)
    interested_tags = models.ManyToManyField("Tag", blank=True)

    def __str__(self):
        return self.user.username

    def handle_follow(self, username):
        user = User.objects.get(username=username)

        if user in self.following.all():
            self.following.remove(user)
        else:
            self.following.add(user)

    def like(self, object):

        if self.user not in object.liked_users.all():
            object.liked_users.add(self.user)

            if type(object) is Post:
                post_tags = object.tags.all()
                self.interested_tags.add(*post_tags)

        else:
            object.liked_users.remove(self.user)

            if type(object) is Post:
                post_tags = object.tags.all()
                self.interested_tags.remove(*post_tags)

        if self.user in object.disliked_users.all():
            object.disliked_users.remove(self.user)
        

    def dislike(self, object):

        if self.user not in object.disliked_users.all():
            object.disliked_users.add(self.user)

            if type(object) is Post:
                post_tags = object.tags.all()
                self.interested_tags.remove(*post_tags)

        else:
            object.disliked_users.remove(self.user)
        
        if self.user in object.liked_users.all():
            object.liked_users.remove(self.user)


    def bookmark_post(self, post_id):

        post = Post.objects.get(id=post_id)

        if post in self.bookmarked_posts.all():
            self.bookmarked_posts.remove(post)
        else:
            self.bookmarked_posts.add(post)


    def get_posts(self,all_posts, seen_posts = []):
        new_posts = all_posts.order_by("-created_date")[:15]
        top_posts = all_posts.order_by("-rating")[:round(len(all_posts)/100)+1]
        followed_users_newest_posts = [user.posts.order_by("-created_date")[0] for user in self.following.all() if user.posts.all()] if self.following.all() else []

        all_interested_posts = []
        random_interested_posts = []
        interested_tags = self.interested_tags.all()

        if interested_tags:
            for post in all_posts:
                for tag in interested_tags:
                    if tag in post.tags.all():
                        all_interested_posts.append(post)

            weights = [all_interested_posts.count(post) for post in all_interested_posts]
            random_interested_posts = random.choices(all_interested_posts, weights=weights,k=3)

            # randomly selects 3 posts from the list "all_interested_posts" based on their count in the list,
            # e.g if a post includes 2 tags that the user is interested in, then the list is
            # going to be including 2 copies of that post, making the possibility to be chosen twice compared to
            # the posts that has only 1 interested tag.
            

        for _ in range(10): #Try Up To 10 Times. I don't want it to be stuck in an infinite loop.
            random_new_post = random.choice(new_posts)
            if str(random_new_post.id) not in seen_posts:
                break

        for _ in range(10):
            random_post = random.choice(all_posts)
            if str(random_post.id) not in seen_posts:
                break

        for _ in range(10):
            random_top_post = random.choice(top_posts)
            if str(random_top_post.id) not in seen_posts:
                break
        
        
        if followed_users_newest_posts:
            for _ in range(10):
                random_fol_1 = random.choice(followed_users_newest_posts)
                if str(random_fol_1.id) not in seen_posts:
                    break
                
            for _ in range(10):
                random_fol_2 = random.choice(followed_users_newest_posts)
                if str(random_fol_2.id) not in seen_posts:
                    break
        else:
            for _ in range(10):
                random_fol_1 = random.choice(all_posts)
                if str(random_fol_1.id) not in seen_posts:
                    break
            for _ in range(10):
                random_fol_2 = random.choice(all_posts)
                if str(random_fol_2.id) not in seen_posts:
                    break
        
        user_posts = [random_new_post, random_post, random_top_post, random_fol_1, random_fol_2] + random_interested_posts 

        for post in user_posts:
            while not user_posts.count(post) == 1:
                user_posts.remove(post)
                for _ in range(10):
                    new = random.choice(all_posts)
                    if new not in user_posts:
                        user_posts.append(new)
                        break

        return user_posts



class Tag(models.Model):
    name = models.CharField(unique=True, max_length=30)
    def __str__(self):
        return self.name



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    video_link = models.TextField(null=False, blank=False)

    liked_users = models.ManyToManyField(User, related_name="post_likes", blank=True)
    disliked_users = models.ManyToManyField(User, related_name="post_dislikes", blank=True)
    description = models.CharField(null=True, blank=True, max_length=255)
    tags = models.ManyToManyField(Tag, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")

    content = models.TextField()
    liked_users = models.ManyToManyField(User, blank=True, related_name="comment_likes")
    disliked_users = models.ManyToManyField(User, related_name="comment_dislikes", blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content