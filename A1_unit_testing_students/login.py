import json

#Login as a user
def login():
    username = input("Enter your username:")
    password = input("Enter your password:")
    #Look for user in database
    with open('users.json', "r") as file:
        data = json.load(file)
        for entry in data:
            if entry["username"] == username:
                if entry["password"] == password:
                    print("Successfully logged in")
                    return {"username": entry["username"], "wallet": entry["wallet"]}
                else:
                    print("Either username or password were incorrect")
                    return None

        print("Username does not exists.")
        register_request = input("Do you want to register? (Y/N): ").lower()

        if register_request.lower() == "y":
            continue_registration = True
            while continue_registration:
                new_password = input("Enter your new password:")

                has_capital_letter = False
                for char in new_password:
                    if char.isupper():
                        has_capital_letter = True
                        break

                has_special_symbol = not(new_password.isalnum())

                valid_length = len(new_password) >= 8

                if has_capital_letter and has_special_symbol and valid_length:
                    address = input("Enter your address: ")
                    phone_number = input("Enter your phone number: ")
                    email_address = input("Enter your email address: ")
                    card_number = input("Enter your credit card number: ")
                    expiry_date = input("Enter your credit card expiry date: ")
                    name_on_card = input("Enter the name on your credit card: ")
                    cvv = input("Enter your credit card cvv: ")
                    new_entry = {"username": username, "password": new_password, "wallet": 0, "address": address, "phone_number": phone_number, "email": email_address, "credit_cards": [{"card_number": card_number, "expiry_date": expiry_date, "name_on_card": name_on_card, "cvv": cvv}]}
                    data.append(new_entry)

                    with open('users.json', "w") as write_file:
                        json.dump(data, write_file)

                    print("Successfully registered")
                    continue_registration = False
                else:
                    print("Password must have at least 1 capital letter, 1 special symbol and be 8 characters long.")

    return None
