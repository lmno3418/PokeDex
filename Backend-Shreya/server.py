from flask import Flask, request, render_template, redirect, url_for, flash
from database import register_user, login_user

app = Flask(__name__)
app.secret_key = "pokedex"
@app.route('/')
def home():
    return render_template('Login.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['userid']
        password = request.form['password']
        full_name = request.form['name']
        email = request.form['email']

        if register_user(user_id, password, full_name, email):
            flash("Registration successful! You can now log in.", "success")
        else:
            flash("Error during registration. Please try again.", "danger")

        return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        user_id = request.form['username']
        password = request.form['password']

        login_result = login_user(user_id, password)

        if login_result == "login_success":
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        elif login_result == "user_not_found":
            error_message = "Invalid User ID. Please register first."
        elif login_result == "invalid_password":
            error_message = "Invalid password. Please try again."
        else:
            error_message = "An error occurred during login. Please try again."

    return render_template('Login.html', login_error=error_message)



if __name__ == '__main__':
    app.run(debug=True)
