import pandas as pd
import joblib
import os
import re
import contractions
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import gdown


# Define base directory (folder where this script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create a dedicated folder for model files
MODEL_DIR = os.path.join(BASE_DIR, "model_files")
os.makedirs(MODEL_DIR, exist_ok=True)

# Google Drive file IDs (replace with your actual IDs)
files = {
    "tfidf_vectorizer.pkl": "1aVoqYtFJWhf2gviwKJFgyhW8TzMYlumR",
    "jobs_tfidf_matrix_compressed.pkl": "1EiOd-9k4_ugScV2dBOaqKeyGejg1n3fZ",
    "jobs_data_compressed.pkl": "1w7DtBlC5WTp9OkK3poQ1stl-9PTDw3oO",
}

# Download missing files once
for filename, file_id in files.items():
    file_path = os.path.join(MODEL_DIR, filename)
    if not os.path.exists(file_path):
        print(f"Downloading {filename} from Google Drive...")
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, file_path, quiet=False)
    else:
        print(f"{filename} already exists. Skipping download.")

# --- Load saved components (your original logic) ---
vectorizer = joblib.load(os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"))
tfidf_matrix = joblib.load(os.path.join(MODEL_DIR, "jobs_tfidf_matrix_compressed.pkl"))
jobs_data = pd.read_pickle(os.path.join(MODEL_DIR, "jobs_data_compressed.pkl"))


# Initialize preprocessing components
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    """Preprocessing function for text cleaning"""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = contractions.fix(text)
    words = [word for word in text.split() if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)

def recommend_jobs(user_df):

    # Combine into one text profile
    user_df["experience_text"] = user_df["years_experience"].astype(str) + " years experience"
    user_df["profile_text"] = (
        user_df["job_title"] + " " +
        user_df["skills"] + " " +
        user_df["experience_level"] + " " +
        user_df["experience_text"] + " " +
        user_df["preferred_industry"] + " " +
        user_df["education_level"] + " " +
        user_df["location"]
    )
    
    # Preprocess the profile text
    user_df["Profile_Cleaned"] = user_df["profile_text"].apply(preprocess_text)
    
    # Convert using existing TF-IDF vectorizer
    user_tfidf = vectorizer.transform(user_df["Profile_Cleaned"])
    
    # Calculate cosine similarity with job TF-IDF matrix
    cosine_sim_new = cosine_similarity(user_tfidf, tfidf_matrix)
    
    # Get top 5 matching jobs
    similarity_series = pd.Series(cosine_sim_new[0], index=jobs_data["title"])
    top_5_matches = similarity_series.sort_values(ascending=False).head(5)
    
    # Prepare detailed results
    recommendations = []
    for job_title, similarity_score in top_5_matches.items():
        job_details = jobs_data[jobs_data["title"] == job_title].iloc[0]
        recommendations.append({
            'job_title': job_title,
            'similarity_score': round(float(similarity_score), 4),
            'location': job_details.get('location', 'N/A'),
            'description': job_details.get('description', 'N/A')[:200] + '...' if len(str(job_details.get('description', ''))) > 200 else job_details.get('description', 'N/A')
        })
    
    return {
        'user_name': user_df["name"].iloc[0],
        'total_recommendations': len(recommendations),
        'recommendations': recommendations,
        'user_profile': user_df["profile_text"].iloc[0]
    }

# Example usage with test data
if __name__ == "__main__":
    # Create DataFrame outside the function
    test_user_df = pd.DataFrame({
        "name": ["Ali Raza"],
        "job_title": ["Data Analyst"],
        "skills": ["Python, SQL, Excel, Power BI"],
        "experience_level": ["Entry"],
        "years_experience": [1],
        "preferred_industry": ["Information Technology"],
        "location": ["Lahore, PK"],
        "education_level": ["Bachelors"]
    })
    
    # Get recommendations by passing DataFrame
    result = recommend_jobs(test_user_df)
    
    # Display results
    print(f"Top job recommendations for {result['user_name']}:\n")
    print("User Profile:", result['user_profile'])
    print("\n" + "="*60 + "\n")
    
    for i, job in enumerate(result['recommendations'], 1):
        print(f"{i}. {job['job_title']}")
        print(f"   Location: {job['location']}")
        print(f"   Match Score: {job['similarity_score']:.2%}")
        print(f"   Description: {job['description']}")
        print()