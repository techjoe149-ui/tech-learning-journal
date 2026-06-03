# password_checker

def check_password_strength(password):
    if len(password) < 6:
        return "weak password"

    elif len(password) < 10:
        return "Moderate password"

    else:
        return "strong password"
