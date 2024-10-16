from codinghobbies.users.models import BaseUser
from codinghobbies.blog.models import Subscription, Post

from django.utils.text import slugify
from django.db import transaction

def count_following(*, user:BaseUser) -> int:
    return Subscription.objects.filter(subscriber=user).count()

def count_posts(*, user:BaseUser) -> int:
    return Post.objects.filter(author=user).count()


def subscribe(*, user:BaseUser, email:str) -> Subscription:
    target = BaseUser.objects.get(email=email)
    sub = Subscription(subscriber=user, target=target)
    sub.full_clean()
    sub.save()
    return sub

def unsubscribe(*, user: BaseUser, email: str) -> dict:
    target = BaseUser.objects.get(email=email)
    Subscription.objects.get(subscriber=user, target=target).delete()

@transaction.atomic
def create_post(*, user: BaseUser, title: str, content: str) -> Post:
    post = Post.objects.create(
        author=user, title=title, content=content,  slug=slugify(title)
    )

    return post