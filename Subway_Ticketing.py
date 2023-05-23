import msvcrt
import os
import time
import sys
from tabulate import tabulate
from time import sleep

stations = ["North Ave", "Quezon Ave", "Kamuning", "Cubao",
            "Santolan", "Ortigas", "Shaw", "Boni", "Guadalupe",
            "Buendia", "Ayala", "Magallanes", "Taft"]

ticket_records = []

fare_table = [
    ["", "North Ave", "Quezon Ave", "Kamuning", "Cubao", "Santolan", "Ortigas", "Shaw", "Boni", "Guadalupe", "Buendia", "Ayala", "Magallanes", "Taft"],
    ["North Ave", 0, 13, 13, 16, 16, 20, 20, 20, 24, 24, 24, 28, 28],
    ["Quezon Ave", 13, 0, 13, 13, 16, 16, 20, 20, 20, 24, 24, 24, 28],
    ["Kamuning", 13, 13, 0, 13, 13, 16, 16, 20, 20, 20, 24, 24, 24],
    ["Cubao", 16, 13, 13, 0, 13, 13, 16, 16, 20, 20, 20, 24, 24],
    ["Santolan", 16, 16, 13, 13, 0, 13, 13, 16, 16, 20, 20, 20, 24],
    ["Ortigas", 20, 16, 16, 13, 13, 0, 13, 13, 16, 16, 20, 20, 20],
    ["Shaw", 20, 20, 16, 16, 13, 13, 0, 13, 13, 16, 16, 20, 20],
    ["Boni", 20, 20, 20, 16, 16, 13, 13, 0, 13, 13, 16, 16, 20],
    ["Guadalupe", 24, 20, 20, 20, 16, 16, 13, 13, 0, 13, 13, 16, 16],
    ["Buendia", 24, 24, 20, 20, 20, 16, 16, 13, 13, 0, 13, 13, 16],
    ["Ayala", 24, 24, 24, 20, 20, 20, 16, 16, 13, 13, 0, 13, 13],
    ["Magallanes", 28, 24, 24, 24, 20, 20, 20, 16, 16, 13, 13, 0, 13],
    ["Taft", 28, 28, 24, 24, 24, 20, 20, 20, 16, 16, 13, 13, 0]
]

column_widths = [max(len(str(row[i])) for row in fare_table) for i in range(len(fare_table[0]))]

class LoginSystem:
    def __init__(self):
        self.username = "admin"
        self.password = "password"

    def authenticate(self, username, password):
        if username == self.username and password == self.password:
            sleep(0.5)
            print("\nAuthentication Successful", end='')
            for i in range(3):
                print('.', end='')
                sys.stdout.flush()
                sleep(1)
            return True
        else:
            print("Authentication failed. Incorrect username or password.")
            return False

    def get_password(self):
        password = ""
        print("Enter password: ", end="", flush=True)
        while True:
            key = msvcrt.getch()  # Get a key press
            key_code = ord(key)
            if key_code == 13:  # Enter key
                print()
                break
            elif key_code == 8:  # Backspace key
                if password:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)  # Erase the last asterisk
            else:
                password += key.decode("utf-8")
                print("*", end="", flush=True)
        return password

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def calculate_fare(starting_station, destination_station):
    starting_index = stations.index(starting_station)
    destination_index = stations.index(destination_station)
    distance = abs(destination_index - starting_index)

    if distance <= 2:
        fare = 13
    elif distance <= 4:
        fare = 16
    elif distance <= 8:
        fare = 20
    elif distance <= 11:
        fare = 24
    else:
        fare = 28

    return fare


def get_distance(starting_station, destination_station):
    return stations.index(destination_station) - stations.index(starting_station)


def ticket_receipt(ticket_record):
    print("\nTicket Receipt:")
    print("Total cost is Php: {}".format(ticket_record["total_cost"]))
    print("Starting station: {}".format(ticket_record["starting_station"]))
    print("Destination station: {}".format(ticket_record["destination_station"]))
    print("Number of tickets: {}".format(ticket_record["number_of_tickets"]))
    print("Senior tickets: {}".format(ticket_record["senior_tickets"]))
    print("PWD tickets: {}".format(ticket_record["pwd_tickets"]))
    print("Payment: Php {:.2f}".format(ticket_record["payment"]))
    print("Change: Php {:.2f}".format(ticket_record["change"]))


