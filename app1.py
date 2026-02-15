# from flask import Flask , render_template , request
# import sqlite3

# app = Flask(__name__)

# @app.route("/", methods=["GET" , "POST"])
# def home():
#     result = None
#     if request.method== "POST":
#         A = int(request.form["A"])
#         B = int(request.form["B"])
#         operations = request.form.get("operations")

#         if operations == "add":
#             result = A + B
#         elif operations == "sub":
#             result = A - B

#         elif operations == "mul":
#             result = A * B

#         elif operations == "div":
#             if B !=0:
#               result = A / B
#             else:
#                 result = "cannot divide by zero" 


#         conn = sqlite3.connect("data.db")
#         cursor = conn.cursor()

#         cursor.execute("CREATE TABLE IF NOT EXISTS records2(A REAL , B REAL ,operations TEXT, result REAL)")
#         cursor.execute("INSERT INTO records2 VALUES(? , ? ,? , ?)" , (A , B ,operations, result))

#         conn.commit()
#         conn.close()

#     return render_template("index.html" , result = result)

# @app.route("/history")
# def history():
#     conn = sqlite3.connect("data.db")
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM records2")
#     records2 = cursor.fetchall()

#     conn.close()

#     return render_template("history.html" , records2=records2)

# if __name__ == "__main__":
#     app.run(debug=True)

# --------------------------------------------------------------------------------------------------------

# ADDING DELETE FUNCTIONS

# from flask import Flask , render_template , request , redirect
# import sqlite3

# app = Flask(__name__)

# @app.route("/", methods=["GET" , "POST"])
# def home():
#     result = None
#     if request.method== "POST":
#         A = int(request.form["A"])
#         B = int(request.form["B"])
#         operations = request.form.get("operations")

#         if operations == "add":
#             result = A + B
#         elif operations == "sub":
#             result = A - B

#         elif operations == "mul":
#             result = A * B

#         elif operations == "div":
#             if B !=0:
#               result = A / B
#             else:
#                 result = "cannot divide by zero" 


#         conn = sqlite3.connect("data.db")
#         cursor = conn.cursor()

#         cursor.execute("CREATE TABLE IF NOT EXISTS records2(id INTEGER PRIMARY KEY AUTOINCREMENT,A REAL , B REAL ,operations TEXT, result REAL)")
#         cursor.execute("INSERT INTO records2 (A , B ,operations, result) VALUES(? , ? ,? , ?)" , (A , B ,operations, result))

#         conn.commit()
#         conn.close()

#     return render_template("index.html" , result = result)

# @app.route("/history")
# def history():
#     conn = sqlite3.connect("data.db")
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM records2")
#     records2 = cursor.fetchall()

#     conn.close()

#     return render_template("history.html" , records2=records2)

# @app.route("/delete/<int:id>")
# def delete(id):
#     conn = sqlite3.connect("data.db")
#     cursor = conn.cursor()

#     cursor.execute("DELETE FROM records2 WHERE id = ?" , (id,))
#     conn.commit()
#     conn.close()

#     return redirect("/history")


# if __name__ == "__main__":
#     app.run(debug=True)

# -----------------------------------------------------------------------------------------------------------------------------

# ADDING EDIT and UPDATE FUNCTION 

from flask import Flask, render_template , request , redirect
import sqlite3

app = Flask(__name__)

@app.route("/" , methods = ["GET" , "POST"])
def home():
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
                result = A/B
            else : 
                result = "cannot divide by zero"

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        conn.execute("CREATE TABLE IF NOT EXISTS records2(id INTEGER PRIMARY KEY AUTOINCREMENT , A REAL , B REAL , operations TEXT , result REAL)")
        conn.execute("INSERT INTO records2 (A, B, operations, result) VALUES(? , ? , ? , ?)" , (A , B , operations , result))

        conn.commit() #This is only needed when you CHANGE the database.
        conn.close()

    return render_template("index.html" , result = result)

@app.route("/history")
def history():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM records2")
    records2 = cursor.fetchall()

    # here we are just selecting the table not changing anything so , no need of commit
    conn.close()

    return render_template("history.html" , records2 = records2 )

@app.route("/delete/<int:id>")
def delete(id):
    conn=sqlite3.connect("data.db")
    cursor = conn.cursor() 

    cursor.execute("DELETE FROM records2 WHERE id = ?" , (id,))

    conn.commit()
    conn.close()

    return redirect("/history")

# if browser goes to edit/5 means flask will get id = 5
@app.route("/edit/<int:id>")
def edit(id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # here the passed value of od will get here and that will get select
    # why (id,) and not (id) because SQlite expects tuple as a parameter and (id,) is a tuple
    cursor.execute("SELECT * FROM records2 WHERE id = ?",(id,))
    records1 = cursor.fetchone()

    conn.close()

    return render_template("edit.html" , records1 = records1)


@app.route('/update/<int:id>' , methods=["POST"])
def update(id):
    A = float(request.form["A"])
    B = float(request.form["B"])
    operations = request.form['operations']

    if operations == "+":
        result = A + B
    elif operations == "-":
        result = A - B
    elif operations == "*":
        result = A * B
    elif operations == "/":
        result = A /B

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(""" UPDATE records2 SET A = ? , B = ? , operations = ? , result = ? WHERE id = ?""" , ( A , B , operations , result , id))

    conn.commit()
    conn.close()

    return redirect('/history')


if __name__ == "__main__":
    app.run(debug= True)

