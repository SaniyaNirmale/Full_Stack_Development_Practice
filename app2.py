from flask import Flask , render_template , request , redirect
import sqlite3

app = Flask(__name__)

@app.route("/",methods = ["GET" , "POST"])
def home():
    result =  None
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
                result = A /B
            else : 
                result = "cannot divide by zero"

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS records2(id INTEGER PRIMARY KEY AUTOINCREMENT , A REAL , B REAL , operations TEXT , result REAL)")
        cursor.execute("INSERT INTO records (A , B operations , result) VALUES(? , ? , ? , ?)" , (A , B , operations , result))

        conn.commit()
        conn.close()

    return render_template("index.html" , result = result)

@app.route("/history")
def history():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM records")
    records2 = cursor.fetchall()

    conn.close()

    return render_template("history.html" , records2 = records2)


@app.route("/delete<int:id>")
def delete(id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM records2 WHERE int = ?",(id,))

    conn.commit()
    conn.close()

    return redirect("/history")



if __name__ == "__main__":
    app.run(debug=True)