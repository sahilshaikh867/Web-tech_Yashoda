from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib


app = Flask(__name__)

# Allow frontend to communicate with Flask
CORS(app)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db():

    connection = sqlite3.connect("users.db")

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================
# CREATE DATABASE TABLE
# ==========================================

def create_table():

    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            username TEXT UNIQUE NOT NULL,

            email TEXT UNIQUE NOT NULL,

            mobile TEXT NOT NULL,

            password TEXT NOT NULL,

            course TEXT NOT NULL,

            address TEXT NOT NULL

        )
    """)

    db.commit()

    db.close()

    print("Database table ready!")


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return "Student Portal Backend is Running!"


# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["POST"])
def register():

    # Receive JSON data

    data = request.get_json()


    # Get values

    name = data.get("name")

    username = data.get("username")

    email = data.get("email")

    mobile = data.get("mobile")

    password = data.get("password")

    course = data.get("course")

    address = data.get("address")


    # ======================================
    # VALIDATION
    # ======================================

    if not name:

        return jsonify({
            "success": False,
            "message": "Name is required"
        })


    if not username:

        return jsonify({
            "success": False,
            "message": "Username is required"
        })


    if not email:

        return jsonify({
            "success": False,
            "message": "Email is required"
        })


    if not mobile:

        return jsonify({
            "success": False,
            "message": "Mobile number is required"
        })


    if not password:

        return jsonify({
            "success": False,
            "message": "Password is required"
        })


    if not course:

        return jsonify({
            "success": False,
            "message": "Course is required"
        })


    if not address:

        return jsonify({
            "success": False,
            "message": "Address is required"
        })


    # ======================================
    # HASH PASSWORD
    # ======================================

    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()


    # ======================================
    # SAVE USER
    # ======================================

    try:

        db = get_db()


        db.execute("""
            INSERT INTO users
            (
                name,
                username,
                email,
                mobile,
                password,
                course,
                address
            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            username,
            email,
            mobile,
            password_hash,
            course,
            address
        ))


        db.commit()

        db.close()


        return jsonify({

            "success": True,

            "message":
                "Registration successful!"

        })


    except sqlite3.IntegrityError:

        return jsonify({

            "success": False,

            "message":
                "Username or email already exists."

        })


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["POST"])
def login():

    # Receive data

    data = request.get_json()


    email = data.get("email")

    password = data.get("password")


    # ======================================
    # VALIDATION
    # ======================================

    if not email:

        return jsonify({

            "success": False,

            "message":
                "Email is required."

        })


    if not password:

        return jsonify({

            "success": False,

            "message":
                "Password is required."

        })


    # ======================================
    # HASH PASSWORD
    # ======================================

    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()


    # ======================================
    # FIND USER
    # ======================================

    db = get_db()


    user = db.execute("""

        SELECT *

        FROM users

        WHERE email = ?

        AND password = ?

    """,
    (
        email,
        password_hash
    )).fetchone()


    db.close()


    # ======================================
    # LOGIN SUCCESS
    # ======================================

    if user:

        return jsonify({

            "success": True,

            "message":
                "Login successful!",

            "user": {

                "name":
                    user["name"],

                "email":
                    user["email"],

                "course":
                    user["course"]

            }

        })


    # ======================================
    # LOGIN FAILED
    # ======================================

    else:

        return jsonify({

            "success": False,

            "message":
                "Invalid email or password."

        })


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    create_table()

    app.run(

        debug=True

    )