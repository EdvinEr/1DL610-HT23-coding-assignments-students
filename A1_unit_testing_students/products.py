from login import login
import re
from checkout_and_payment import checkoutAndPayment
import csv



#Display all the products
def display_csv_as_table(csv_filename):
    with open(csv_filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        print(header)
        # Print each row
        for row in csv_reader:
            print(row)

#Display products filtered by name
def display_filtered_table(csv_filename, search):
    with open(csv_filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        print(header)

        condition_index = header.index("Product")
        # Print each row
        for i, row in enumerate(csv_reader):
            if re.search(row[condition_index],search,re.IGNORECASE):
                print(row)

#Search for a product and buy it
def searchAndBuyProduct():
    login_info = None
    marker = True
    #Login as a user
    while marker:
        login_info = login()
        if login_info is not None:
            marker = False
            break
    #Search for products then begin to shop
    while True:
        search = input("Search for products in inventory (type all for whole inventory):")
        if search.lower() == "all":
            display_csv_as_table("products.csv")
        else:
            display_filtered_table("products.csv", search)
        check = input("Ready to shop? (Y/N)")
        if check.lower() == "y":
            break
    checkoutAndPayment(login_info)