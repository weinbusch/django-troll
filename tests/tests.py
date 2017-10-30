import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

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
        form.is_valid()
        comment = form.save()
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
        form.is_valid()
        self.assertIn('comment', form.errors)

    def test_hidden_and_visible_fields(self):
        form = CommentForm()
        self.assertIn('comment', [bf.name for bf in form.visible_fields()])
        self.assertIn('content_type', [bf.name for bf in form.hidden_fields()])
        self.assertIn('object_id', [bf.name for bf in form.hidden_fields()])

class Views(TestCase):

    def test_book_absolute_url(self):
        book = Book.objects.create()
        response = self.client.get(book.get_absolute_url())
        self.assertEqual(response.status_code, 200)

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
