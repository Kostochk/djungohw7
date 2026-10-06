from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reader_profile', null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name="Ім'я")
    last_name = models.CharField(max_length=100, verbose_name="Прізвище")
    phone = models.CharField(max_length=20, verbose_name="Контактний телефон")
    email = models.EmailField(verbose_name="Email")
    registration_date = models.DateField(auto_now_add=True, verbose_name="Дата запису до бібліотеки")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва книги")
    author = models.CharField(max_length=150, verbose_name="Автор")
    publication_year = models.PositiveIntegerField(verbose_name="Рік видання")
    style = models.CharField(max_length=100, verbose_name="Стиль/Жанр")
    publisher = models.CharField(max_length=150, verbose_name="Видавництво")
    current_reader = models.ForeignKey(
        Reader, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='borrowed_books',
        verbose_name="Хто взяв книгу"
    )

    @property
    def is_available(self):
        """Перевірка наявності книги в бібліотеці"""
        return self.current_reader is None

    def __str__(self):
        return self.title


@receiver(post_migrate)
def create_reader_group(sender, **kwargs):
    if sender.name == 'your_app_name': 
        group, created = Group.objects.get_or_create(name='Readers')
        
        content_type = ContentType.objects.get_for_model(Book)
        view_book_permission = Permission.objects.get(codename='view_book', content_type=content_type)
        
        group.permissions.add(view_book_permission)