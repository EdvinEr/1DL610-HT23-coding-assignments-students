import csv
from logout import logout
import json

#User class to represent user information
class User:
    def __init__(self, name, wallet):
        self.name = name
        self.wallet = float(wallet)

#Product class to represent product information
class Product:
    def __init__(self, name, price, units):
        self.name = name
        self.price = float(price)
        self.units = int(units)

#A method to get product details as a list
    def get_product(self):
        return [self.name, self.price, self.units]

#ShoppingCart class to represent the user's shopping cart
class ShoppingCart:
    def __init__(self):
        self.items = []

    # Method to add a product to the cart
    def add_item(self, product):
        self.items.append(product)

    # Method to remove a product from the cart
    def remove_item(self, product):
        self.items.remove(product)

    # Method to retrieve the items in the cart
    def retrieve_item(self):
        return self.items

    # Method to clear all items from the cart
    def clear_items(self):
        self.items = []

    # Method to calculate the total price of items in the cart
    def get_total_price(self):
        return sum(item.price for item in self.items)

# Function to load products from a CSV file
def load_products_from_csv(file_path):
    products = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products.append(Product(row['Product'], row['Price'], row['Units']))
    return products

# Load products from the CSV file
products= load_products_from_csv("products.csv")
cart = ShoppingCart()

# Function to complete the checkout process
def checkout(user, cart):
    products = load_products_from_csv("products.csv")

    if not cart.items:
        print("\nYour basket is empty. Please add items before checking out.")
        return

    total_price = cart.get_total_price()

    if total_price > user.wallet:
        print("\n")
        print(f"You don't have enough money to complete the purchase.")
        print("Please try again!")
        return

    # Deduct the total price from the user's wallet
    user.wallet -= total_price
    # Update product units and remove products with zero units
    for item in cart.items:
        item.units -= 1
        if item.units == 0:
            products.remove(item)
    # Clear the cart
    cart.items = []

    # Print a thank you message with the remaining balance
    print("\n")
    print(f"Thank you for your purchase, {user.name}! Your remaining balance is {user.wallet}")
    
# Function to check the cart and proceed to checkout if requested
def check_cart(user, cart):
    # Print products in the cart
    for i in cart.retrieve_item():
        print(i.get_product())
    # Ask the user if they want to checkout
    question = input("Do you want to checkout (Y/N)?")
    if question.lower()  == "y":
        return checkout(user,cart)
    else:
        return False

# Main function for the shopping and checkout process
def checkoutAndPayment(login_info):
    products = load_products_from_csv("products.csv")
    cart = ShoppingCart()

    # Create/retrieve a user using login information
    user = User(login_info["username"], login_info["wallet"])
    # Display available products
    for i, product in enumerate(products):
        print(f"{i + 1}. {product.name} - ${product.price} - Units: {product.units}")

    while True:

        # Get user input for product selection in numbers
        choice = input("\nEnter the product number you want to add to your cart (c to check cart, l to logout): ")

        if choice == 'c':
            # Check the cart and proceed to checkout if requested
            check = check_cart(user, cart)
            if check is False:
                continue
        elif choice == 'l':
            # Logout the user
            ask_logout = logout(cart)
            if ask_logout is True:

                with open('users.json', "r") as file:
                    data = json.load(file)
                    for entry in data:
                        if entry["username"] == user.name:
                            entry['wallet'] = user.wallet

                with open('users.json', 'w') as file:
                    json.dump(data, file)

                print("You have been logged out")
                break
            else:
                continue
        elif choice.isdigit() and 1 <= int(choice) <= len(products):
            # Add the selected product to the cart
            selected_product = products[int(choice) - 1]
            if selected_product.units > 0:
                cart.add_item(selected_product)
                print(f"{selected_product.name} added to your cart.")
            else:
                print(f"Sorry, {selected_product.name} is out of stock.")
        else:
            print("\nInvalid input. Please try again.")

