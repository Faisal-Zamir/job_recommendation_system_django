from django import forms

class JobRecommendationForm(forms.Form):
    # Experience level choices
    EXPERIENCE_LEVELS = [
        ('Internship', 'Internship'),
        ('Entry', 'Entry Level'),
        ('Mid', 'Mid Level'),
        ('Senior', 'Senior Level'),
        ('Executive', 'Executive'),
    ]
    
    # Education level choices
    EDUCATION_LEVELS = [
        ('High School', 'High School'),
        ('Associate', 'Associate Degree'),
        ('Bachelors', 'Bachelor\'s Degree'),
        ('Masters', 'Master\'s Degree'),
        ('PhD', 'PhD'),
    ]
    
    # Preferred Industry choices
    INDUSTRY_CHOICES = [
        ('Information Technology', 'Information Technology'),
        ('Finance', 'Finance & Banking'),
        ('Healthcare', 'Healthcare'),
        ('Education', 'Education'),
        ('Manufacturing', 'Manufacturing'),
        ('Retail', 'Retail'),
        ('Other', 'Other'),
    ]
    
    # Skills choices
    SKILLS_CHOICES = [
        ('Python', 'Python'),
        ('SQL', 'SQL'),
        ('Excel', 'Excel'),
        ('Power BI', 'Power BI'),
        ('Tableau', 'Tableau'),
        ('R', 'R'),
        ('Java', 'Java'),
        ('JavaScript', 'JavaScript'),
        ('React', 'React'),
        ('Node.js', 'Node.js'),
        ('AWS', 'AWS'),
        ('Docker', 'Docker'),
        ('Machine Learning', 'Machine Learning'),
        ('Data Analysis', 'Data Analysis'),
        ('Project Management', 'Project Management'),
    ]
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Ali Raza',
            'value': 'Ali Raza'
        })
    )
    
    job_title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Data Analyst',
            'value': 'Data Analyst'
        })
    )
    
    skills = forms.MultipleChoiceField(
        choices=SKILLS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    experience_level = forms.ChoiceField(
        choices=EXPERIENCE_LEVELS,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    years_experience = forms.IntegerField(
        min_value=0,
        max_value=50,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'value': '1'
        })
    )
    
    preferred_industry = forms.ChoiceField(
        choices=INDUSTRY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    location = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Lahore, PK',
            'value': 'Lahore, PK'
        })
    )
    
    education_level = forms.ChoiceField(
        choices=EDUCATION_LEVELS,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )