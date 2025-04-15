from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import Profile

def is_super_admin(user):
    return hasattr(user, 'profile') and user.profile.is_super_admin

def is_group_admin(user):
    return hasattr(user, 'profile') and user.profile.is_group_admin

def find_study_partners(user):
    user_profile = Profile.objects.get(user=user)
    all_profiles = Profile.objects.exclude(user=user)

    # Filter profiles based on preferred gender
    if user_profile.preferred_gender and user_profile.preferred_gender != '':
        all_profiles = all_profiles.filter(gender=user_profile.preferred_gender)

    # Create a list of features for each profile that is not the user
    profiles_data = []
    for profile in all_profiles:
        features = (
            f"""{profile.major}, {profile.grade}, 
            {profile.grove_or_game_day}, {profile.ideal_study_spot}, 
            {profile.study_time}, {profile.energy_source}, 
            {profile.personality_label}, {profile.group_project_role}, 
            {profile.personal_motto}, {profile.exam_prep_style}, 
            {profile.productivity_time}, {profile.academic_strength}, 
            {profile.accountability_style}, {profile.weekend_vibe}, 
            {profile.meet_people}, {profile.wish_more_of}, 
            {profile.favorite_tradition}, {profile.hot_take}, 
            {profile.secret_campus_hack}, {profile.todays_vibe}, 
            {profile.planner_fullness}, {profile.social_energy}, 
            {profile.ghost_likelihood}, {profile.major_approach}, 
            {profile.post_grad_plan}, {profile.college_motivation}, 
            {profile.campus_groups}, {profile.match_involvement_importance}, 
            {profile.social_energy_on_campus}"""
        )
        profiles_data.append(features)

    # The current user's features
    user_features = (
        f"""{user_profile.major}, {user_profile.grade}, 
            {user_profile.grove_or_game_day}, {user_profile.ideal_study_spot}, 
            {user_profile.study_time}, {user_profile.energy_source}, 
            {user_profile.personality_label}, {user_profile.group_project_role}, 
            {user_profile.personal_motto}, {user_profile.exam_prep_style}, 
            {user_profile.productivity_time}, {user_profile.academic_strength}, 
            {user_profile.accountability_style}, {user_profile.weekend_vibe}, 
            {user_profile.meet_people}, {user_profile.wish_more_of}, 
            {user_profile.favorite_tradition}, {user_profile.hot_take}, 
            {user_profile.secret_campus_hack}, {user_profile.todays_vibe}, 
            {user_profile.planner_fullness}, {user_profile.social_energy}, 
            {user_profile.ghost_likelihood}, {user_profile.major_approach}, 
            {user_profile.post_grad_plan}, {user_profile.college_motivation}, 
            {user_profile.campus_groups}, {user_profile.match_involvement_importance}, 
            {user_profile.social_energy_on_campus}"""
        )
    profiles_data.insert(0, user_features)

    if len(profiles_data) <= 1:  # Only the user's profile, so no matches
        return "No matches yet!" 

    # Convert text data into vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(profiles_data)

    # Compute cosine similarity
    similarity_scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    # Match users with highest similarity
    best_match_indices = np.argsort(similarity_scores)[::-1] 
    best_matches = [all_profiles[int(i)] for i in best_match_indices] 

    return best_matches