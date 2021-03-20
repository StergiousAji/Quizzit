from django.shortcuts import render

# Create your views here.
def home(request):
    context_dict = {}
    
    return render(request, 'quizzit/home.html', context_dict)

def about(request):
    context_dict = {}
    
    return render(request, 'quizzit/about.html', context_dict)

def categories(request):
    category_list = None
    # category_list = Category.objects
    context_dict = {'categories': category_list,}
    
    return render(request, 'quizzit/categories.html', context_dict)