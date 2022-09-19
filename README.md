# social-media-platform 's Features
> A social media platform.

Every action on the website is live and does not require to redirect the user.

*This is made with AJAX requests.*

## User Actions

### Register
Registration form of the website

![register](https://user-images.githubusercontent.com/93938698/190922056-ee41ea66-32d9-4bf2-b5fc-8482cb6938c9.png)

***

### Log In To Account
Login form of the website

![login](https://user-images.githubusercontent.com/93938698/190922060-8e43c0ee-5fee-425d-af64-9e951e3e2fee.png)

***

### Log Out
The log-out button logs the user out and then sends them back to where they came (HTTP_REFERER)

![logout](https://user-images.githubusercontent.com/93938698/190923910-8b208214-12e5-4c6e-a2a7-b7cab414aa1b.gif)

## Viewing Posts

### Feed
The homepage of the website, it loads more posts as the user goes. There is no need to refresh the page.

*It is made with Django Channels.*

![feed](https://user-images.githubusercontent.com/93938698/190931970-b9eb13c8-eaf0-4e6c-b25d-4007cf167a25.gif)

The feed includes:

* 3 random posts that user might be interested in.
* 1 random new post
* 1 all random post
* 1 random top post
* 2 newest posts of followed users (if the user is not following any users, replace with 2 random posts.)

The top rated 3 comments of the post are shown at the end of each post.

The feed page loads new posts everytime the user reaches the last post. There is 3 seconds cooldown for this action and the user must be authenticated.

Tags of the posts open the posts page and filters the posts by the tag when clicked.

***

### Filter Posts
![filterposts](https://user-images.githubusercontent.com/93938698/190927782-4d1f311f-5c1f-4248-a435-609ca57e6438.gif)

Posts can be filtered by:

1. Date
   * All Time
   * This Year
   * This Month
   * This Week
   * Today

2. Tag name

Posts can be ordered by:

* Rating
* Comment Count
* Vote Count
* Date
* Random

And the order can be selected:
* Ascending
* Descending

The user can select how many posts per page is going to be shown, and also they can select the page number.

***

### View Post
![viewpost](https://user-images.githubusercontent.com/93938698/190922087-b9b0ddae-ec29-43f0-8013-b9f756153d28.png)

## Post Actions

### Create 
![sharepost](https://user-images.githubusercontent.com/93938698/190922092-2bb9f0d0-077c-4926-989e-2c31c7b2c4f0.png)
![aftersharingpost](https://user-images.githubusercontent.com/93938698/190922093-1e54db4e-dcd9-4908-9421-7ad1e4655b10.png)

***

### View
![viewpost](https://user-images.githubusercontent.com/93938698/190922107-6b4deb6f-dd07-4cac-a79e-9935181cc01a.png)

***

### Edit
![updatepost](https://user-images.githubusercontent.com/93938698/190922100-46b8ff22-ea03-4f5c-88af-26d0be506fde.png)
![afterupdating](https://user-images.githubusercontent.com/93938698/190922120-2687031a-904e-46fa-b4c4-39fc0fbcb8d9.png)

***

### Delete
![deletepost](https://user-images.githubusercontent.com/93938698/190922113-9275ee6f-a1c3-4b12-ba53-b19d2d268be4.png)

***

### Like, Dislike, Bookmark

![likedislikebookmarkpost1](https://user-images.githubusercontent.com/93938698/190922870-ebd876a4-6157-46ad-87f5-b85d4c2043b8.gif)

***

### Share
When clicked, the video link gets copied to clipboard and share button's background color turns green.
![share](https://user-images.githubusercontent.com/93938698/190924500-e9879590-2b4b-41dd-8530-2a567c1b9248.gif)


## Comment Actions

### Make Comment, Like, Dislike, Delete
![commentactions](https://user-images.githubusercontent.com/93938698/190925639-f381b2b5-8f14-4dd6-90ab-adee7cc53037.gif)

## Profiles

### Self Profile Page
![selfprofile](https://user-images.githubusercontent.com/93938698/190922132-7d3a3c93-732d-43ba-943e-9942c500550f.png)

***

### Another User's Profile Page
![someoneelsesprofile](https://user-images.githubusercontent.com/93938698/190922137-af6df15f-8bc3-4735-80a9-b1d08b0d1328.png)

***

### Follow User, Followed Users, Users You May Know
![followandfollowedusers](https://user-images.githubusercontent.com/93938698/190924816-04ed9751-499b-4752-bcb3-3c69ba1e5f64.gif)

_Users You May Know_ section consists of the users that the user's followed users follow.

The more followed users of the user is following a user , the higher that user is going to be shown in the _Users You May Know_ section.

***

### Followers
Users can view their followers by going to their profiles and clicking the Followers button right to their profile pictures.

![followers](https://user-images.githubusercontent.com/93938698/190924609-4897caf4-e559-4a00-a42c-9eecd692ce61.png)

***

### Liked, Disliked, Bookmarked Posts
When the user likes, dislikes or bookmarkes a post, they can go to their profile and look for the post by clicking the related section of the sidebar on the left.

![likedislikebookmarkpost1](https://user-images.githubusercontent.com/93938698/190922870-ebd876a4-6157-46ad-87f5-b85d4c2043b8.gif)
