from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import User, Follow, Like


def get_likes_of_post(post):
    return Like.objects.filter(post=post).count()


def get_followers_amount(user):
    return Follow.objects.filter(following=user).count()


def render_posts(posts, page, user):
    renderable_posts = []

    for post in posts:
        renderable_posts.append({
            "id": post.id,
            "content": post.content,
            "author": post.author.username,
            "is_editable": user == post.author,
            "author_id": post.author.id,
            "timestamp": post.timestamp.strftime("%B %d, %Y at %H:%M"),
            "likes": get_likes_of_post(post),
            "is_liked": is_post_liked(user, post)
        })

    if page >= 1:
        paginator = Paginator(renderable_posts, 10)

        return {
            "posts": paginator.page(page).object_list,
            "hasPrevious": page > 1,
            "hasNext": paginator.num_pages > page,
        }
    else:
        return {
            "posts": renderable_posts,
            "hasPrevious": False,
            "hasNext": False
        }


def get_followed_users_ids(user):
    return Follow.objects.filter(follower=user).values_list('following', flat=True)


def is_user_followable(profile_user, user):
    return user.is_authenticated and\
        profile_user!= user and not\
        Follow.objects.filter(follower=user, following=profile_user).exists()


def is_user_unfollowable(profile_user, user):
    return user.is_authenticated and\
        profile_user!= user and\
        Follow.objects.filter(follower=user, following=profile_user).exists()


def is_post_liked(user, post):
    return user.is_authenticated and\
        Like.objects.filter(user=user, post=post).exists()
