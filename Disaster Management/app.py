from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

# =========================================================
# APPLICATION SETTINGS
# =========================================================

app.secret_key = "DMS_ITPM_2026_SECRET_KEY"

DATABASE = "database.db"


# =========================================================
# DATABASE
# =========================================================

def get_db():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():

    connection = get_db()

    cursor = connection.cursor()


    # -----------------------------------------------------
    # USERS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT DEFAULT 'user'

        )
    """)


    # -----------------------------------------------------
    # INCIDENTS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            incident_type TEXT NOT NULL,

            location TEXT NOT NULL,

            severity TEXT NOT NULL,

            description TEXT NOT NULL,

            reported_by TEXT NOT NULL,

            status TEXT DEFAULT 'Pending',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)


    # -----------------------------------------------------
    # ALERTS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            message TEXT NOT NULL,

            severity TEXT NOT NULL,

            location TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)


    # -----------------------------------------------------
    # SHELTERS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shelters (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            location TEXT NOT NULL,

            capacity INTEGER NOT NULL,

            available INTEGER NOT NULL

        )
    """)


    # -----------------------------------------------------
    # RESPONSE TEAMS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            team_type TEXT NOT NULL,

            location TEXT NOT NULL,

            status TEXT DEFAULT 'Available'

        )
    """)


    # =====================================================
    # DEFAULT ADMIN
    # =====================================================

    admin_password = generate_password_hash("admin123")


    cursor.execute("""
        INSERT OR IGNORE INTO users
        (
            name,
            email,
            password,
            role
        )
        VALUES (?, ?, ?, ?)
    """, (
        "Administrator",
        "admin@dms.com",
        admin_password,
        "admin"
    ))


    # =====================================================
    # DEFAULT ALERTS
    # =====================================================

    alert_count = cursor.execute("""
        SELECT COUNT(*)
        FROM alerts
    """).fetchone()[0]


    if alert_count == 0:

        alerts = [

            (
                "Heavy Rainfall Warning",

                "Residents in low-lying areas should remain alert and avoid unnecessary travel.",

                "High",

                "Coastal Odisha"
            ),

            (
                "Strong Wind Advisory",

                "Secure loose objects and follow local emergency instructions.",

                "Medium",

                "Odisha Coast"
            ),

            (
                "Community Preparedness Notice",

                "Check emergency kits and keep important emergency contact numbers accessible.",

                "Low",

                "All Areas"
            )

        ]


        cursor.executemany("""
            INSERT INTO alerts
            (
                title,
                message,
                severity,
                location
            )
            VALUES (?, ?, ?, ?)
        """, alerts)


    # =====================================================
    # DEFAULT SHELTERS
    # =====================================================

    shelter_count = cursor.execute("""
        SELECT COUNT(*)
        FROM shelters
    """).fetchone()[0]


    if shelter_count == 0:

        shelters = [

            (
                "Community Relief Centre",
                "Bhubaneswar",
                500,
                320
            ),

            (
                "Cyclone Shelter",
                "Puri",
                800,
                550
            ),

            (
                "Emergency Shelter",
                "Cuttack",
                400,
                280
            ),

            (
                "Coastal Relief Centre",
                "Balasore",
                600,
                410
            )

        ]


        cursor.executemany("""
            INSERT INTO shelters
            (
                name,
                location,
                capacity,
                available
            )
            VALUES (?, ?, ?, ?)
        """, shelters)


    # =====================================================
    # DEFAULT RESPONSE TEAMS
    # =====================================================

    team_count = cursor.execute("""
        SELECT COUNT(*)
        FROM teams
    """).fetchone()[0]


    if team_count == 0:

        teams = [

            (
                "Team Alpha",
                "Medical Response",
                "Bhubaneswar",
                "Available"
            ),

            (
                "Team Bravo",
                "Search & Rescue",
                "Puri",
                "Available"
            ),

            (
                "Team Charlie",
                "Fire & Rescue",
                "Cuttack",
                "On Duty"
            ),

            (
                "Team Delta",
                "Relief & Logistics",
                "Balasore",
                "Available"
            )

        ]


        cursor.executemany("""
            INSERT INTO teams
            (
                name,
                team_type,
                location,
                status
            )
            VALUES (?, ?, ?, ?)
        """, teams)


    connection.commit()

    connection.close()


# =========================================================
# LOGIN REQUIRED
# =========================================================

def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please login to continue.",
                "warning"
            )

            return redirect(
                url_for("login")
            )

        return function(*args, **kwargs)

    return wrapper


# =========================================================
# ADMIN REQUIRED
# =========================================================

def admin_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if session.get("role") != "admin":

            flash(
                "Administrator access required.",
                "danger"
            )

            return redirect(
                url_for("dashboard")
            )

        return function(*args, **kwargs)

    return wrapper


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    if "user_id" in session:

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "about.html"
    )


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )


        connection = get_db()


        user = connection.execute("""
            SELECT *
            FROM users
            WHERE email = ?
        """, (
            email,
        )).fetchone()


        connection.close()


        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]

            session["name"] = user["name"]

            session["email"] = user["email"]

            session["role"] = user["role"]


            flash(
                "Login successful.",
                "success"
            )


            return redirect(
                url_for("dashboard")
            )


        flash(
            "Invalid email or password.",
            "danger"
        )


    return render_template(
        "login.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name"
        )

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )


        hashed_password = generate_password_hash(
            password
        )


        connection = get_db()


        try:

            connection.execute("""
                INSERT INTO users
                (
                    name,
                    email,
                    password
                )
                VALUES (?, ?, ?)
            """, (
                name,
                email,
                hashed_password
            ))


            connection.commit()


            flash(
                "Registration successful. Please login.",
                "success"
            )


            return redirect(
                url_for("login")
            )


        except sqlite3.IntegrityError:

            flash(
                "This email is already registered.",
                "danger"
            )


        finally:

            connection.close()


    return render_template(
        "register.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()


    flash(
        "You have been logged out.",
        "success"
    )


    return redirect(
        url_for("home")
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    connection = get_db()


    incident_count = connection.execute("""
        SELECT COUNT(*)
        FROM incidents
    """).fetchone()[0]


    alert_count = connection.execute("""
        SELECT COUNT(*)
        FROM alerts
    """).fetchone()[0]


    shelter_count = connection.execute("""
        SELECT COUNT(*)
        FROM shelters
    """).fetchone()[0]


    team_count = connection.execute("""
        SELECT COUNT(*)
        FROM teams
    """).fetchone()[0]


    recent_incidents = connection.execute("""
        SELECT *
        FROM incidents
        ORDER BY id DESC
        LIMIT 5
    """).fetchall()


    alerts = connection.execute("""
        SELECT *
        FROM alerts
        ORDER BY id DESC
        LIMIT 5
    """).fetchall()


    connection.close()


    return render_template(
        "dashboard.html",

        incident_count=incident_count,

        alert_count=alert_count,

        shelter_count=shelter_count,

        team_count=team_count,

        recent_incidents=recent_incidents,

        alerts=alerts
    )


# =========================================================
# ALERTS
# =========================================================

@app.route("/alerts")
@login_required
def alerts():

    connection = get_db()


    alerts = connection.execute("""
        SELECT *
        FROM alerts
        ORDER BY id DESC
    """).fetchall()


    connection.close()


    return render_template(
        "alerts.html",
        alerts=alerts
    )


# =========================================================
# LATEST ALERT API
# =========================================================

@app.route("/api/latest-alert")
@login_required
def latest_alert():

    connection = get_db()


    alert = connection.execute("""
        SELECT
            id,
            title,
            message,
            severity,
            location,
            created_at
        FROM alerts
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()


    connection.close()


    if alert is None:

        return {
            "alert": None
        }


    return {
        "alert": {

            "id": alert["id"],

            "title": alert["title"],

            "message": alert["message"],

            "severity": alert["severity"],

            "location": alert["location"],

            "created_at": alert["created_at"]

        }
    }


