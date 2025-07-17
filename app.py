from flask import Flask, render_template, request, redirect, session
import pyodbc
from db_config import conn_str

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for using sessions

# Connect to SQL Server
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        cursor.execute("SELECT * FROM Head WHERE HID = ? AND Password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            session['user'] = username
            return redirect('/dashboard')
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html')
@app.route('/add_group', methods=['GET', 'POST'])
def add_group():
    if 'user' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        group_id = request.form['group_id']
        group_name = request.form['group_name']

        try:
            cursor.execute("INSERT INTO Groups (Group_id, Group_name) VALUES (?, ?)", (group_id, group_name))
            conn.commit()
            return "Group added successfully!"
        except pyodbc.IntegrityError as e:
            return "Error: " + str(e)
    
    return render_template('add_group.html')

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        member_id = request.form['member_id']
        mname = request.form['mname']
        group_id = request.form['group_id']
        phone_no = request.form['phone_no']
        address = request.form['address']
        age = request.form['age']
        gender = request.form['gender']

        try:
            cursor.execute("""
                INSERT INTO Member (Member_ID, MName, Group_id, Phone_no, Address, Age, Gender)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (member_id, mname, group_id, phone_no, address, age, gender))
            conn.commit()
            return "Member added successfully!"
        except Exception as e:
            return "Error: " + str(e)

    return render_template('add_member.html')

@app.route('/members')
def view_members():
    if 'user' not in session:
        return redirect('/login')

    cursor.execute("SELECT * FROM Member")
    members = cursor.fetchall()
    print(members)
    return render_template('members.html', members=members)

@app.route('/groups')
def view_groups():
    if 'user' not in session:
        return redirect('/login')

    cursor.execute("SELECT * FROM Groups")
    groups = cursor.fetchall()
    return render_template('groups.html', groups=groups)

@app.route("/view_savings")
def view_savings():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Savings")
    savings = cursor.fetchall()
    return render_template("savings.html", savings=savings)


@app.route('/add_savings', methods=['GET', 'POST'])
def add_savings():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        member_id = request.form['member_id']
        amount = float(request.form['amount'])

        try:
            cursor.execute("EXEC UpdateTotalSavings ?, ?", (member_id, amount))
            conn.commit()
            return "Savings updated successfully!"
        except pyodbc.IntegrityError as e:
            return "Error: " + str(e)
    return render_template('add_savings.html')

@app.route('/add_loan', methods=['GET', 'POST'])
def add_loan():
    if 'user' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        member_id = request.form['member_id']
        loan_amount = float(request.form['loan_amount'])
        ewi = float(request.form['ewi'])
        amount_paid = float(request.form['amount_paid'])

        # Check if loan already exists
        cursor.execute("SELECT * FROM Loan WHERE Member_ID = ?", (member_id,))
        existing_loan = cursor.fetchone()
        
        if existing_loan:
            return "Loan already exists for this member!"

        try:
            cursor.execute("""
                INSERT INTO Loan (Member_ID, loan_amount, EWI, amount_paid)
                VALUES (?, ?, ?, ?)
            """, (member_id, loan_amount, ewi, amount_paid))
            conn.commit()
            return "Loan added successfully!"
        except Exception as e:
            return "Error: " + str(e)

    # Get members list for dropdown
    cursor.execute("SELECT Member_ID, MName FROM Member")
    members = cursor.fetchall()

    return render_template('add_loan.html', members=members)

@app.route('/add_suraksha', methods=['GET', 'POST'])
def add_suraksha():
    if 'user' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        member_id = request.form['member_id']
        suraksha_no = request.form['suraksha_no']
        group_id = request.form['group_id']
        amount_paid = float(request.form['amount_paid'])
        dependants = int(request.form['dependants'])

        try:
            cursor.execute("EXEC InsertSurakshaRecord ?, ?, ?, ?, ?", 
                           (member_id, suraksha_no, group_id, amount_paid, dependants))
            conn.commit()
            return "Suraksha record added successfully!"
        except Exception as e:
            return "Error: " + str(e)

    # Get dropdown options
    cursor.execute("SELECT Member_ID FROM Member")
    members = cursor.fetchall()
    cursor.execute("SELECT Group_id FROM Groups")
    groups = cursor.fetchall()

    return render_template('add_suraksha.html', members=members, groups=groups)

@app.route('/view_suraksha')
def view_suraksha():
    if 'user' not in session:
        return redirect('/login')
    
    cursor.execute("SELECT * FROM Suraksha")
    data = cursor.fetchall()
    return render_template('suraksha.html', data=data)


@app.route('/loans')
def view_loans():
    if 'user' not in session:
        return redirect('/login')
    
    cursor.execute("""
        SELECT Member.Member_ID, Member.MName, Loan.loan_amount, Loan.EWI, Loan.amount_paid, Loan.amount_remaining
        FROM Loan
        JOIN Member ON Loan.Member_ID = Member.Member_ID
    """)
    loans = cursor.fetchall()
    
    return render_template('loans.html', loans=loans)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
