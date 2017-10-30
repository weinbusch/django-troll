
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from django_troll.forms import CommentForm

@require_POST
def add_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        obj = form.save()
        return redirect(obj.content_object)