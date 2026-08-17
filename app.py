from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ---------------- DATABASE CONFIG ----------------

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ---------------- DATABASE MODELS ----------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100))
    amount = db.Column(db.Float)
    goal = db.Column(db.Float)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    amount = db.Column(db.Float)


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return "Email and password are required!"

        email = email.strip().lower()

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already registered!"

        new_user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html")


# ---------------- LOGIN ----------------

# ---------------- LOGIN ----------------

# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return "Please enter email and password."

        email = email.strip().lower()

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            return redirect(url_for("dashboard"))

        return "Invalid Login"

    return render_template("login.html")

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", name="User")


# ---------------- INCOME ----------------

@app.route("/income", methods=["GET", "POST"])
def income():

    if request.method == "POST":

        source = request.form.get("source")
        amount = float(request.form.get("amount") or 0)
        goal = float(request.form.get("goal") or 0)

        # Remove previous income
        Income.query.delete()
        db.session.commit()

        new_income = Income(
            source=source,
            amount=amount,
            goal=goal
        )

        db.session.add(new_income)
        db.session.commit()

        return redirect(url_for("expense"))

    return render_template("income.html")


# ---------------- EXPENSE ----------------

@app.route("/expense", methods=["GET", "POST"])
def expense():

    if request.method == "POST":

        food = float(request.form.get("food") or 0)
        clothing = float(request.form.get("clothing") or 0)
        travel = float(request.form.get("travel") or 0)
        fees = float(request.form.get("fees") or 0)
        essentials = float(request.form.get("essentials") or 0)
        medical = float(request.form.get("medical") or 0)
        entertainment = float(request.form.get("entertainment") or 0)
        shopping = float(request.form.get("shopping") or 0)
        others = float(request.form.get("others") or 0)

        # Remove previous expenses
        Expense.query.delete()
        db.session.commit()

        categories = [
            ("Food", food),
            ("Clothing", clothing),
            ("Travel", travel),
            ("Fees", fees),
            ("Daily Essentials", essentials),
            ("Medical", medical),
            ("Entertainment", entertainment),
            ("Shopping", shopping),
            ("Others", others)
        ]

        for category, amount in categories:

            if amount > 0:

                expense = Expense(
                    category=category,
                    amount=amount
                )

                db.session.add(expense)

        db.session.commit()

        return redirect(url_for("analysis"))

    return render_template("expense.html")


# ---------------- ANALYSIS ----------------

@app.route("/analysis")
def analysis():

    incomes = Income.query.all()
    expenses = Expense.query.all()

    total_income = sum(i.amount for i in incomes)
    total_expense = sum(e.amount for e in expenses)

    balance = total_income - total_expense

    goal = incomes[0].goal if incomes else 0

    if total_income > 0:
        savings_percentage = (balance / total_income) * 100
    else:
        savings_percentage = 0

    if balance >= goal:

        goal_status = (
            "Congratulations! "
            "You achieved your monthly savings goal."
        )

    else:

        goal_status = (
            f"You need Rs. {goal - balance:.2f} "
            "more to reach your goal."
        )

    highest_expense = None

    if expenses:
        highest_expense = max(
            expenses,
            key=lambda x: x.amount
        )

    if savings_percentage >= 50:

        suggestion = (
            "Excellent! You are saving "
            "a large portion of your income."
        )

    elif savings_percentage >= 30:

        suggestion = (
            "Good! Your finances are under control."
        )

    elif savings_percentage >= 10:

        suggestion = (
            "Try reducing unnecessary expenses "
            "to save more."
        )

    else:

        suggestion = (
            "Your expenses are very high. "
            "Consider reviewing your spending."
        )

    return render_template(
        "analysis.html",
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        goal=goal,
        goal_status=goal_status,
        savings_percentage=round(savings_percentage, 2),
        suggestion=suggestion,
        highest_expense=highest_expense,
        expenses=expenses
    )


# ---------------- CREATE DATABASE ----------------

with app.app_context():
    db.create_all()


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)