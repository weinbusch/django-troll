from django.conf.urls import url, include
from django.views.generic import DetailView, ListView

from tests.models import Book

urlpatterns = [
    url(r'^$', ListView.as_view(model=Book), name='index'),
    url(r'^comments/', include('django_troll.urls')),
    url(r'^book/(?P<pk>\d+)/$', DetailView.as_view(model=Book), name='book_detail'),
]