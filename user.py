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

@app.route("/items_picked", methods =['POST'])
def items_picked():
    if request.method == 'POST':
        userDetails = request.form
        datas = request.get_json()
        csvfilename=datas[0]["PickListNo"] + "done" + ".csv"
    
        for data in datas[0]["items"] :
            data["ItemNo"] = data.pop("number")
            data["ItemDescription"] = data.pop("description")
            data["Quantity"] = data.pop("quantity")
            data["Location"] = data.pop("location")
            data["KitNo"] = datas[0]["KitNo"]
            data["PickListNo"] = datas[0]["PickListNo"]
            data["Station"] = datas[0]["Station"]
            data["Kitter"] = datas[0]["Kitter"]
            data["UniqueNo"] = datas[0]["UniqueNo"]
        fields = ("KitNo","PickListNo","Station","Kitter","UniqueNo","ItemNo","ItemDescription","Quantity","Location","quantity_picked")

        with open (csvfilename,"w") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for data in datas[0]["items"]:
                writer.writerow(data)
        return json.dumps("done")


@app.route("/list", methods = ['GET'])
def itemlist():
    fields = ("KitNo","PickListNo","Station","Kitter","UniqueNo","ItemNo","ItemDescription","Quantity","Location","SerialNo")
    info = {}
    items = []
    data = []
    csvfilename = request.args.get("csvfilename") + ".csv"
    try:
        with open (csvfilename,"r") as file:
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
        print(json.dumps([info], indent = 4))
        return json.dumps([info], indent = 4) 
        
    except FileNotFoundError :
        return ('' , 400)          

if __name__ == '__main__':
    app.run(host="10.160.0.3" , debug = True )    