# =========================================================
# ADMIN CREATE ALERT
# =========================================================

@app.route(
    "/admin/create-alert",
    methods=["POST"]
)
@login_required
@admin_required
def create_alert():

    title = request.form.get(
        "title"
    )

    message = request.form.get(
        "message"
    )

    severity = request.form.get(
        "severity"
    )

    location = request.form.get(
        "location"
    )


    if not title or not message or not severity:

        flash(
            "Please fill all required alert fields.",
            "danger"
        )

        return redirect(
            url_for("admin_monitoring")
        )


    connection = get_db()


    connection.execute("""
        INSERT INTO alerts
        (
            title,
            message,
            severity,
            location
        )
        VALUES (?, ?, ?, ?)
    """, (
        title,
        message,
        severity,
        location
    ))


    connection.commit()

    connection.close()


    flash(
        "Emergency alert published successfully!",
        "success"
    )


    return redirect(
        url_for("admin_monitoring")
    )


# =========================================================
# ADMIN DELETE ALERT
# =========================================================

@app.route(
    "/admin/delete-alert/<int:alert_id>",
    methods=["POST"]
)
@login_required
@admin_required
def delete_alert(alert_id):

    connection = get_db()


    connection.execute("""
        DELETE FROM alerts
        WHERE id = ?
    """, (
        alert_id,
    ))


    connection.commit()

    connection.close()


    flash(
        "Emergency alert removed successfully.",
        "success"
    )


    return redirect(
        url_for("admin_monitoring")
    )


