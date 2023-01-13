from django.test import TestCase

# Create your tests here.

# import sys, os
#
from catalog.models import Author, BookInstance, Book, Genre


#
# myPath = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, myPath + '/../')
class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        print(1234)
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author=Author.objects.get(id=1)
        """Мы не можем получить поле verbose_name напрямую через 
        author.first_name.verbose_name, потому что author.first_name является строкой.
         Вместо этого, нам надо использовать атрибут _meta объекта автора для получения того 
         экземпляра поля, который будет использоваться для получения дополнительной информации"""
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label,'first name')

    def test_date_of_death_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        """Мы выбрали метод assertEquals(field_label,'first name')
         вместо assertTrue(field_label == 'first name'), потому что,
          в случае провала теста, в выводе будет указано какое именно значение содержит метка
           и это немного облегчит нам задачу по отладке кода."""
        self.assertEquals(field_label,'died')

    def test_first_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        author=Author.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEquals(expected_object_name,str(author))

    def test_get_absolute_url(self):
        author=Author.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(),'/catalog/author/1')

    def test_last_name_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label,'last name')

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 100)

    def test_date_of_birth_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label,'date of birth')

class BookInstanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        print(1234)
        genre = Genre.objects.create(name='Big')
        author = Author.objects.create(first_name='Big', last_name='Bob')
        book = Book(title='Big', author=author,summary='big',isbn='2',genre=genre)
        BookInstance(book=book, imprint='Bob',due_back='null')

    def test_imprint_label(self):
        book_instance=BookInstance.objects.get(id=1)
        imprint_label = book_instance._meta.get_field('imprint').verbose_name
        self.assertEquals(imprint_label,'imprint')