def order_tickets(starting_station, destination_station):
    while starting_station not in stations or destination_station not in stations:
        print("Invalid starting station or destination station. Please try again.\n")
        starting_station = input("Enter your starting station: ")
        destination_station = input("Enter your destination station: ")

    number_of_tickets = int(input("Enter the number of tickets you want to order: "))
    total_cost = number_of_tickets * calculate_fare(starting_station, destination_station)

    # Determine if the user has senior or PWD tickets
    senior_tickets = int(input("Enter the number of senior tickets you want to order: "))
    pwd_tickets = int(input("Enter the number of PWD tickets you want to order: "))

    # Calculate the total cost of the tickets
    total_cost -= (senior_tickets * 0.2) + (pwd_tickets * 0.2)
    print(f"\nTotal fare: {total_cost}")

    while True:
          payment = float(input("Enter payment: "))
          if payment >= total_cost:
             change = payment - total_cost
             break
          else:
              print("Insufficient balance. Please enter a higher payment amount.")


    ticket_record = {
        "starting_station": starting_station,
        "destination_station": destination_station,
        "number_of_tickets": number_of_tickets,
        "senior_tickets": senior_tickets,
        "pwd_tickets": pwd_tickets,
        "total_cost": total_cost,
        "payment": payment,
        "change": change
    }

    ticket_receipt(ticket_record)

    ticket_records.append(ticket_record)


def print_ticket_records():
    for ticket in ticket_records:
        print("\nStarting station: {}".format(ticket["starting_station"]))
        print("Destination station: {}".format(ticket["destination_station"]))
        print("Number of tickets: {}".format(ticket["number_of_tickets"]))
        print("Senior tickets: {}".format(ticket["senior_tickets"]))
        print("PWD tickets: {}".format(ticket["pwd_tickets"]))
        print("Total cost is Php: {}".format(ticket["total_cost"]))
        print("Payment: Php {:.2f}".format(ticket["payment"]))
        print("Change: Php {:.2f}".format(ticket["change"]))




def main():
    while True:
        login_system = LoginSystem()
        print("\n\t ADMIN LOGIN\n")
        username = input("Enter username: ")
        password = login_system.get_password()
        if login_system.authenticate(username, password):
            time.sleep(2)
            clear_screen()
            break

    while True:
        print("\nWelcome to the MRT Ticketing System!")
        print("Please select from the following options:")
        print("[F] View Fare Table")
        print("[B] Buy a ticket")
        print("[P] Print all ticket records")
        print("[E] Exit the program")

        user_choice = input("What would you like to do? ")

        if user_choice == "F" or user_choice == "f":

            print("\n")
            # Print the fare system table
            for row in fare_table:
                row_formatted = "|".join("{:{}}".format(str(item), width) for item, width in zip(row, column_widths))
                print(row_formatted)

            print("\n")
            input("Press any key to continue...")
            clear_screen()


        elif user_choice == "B" or user_choice == "b":

            clear_screen()
            print("\n")

            # Print the fare system table
            for row in fare_table:
                row_formatted = "|".join("{:{}}".format(str(item), width) for item, width in zip(row, column_widths))
                print(row_formatted)

            print("\n20% Discount for Senior's and PW-D's")

            while True:
                  starting_station = input("Enter your starting station: ")
                  destination_station = input("Enter your destination station: ")

                  if starting_station != destination_station:
                      break
                  else:
                      print("\nInvalid input. Starting and destination stations cannot be the same. Please try again.\n")

            order_tickets(starting_station, destination_station)

            input("\nPress any key to continue...")
            clear_screen()

        elif user_choice == "P" or user_choice == "p":
            print_ticket_records()
            input("\nPress any key to continue...")
            clear_screen()


        elif user_choice == "E" or user_choice == "e":
            break

        else:
            print("Invalid option. Please try again.")


main()
