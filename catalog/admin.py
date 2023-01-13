from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# Register your models here.
class BooksAutorInline(admin.TabularInline):
    model = Book
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    inlines = [BooksAutorInline]
    fields = ['first_name', 'last_name',   ('date_of_birth', 'date_of_death')]



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]
# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display=('id','due_back')
    list_filter = ('status', 'due_back')
    fieldsets = (
        ('King', {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )



# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
# admin.site.register(BookInstance)
