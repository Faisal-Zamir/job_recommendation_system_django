import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import JobRecommendationForm
from job_recommender.Model_Files.user_jobs_recommendation import recommend_jobs


def homepage(request):
    recommendations = None
    user_info = None

    if request.method == 'POST':
        form = JobRecommendationForm(request.POST)
        if form.is_valid():
            # Get cleaned data from form
            cleaned_data = form.cleaned_data
            print("Cleaned Data:", cleaned_data)  # Debugging line
            # Convert skills list to comma-separated string
            skills_string = ', '.join(cleaned_data['skills'])
            
            # Create user info dictionary
            user_info = {
                "name": cleaned_data['name'],
                "job_title": cleaned_data['job_title'],
                "skills": skills_string,
                "experience_level": cleaned_data['experience_level'],
                "years_experience": cleaned_data['years_experience'],
                "preferred_industry": cleaned_data['preferred_industry'],
                "location": cleaned_data['location'],
                "education_level": cleaned_data['education_level']
            }
            
            # Create DataFrame from user info
            user_df = pd.DataFrame({
                "name": [user_info["name"]],
                "job_title": [user_info["job_title"]],
                "skills": [user_info["skills"]],
                "experience_level": [user_info["experience_level"]],
                "years_experience": [user_info["years_experience"]],
                "preferred_industry": [user_info["preferred_industry"]],
                "location": [user_info["location"]],
                "education_level": [user_info["education_level"]]
            })
            
            # Get job recommendations
            print("User DataFrame:\n", user_df)  # Debugging line
            recommendations = recommend_jobs(user_df)

            if recommendations:
                for job in recommendations['recommendations']:
                    job['similarity_score'] = round(job['similarity_score'] * 100, 2)
            
            # # Print results to console (for debugging)
            # print("\n" + "="*60)
            # print("JOB RECOMMENDATION RESULTS")
            # print("="*60)
            # print(f"User: {recommendations['user_name']}")
            # print(f"Profile: {recommendations['user_profile']}")
            # print(f"Total Recommendations: {recommendations['total_recommendations']}")
            # print("\nTop Job Recommendations:")
            
            # for i, job in enumerate(recommendations['recommendations'], 1):
            #     print(f"{i}. {job['job_title']}")
            #     print(f"   Location: {job['location']}")
            #     print(f"   Match Score: {job['similarity_score']:.2%}")
            #     print(f"   Description: {job['description']}")
            #     print()
                
    else:
        form = JobRecommendationForm()
    
    context = {
        'form': form,
        'recommendations': recommendations,
        'user_info': user_info
    }
    return render(request, 'job_recommender/homepage.html', context)
