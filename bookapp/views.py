from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import StudentRegistrationForm, BookForm, IssueBookForm
from .models import Book, Student, IssuedBook
from datetime import date, datetime, timedelta
from django.db.models import Q

def index(request):
    return render(request, "index.html")

def view_books(request):
    books = Book.objects.all()
    return render(request, "view_books.html", {'books': books})

@login_required(login_url='/admin_login')
def view_students(request):
    if request.user.is_superuser:
        students = Student.objects.all()
        return render(request, "view_students.html", {'students': students})
    else:
        return HttpResponse("You are not authorized to view this page.")

@login_required(login_url='/admin_login')
def view_issued_book(request):
    issued_books = IssuedBook.objects.all()
    issued_books_data = [
        {
            'book': issued_book.book,
            'student': issued_book.student,
            'issued_date': issued_book.issued_date,
            'expiry_date': issued_book.expiry_date
        }
        for issued_book in issued_books
    ]
    return render(request, 'view_issued_book.html', {'issued_books_data': issued_books_data})

@login_required
def student_issued_books(request):
    student = request.user.student
    issued_books = IssuedBook.objects.filter(student=student)
    context = {'issued_books': issued_books}
    return render(request, 'student_issued_books.html', context)

@login_required(login_url='/student_login')
def profile(request):
    student = Student.objects.get(user=request.user)
    context = {'student': student}
    return render(request, "profile.html", context)

@login_required(login_url='/student_login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']

        student.user.email = email
        student.phone = phone
        student.branch = branch
        student.classroom = classroom
        student.roll_no = roll_no
        student.user.save()
        student.save()
        alert = True
        return render(request, "edit_profile.html", {'alert': alert})
    return render(request, "edit_profile.html")

@login_required(login_url='/admin_login')
def delete_book(request, myid):
    if request.user.is_superuser:
        books = Book.objects.filter(id=myid)
        books.delete()
        return redirect("/view_books")
    else:
        return HttpResponse("You are not authorized to delete books.")

@login_required(login_url='/admin_login')
def delete_student(request, myid):
    if request.user.is_superuser:
        students = Student.objects.filter(id=myid)
        students.delete()
        return redirect("/view_students")
    else:
        return HttpResponse("You are not authorized to delete students.")

@login_required(login_url='/student_login')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert': alert})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {'currpasswrong': currpasswrong})
        except:
            pass
    return render(request, "change_password.html")

def student_registration(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        student_form = StudentRegistrationForm(request.POST, request.FILES)

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            return redirect("/student_login")
    else:
        user_form = UserCreationForm()
        student_form = StudentRegistrationForm()

    return render(request, "student_registration.html", {'user_form': user_form, 'student_form': student_form})

def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("/profile")
        else:
            alert = True
            return render(request, "student_login.html", {'alert': alert})
    return render(request, "student_login.html")

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/add_book")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert': alert})
    return render(request, "admin_login.html")

def Logout(request):
    logout(request)
    return redirect("/")

@user_passes_test(lambda u: u.is_superuser, login_url='/admin_login')
@login_required(login_url='/admin_login')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect('success_url')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

def success_view(request):
    return render(request, "success.html")

@login_required
def issue_book(request, isbn=None):
    book = None
    if isbn:
        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            return HttpResponse("Book not found")

    form = IssueBookForm(
        user=request.user,
        data=request.POST or None,
        initial={'isbn2': book} if book else None
    )

    if request.method == "POST" and form.is_valid():
        obj = IssuedBook()
        if request.user.is_superuser:
            obj.student = form.cleaned_data['name2']
        else:
            obj.student = request.user.student

        obj.book = form.cleaned_data['isbn2']
        obj.save()

        alert = True
        redirect_url = "/issue_book" if request.user.is_superuser else "/student_issued_books"
        return render(request, "issue_book.html", {'alert': alert, 'redirect_url': redirect_url})

    return render(request, "issue_book.html", {'form': form})

@login_required
def view_all_books(request):
    books = Book.objects.all()
    filter_form = BookForm(request.GET or None)

    if filter_form.is_valid():
        category = filter_form.cleaned_data.get('category')
        if category:
            books = books.filter(category=category)

    context = {'books': books, 'filter_form': filter_form}
    return render(request, 'view_all_books.html', context)

def search_books(request):
    query = request.GET.get('q')
    books = Book.objects.filter(
        Q(name__icontains=query) |
        Q(author__icontains=query) |
        Q(isbn__icontains=query)
    ) if query else Book.objects.all()

    context = {'books': books, 'query': query}
    return render(request, 'view_books.html', context)
