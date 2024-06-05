from modules.database.db_manager import DatabaseManager
from modules.psw_manager.psw_manager import PasswordManager
from modules.UserInputHandler.UserInputHandler import UserInputHandler
from modules.crypto.crypto_manager import CryptoManager
import pyperclip


class PasswordManagerApp:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.db_manager.connect()
        self.db_manager.setup_db()
        self.crypto_manager = CryptoManager(
            self.db_manager, password=self.db_manager.password + self.db_manager.user
        )
        self.password_manager = PasswordManager(self.db_manager, self.crypto_manager)
        self.user_input_handler = UserInputHandler(self.password_manager)

    def run(self):
        while True:
            print("\nPassword Manager")
            print("-" * 40)
            print("1. Add Password")
            print("2. Retrieve Password")
            print("3. Delete Password")
            print("4. Update Password")
            print("5. Generate Random Password")
            print("6. Show all passwords")
            print("7. Delete database")
            print("8. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.user_input_handler.add_password()
            elif choice == "2":
                self.user_input_handler.retrieve_password()
            elif choice == "3":
                self.user_input_handler.delete_password()
            elif choice == "4":
                self.user_input_handler.update_password()
            elif choice == "5":
                psw = self.password_manager.generate_password()
                pyperclip.copy(psw)
                print("\n" + "-" * 40)
                print(f"Generated password: {psw}")
                print("Password copied to clipboard!")
                print("-" * 40 + "\n")
            elif choice == "6":
                self.password_manager.show_all_passwords()
            elif choice == "7":
                self.db_manager.delete_db()
            elif choice == "8":
                self.db_manager.disconnect()
                break
            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":

    app = PasswordManagerApp()
    # run the app
    app.run()
