from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book, Reader

@login_required
@permission_required('your_app_name.view_book', raise_exception=True)
def book_list_view(request):
    """Відображення списку книг (Завдання 3 та 5)"""
    mode = request.GET.get('mode', 'all')
    if mode == 'available':
        books = Book.objects.filter(current_reader__isnull=True)
        title = "Книги у наявності"
    else:
        books = Book.objects.all()
        title = "Усі книги"
        
    return render(request, 'library/book_list.html', {
        'books': books,
        'title': title,
        'mode': mode
    })


@login_required
@permission_required('your_app_name.view_reader', raise_exception=True)
def reader_list_view(request):
    """Відображення списку читачів (Завдання 3)"""
    readers = Reader.objects.all()
    return render(request, 'library/reader_list.html', {'readers': readers})


@login_required
@permission_required('your_app_name.view_reader', raise_exception=True)
def reader_detail_view(request, pk):
    """Детальна інформація про читача та його книги (Завдання 3)"""
    reader = get_object_or_404(Reader, pk=pk)
    borrowed_books = reader.borrowed_books.all() 
    
    return render(request, 'library/reader_detail.html', {
        'reader': reader,
        'borrowed_books': borrowed_books
    })