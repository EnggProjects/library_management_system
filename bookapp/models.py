from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

def get_expiry_date():
    """
    Function to generate the default expiry date (14 days from today)
    """
    return datetime.today() + timedelta(days=14)

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science', 'Science'),
        ('Biography', 'Biography'),
        ('Poetry', 'Poetry'),
        ('Education', 'Education'),
    ]

    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    pdf_file = models.FileField(upload_to='book_pdfs/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} [{self.isbn}]"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    classroom = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=3, unique=True)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} [{self.branch}] [{self.classroom}] [{self.roll_no}]"

class IssuedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='issued_books', null=True)
    issued_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(default=get_expiry_date)

    def __str__(self):
        return f"{self.book.name} - {self.student.user.username if self.student else 'No Student'}"