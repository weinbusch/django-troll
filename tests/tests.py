import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.template import Template, Context

from django_troll.models import Comment
from django_troll.forms import CommentForm

from tests.models import Book, Movie

class CommentModel(TestCase):

    def test_create_comments_on_books_and_movies(self):
        book = Book.objects.create()
        comment = Comment.objects.create(
            comment='I like!',
            content_object=book,
        )
        self.assertEqual(comment.timestamp.date(), datetime.date.today())

        movie = Movie.objects.create()
        comment = Comment.objects.create(
            comment='I like!',
            content_object=movie,
        )
        self.assertEqual(comment.timestamp.date(), datetime.date.today())
        self.assertEqual(comment.content_type, ContentType.objects.get_for_model(movie))

    def test_delete_comment(self):
        book = Book.objects.create()
        comment = Comment.objects.create(content_object=book, comment='Delete me!')
        comment.delete()
        self.assertEquals(Book.objects.count(), 1)
        self.assertEquals(Comment.objects.count(), 0)

        # The following depends on a GenericRelation in the Book model
        comment = Comment.objects.create(content_object=book, comment='I will go, when you go.')
        book.delete()
        self.assertEquals(Book.objects.count(), 0)
        self.assertEquals(Comment.objects.count(), 0)

    def test_different_api(self):
        book = Book.objects.create()
        ct = ContentType.objects.get_for_model(book)

        comment = Comment.objects.create(
            content_type=ct,
            object_id=book.pk,
            comment='Test'
        )

        self.assertEquals(comment.content_object, book)

class Forms(TestCase):

    def test_create_comment(self):
        book = Book.objects.create()
        ct = ContentType.objects.get_for_model(book)
        data = {
            'comment': 'ALL CAPITAL LETTERS AND EXCLAMATION MARKS!!!!!!',
            'object_id': book.pk,
            'content_type': ct.pk,
        }
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.content_object, book)

    def test_errors(self):
        book = Book.objects.create()
        ct = ContentType.objects.get_for_model(book)
        data = {
            'comment': '',
            'object_id': book.pk,
            'content_type': ct.pk,
        }
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors)

    def test_hidden_and_visible_fields(self):
        form = CommentForm()
        self.assertIn('comment', [bf.name for bf in form.visible_fields()])
        self.assertIn('content_type', [bf.name for bf in form.hidden_fields()])
        self.assertIn('object_id', [bf.name for bf in form.hidden_fields()])

    def test_required_fields(self):
        form = CommentForm()
        self.assertTrue(form.fields['comment'].required)
        self.assertTrue(form.fields['object_id'].required)
        self.assertTrue(form.fields['content_type'].required)
                
class Views(TestCase):

    def test_allowed_methods(self):
        response = self.client.get(reverse('comment_add'))
        self.assertEquals(response.status_code, 405)

    def test_post_comment(self):
        book = Book.objects.create()
        ct = ContentType.objects.get_for_model(book)
        data = {
            'comment': 'Post this!',
            'object_id': book.pk,
            'content_type': ct.pk,
        }
        response = self.client.post(reverse('comment_add'), data=data)
        self.assertEquals(Comment.objects.count(), 1)
        self.assertRedirects(response, book.get_absolute_url())

    def test_post_invalid_comment(self):
        book = Book.objects.create()
        ct = ContentType.objects.get_for_model(book)
        data = {
            'comment': '',
            'object_id': book.pk,
            'content_type': ct.pk,
        }
        response = self.client.post(reverse('comment_add'), data=data)
        self.assertEquals(Comment.objects.count(), 0)
        self.assertRedirects(response, book.get_absolute_url())

class TemplateTags(TestCase):

    def test_comment_form_for_object(self):
        book = Book.objects.create()
        template = Template('{% load troll %}{% comment_form_for_object object as form %}')
        context = Context({'object': book})
        out = template.render(context)
        form = context['form']
        self.assertEqual(form.initial['content_type'], ContentType.objects.get_for_model(book))
        self.assertEqual(form.initial['object_id'], book.pk)

    def test_render_comment_for_object(self):
        book = Book.objects.create()
        template = Template('{% load troll %}{% render_comment_form_for_object object %}')
        context = Context({'object': book})
        out = template.render(context)
        post_url = reverse('comment_add')
        self.assertIn('<form action="{}" method="POST">'.format(post_url), out)
        self.assertIn('</form>', out)      
        self.assertNotIn('form', context)  

    def test_get_comments_for_object(self):
        book = Book.objects.create()
        Comment.objects.create(comment='First', content_object=book)
        Comment.objects.create(comment='Second', content_object=book)
        template = Template('{% load troll %}{% get_comments_for_object object as comments %}')
        context = Context({'object': book})
        out = template.render(context)
        qs = context['comments']
        self.assertEqual(qs.count(), 2)

    def test_render_comments_for_object(self):
        book = Book.objects.create()
        c1 = Comment.objects.create(comment='First', content_object=book)
        Comment.objects.create(comment='Second', content_object=book)
        template = Template('{% load troll %}{% render_comments_for_object object %}')
        context = Context({'object': book})
        out = template.render(context)
        self.assertIn('<span class="timestamp">', out)
        self.assertIn('First', out)