# =========================================================
# INCIDENTS
# =========================================================

@app.route("/incidents")
@login_required
def incidents():

    connection = get_db()


    incidents = connection.execute("""
        SELECT *
        FROM incidents
        ORDER BY id DESC
    """).fetchall()


    connection.close()


    return render_template(
        "incidents.html",
        incidents=incidents
    )


# =========================================================
# REPORT INCIDENT
# =========================================================

@app.route(
    "/report",
    methods=["GET", "POST"]
)
@login_required
def report():

    if request.method == "POST":

        incident_type = request.form.get(
            "incident_type"
        )

        location = request.form.get(
            "location"
        )

        severity = request.form.get(
            "severity"
        )

        description = request.form.get(
            "description"
        )

        reported_by = session["name"]


        connection = get_db()


        connection.execute("""
            INSERT INTO incidents
            (
                incident_type,
                location,
                severity,
                description,
                reported_by
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            incident_type,
            location,
            severity,
            description,
            reported_by
        ))


        connection.commit()

        connection.close()


        flash(
            "Incident reported successfully!",
            "success"
        )


        return redirect(
            url_for("incidents")
        )


    return render_template(
        "report.html"
    )


# =========================================================
# SHELTERS
# =========================================================

@app.route("/shelters")
@login_required
def shelters():

    connection = get_db()


    shelters = connection.execute("""
        SELECT *
        FROM shelters
        ORDER BY id
    """).fetchall()


    connection.close()


    return render_template(
        "shelters.html",
        shelters=shelters
    )


# =========================================================
# RESPONSE TEAMS
# =========================================================

@app.route("/teams")
@login_required
def teams():

    connection = get_db()


    teams = connection.execute("""
        SELECT *
        FROM teams
        ORDER BY id
    """).fetchall()


    connection.close()


    return render_template(
        "teams.html",
        teams=teams
    )


# =========================================================
# ADMIN MONITORING
# =========================================================

@app.route("/admin-monitoring")
@login_required
@admin_required
def admin_monitoring():

    connection = get_db()


    incidents = connection.execute("""
        SELECT *
        FROM incidents
        ORDER BY id DESC
    """).fetchall()


    users = connection.execute("""
        SELECT
            id,
            name,
            email,
            role
        FROM users
        ORDER BY id DESC
    """).fetchall()


    alerts = connection.execute("""
        SELECT *
        FROM alerts
        ORDER BY id DESC
    """).fetchall()


    connection.close()


    return render_template(
        "admin_monitoring.html",

        incidents=incidents,

        users=users,

        alerts=alerts
    )


# =========================================================
# UPDATE INCIDENT STATUS
# =========================================================

@app.route(
    "/update-status/<int:incident_id>",
    methods=["POST"]
)
@login_required
@admin_required
def update_status(incident_id):

    status = request.form.get(
        "status"
    )


    connection = get_db()


    connection.execute("""
        UPDATE incidents
        SET status = ?
        WHERE id = ?
    """, (
        status,
        incident_id
    ))


    connection.commit()

    connection.close()


    flash(
        "Incident status updated successfully.",
        "success"
    )


    return redirect(
        url_for("admin_monitoring")
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
    )