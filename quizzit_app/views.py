from django.shortcuts import render, redirect
from django.http import HttpResponse
from quizzit_app.models import Category, Record, Quiz, Question, Register_User, UserProfile
from quizzit_app.forms import UserForm, UserProfileForm, RecordForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


category_list = Category.objects.all()

# Create your views here.
def home(request):
    top_3_quizzes = Quiz.objects.order_by('-views')[:3]
    context_dict = { 'categories': category_list,
                     'most_popular_quiz_1': top_3_quizzes[0],
                     'most_popular_quiz_2': top_3_quizzes[1],
                     'most_popular_quiz_3': top_3_quizzes[2] }
    
    return render(request, 'quizzit/home.html', context_dict)

def about(request):
    context_dict = {'categories': category_list,}
    
    return render(request, 'quizzit/about.html', context_dict)

def categories(request):
    context_dict = {'categories': category_list,}
    
    return render(request, 'quizzit/categories.html', context_dict)

# Global Variable index to display correct Question.
index = 0
score = 0
score_list = []
user_done = False
total_score = 0
def show_category(request, category_name_slug):
    context_dict = {'categories': category_list,}
    # .get() method returns only one object or a DoesNotExist exception
    try:
        category = Category.objects.get(slug=category_name_slug)
        quizzes = Quiz.objects.all().filter(category=category)

        context_dict['category'] = category
        context_dict['quiz'] = quizzes
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['quiz'] = None
    
    # Reset the Question index and booleans
    global index, score, score_list, user_done, total_score
    index = 0
    score = 0
    user_done = False
    total_score = 0
    score_list = []
    for i in range(7):
        score_list.append(0)

    return render(request, 'quizzit/category.html', context=context_dict)

def quiz(request, category_name_slug, quiz_name_slug):
    context_dict = {'categories': category_list,}
    global index, score, score_list, user_done, total_score
    try:
        quiz = Quiz.objects.get(slug=quiz_name_slug)
        quiz.views += 1
        quiz.save()

        questions = Quiz.objects.get(quizID=quiz.quizID).question_set.all()

        record = None
        if (request.is_ajax() ):
            data = request.POST
            data_ = dict(data.lists())
            data_.pop('csrfmiddlewaretoken')
            print(data_)
            user = request.user
            
            question_text = list(data_.keys())[0]
            question = Question.objects.get(question_text=question_text)
            user_answer = data_[question_text]
            index = int(data_['index'][0])

            print("User Answer: " + user_answer[0][0] + " | Correct Answer: " + question.answer)
            print(index-1)
            if (user_answer[0][0] == question.answer and score_list[index-1] == 0):
                score_list[index-1] = 1
            
            print("Score: " + str(score_list))

            if (question.index == len(questions)):
                total_score = sum(score_list)
                user_done = True

        # .get() method returns only one object or a DoesNotExist exception

        # Only set the current question if index is less than number of questions.
        if (index < len(questions)):
            question = questions[index]
        else:
            question = None

        context_dict['category_name_slug'] = category_name_slug
        # context_dict['record_form'] = record_form
        context_dict['quiz'] = quiz
        context_dict['question'] = question
        context_dict['index'] = index
        context_dict['num_of_questions'] = len(questions)
        context_dict['user_done'] = user_done
        context_dict['user_score'] = total_score
    except Category.DoesNotExist:
        context_dict['quiz'] = None
        context_dict['question'] = None
        context_dict['index'] = None

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
    
    return render(request, 'quizzit/register.html', {'user_form': user_form , 'profile_form': profile_form, 'registered': registered, 'categories': category_list,})

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
            return render(request, 'quizzit/login.html', {'invalid_login': invalid_login , 'categories': category_list,})
    else:
        return render(request, 'quizzit/login.html', {'invalid_login': invalid_login , 'categories': category_list,})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('quizzit:home'))

def leaderboards(request):
    context_dict = {'categories': category_list,}
    
    return render(request, 'quizzit/leaderboards.html', context_dict)
