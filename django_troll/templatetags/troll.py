
from django import template
from django.contrib.contenttypes.models import ContentType

from django_troll.forms import CommentForm

register = template.Library()

@register.assignment_tag
def comment_form_for_object(obj):
    '''
    {% comment_form_for_object object as form %}
    '''

    initial = {
        'content_type': ContentType.objects.get_for_model(obj),
        'object_id': obj.pk
    }
    form = CommentForm(initial=initial)
    return form

@register.inclusion_tag('django_troll/form.html')
def render_comment_form_for_object(obj):
    form = comment_form_for_object(obj)
    return {'form': form}