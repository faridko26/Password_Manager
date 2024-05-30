import string
import random
import pyperclip


class PasswordManager:
    def __init__(self, db_manager, crypto_manager):
        self.crypto_manager = crypto_manager
        self.db_manager = db_manager

    def add_password(self, website, username, password, table_name="accounts"):
        encrypted_password = self.crypto_manager.encrypt(password)
        salt = self.crypto_manager.get_salt()
        query = f"INSERT INTO {table_name} (website, username, password, salt) VALUES (%s, %s, %s, %s)"
        self.db_manager.execute_query(
            query, (website, username, encrypted_password, salt)
        )

    def get_password(self, website):
        query = (
            "SELECT username, password, salt, created_at FROM accounts WHERE website=%s"
        )
        results = self.db_manager.fetch_all(query, (website,))
        return results

    def show_all_passwords(self):
        query = "SELECT website, username, password, salt, created_at FROM accounts"
        results = self.db_manager.fetch_all(query)
        if results:
            print("\n" + "-" * 40)
            print(f"All Passwords:")
            print("-" * 40)
            for index, result in enumerate(results, start=1):
                salt = result[3]
                encrypted_password = result[2]
                decrypted_password = self.crypto_manager.decrypt(
                    encrypted_password, salt
                )
                print(
                    f"{index}. Website: {result[0]}, Username: {result[1]}, Password: {decrypted_password}  Created at: {result[4]}"
                )
            print("-" * 40 + "\n")
        else:
            print("\n" + "-" * 40)
            print("database is empty")
            print("-" * 40)

    def display_passwords(self, website, query_results):
        # Adding a header with separation lines
        print("\n" + "-" * 40)
        print(f"Results for '{website}':")
        print("-" * 40)

        if query_results:
            for index, result in enumerate(query_results, start=1):
                salt = result[2]
                encrypted_password = result[1]
                decrypted_password = self.crypto_manager.decrypt(
                    encrypted_password, salt
                )
                print(
                    f"{index}. Username: {result[0]}, Password: {decrypted_password}    Created at: {result[3]}"
                )
            print("-" * 40 + "\n")
        else:
            print("No password found for this website.")
            print("-" * 40)

    def option_to_copy_password(self, query_results):
        if query_results:

            while True:
                copy_choice = (
                    input("Do you want to copy a password to the clipboard? (y/n): ")
                    .strip()
                    .lower()
                )
                if copy_choice in ["y", "n"]:
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

            if copy_choice == "y":
                while True:
                    try:
                        password_number = int(
                            input("Enter the number of the password to copy: ")
                        )
                        if 1 <= password_number <= len(query_results):
                            salt = query_results[password_number - 1][2]
                            encrypted_password = query_results[password_number - 1][1]
                            decrypted_password = self.crypto_manager.decrypt(
                                encrypted_password, salt
                            )
                            pyperclip.copy(decrypted_password)
                            print("\n" + "-" * 40)
                            print(
                                f"Password for username '{query_results[password_number - 1][0]}' copied to clipboard!"
                            )
                            print("-" * 40 + "\n")
                            break
                        else:
                            print(
                                f"Invalid number. Please enter a number between 1 and {len(query_results)}."
                            )
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

    def delete_password(self, website, username):
        query = "DELETE FROM accounts WHERE website=%s AND username=%s"
        self.db_manager.execute_query(query, (website, username))

    def update_password(self, website, username, new_password):
        encrypted_password = self.crypto_manager.encrypt(new_password)
        salt = self.crypto_manager.get_salt()
        query = (
            "UPDATE accounts SET password=%s, salt=%s WHERE website=%s AND username=%s"
        )
        self.db_manager.execute_query(
            query, (encrypted_password, salt, website, username)
        )

    def generate_password(self, default_length=None):
        length = default_length
        if isinstance(default_length, int) and default_length > 0:
            length = default_length
        else:
            while True:
                try:
                    length = int(
                        input(f"Enter the length of the password : ") or default_length
                    )
                    if length <= 0:
                        raise ValueError("Password length must be a positive integer.")
                    break
                except ValueError as e:
                    print(f"Invalid input: {e}. Please enter a valid number.")

        characters = list(string.ascii_letters + string.digits + string.punctuation)
        random.shuffle(characters)
        password = [random.choice(characters) for _ in range(length)]

        # Shuffling the resultant password
        random.shuffle(password)

        # Converting the list to string and returning it
        return "".join(password)
