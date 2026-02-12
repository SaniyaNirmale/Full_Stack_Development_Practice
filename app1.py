from flask import Flask , render_template , request
import sqlite3

app = Flask(__name__)

@app.route("/" , methods=["GET" , "POST"])
def home():
    result = None

    if request.method == "POST":
        A = int(request.form["A"])
        B = int(request.form["B"])
        result = A + B

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS records(A REAL , B REAL , result REAL)")
        cursor.execute("INSERT INTO records VALUES(? , ? , ?) " ,(A , B , result))

        conn.commit()
        conn.close()
                       
    return render_template("index1.html" , result= result)
    
if __name__ == "__main__":
    app.run(debug=True)
