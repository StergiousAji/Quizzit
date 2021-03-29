from django.contrib import admin
from quizzit_app.models import Register_User, Category, Quiz, Question, Record

class RegisterUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'admin')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug':('name',)}

class QuizAdmin(admin.ModelAdmin):
    list_display = ('quizID', 'name', 'difficulty', 'category', 'views')
    prepopulated_fields = {'slug':('quizID',)}

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('index', 'question_text', 'choiceA', 'choiceB', 'choiceC', 'choiceD', 'answer')

class RecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score')

admin.site.register(Register_User, RegisterUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Record, RecordAdmin)
