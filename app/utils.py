from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import FriendRequest, Profile

def is_super_admin(user):
    return hasattr(user, 'profile') and user.profile.is_super_admin

def is_group_admin(user):
    return hasattr(user, 'profile') and user.profile.is_group_admin

def find_study_partners(user):
    try:
        user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return "No matches yet!"

    # Exclude liked, disliked, friends, sent/received friend requests
    liked = user_profile.liked_profiles.all()
    disliked = user_profile.disliked_profiles.all()
    friends = user_profile.friends.all()

    sent_requests = FriendRequest.objects.filter(sender=user, accepted=False).values_list("receiver__profile__id", flat=True)
    received_requests = FriendRequest.objects.filter(receiver=user, accepted=False).values_list("sender__profile__id", flat=True)

    excluded_ids = list(liked.values_list("id", flat=True)) + \
                   list(disliked.values_list("id", flat=True)) + \
                   list(friends.values_list("id", flat=True)) + \
                   list(sent_requests) + \
                   list(received_requests)

    # Filter eligible profiles
    all_profiles = Profile.objects.exclude(user=user).exclude(id__in=excluded_ids)

    # Match preferred gender
    if user_profile.preferred_gender:
        all_profiles = all_profiles.filter(gender=user_profile.preferred_gender)

    if not all_profiles.exists():
        return "No matches yet!"

    # Turn profiles into string features
    def stringify_profile(profile):
        return f"""{profile.major}, {profile.major}, {profile.major},  # triple weight
        {profile.grade}, 
        {profile.grove_or_game_day}, {profile.ideal_study_spot}, 
        {profile.study_time}, {profile.energy_source}, 
        {profile.group_project_role}, 
        {profile.exam_prep_style}, 
        {profile.academic_strength}, 
        {profile.accountability_style},
        {profile.wish_more_of}, 
        {profile.hot_take}, 
        {profile.planner_fullness}, {profile.social_energy}, 
        {profile.major_approach}, 
        {profile.post_grad_plan}, {profile.college_motivation}, 
        {profile.campus_groups}, {profile.match_involvement_importance}, 
        {profile.social_energy_on_campus}"""

    profiles_data = [stringify_profile(p) for p in all_profiles]
    user_features = stringify_profile(user_profile)
    profiles_data.insert(0, user_features)

    # Vectorize and rank
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(profiles_data)
    similarity_scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    best_match_indices = np.argsort(similarity_scores)[::-1]
    best_matches = [all_profiles[int(i)] for i in best_match_indices]

    return best_matches
