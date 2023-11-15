import mysql.connector,sys
import datetime
from mysql.connector import Error
from flask import Flask, request, jsonify, render_template,redirect, url_for
from random import randint


app = Flask(__name__)


@app.route('/',methods=['GET', 'POST'])
def renderLoginPage():
    events = runQuery("SELECT * FROM events")
    branch =  runQuery("SELECT * FROM branch")
    if request.method == 'POST':
        Name = request.form['FirstName'] + " " + request.form['LastName']
        Mobile = request.form['MobileNumber']
        Branch_id = request.form['Branch']
        Event = request.form['Event']
        Email = request.form['Email']

        if len(Mobile) != 10:
            return render_template('loginfail.html',errors = ["Invalid Mobile Number!"])

        if Email[-4:] != '.com':
            return render_template('loginfail.html', errors = ["Invalid Email!"])

        if len(runQuery("SELECT * FROM participants WHERE event_id={} AND mobile={}".format(Event,Mobile))) > 0 :
            return render_template('loginfail.html', errors = ["Student already Registered for the Event!"])

        if runQuery("SELECT COUNT(*) FROM participants WHERE event_id={}".format(Event)) >= runQuery("SELECT participants FROM events WHERE event_id={}".format(Event)):
            return render_template('loginfail.html', errors = ["Participants count fullfilled Already!"])

        runQuery("INSERT INTO participants(event_id,fullname,email,mobile,college,branch_id) VALUES({},\"{}\",\"{}\",\"{}\",\"COEP\",\"{}\");".format(Event,Name,Email,Mobile,Branch_id))

        return render_template('index.html',events = events,branchs = branch,errors=["Succesfully Registered!"])

    return render_template('index.html',events = events,branchs = branch)
    


@app.route('/loginfail',methods=['GET'])
def renderLoginFail():
    return render_template('loginfail.html')


@app.route('/admin', methods=['GET', 'POST'])
def renderAdmin():
    if request.method == 'POST':
        UN = request.form['username']
        PS = request.form['password']

        cred = runQuery("SELECT * FROM admin")
        print(cred)
        for user in cred:
            if UN==user[0] and PS==user[1]:
                return redirect('/eventType')

        return render_template('admin.html',errors=["Wrong Username/Password"])

    return render_template('admin.html')    

@app.route('/clubLogin',methods=['GET','POST'])
def renderClub():
    if request.method == 'POST':
        UN = request.form['username']
        PS = request.form['password']

        cred = runQuery("SELECT * FROM club")
        print(cred)
        for user in cred:
            if UN==user[0] and PS==user[1]:
                return redirect('/eventinfo')

        return render_template('club.html',errors=["Wrong Username/Password"])

    return render_template('clubLogin.html')

@app.route('/eventType',methods=['GET','POST'])
# def getEvents():
#     eventTypes = runQuery("SELECT *,(SELECT COUNT(*) FROM participants AS P WHERE T.type_id IN (SELECT type_id FROM events AS E WHERE E.event_id = P.event_id ) ) AS COUNT FROM event_type AS T;") 

#     events = runQuery("SELECT event_id,event_title,(SELECT COUNT(*) FROM participants AS P WHERE P.event_id = E.event_id ) AS count FROM events AS E;")

#     types = runQuery("SELECT * FROM event_type;")

#     location = runQuery("SELECT * FROM location")


#     if request.method == "GET":
#         try:
#             Name = request.form["newEvent"]
#             fee=request.form["Fee"]
#             participants = request.form["maxP"]
#             Type=request.form["EventType"]
#             Location = request.form["EventLocation"]
#             Date = request.form['Date']
#             # UPDATE events SET approval_status = "Approved" WHERE event_id = 1;
#             # runQuery("UPDATE events SET approval_status = \"Approved\" WHERE event_id = {}".format(EventId))
#             runQuery("INSERT INTO events(event_title,event_price,participants,type_id,location_id,date) VALUES(\"{}\",{},{},{},{},\'{}\');".format(Name,fee,participants,Type, Location,Date))

