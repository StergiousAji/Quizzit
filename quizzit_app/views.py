from django.shortcuts import render, redirect
from django.http import HttpResponse
from quizzit_app.models import Category, Record, Quiz, Register_User, UserProfile
from quizzit_app.forms import UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

category_list = Category.objects.all()

# Create your views here.
def home(request):
    context_dict = {'categories': category_list,}
    
    return render(request, 'quizzit/home.html', context_dict)

def about(request):
    context_dict = {'categories': category_list,}
    
    return render(request, 'quizzit/about.html', context_dict)

def categories(request):
    context_dict = {'categories': category_list,}
    
    return render(request, 'quizzit/categories.html', context_dict)

def show_category(request, category_name_slug):
    context_dict = {'categories': category_list,}
    # .get() method returns only one object or a DoesNotExist exception
    try:
        category = Category.objects.get(slug=category_name_slug)

        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None

    return render(request, 'quizzit/category.html', context=context_dict)

def quiz(request):#, quiz_name_slug):
    context_dict = {'categories': category_list,}
    # .get() method returns only one object or a DoesNotExist exception
    # try:
    #     quiz = Quiz.objects.get(slug=quiz_name_slug)

    #     context_dict['quiz'] = quiz
    # except Category.DoesNotExist:
    #     context_dict['quiz'] = None

    return render(request, 'quizzit/quiz.html', context=context_dict)

def howtoplay(request):
    context_dict = {'categories': category_list,}
    
    return render(request, 'quizzit/howtoplay.html', context_dict)

def register(request):
    registered = False

    if (request.method == 'POST'):
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if (user_form.is_valid() and profile_form.is_valid()):
            user = user_form.save()
            # Hash the user's password before saving to the database.
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if ('picture' in request.FILES):
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        # If not a HTTP POST then render a blank form.
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'quizzit/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    invalid_login = False

    if (request.method == 'POST'):
        # request.POST.get(<variable>) returns None as oppposed to a KeyError Exception as with request.POST[<variable>]
        username = request.POST.get('username')
        password = request.POST.get('password')
        # If user exists a User object is returned otherwise None.
        user = authenticate(username=username, password=password)

        if (user):
            if (user.is_active):
                login(request, user)
                return redirect(reverse('quizzit:home'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            invalid_login = True
            return render(request, 'quizzit/login.html', {'invalid_login': invalid_login })
    else:
        return render(request, 'quizzit/login.html', {'invalid_login': invalid_login })

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def leaderboards(request):
    context_dict = {}
    
    return render(request, 'quizzit/leaderboards.html', context_dict)