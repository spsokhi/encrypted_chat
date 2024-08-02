# End-to-End Encrypted Chat Application

This project is a secure chat application built with Python Flask, featuring end-to-end encryption using AES for message security. The application includes an admin panel for user management, a login system, and a chat room with a dynamic user list.

## Features

- **End-to-End Encryption:** Ensures secure communication between users using AES encryption.
- **Admin Panel:** Allows administrators to add and remove users.
- **User Authentication:** Secure login system for users and admins.
- **Real-time Chat:** Supports real-time messaging with an active user list.
- **Responsive Design:** Modern and responsive UI for various screen sizes.

## Project Structure
```
 encrypted_chat/
│
├── templates/ # HTML templates
│ ├── login.html # Login page
│ ├── admin.html # Admin panel
│ └── chat.html # Chat room
│
├── static/ # Static files
│ └── style.css # CSS styles
│
├── admin.csv # Admin credentials
├── users.csv # User credentials
├── app.py # Main application code
├── requirements.txt # Python dependencies
└── .gitignore # Git ignore file
```

## Installation

To run this project locally, follow these steps:

### Prerequisites

- **Python 3.x:** Make sure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

- **Git:** You need Git to clone the repository. You can download it from [git-scm.com](https://git-scm.com/downloads).

### Step-by-Step Guide

1. **Clone the Repository:**

   Open your terminal and run the following command to clone the repository:

   ```
   git clone https://github.com/your-username/encrypted_chat.git
   
2. **Navigate to the Project Directory:**
   Change into the project directory:
   ```
   cd encrypted_chat
3. **Create a Virtual Environment:**
   ```
   python -m venv venv

4. **Activate the Virtual Environment:**
 + On Windows:
   ```
   venv\Scripts\activate
   
 + On macOS and Linux:
 ```
source venv/bin/activate
```
5. **Install the Required Packages:**
   Install the required Python packages using pip:
   ```
   pip install -r requirements.txt

6. **Run the Application:**
   Start the Flask application:
 ```
  python app.py
```
7. **Access the Application:**

 Open your web browser and go to `http://localhost:5000` to access the chat application.


## Configuration
### Admin Credentials
+ The admin.csv file contains admin credentials in the format username,password.
+ Update this file to manage admin logins.
### User Credentials
+ The users.csv file contains user credentials in the format username,password.
+ The admin panel allows you to add and remove users.
### Security Considerations
+ Encryption Key: Ensure that the encryption key used for AES encryption is kept secure and not exposed in your code.
+ Sensitive Files: The .gitignore file is configured to exclude sensitive files like .env from being committed to the repository.

## Troubleshooting
### Common Issues
+ **Virtual Environment Activation Fails:**

Ensure that you have the correct permissions and are using the correct command for your operating system.

+ **Dependencies Not Installing:**

Verify that your virtual environment is activated and that requirements.txt is correctly formatted.

+ **Application Not Starting:**

Check for syntax errors in your code or ensure all required files are present.


