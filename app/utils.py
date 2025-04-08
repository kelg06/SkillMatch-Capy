from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import *

def is_super_admin(user):
    return hasattr(user, 'profile') and user.profile.is_super_admin

def is_group_admin(user):
    return hasattr(user, 'profile') and user.profile.is_group_admin

def find_study_partners(user):
    user_profile = Profile.objects.get(user=user)
    all_profiles = Profile.objects.exclude(user=user)

    # Create a list of features for each profile that is not the user
    profiles_data = []
    for profile in all_profiles:
        features = f"{profile.hobbies}, {profile.study_times}, {profile.goals_after}"
        profiles_data.append(features)

    # The current user's features, no need for a list because there's only one.
    user_features = f"{user_profile.hobbies}, {user_profile.study_times}, {user_profile.goals_after}"
    profiles_data.insert(0, user_features)

    # Convert text data into vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(profiles_data)

    # Compute cosine similarity
    similarity_scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    
    # Match users with highest similarity
    best_match_indices = np.argsort(similarity_scores)[::-1]  # Sort in descending order
    best_matches = [all_profiles[int(i)] for i in best_match_indices]  # Convert to int

    return best_matches
