import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Quizzit.settings')

import django
django.setup()
from quizzit_app.models import Register_User, Category, Quiz, Question, Record

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
        u = add_reg_user(user['username'], user['email'], user['password'], user['admin'])

        print(f'- added User: {u}')



    cate_list = [
        {'name': 'History',},
        {'name': 'Geography',},
        {'name': 'Sport',},
        {'name': 'Mathematics',},
        {'name': 'Biology',},
        {'name': 'Business',},
        {'name': 'Physics',},
        {'name': 'Movies',},
        {'name': 'TV Shows',},
        {'name': 'Chemistry',},
    ]

    for cate in cate_list:
        c = add_cate(cate['name'])

        print(f'- added Cate: {c}')



    dir_path = 'quiz data'
    quiz_list = read_json_files(dir_path)

    for quiz in quiz_list:
        cate_obj = Category.objects.get(name=quiz['category'])
        q = add_quiz(quiz['name'], quiz['difficulty'], cate_obj, quiz['views']) 

        print(f'- added Quiz: {q}')

        for question in quiz['questions']:
            que = add_question(question['index'], question['text'], question['choiceA'], question['choiceB'], 
                               question['choiceC'], question['choiceD'], question['answer'], q)

            print(f'- added Question: {que} to {q}')


    # record_list = [
    #     {'user': 'Alice',
    #      'quiz': 1,
    #      'score': 10},
    #     {'user': 'Bob',
    #      'quiz': 2,
    #      'score': 20},
    #     {'user': 'Charlie',
    #      'quiz': 3,
    #      'score': 30},
    # ]

    # for record in record_list:
    #     reg_user_obj = Register_User.objects.get(username=record['username'])
    #     quiz_obj = Quiz.objects.get(quizID=record['quizID'])
    #     r = add_record(reg_user_obj, quiz_obj, record['score'])

    #     print(f'- added Record: {r}')



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



def add_quiz(name, difficulty, category, views=0):
    quiz = Quiz.objects.get_or_create(name=name, difficulty=difficulty.upper(), category=category)[0]
    quiz.views = views
    
    quiz.save()
    return quiz



def add_question(index, question_text, choiceA, choiceB, choiceC, choiceD, answer, quiz):
    question = Question.objects.get_or_create(index=index, quiz=quiz, answer=answer.upper())[0]
    question.question_text = question_text
    question.choiceA = choiceA
    question.choiceB = choiceB
    question.choiceC = choiceC
    question.choiceD = choiceD

    question.save()
    return question



def add_record(user, quiz, score=0):
    record = Record.objects.get_or_create(user=user, quiz=quiz)[0]
    record.score = score

    record.save()
    return record



def read_json_files(dir_path):
    """Read all the json files in the given directory and its sub directory. Return a list of quiz's dictionaries."""
    import json
    import os

    quiz_list = []
    file_ignore = [os.path.join(dir_path, 'Quiz of Day'),]

    for file in os.listdir(dir_path): 
        file_path = os.path.join(dir_path, file)

        if file_path in file_ignore:
            continue

        if os.path.isdir(file_path):
            quiz_list.extend(read_json_files(file_path))
        else:
            with open(file_path, 'r', encoding='utf-8') as quiz:
                quiz_list.append(json.load(quiz))
            
    return quiz_list



def create_json_template(file_path):
    import json

    quiz = '''{ 
    "name": "template", 
    "difficulty": "EASY", 
    "category": "History", 
    "views": 0,
    "questions": [
        {"index": 1, 
         "text": "text",
         "choiceA": "sth",
         "choiceB": "sth",
         "choiceC": "sth",
         "choiceD": "sth",
         "answer": "A"}, 

        {"index": 2,
         "text": "text",
         "choiceA": "sth",
         "choiceB": "sth",
         "choiceC": "sth",
         "choiceD": "sth",
         "answer": "A"}, 

        {"index": 3,
         "text": "text",
         "choiceA": "sth",
         "choiceB": "sth",
         "choiceC": "sth",
         "choiceD": "sth",
         "answer": "A"},

        {"index": 4,
         "text": "text",
         "choiceA": "sth",
         "choiceB": "sth",
         "choiceC": "sth",
         "choiceD": "sth",
         "answer": "A"},

        {"index": 5,
         "text": "text",
         "choiceA": "sth",
         "choiceB": "sth",
         "choiceC": "sth",
         "choiceD": "sth",
         "answer": "A"},

        {"index": 6,
         "text": "text",
         "choiceA": "sth",
         "choiceB": "sth",
         "choiceC": "sth",
         "choiceD": "sth",
         "answer": "A"},

        {"index": 7,
         "text": "text",
         "choiceA": "sth",
         "choiceB": "sth",
         "choiceC": "sth",
         "choiceD": "sth",
         "answer": "A"}
    ]
    }'''
    
    with open(file_path, 'x') as f:
        json.dump(json.loads(quiz), f, indent = 4) 
        print(f'Created {file_path}')



############################## remember to delete ####################################
def test():
    cate_obj = Category.objects.get(name='History')

    print('--', Category.objects.get(name='History').quiz_set.all())
    print('--', Quiz.objects.filter(category__name='History', difficulty='EASY'))

    print('--', Quiz.objects.all())
    print('--')
    quiz_obj = Quiz.objects.get(quizID='HIST-M-01')
    print('-- {}, {}, {}'.format(quiz_obj, type(quiz_obj), quiz_obj.id))
    print('-- {}, {}, {}'.format(quiz_obj.name, quiz_obj.difficulty, quiz_obj.category))
    print('--', quiz_obj.views)
    print('--', quiz_obj.question_set.all()[0])
    print('--', quiz_obj.question_set.get(index=1))
    print('--', Question.objects.all())


########################################################################################



# Start execution here!
if __name__ == '__main__':
    print('Starting quizzit_app population script...')
    # populate()
    test()
    # create_json_template(r'quiz data/Chemistry/Chemitry hard quiz 1.json')






    