#         except:
#             EventId=request.form["EventId"]
#             runQuery("UPDATE events SET approval_status = \"Approved\" WHERE event_id = {}".format(EventId))
# #     print("Hello")
# #     flag = ""
# #     if request.method == 'POST':
# #         event_id = request.args.get('EventId')  # Get the selected event ID
# #         if request.form['action'] == 'Approve':
# #             # Handle the Approve action here
# #             # Perform actions for approval
# #             # return f"Event {event_id} approved"
# #             print("Hello")
# #             flag = "Approved"
# #             runQuery("UPDATE events SET approval_status = \"Approved\" WHERE event_id = {}".format(event_id))
# #         elif request.form['action'] == 'Reject':
# #             # Handle the Reject action here
# #             # Perform actions for rejection
# #             # return f"Event {event_id} rejected"
# #             print("Hello")
# #             flag = "Rejected"
# #             runQuery("UPDATE events SET approval_status = \"Rejected\" WHERE event_id = {}".format(event_id))
#     return render_template('events.html',events = events,eventTypes = eventTypes,types = types,locations = location) 
def getEvents():
    eventTypes = runQuery("SELECT *,(SELECT COUNT(*) FROM participants AS P WHERE T.type_id IN (SELECT type_id FROM events AS E WHERE E.event_id = P.event_id ) ) AS COUNT FROM event_type AS T;") 
    events = runQuery("SELECT event_id,event_title,(SELECT COUNT(*) FROM participants AS P WHERE P.event_id = E.event_id ) AS count FROM events AS E;")
    types = runQuery("SELECT * FROM event_type;")
    location = runQuery("SELECT * FROM location")

    if request.method == "POST":
        try:
            Name = request.form["newEvent"]
            fee=request.form["Fee"]
            participants = request.form["maxP"]
            Type=request.form["EventType"]
            Location = request.form["EventLocation"]
            Date = request.form['Date']
            runQuery("INSERT INTO events(event_title,event_price,participants,type_id,location_id,date) VALUES(\"{}\",{},{},{},{},\'{}\');".format(Name,fee,participants,Type, Location,Date))

        except:
            # Handling the Approve functionality
            if "EventId" in request.form and "approve_button" in request.form:
                EventId = request.form["EventId"]
                runQuery("UPDATE events SET approval_status = 'Approved' WHERE event_id = {}".format(EventId))
            # Handling the Reject functionality
            elif "EventId" in request.form and "reject_button" in request.form:
                EventId = request.form["EventId"]
                runQuery("DELETE from events WHERE event_id = {}".format(EventId))

    return render_template('events.html',events = events,eventTypes = eventTypes,types = types,locations = location) 

@app.route('/eventinfo')
def rendereventinfo():
    events=runQuery("SELECT *,(SELECT COUNT(*) FROM participants AS P WHERE P.event_id = E.event_id ) AS count FROM events AS E LEFT JOIN event_type USING(type_id) LEFT JOIN location USING(location_id) WHERE approval_status =\"Approved\";")

    return render_template('events_info.html',events = events)

@app.route('/participants',methods=['GET','POST'])
def renderParticipants():
    
    events = runQuery("SELECT * FROM events;")

    if request.method == "POST":
        Event = request.form['Event']

        participants = runQuery("SELECT p_id,fullname,mobile,email FROM participants WHERE event_id={}".format(Event))
        return render_template('participants.html',events = events,participants=participants)

    return render_template('participants.html',events = events)

@app.route('/showRequests',methods=['GET','POST'])
def renderRequest():

    return render_template('showRequests.html')

@app.route('/registerEvent',methods=['GET','POST'])
def renderRegisterEvent():

    return render_template('registerEvent.html')

@app.route('/bookroom',methods=['GET','POST'])
def renderBookRoom():
    if request.method=="POST":
        ClubName=request.form["ClubName"]
        Room=request.form["roomno"]
        Date=request.form["Date"]
        StartTime=request.form["StartTime"]
        EndTime=request.form["EndTime"]
        Purpose=request.form["Purpose"]
        runQuery("INSERT INTO room_booking(room_id,date,time,purpose) VALUES({},\'{}\',\'{}\',\'{}\');".format(Room,Date,Time,Purpose))
        return render_template('bookroom.html',errors=["Room Booked Successfully!"])

    return render_template('bookroom.html')


def runQuery(query):

    try:
        db = mysql.connector.connect( host='localhost',database='dbms2023',user='root',password='India2017@')

        if db.is_connected():
            print("Connected to MySQL, running query: ", query)
            cursor = db.cursor(buffered = True)
            cursor.execute(query)
            db.commit()
            res = None
            try:
                res = cursor.fetchall()
            except Exception as e:
                print("Query returned nothing, ", e)
                return []
            return res

    except Exception as e:
        print(e)
        return []

    db.close()

    print("Couldn't connect to MySQL")
    return None


if __name__ == "__main__":
    app.run() 
