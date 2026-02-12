# from flask import Flask

# app = Flask(__name__) # creating website and giving flask the location of file (__name__)

# @app.route("/") #when someone visit the route (/) run the function below.
# def home(): # python function # flask connects URL to python function
#     return "Hello World"

# # Browser sends request -> server sends response -> browser display response
# if __name__ == "__main__": #when we run this code python internally sets this , so condition = true 
#         app.run(debug=True) #and then this runs 



# # ⬇
# # Flask creates app
# # ⬇
# # Server starts
# # ⬇
# # You open browser
# # ⬇
# # Browser sends request to /
# # ⬇
# # Flask finds matching route
# # ⬇
# # Runs home()
# # ⬇
# # Returns "Hello World"
# # ⬇
# # Browser shows it


# ------------------------------------------------------------------

# from flask import Flask , render_template 
# #we use templates beacuase flask is designed to search under (project/templates/) 
# # so we have to create html file under templates

# app = Flask(__name__)
# @app.route("/")
# def home():
#     return render_template("index.html") #instead of sending plain text here we are sending a webpage.

# if(__name__) == "__main__":
#     app.run(debug=True)


# -----------------------------------------------------------------

# -------------------------------------------------------------------------

# from flask import Flask , render_template , request 
# # request = browser's request to the server
# app = Flask(__name__)

# @app.route("/", methods=["GET","POST"])
# def home(): 
#     if request.method == "POST": # this lines check if the user submit the form 
#         # request.form => its a dictionary its store the value entered in the input
#         A = int(request.form["A"])
#         B = int(request.form["B"])
#         result = A + B
#         # Form data → always string
#         #Convert manually if you need numbers like (A = int(request.form["A"]))
#         return "result is" + str(result) #its like frontend send data , backend recieved it and then backend responded to confirm
    
#     return render_template("index.html" , result= result) #if user did not give any input , just show the interface
# # as in return render_template i added result= result so now it passes the result to HTML
# # if(__name__) == "__main__":
# #         app.run(debug=True)


# --------------------------------------------------------------------------------
#Adding database =>

from flask import Flask , render_template , request 
import sqlite3

app = Flask(__name__)

@app.route("/" , methods=["GET","POST"])
def home():
    result = None
    if request.method == "POST":
        A = int(request.form["A"])
        B = int(request.form["B"])
        result = A + B

        conn = sqlite3.connect("data.db") #checks if the data.db exist if no then it creates it and here conn= connection(joins code and database)
        cursor = conn.cursor() # use cursor to write SQL query , sends commands to database and reads results

        cursor.execute("CREATE TABLE IF NOT EXISTS records(A REAL , B REAL result REAL)") #it creates a table 
        cursor.execute("INSERT INTO records VALUES(? , ? , ?)" , (A,B,result)) # here (A , B , result) is a tuple and ? is a placeholder

        conn.commit() #it saves data
        conn.close() # it closes the connection
    
    return render_template("index.html" , result = result)

if __name__ == "__main__":
    app.run(debug = True)





