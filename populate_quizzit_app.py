import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Quizzit.settings')

import django
django.setup()
from quizzit_app.models import Register_User, Category, Quiz, Record

def populate():
    reg_user_list = [
        {'username': 'Alice',
         'email': 'alice@gmail.com',
         'password': 'alice1234',
         'admin': False},

        {'username': 'Bob',
         'email': 'bob@gmail.com',
         'password': 'bob1234',
         'admin': False},

        {'username': 'Charlie',
         'email': 'charlie@gmail.com',
         'password': 'charlie1234',
         'admin': False},
    ]

    for user in reg_user_list:
        add_reg_user(user['username'], user['email'], user['password'], user['admin'])

    # Print out the user we have added.
    for user in Register_User.objects.all():
        print(f'- added User: {user}')



    cate_list = [
        {'name': 'History'},
        {'name': 'Geography'},
        {'name': 'Sport'},
        {'name': 'Mathematics'},
        {'name': 'Biology'},
        {'name': 'Business'},
        {'name': 'Physics'},
        {'name': 'Movies'},
        {'name': 'TV Shows'},
        {'name': 'Chemistry'},
    ]

    for cate in cate_list:
        add_cate(cate['name'])

    # Print out the cate we have added.
    for cate in Category.objects.all():
        print(f'- added Cate: {cate}')


    # quiz_list = [
    #     {'quizID': 1,
    #      'name': 'Quiz 1',
    #      'difficulty': 'Easy',
    #      'question': 'question 1',
    #      },

    #     {'quizID': 2,
    #      'name': 'Quiz 2',
    #      'difficulty': 'Medium',
    #      'question': 'question 2',},

    #     {'quizID': 3,
    #      'name': 'Quiz 3',
    #      'difficulty': 'Difficulty',
    #      'question': 'question 3',},
    # ]
    # quiz_dict = {
    #    'Category B': quiz_list,
    # }

    # for cate, quiz_l in quiz_dict.items():
    #     cate_obj = Category.objects.get(name=cate)
    #     for quiz in quiz_l:
    #         add_quiz(quiz['quizID'], quiz['name'], quiz['difficulty'], quiz['question'], cate_obj)

    # # Print out the quiz we have added.
    # for quiz in Quiz.objects.all():
    #     print(f'- added quiz: {quiz}')

    
    # record_list = [
    #     {'username': 'Alice',
    #      'quizID': 1,
    #      'score': 10},
    #     {'username': 'Bob',
    #      'quizID': 2,
    #      'score': 20},
    #     {'username': 'Charlie',
    #      'quizID': 3,
    #      'score': 30},
    # ]

    # for record in record_list:
    #     reg_user_obj = Register_User.objects.get(username=record['username'])
    #     quiz_obj = Quiz.objects.get(quizID=record['quizID'])

    #     add_record(reg_user_obj, quiz_obj, record['score'])

    # # Print out the cate we have added.
    # for record in Record.objects.all():
    #     print(f'- added Record: {record}')


def add_reg_user(username, email, password, admin=False):
    reg_user = Register_User.objects.get_or_create(username=username)[0]
    reg_user.email = email
    reg_user.password = password
    reg_user.admin = admin

    reg_user.save()
    return reg_user


def add_cate(name):
    cate = Category.objects.get_or_create(name=name)[0]

    cate.save()
    return cate

def add_quiz(quizID, name, difficulty, questions, category):
    quiz = Quiz.objects.get_or_create(quizID=quizID, category=category)[0]
    quiz.name = name
    quiz.difficulty = difficulty
    quiz.questions = questions

    quiz.save()
    return quiz

def add_record(username, quizID, score=0):
    record = Record.objects.get_or_create(username=username, quizID=quizID)[0]
    record.score = score

    record.save()
    return record
    

# Start execution here!
if __name__ == '__main__':
    print('Starting quizzit_app population script...')
    populate()