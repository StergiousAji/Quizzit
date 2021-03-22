from django.db import models


class Register_User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=35)
    admin = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Register Users'

    def __str__(self):
        return self.username



class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name



class Quiz(models.Model):
    EASY = 'Easy'
    MED = 'Medium'
    DIFF = 'Difficult'
    difficulty_choices = [(EASY, 'Easy'), (MED, 'Medium'), (DIFF, 'Difficult')]

    quizID = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=30)
    difficulty = models.CharField(max_length=15, choices=difficulty_choices)
    questions = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return f'({self.quizID}, {self.name}, {self.category})'



class Record(models.Model):
    username = models.ForeignKey(Register_User, on_delete=models.CASCADE)
    quizID = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Records'

    def __str__(self):
        return f'{self.username}, {self.quizID}'  