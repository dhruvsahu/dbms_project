import mysql.connector
from flask import Flask, request, session, render_template,redirect

import os

sql_pass = os.environ['sql_pass']

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/',methods=['GET', 'POST'])
def renderLoginPage():
    events = runQuery("SELECT * FROM events")
    return render_template('index.html',events = events)
    


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
                return redirect('/select')

        return render_template('admin.html',errors=["Wrong Username/Password"])

    return render_template('admin.html')    

@app.route('/events_info',methods=['GET','POST'])
def renderEventsInfo():
    events = runQuery("SELECT * FROM events where Approval_Status=\"Approved\";")
    return render_template('events_info.html',events = events)

@app.route('/select',methods=['GET','POST'])
def renderSelect():
    if request.method == 'POST':
        if request.form['action'] == 'meetings':
            return redirect('/meetings')
        elif request.form['action'] == 'events':
            return redirect('/events')
        else:
            return "Invalid action"
    
    return render_template('select.html')

@app.route('/meetings',methods=['GET','POST'])
def renderMeetings():
    meets = runQuery("SELECT * FROM roombooking;")

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
            if "EventId" in request.form and "approve_button" in request.form:
                EventId = request.form["EventId"]
                runQuery("UPDATE events SET approval_status = 'Approved' WHERE event_id = {}".format(EventId))
            elif "EventId" in request.form and "reject_button" in request.form:
                EventId = request.form["EventId"]
                runQuery("DELETE from events WHERE event_id = {}".format(EventId))
                runQuery("SELECT * FROM events;")
            return render_template('meetings.html',meets = meets)
            

    return render_template('meetings.html',meets = meets)


@app.route('/clubLogin',methods=['GET','POST'])
def renderClub():
    if request.method == 'POST':
        UN = request.form['username']
        PS = request.form['password']

        cred = runQuery("SELECT * FROM club")
        print(cred)
        for user in cred:
            if UN==user[1] and PS==user[2]:
                session['username'] = UN
                return redirect('/club')

        return render_template('clubLogin.html',errors=["Wrong Username/Password"])

    return render_template('clubLogin.html')

@app.route('/events',methods=['GET','POST'])
def getEvents():
    events = runQuery("SELECT * FROM events;")

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
            if "EventId" in request.form and "approve_button" in request.form:
                EventId = request.form["EventId"]
                runQuery("UPDATE events SET approval_status = 'Approved' WHERE event_id = {}".format(EventId))
            elif "EventId" in request.form and "reject_button" in request.form:
                EventId = request.form["EventId"]
                runQuery("DELETE from events WHERE event_id = {}".format(EventId))
                runQuery("SELECT * FROM events;")
            return render_template('events.html',events = events)
            

    return render_template('events.html',events = events)


@app.route('/club',methods=['GET','POST'])
def renderClubPage():
    if request.method == 'POST':
        if request.form['action'] == 'showRequests':
            return redirect('/showRequests')
        elif request.form['action'] == 'registerEvent':
            return redirect('/registerEvent')
        elif request.form['action'] == 'bookroom':
            return redirect('/bookroom')
        else:
            return "Invalid action"
    return render_template('club.html')

@app.route('/showRequests',methods=['GET','POST'])
def renderRequest():
    username = session['username']
    events = runQuery("SELECT * FROM events WHERE Club_Name = \'{}\';".format(username))
    rooms = runQuery("SELECT * FROM roombooking WHERE Club_Name = \'{}\';".format(username))
    return render_template('showRequests.html',events = events, rooms = rooms)

@app.route('/registerEvent',methods=['GET','POST'])
def renderRegisterEvent():
    if request.method=="POST":
        EventName=request.form["EventName"]
        ClubName=request.form["ClubName"]
        Date=request.form["Date"]
        StartTime=request.form["StartTime"]
        EndTime=request.form["EndTime"]
        Venue=request.form["Venue"]
        RegistrationFee=request.form["RegistrationFee"]
        Description=request.form["EventDescription"]
        runQuery("call insert_event(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{},\'{}\');".format(EventName,ClubName,Date,StartTime,EndTime,Venue,RegistrationFee,Description))
        return render_template('registerEvent.html',errors=["Event Registered Successfully!"])

    return render_template('registerEvent.html')

@app.route('/bookroom',methods=['GET','POST'])
def renderBookRoom():
    if request.method=="POST":
        ClubName=request.form["ClubName"]
        Room=request.form["roomno"]
        Date=request.form["Date"]
        StartTime=request.form["StartTime"]
        EndTime=request.form["EndTime"]
        AcadBlock=request.form["Venue"]
        Description=request.form["Description"]
        runQuery("call insert_roombooking(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');".format(ClubName,AcadBlock,Room,Date,StartTime,EndTime,Description))
        return render_template('bookroom.html',errors=["Room Booked Successfully!"])

    return render_template('bookroom.html')



def runQuery(query):

    try:
        db = mysql.connector.connect( host='localhost',database='dbmsproj',user='root',password=sql_pass)

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
