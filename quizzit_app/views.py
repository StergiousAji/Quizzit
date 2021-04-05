from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from quizzit_app.models import Category, Record, Quiz, Question, Register_User, UserProfile
from quizzit_app.forms import UserForm, UserProfileForm, RecordForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import itertools

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

    return render(request, 'quizzit/category.html', context=context_dict)


# use mutable default arguments as global variables
def quiz(request, category_name_slug, quiz_name_slug, global_data={'index':0, 'chosen_ans':[]}):
    quiz = Quiz.objects.get(slug=quiz_name_slug)
    questions = quiz.question_set.all()

    point = {
        Quiz.EASY: 100,
        Quiz.MED: 200,
        Quiz.HARD: 300,
    }[quiz.difficulty]

    start_time = {
        Quiz.EASY: 3 * 60,
        Quiz.MED: 6 * 60,
        Quiz.HARD: 10 * 60,
    }[quiz.difficulty]


    # if called by clicking the next button
    if request.POST.get('isNextClicked', False): 
        data = request.POST
        global_data['chosen_ans'].append( data['chosenAnswer'] )

        global_data['index'] += 1
        question = questions[global_data['index']]

        response_dict = {
            'question_text': question.question_text,
            'index': question.index,
            'choiceA': question.choiceA,
            'choiceB': question.choiceB,
            'choiceC': question.choiceC,
            'choiceD': question.choiceD,
            'chosenAnswer': '',
            'isLast': global_data['index'] == len(questions) - 1,
        }

        return JsonResponse(response_dict, safe=False)


    # if called by clicking the finish button
    if request.POST.get('isFinishClicked', False): 
        data = request.POST
        global_data['index'] += 1
        global_data['chosen_ans'].append( data['chosenAnswer'] )

        time_remain = int(data['timeRemain'])        
        score = 0
        weight = 0.5
        for ans, question in zip(global_data['chosen_ans'], questions):
            if ans == question.answer:
                score += point
        score = int( score * (1 + time_remain/start_time * weight) )

        time_remain = '{}:{}'.format(str(time_remain//60), str(time_remain%60).zfill(2))

        ques_and_anss = itertools.zip_longest(questions, global_data['chosen_ans'], fillvalue='')
        ques_and_anss = [(x, 'Not Answered') if y == '' else (x,y) for x,y in ques_and_anss]
        
        context_dict = {
            'quiz': quiz,
            'finished': True,
            'ques_and_anss': ques_and_anss,
            'time_remain': time_remain,
            'question_score': point,
            'score': score,
        }
        
        response = render(request, 'quizzit/quiz.html', context=context_dict)
        html_str = response.content
        # slice the byte string such that it only contains the <body> section
        response.content = html_str[html_str.find(b'<body>'): html_str.find(b'</body>')+len(b'</body>')]

        return response


    ## when the page is first loaded or reloaded
    # reset the global values
    global_data['index'] = 0
    global_data['chosen_ans'] = []
    
    context_dict = {
        'category_name_slug': category_name_slug,
        'quiz': quiz,
        'question': questions[global_data['index']],
        'num_of_questions': len(questions),
        'start_time': start_time,
        'finished': False,
    }
    
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


