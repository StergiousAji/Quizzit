from django.contrib import admin
from quizzit_app.models import Register_User, Category, Quiz, Record

class RegisterUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'admin')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('quizID', 'name', 'difficulty', 'questions', 'category')

class RecordAdmin(admin.ModelAdmin):
    list_display = ('username', 'quizID', 'score')

admin.site.register(Register_User, RegisterUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Record, RecordAdmin)
