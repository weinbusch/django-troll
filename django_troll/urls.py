from django.conf.urls import url, include

from django_troll import views

urlpatterns = [
    url(r'^add/$', views.add_comment, name='comment_add'),
]