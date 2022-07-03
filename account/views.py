import datetime as dt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from crab.models import Error


from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm, ContactForm


def register_user(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password1'])
        new_user.save()
        messages.success(request, 'İstifadəçi sistemə əlavə edildi')
        return render(request, 'account/register_done.html', {'new_user': 'new_user'})
    context = {
        'form': form
    }
    return render(request, 'account/register.html', context=context)


def user_login(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('index')
    context = {
        'form': form
    }
    return render(request, 'account/login.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('index')


def update_user(request):
    contact_form = ContactForm
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.city = data['city']
                user.category = data['category']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Məlumatlar yeniləndi.')
                return redirect('update')
        else:
            form = UserUpdateForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'city': user.city,
                'category': user.category,
                'send_email': user.send_email
            })
        context = {
            'form': form,
            'contact_form': contact_form
        }
        return render(request, 'account/update.html', context=context)
    else:
        return redirect('account/login.html')


def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            city = data.get('city')
            category = data.get('category')
            email = data.get('email')
            qs = Error.objects.filter(create_at=dt.date.today())
            if qs.exists():
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'city': city, 'category': category, 'email': email})
                err.data['user_data'] = data
                err.save()
            else:
                data = [{'city': city, 'category': category, 'email': email}]
                Error(data=f"user_data:{data}").save()
            messages.success(request, 'Məlumatlar servisin administrasiyasına göndərildi.')
            return redirect('update')
        else:
            return redirect('account/update.html')
    else:
        return redirect('account/login.html')
