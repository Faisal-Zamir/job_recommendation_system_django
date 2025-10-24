from django.shortcuts import render

def homepage(request):
    return render(request, 'job_recommender/homepage.html')