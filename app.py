from flask import Flask, render_template, request, redirect, url_for, flash, session
import csv
import os
from flask_socketio import SocketIO, emit, join_room, leave_room
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
socketio = SocketIO(app)

# Define the encryption key (must be 32 bytes for AES-256)
encryption_key = os.urandom(32)

# In-memory storage for users
active_users = set()

# Helper function to encrypt messages
def encrypt_message(message):
    # Use a random initialization vector (IV)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(encryption_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(message.encode()) + encryptor.finalize()
    # Return the encrypted message and IV encoded in base64 for transmission
    return base64.b64encode(iv + encrypted).decode()

# Helper function to decrypt messages
def decrypt_message(encrypted_message):
    encrypted_message_bytes = base64.b64decode(encrypted_message)
    iv = encrypted_message_bytes[:16]
    encrypted_message_bytes = encrypted_message_bytes[16:]
    cipher = Cipher(algorithms.AES(encryption_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_message_bytes) + decryptor.finalize()
    return decrypted.decode()

# Function to load admin credentials from admin.csv
def load_admin_credentials():
    admins = {}
    if os.path.exists('admin.csv'):
        with open('admin.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Check if the row is not empty
                    username, password = row
                    admins[username] = password
    return admins

# Function to load user credentials from users.csv
def load_user_credentials():
    users = {}
    if os.path.exists('users.csv'):
        with open('users.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Check if the row is not empty
                    username, password = row
                    users[username] = password
    return users

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admins = load_admin_credentials()
        users = load_user_credentials()

        # Check if the user is an admin
        if username in admins and admins[username] == password:
            session['username'] = username
            session['is_admin'] = True
            return redirect(url_for('admin_page'))

        # Check if the user is a regular user
        elif username in users and users[username] == password:
            session['username'] = username
            session['is_admin'] = False
            return redirect(url_for('chat'))

        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Route for the admin page
@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if 'username' not in session or not session.get('is_admin', False):
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))

    users = load_user_credentials()

    if request.method == 'POST':
        if 'add_user' in request.form:
            new_username = request.form['new_username']
            new_password = request.form['new_password']
            if new_username and new_password:
                users[new_username] = new_password
                save_user_credentials(users)
                flash('User added successfully!', 'success')
            else:
                flash('Please provide a valid username and password!', 'danger')

        if 'remove_user' in request.form:
            remove_username = request.form['remove_username']
            if remove_username in users:
                del users[remove_username]
                save_user_credentials(users)
                flash('User removed successfully!', 'success')
            else:
                flash('User not found!', 'danger')

    return render_template('admin.html', users=users)

# Route for the chat page
@app.route('/chat')
def chat():
    if 'username' not in session:
        flash('Please log in first!', 'danger')
        return redirect(url_for('login'))

    # Pass the encryption key to the client securely
    return render_template('chat.html', username=session['username'], encryption_key=base64.b64encode(encryption_key).decode())

# WebSocket event for handling messages
@socketio.on('send_message')
def handle_message(data):
    if 'username' not in session:
        emit('error', {'message': 'User not logged in'})
        return

    encrypted_message = data.get('encrypted_message', '')

    # Decrypt the message
    try:
        decrypted_message = decrypt_message(encrypted_message)
        print(f"Decrypted message: {decrypted_message}")
        # Broadcast the message to all connected clients
        emit('receive_message', {'username': session['username'], 'message': decrypted_message}, broadcast=True)
    except Exception as e:
        print(f"Failed to decrypt message: {e}")
        emit('error', {'message': 'Failed to decrypt message'})

# WebSocket event for user joining
@socketio.on('user_joined')
def handle_user_joined(data):
    username = data.get('username')
    if username:
        active_users.add(username)
        print(f"User joined: {username}")
        # Update user list for all clients
        emit('update_user_list', list(active_users), broadcast=True)

# WebSocket event for user leaving
@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    if username in active_users:
        active_users.remove(username)
        print(f"User left: {username}")
        # Update user list for all clients
        emit('update_user_list', list(active_users), broadcast=True)

# Function to save user credentials to users.csv
def save_user_credentials(users):
    with open('users.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for username, password in users.items():
            writer.writerow([username, password])

# Route for logging out
@app.route('/logout')
def logout():
    username = session.get('username')
    if username in active_users:
        active_users.remove(username)
        emit('update_user_list', list(active_users), broadcast=True)
    session.pop('username', None)
    session.pop('is_admin', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
