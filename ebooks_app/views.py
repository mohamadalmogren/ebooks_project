from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .forms import ContactForm, BookForm, UserForm, ProfileForm, LoginForm
from .models import Book

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

def is_admin_group(user):
    return user.groups.filter(name='admin').exists()

def private_view(request):
    if is_admin_group(request.user):
        return render(request, 'private.html', {})
    else:
        return HttpResponseRedirect(reverse('home'))

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    template_name = 'book_form.html'

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    template_name = 'book_form.html'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('home')
    template_name = 'book_confirm_delete.html'

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.error(request, 'user is not active')
            else:
                messages.error(request, 'invalid username of password')
    
    data = {'form': form}
    return render(request, 'login.html', data)

def register(request):
    userForm = UserForm()
    profileForm = ProfileForm()

    if request.method == 'POST':
        userForm = UserForm(request.POST)
        profileForm = ProfileForm(request.POST)

        if userForm.is_valid() and profileForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = profileForm.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect(reverse('home'))

    data = { 'userForm': userForm, 'profileForm': profileForm}
    return render(request, 'register.html', data)


def index(request):
    books = Book.objects.all()
    data = {
        'books': books
     }
    return render(request, 'index.html', data)

def detail(request, pk):    
    book = get_object_or_404(Book, pk=pk)    
    data = {
        'book': book
    }
    return render(request, 'detail.html', data)

def add_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            if 'picture' in request.FILES:
                book.picture = request.FILES['picture']
            book.save()            
            messages.success(request, 'your book have been added succesfully')
            return HttpResponseRedirect(reverse('home'))

    data = {
        'form': form
    }
    return render(request, 'add_book.html', data)

def contact(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            body = form.cleaned_data['body']
            send_email(name, email, body)
            form = ContactForm()
            messages.success(request, 'email is sent, we will contact you soon')
            return HttpResponseRedirect(reverse('contact'))
    data = { 
        'form': form
    }
    return render(request, 'contact.html', data)

def send_email(name, email, body):
    print('sending email done')