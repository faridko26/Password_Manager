import pyperclip


class UserInputHandler:
    def __init__(self, password_manager):
        self.password_manager = password_manager

    def add_password(self):
        website = input("Enter website: ")
        username = input("Enter username: ")

        while True:
            choice = input("Do you want to generate a password (y/n)? ").strip().lower()
            if choice in ["y", "n"]:
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        if choice == "y":
            password = self.password_manager.generate_password()
            print(f"Generated password: {password}")
        else:
            password = input("Enter password: ")

        pyperclip.copy(password)

        self.password_manager.add_password(website, username, password)
        print("\n" + "-" * 40)
        print("Password added successfully!")
        print("Password copied to clipboard!")
        print("-" * 40 + "\n")

    def retrieve_password(self):
        website = input("Enter website to retrieve password for: ")
        results = self.password_manager.get_password(website)

        self.password_manager.display_passwords(website, results)
        self.password_manager.option_to_copy_password(results)

    def delete_password(self):
        website = input("Enter website to delete password for: ")
        results = self.password_manager.get_password(website)
        self.password_manager.display_passwords(website, results)
        if results:

            while True:
                try:
                    password_number = int(
                        input("Enter the number of the password to delete: ")
                    )
                    if 1 <= password_number <= len(results):
                        username_to_delete = results[password_number - 1][0]
                        break
                    else:
                        print(
                            f"Invalid number. Please enter a number between 1 and {len(results)}."
                        )
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            while True:
                choice = (
                    input(
                        f"Are you sure you want to delete the password for username '{username_to_delete}'? (y/n): "
                    )
                    .strip()
                    .lower()
                )
                if choice in ["y", "n"]:
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

            if choice == "y":
                self.password_manager.delete_password(website, username_to_delete)
                print("\n" + "-" * 40)
                print(
                    f"Password for username '{username_to_delete}' at '{website}' deleted successfully!"
                )
                print("-" * 40 + "\n")
            else:
                print("\n" + "-" * 40)
                print("Password deletion canceled.")
                print("-" * 40 + "\n")

    def update_password(self):
        website = input("Enter website to update password for: ")
        results = self.password_manager.get_password(website)
        self.password_manager.display_passwords(website, results)
        if results:

            while True:
                try:
                    password_number = int(
                        input("Enter the number of the account to update: ")
                    )
                    if 1 <= password_number <= len(results):
                        username_to_update = results[password_number - 1][0]
                        break
                    else:
                        print(
                            f"Invalid number. Please enter a number between 1 and {len(results)}."
                        )
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            while True:
                choice = (
                    input(
                        f"Are you sure you want to update the password for username '{username_to_update}'? (y/n): "
                    )
                    .strip()
                    .lower()
                )
                if choice in ["y", "n"]:
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

            if choice == "y":
                while True:
                    choice = (
                        input("Do you want to generate a password (y/n)? ")
                        .strip()
                        .lower()
                    )
                    if choice in ["y", "n"]:
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")

                if choice == "y":
                    new_password = self.password_manager.generate_password()

                else:
                    new_password = input("Enter password: ")

                pyperclip.copy(new_password)
                self.password_manager.update_password(
                    website, username_to_update, new_password
                )

                print("\n" + "-" * 40)
                print(
                    f"Password for username '{username_to_update}' at '{website}' updated successfully!"
                )
                print(f"New password: {new_password}")
                print("New Password copied to clipboard!")
                print("-" * 40 + "\n")
            else:
                print("\n" + "-" * 40)
                print("Password update canceled.")
                print("-" * 40 + "\n")
