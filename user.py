from types import MethodType
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import yaml
import json
import csv




app = Flask(__name__)

db = yaml.load(open('back.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host'] 
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']



mysql = MySQL(app)

@app.route('/register', methods =['POST'])
def index():
    if request.method == 'POST':
        userDetails = request.form
        Name = userDetails['Name']
        Surname = userDetails['Surname']
        Email = userDetails['Email']
        Password = userDetails['Password']
        ConfirmPassword = userDetails['ConfirmPassword']
       
        data = request.get_json()
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(Name,Surname,Email,Password,ConfirmPassword) VALUES(%s, %s, %s, %s, %s)", (Name,Surname,Email,Password,ConfirmPassword))
        mysql.connection.commit() 
        cur.close()
        return 'great success'
        

@app.route("/login", methods =['POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        Email = userDetails['Email']
        Password = userDetails['Password']
        data = request.get_json()
        
        cur = mysql.connection.cursor()
        count = cur.execute('select * from users where Email=%s and Password=%s', (Email,Password)) 
        mysql.connection.commit() 
        cur.close()
        if count == 0:
            return "Okay"
        else:
            return "User exist"  


@app.route("/list", methods = ['GET'])
def itemlist():
    fields = ("KitNo","PickListNo","Station","Kitter","UniqueNo","ItemNo","ItemDescription","Quantity","Location","SerialNo")
    info = {}
    items = []
    with open (r"item2.csv","r") as file:
        reader = csv.DictReader( file, fields)
        for row in reader:
            break

        for row in reader:
            info["KitNo"] = row["KitNo"]
            info["PickListNo"] = row["PickListNo"]
            info["Station"] = row["Station"]
            info["Kitter"] = row["Kitter"]
            info["UniqueNo"] = row["UniqueNo"]
            

            

            items.append({"number" : row["ItemNo"] ,
                "description" : row["ItemDescription"] ,
                "quantity" : row["Quantity"] ,
                "location" : row["Location"]})
        
        info["items"]= items

        #with open("jsonFilename", 'w', encoding = 'utf-8') as jsonfile:  
        return json.dumps(info, indent = 4)  
            

if __name__ == '__main__':
    app.run(debug = True )    