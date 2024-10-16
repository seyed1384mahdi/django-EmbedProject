from django.urls import path, include

urlpatterns = [
    path('blog/', include(('codinghobbies.blog.urls', 'blog'))),
    path('users/', include(('codinghobbies.users.urls', 'users')))
]
