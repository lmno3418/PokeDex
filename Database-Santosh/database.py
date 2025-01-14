import psycopg2
from psycopg2 import sql
import bcrypt

# Database connection details
DB_HOST = "localhost"
DB_NAME = "santoshh"
DB_USER = "postgres"
DB_PASSWORD = "8975"


# Connect to PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None


# Register a new user
def register_user(user_id, password, full_name, email):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cur.execute("""
                INSERT INTO users (user_id, password, full_name, email)
                VALUES (%s, %s, %s, %s)
            """, (user_id, hashed_password, full_name, email))
            conn.commit()
            return True
        except Exception as e:
            print("Error during registration:", e)
            return False
        finally:
            conn.close()

# Verify login credentials
def login_user(user_id, password):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            # Check if the user exists
            cur.execute("SELECT password FROM users WHERE user_id = %s", (user_id,))
            result = cur.fetchone()

            if result is None:
                # User ID does not exist
                print("Invalid User ID.")
                return "user_not_found"

            # Check if the password matches
            if bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                return "login_success"
            else:
                return "invalid_password"
        except Exception as e:
            print("Error during login:", e)
            return "error"
        finally:
            conn.close()


# Main program
if __name__ == "__main__":
    print("1. Register")
    print("2. Login")
    choice = input("Choose an option (1/2): ")

    if choice == "1":
        user_id = input("Enter User ID: ")
        password = input("Enter Password: ")
        register_user(user_id, password)
    elif choice == "2":
        user_id = input("Enter User ID: ")
        password = input("Enter Password: ")
        login_user(user_id, password)
    else:
        print("Invalid choice.")
