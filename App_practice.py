from flask import Flask , render_template ,request , redirect , session
import sqlite3

app = Flask(__name__)

app.secret_key = "supersecretkey"
def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records2(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        A REAL,
        B REAL,
        operations TEXT,
        result REAL
    )
    """)

    # Check if user_id column exists
    cursor.execute("PRAGMA table_info(records2)")
    columns = [col[1] for col in cursor.fetchall()]

    if "user_id" not in columns:
        cursor.execute("ALTER TABLE records2 ADD COLUMN user_id INTEGER")

    conn.commit()
    conn.close()
    
@app.route("/" , methods=["GET","POST"])
def home():
    if "user_id" not in session:
        return redirect("/login")
    result = None

    if request.method == "POST":
        A = int(request.form["A"])
        B = int(request.form["B"])
        operations = request.form.get("operations")

        if operations == "add":
            result = A + B
        elif operations == "sub":
            result = A - B
        elif operations == "mul":
            result = A * B
        elif operations == "div":
            if B != 0:
                result  = A / B
            else :
                result = "cannot divide by zero"


    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS records3 (id INTEGER PRIMARY KEY AUTOINCREMENT ,user_id INTEGER, A REAL , B REAL , operations TEXT , result REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE , password TEXT)")

    if result is not None:
        user_id = session("user_id")

        cursor.execute("INSERT INTO records3(user_id , A , B ,operations , result) VALUES(?,?,?,?,?)",(user_id,A , B, operations ,result))

    conn.commit()
    conn.close()

    return render_template("index.html",result = result)


@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/login")
    
    user_id = session["user_id"]

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM records3 WHERE user_id=?",(user_id,))
    records3 = cursor.fetchall()
    conn.close()

    return render_template("history.html",records3=records3)

@app.route("/delete/<int:id>")
def delete(id):
    if "user_id" not in session:
        return redirect("/login")
    
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM records3 WHERE id=? AND user_id=?",(id,session["user_id"]))

    conn.commit()
    conn.close()

    return redirect("/history")

@app.route("/edit/<int:id>")
def edit(id):
    if "user_id" not in session:
        return redirect("/login")
    
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM records3 WHERE id=? AND user_id=?",(id,session["user_id"]))
    records4 = cursor.fetchone()

    conn.close()

    return render_template("edit.html",records4 = records4)

@app.route("/update/<int:id>",methods=["POST"])
def update(id):
    if "user_id" not in session:
        return redirect ("/login")
    
    A = float(request.form["A"])
    B = float(request.form["B"])

    operations = request.form["operations"]

    if operations == "+":
        result = A + B
    elif operations == "-":
        result = A - B
    elif operations == "*":
        result = A * B
    elif operations == "/":
        if B!=0:
            result = A /B
        else : 
            result = "cannot divide by zero"


    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE records3 SET A = ? , B = ?,operations =? , result = ? WHERE id=? AND user_id=?",(A,B,operations,result,id,session["user_id"]))

    conn.commit()
    conn.close()

    return redirect("/login")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))

        conn.commit()
        conn.close()

        return redirect ("/login")
    
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        cursor.execute("SELECT* FROM users WHERE username=? AND password=?",(username,password))

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] - user[0]
            return redirect("/")
        else:
            return "invalid username or password"
        
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id",None)
    return redirect("/login")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)


            
