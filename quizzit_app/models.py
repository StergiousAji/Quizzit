from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Register_User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='profile_images', blank=True)


    class Meta:
        verbose_name_plural = 'Register Users'

    def __str__(self):
        return self.username



class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)


    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


    def __str__(self):
        return self.name



class Quiz(models.Model):
    EASY = 'EASY'
    MED = 'MEDIUM'
    HARD = 'HARD'
    # The 1st element in each tuple is the actual value that will be stored in the database. 
    # The 2nd element is displayed by the field’s form widget.
    difficulty_choices = [(EASY, 'Easy'), (MED, 'Medium'), (HARD, 'Hard')]

    name = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=10, choices=difficulty_choices)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    
    quizID = models.CharField(max_length=10, unique=True, blank=True)
    slug = models.SlugField(unique=True)
    

    class Meta:
        verbose_name_plural = 'Quizzes'
        constraints = [
            models.UniqueConstraint(fields=['name', 'difficulty', 'category'], name='unique quiz constraint'),
            models.CheckConstraint(check=models.Q(difficulty__in=['EASY','MEDIUM','HARD']), name="difficulty validity constraint"),
        ]

    def save(self, *args, **kwargs):
        self.create_quizID()
        self.slug = slugify(self.quizID)

        super(Quiz, self).save(*args, **kwargs)

    def create_quizID(self):
        # all the id of quizzes with the same category name and difficulty level
        id_list = [q.id for q in Quiz.objects.filter(category__name=self.category.name, difficulty=self.difficulty)]
        # if the quiz does not exist yet
        if self.id not in id_list:
            count = len(id_list)
            q_ID = '{}-{}-{}'.format(
                self.category.name[:4].replace(' ', '_').upper(), 
                self.difficulty[0], 
                f'{count+1}'.zfill(2)
            )
            self.quizID = q_ID

    def __str__(self):
        return f'{self.quizID}'



class Question(models.Model):
    answer_choices = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]

    index = models.IntegerField()
    question_text = models.CharField(max_length=500)
    choiceA = models.CharField(max_length=100)
    choiceB = models.CharField(max_length=100)
    choiceC = models.CharField(max_length=100)
    choiceD = models.CharField(max_length=100)
    answer = models.CharField(max_length=1, choices=answer_choices)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    

    class Meta:
        verbose_name_plural = 'Questions'
        constraints = [
            models.UniqueConstraint(fields=['index', 'quiz'], name='unique question constraint'),
            models.CheckConstraint(check=models.Q(answer__in=['A','B','C','D']), name="answer validity constraint"),
        ]

    def __str__(self):
        return f'{self.quiz}(Q{self.index}, {self.question_text[:10]})'



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



