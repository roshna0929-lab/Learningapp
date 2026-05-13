from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

USERS_FILE = "users.json"
RECORDS_FILE = "records.json"

# -----------------------------
# CREATE FILES IF NOT EXISTS
# -----------------------------

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(RECORDS_FILE):
    with open(RECORDS_FILE, "w") as f:
        json.dump([], f)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def load_records():
    with open(RECORDS_FILE, "r") as f:
        return json.load(f)

def save_records(records):
    with open(RECORDS_FILE, "w") as f:
        json.dump(records, f, indent=4)

# -----------------------------
# HOME ROUTE
# -----------------------------

@app.route("/")
def home():
    return jsonify({
        "message": "Smart Learning App Backend Running"
    })

# -----------------------------
# SIGNUP
# -----------------------------

@app.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "message": "All fields are required"
        }), 400

    users = load_users()

    # CHECK EXISTING USER
    for user in users:
        if user["username"] == username:
            return jsonify({
                "message": "User already exists"
            }), 400

    new_user = {
        "username": username,
        "password": password
    }

    users.append(new_user)

    save_users(users)

    return jsonify({
        "message": "Signup Successful"
    })

# -----------------------------
# LOGIN
# -----------------------------

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    users = load_users()

    for user in users:

        if user["username"] == username and user["password"] == password:

            return jsonify({
                "message": "Login Successful",
                "user": username
            })

    return jsonify({
        "message": "Invalid Username or Password"
    }), 401

# -----------------------------
# SAVE QUIZ RECORD
# -----------------------------

@app.route("/save_record", methods=["POST"])
def save_record():

    data = request.get_json()

    records = load_records()

    records.append(data)

    save_records(records)

    return jsonify({
        "message": "Record Saved Successfully"
    })

# -----------------------------
# GET ALL RECORDS
# -----------------------------

@app.route("/admin_records", methods=["GET"])
def admin_records():

    password = request.args.get("password")

    if password != "admin":
        return jsonify({
            "message": "Unauthorized Access"
        }), 403

    records = load_records()

    return jsonify(records)

# -----------------------------
# DELETE RECORD
# -----------------------------

@app.route("/delete_record/<int:index>", methods=["DELETE"])
def delete_record(index):

    password = request.args.get("password")

    if password != "admin":
        return jsonify({
            "message": "Unauthorized Access"
        }), 403

    records = load_records()

    if index >= len(records):
        return jsonify({
            "message": "Record Not Found"
        }), 404

    deleted_record = records.pop(index)

    save_records(records)

    return jsonify({
        "message": "Record Deleted",
        "deleted_record": deleted_record
    })

# -----------------------------
# UPDATE RECORD
# -----------------------------

@app.route("/update_record/<int:index>", methods=["PUT"])
def update_record(index):

    password = request.args.get("password")

    if password != "admin":
        return jsonify({
            "message": "Unauthorized Access"
        }), 403

    new_data = request.get_json()

    records = load_records()

    if index >= len(records):
        return jsonify({
            "message": "Record Not Found"
        }), 404

    records[index] = new_data

    save_records(records)

    return jsonify({
        "message": "Record Updated Successfully"
    })

# -----------------------------
# GET ALL USERS
# -----------------------------

@app.route("/users", methods=["GET"])
def get_users():

    password = request.args.get("password")

    if password != "admin":
        return jsonify({
            "message": "Unauthorized Access"
        }), 403

    users = load_users()

    return jsonify(users)

# -----------------------------
# RUN APP
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
