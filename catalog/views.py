from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from .forms import RenewBookForm


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 3

    def get_queryset(self):
        return Book.objects.all()



class AuthorDetailView(LoginRequiredMixin, generic.DetailView):

    model = Author



class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    login_url = '/accounts/login/'
    redirect_field_name = 'futers'
    paginate_by = 2

    def get_queryset(self):
        return Author.objects.all()


@login_required
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.

    num_genres = Genre.objects.all().count()
    num_roman = Genre.objects.filter(name__icontains='roman').count()
    num_a = Book.objects.filter(title__icontains='p').count()
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context

    num_authors = Author.objects.count()  # The 'all()' is implied by default.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(
        request,
        'index.html',
        context={
            'num_books':num_books,
            'num_instances':num_instances,
            'num_instances_available':num_instances_available,
            'num_authors':num_authors,
            'num_genres':num_genres,
            'num_roman':num_roman,
            'num_a':num_a,
            'num_visits': num_visits,
        },
    )
# Create your views here.


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o')\
            .order_by('due_back')

class BorrowedBooksByUserListView(PermissionRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_all.html'
    permission_required = 'can_mark_returned'
    paginate_by = 2
    # Or multiple permissions
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, book_id):
    book_inst = get_object_or_404(BookInstance, pk=book_id)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            #(здесь мы просто присваиваем их полю due_back)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('borrowed') )

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death': '12/10/2016',}
    permission_required = 'add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    permission_required = 'change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'delete_author'

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    initial={'date_of_death': '12/10/2016',}
    permission_required = 'add_book'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title','author','summary','isbn','genre']
    permission_required = 'change_book'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'delete_book'


