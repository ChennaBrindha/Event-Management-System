from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

def load_data(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

# ---------------- Login ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_data("users.json")
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            role = users[username]["role"]
            if role == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("user_dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

# ---------------- User Dashboard ----------------
@app.route("/user")
def user_dashboard():
    return render_template("user.html")

# ---------------- User: View Events ----------------
@app.route("/view-events")
def view_events():
    events = load_data("events.json")
    return render_template("view_events.html", events=events)

# ---------------- User: Register for Event ----------------
@app.route("/register-event", methods=["GET", "POST"])
def register_event():
    events = load_data("events.json")
    if request.method == "POST":
        participant_name = request.form["name"]
        event_id = request.form["event_id"]

        participants = load_data("participants.json")
        if event_id not in participants:
            participants[event_id] = []
        participants[event_id].append(participant_name)

        with open("participants.json", "w") as f:
            json.dump(participants, f, indent=4)

        return render_template("register_event.html", events=events, message="Registered Successfully!")

    return render_template("register_event.html", events=events)

if __name__ == "__main__":
    app.run(debug=True)
