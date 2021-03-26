from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Register_User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=60)
    password = models.CharField(max_length=30)
    admin = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='profile_images', blank=True)


    class Meta:
        verbose_name_plural = 'Register Users'

    def __str__(self):
        return self.username



class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name



class Quiz(models.Model):
    EASY = 'EASY'
    MED = 'MEDIUM'
    HARD = 'HARD'
    difficulty_choices = [(EASY, 'Easy'), (MED, 'Medium'), (HARD, 'Hard')]

    name = models.CharField(max_length=30)
    difficulty = models.CharField(max_length=10, choices=difficulty_choices)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    quizID = models.CharField(max_length=10, unique=True, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        #_# create quizID field from category and difficulty fields
        # the id of quizzes with same category name and difficulty level
        id_list = [q.id for q in Quiz.objects.filter(category__name=self.category.name, difficulty=self.difficulty)]
        if self.id not in id_list:
            count = len(id_list)
            q_ID = '{}-{}-{}'.format(self.category.name[:4].upper(), self.difficulty[0], f'{count+1}'.zfill(2))
            self.quizID = q_ID

        super(Quiz, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return f'{self.quizID}'



class Question(models.Model):
    # By default, Django create a field named as 'id' which is an auto-incrementing primary key
    question_text = models.CharField(max_length=500)
    choiceA = models.CharField(max_length=100)
    choiceB = models.CharField(max_length=100)
    choiceC = models.CharField(max_length=100)
    choiceD = models.CharField(max_length=100)
    answer = models.CharField(max_length=1)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f'Question({self.question_text[:20]})'



class Record(models.Model):
    user = models.ForeignKey(Register_User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Records'

    def __str__(self):
        return f'Record({self.user}, {self.quiz}, {self.score})'  




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    def __str__(self):
        return self.user



