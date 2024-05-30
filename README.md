# Password Manager


## Description

This is a Python-based password manager application that securely stores and manages your passwords. The application utilizes MySQL database for storage and encryption techniques to ensure the security of your sensitive information.

## Installation

1. **Download MySQL Database:**

   Before running the password manager application, you need to download and install MySQL Database. You can download MySQL Database from [here](https://dev.mysql.com/downloads/mysql/).

2. **Installation:**

   Follow the installation instructions provided for MySQL Database during the download process. Make sure to create a password for the database during installation.

3. **Python Environment Setup:**

   To ensure compatibility and consistency, the project is run in Python version 3.8.3. It is recommended to create a virtual environment for this project. You can use the following commands to set up the virtual environment and install dependencies:

   ```sh
   # Create a virtual environment
   python3 -m venv myenv

   # Activate the virtual environment
   # On Windows:
   myenv\Scripts\activate
   # On macOS and Linux:
   source myenv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

## Usage

### Run the Program
After installing MySQL Database, activating the virtual environment, and installing dependencies, you are ready to use the password manager application. Run the program using your preferred Python environment.

### Login Credentials
You will be prompted to provide your MySQL database username (root is default username) and password. These credentials are required to establish a connection with the database.

### Encryption and Decryption
The provided username and password are used to generate a key for encryption and decryption of passwords stored in the database. Additionally, a unique salt is generated for each password to enhance security.
