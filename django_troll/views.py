
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from django_troll.forms import CommentForm

def get_content_object(data):
    ct = data['content_type']
    pk = data['object_id']
    return ct.get_object_for_this_type(pk=pk)

@require_POST
def add_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        obj = form.save()
        return redirect(obj.content_object)
    # Try to redirect to content_object
    content_object = get_content_object(form.cleaned_data)
    return redirect(content_object)