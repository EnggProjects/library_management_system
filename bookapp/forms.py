from django import forms
from .models import Book, Student

class IssueBookForm(forms.Form):
    isbn2 = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        empty_label="Book Name [ISBN]",
        to_field_name="isbn",
        label="Book (Name and ISBN)"
    )
    name2 = forms.ModelChoiceField(
        queryset=Student.objects.none(),
        empty_label="Name [Branch] [Class] [Roll No]",
        label="Student Details"
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.is_superuser:
            self.fields['name2'].queryset = Student.objects.all()
        else:
            self.fields['name2'].queryset = Student.objects.filter(user=user)

        self.fields['isbn2'].widget.attrs.update({'class': 'form-control'})
        self.fields['name2'].widget.attrs.update({'class': 'form-control'})

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['branch', 'classroom', 'roll_no', 'phone', 'image']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'isbn', 'category', 'pdf_file']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter book name'})
        self.fields['author'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter author name'})
        self.fields['isbn'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter ISBN number'})
        self.fields['category'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select category'})
        self.fields['pdf_file'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload PDF file'})

        for field_name, field in self.fields.items():
            field.required = True
