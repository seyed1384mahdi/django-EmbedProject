from django.db.models import QuerySet
from codinghobbies.blog.models import Post, Subscription
from codinghobbies.users.models import BaseUser
from codinghobbies.blog.filters import PostFilter


def get_subscribers(*, user:BaseUser) -> QuerySet[Subscription]:
    return Subscription.objects.filter(subscriber=user)

def post_detail(*, slug:str, user:BaseUser, self_include:bool = True) -> QuerySet[Post]:
    subscribtions = list(Subscription.objects.filter(subscriber=user).values_list("target", flat=True))
    if self_include:
        subscribtions.append(user.id)
    
    return Post.objects.get(slug=slug, author__in=subscribtions)

def post_list(*, filters=None, user:BaseUser, self_include:bool = True) -> QuerySet[Post]:
    filters = filters or {}
    subscriptions = list(Subscription.objects.filter(subscriber=user).values_list("target", flat=True))
    if self_include:
        subscriptions.append(user.id)
    if subscriptions:
        qs = Post.objects.filter(author__in=subscriptions)
        return PostFilter(filters, qs).qs
    return Post.objects.none()
    