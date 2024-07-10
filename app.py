from flask import Flask, render_template, request, redirect

# Importing the ORM engine/module
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connecting flask app with database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"

# Instance of SQLAlchemy
database = SQLAlchemy(app)

# Python class: Basically this is mapping to database schema
class User(database.Model):

    __tablename__ = "StudentTable"

    Sno = database.Column(database.Integer, primary_key = True)
    Name = database.Column(database.String(100), nullable = False)
    Roll_Number = database.Column(database.Text, nullable = False)
    College_ID = database.Column(database.Text, nullable = False)
    DOB = database.Column(database.Integer, nullable = False)


# route 1: Index route
@app.route("/", methods = ["GET", "POST"])
def index():

    # Handling POST request
    if request.method == "POST":

        # Extracting data 
        student_Name = request.form.get("stdName")
        student_RollNo = request.form.get("stdRollNo")
        student_CollegeID = request.form.get("stdID")
        student_DOB = request.form.get("stdDOB")

        # print(student_Name, student_RollNo, student_CollegeID, student_DOB)

        # Adding it to database 
        # New object(newUser) of python/model class ---> Row in the table of database
        
        newUser = User(Name=student_Name, Roll_Number = student_RollNo, College_ID= student_CollegeID, DOB= student_DOB)

        # Adding it to the database
        database.session.add(newUser)
        database.session.commit()

        # redirect
        return redirect("/")


    # Handling GET request
    else:

        # Getting all the users from database/read operation
        allUsers = User.query.all()


        # Response to client
        return render_template('index.html', allUsers = allUsers)

    
# Route 2: Delete a task from table
@app.route('/delete')
def delete():
    # Extracting the serial number
    serial_number = request.args.get('serial_no')
    
    # Ensure serial_number is provided
    if not serial_number:
        return "Missing serial number", 400

    # Fetching the user with Sno = serial_number
    user = User.query.filter_by(Sno=serial_number).first()
    
    # Check if the user exists
    if user:
        # Deleting the user
        database.session.delete(user)
        database.session.commit()
        return redirect('/')
    else:
        return "User not found or invalid serial number", 404

# Third route: Updating a task

@app.route('/update', methods=["GET", "POST"])
def update():
    serial_number = request.args.get('serial_no')
    if not serial_number:
        return "Missing serial number", 400

    user = User.query.filter_by(Sno=serial_number).first()
    if not user:
        return "User not found", 404

    if request.method == "POST":
        user.Name = request.form.get("stdName")
        user.Roll_Number = request.form.get("stdRollNo")
        user.College_ID = request.form.get("stdID")
        user.DOB = request.form.get("stdDOB")

        database.session.commit()
        return redirect('/')
    else:
        return render_template('update.html', reqTask=user)

if __name__ == "__main__":
    app.run(debug=True)

