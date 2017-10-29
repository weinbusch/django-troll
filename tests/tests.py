import datetime

from django.test import TestCase

from django_troll.models import Comment

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

