# display.py
def display_skills(skill_list):
    print("\n===== SKILLS ====")
    for skill in skill_list:
        print("-", skill)


def display_profile(profile):

    print("\n==== PROFILE ====")

    for key, value in profile.items():
        print(f"{key}:{value}")
