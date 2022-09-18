import json
from channels.generic.websocket import WebsocketConsumer
from .models import Post
from django.db.models import Count
from django.urls import reverse
from django.utils.timesince import timesince

class PostConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if self.user:
            self.accept()
            self.all_posts = Post.objects.annotate(rating = Count("liked_users")-Count("disliked_users"), comment_count = Count("post_comments"))

    def receive(self, text_data):
        seen_posts = text_data.split(",")

        feed_posts = self.user.profile.get_posts(self.all_posts,seen_posts)

        for post in feed_posts:
            post.rating = len(post.liked_users.all()) - len(post.disliked_users.all())

        stringified_posts = []

        for post in feed_posts:
            post.best_3_comments = post.post_comments.annotate(rating=Count("liked_users")-Count("disliked_users")).order_by("-rating")[:3]

        for post in feed_posts:
            stringified_posts.append(f"""
                <div class="feed-post" id="post-{ post.id }">
            <div class="post-head">
                <a class="user" href="{reverse("user-profile-page", kwargs={"username":f"{post.user}"})}">
                    <img src="https://picsum.photos/seed/{post.user.id}/100" alt="User Profile Picture">
                    <p>{post.user.username}</p>
                </a>
                
            </div>

            <div class="post-body">
            <div class="youtube" data-embed="{post.video_link}"></div>
            </div>

            <div class="post-footer">
                <div class="likes-section footer-section">
                    <i class="p-like-btn-{post.id} like-button fa-solid fa-heart {"liked" if self.user in post.liked_users.all() else ""}" onclick='like(`{reverse("like-post", kwargs={"post_id":post.id})}`, `p`, `{post.id}`)'></i>
                    <p class="p-points-{ post.id }">{ post.rating }</p>
                    <i class="p-dislike-btn-{post.id} dislike-button fa-solid fa-heart-crack {"disliked" if self.user in post.disliked_users.all() else ""}" onclick='dislike(`{reverse("dislike-post", kwargs={"post_id":post.id})}`,`p`,`{post.id}`)'></i>
                </div>
                <div class="comments-section footer-section">
                    <a href="{reverse("post-page", kwargs={"post_id":post.id})}#post-comments"><i class="fa-solid fa-comment"></i></a>
                </div>
                <div class="share-section footer-section share-btn-{post.id}" onclick="share_post(`{ post.id }`)">
                    <p><i class="fa-solid fa-share-nodes"></i></p>
                </div>
                <div class="bookmark-section footer-section" onclick='bookmark_post(`{reverse("bookmark-post", kwargs={"post_id":post.id})}`,`{ post.id }`)'>

                    <i class="bookmark-btn-{post.id} fa-{"solid" if post in self.user.profile.bookmarked_posts.all() else "regular"} fa-bookmark"></i>

                    
                </div>
            </div>

            <div class="post-end">

                <div class="post-info">
                    {f"<small>{timesince(post.created_date)} ago</small>" if post.created_date == post.updated_date else f"<small>{ timesince(post.created_date) } ago (updated)</small>"}
                </div>

                <div class="post-description">
                    <p>{ post.description }</p>
                </div>
                <div class="post-tags">
                {"".join([f'<a href="{reverse("posts-page")}?tag={tag.name}" class="post-tag">#{tag.name}</a>' for tag in post.tags.all()]) if post.tags.all() else ""}
                </div>
                <div class="post-comments">
                {"".join([f'<div class="comment"><p><strong>{ comment.user.username }</strong></p>          <p>{comment.content}</p></div>' for comment in post.best_3_comments]) if post.best_3_comments else ""}
                </div>
            </div>
        </div>""")

        self.send(text_data=json.dumps(stringified_posts))