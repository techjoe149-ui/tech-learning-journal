# password_checker.py

def password_checker():

    while True:

        password = input("Create password: ")

        if len(password) < 8:
            print("password incomplete")
            continue
        has_number = False

        for character in password:
            if character.isdigit():
                has_number = True

        if has_number:
            print("strong password.")
            break
        else:
            print("Password must contain a number and at least one capital letter.")
