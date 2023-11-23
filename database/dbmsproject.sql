CREATE DATABASE dbmsproj;
USE dbmsproj;



CREATE TABLE admin(
Username varchar(100) NOT NULL,
Password varchar(100) NOT NULL
);

INSERT INTO admin VALUES
('Admin1','password1'),
('Admin2','password2');




CREATE TABLE club(
Club_ID int primary key auto_increment, 
Name varchar(100), 
password varchar(100), 
email varchar(100), 
contact bigint(10) unsigned )
auto_increment=1001;

INSERT INTO Club(Name, password, email, contact) VALUES
    ("Entrepreneurship Cell","ecell123", "ecell@snu.edu.in",9045982085),
    ("Inferno","inferno123","inferno@snu.edu.in",8374345644),
    ("Feeding India","feedingindia123","teamfeedingindia@snu.edu.in",8730295874),
    ("Snuphoria","snuphoria123","snuphoria@snu.edu.in",9840058938),
    ("Metanoia","metanoia123","metanoia@snu.edu.in",6800887933);


CREATE TABLE events 
(Event_ID int primary key auto_increment,
Name varchar(100),
Club_Name varchar(100),
Date date,
Start_Time Time,
End_Time Time,
Venue varchar(100),
Registration_Fee int,
Description varchar(100),
Approval_Status varchar(100) DEFAULT "PENDING");





CREATE TABLE roombooking
(Booking_ID int primary key auto_increment,
Club_Name varchar(100),
Acad_Block varchar(2),
Room_No int,
Date date,
Start_Time Time,
End_Time Time,
Description varchar(100),
Approval_Status varchar(100) DEFAULT "PENDING"
)auto_increment=1001;



CREATE TABLE booking
(Booking_ID int primary key auto_increment, 
Club_Name varchar(100), 
Date date, 
Start_Time Time, 
End_Time Time, 
purpose varchar(100),
Approval_Status varchar(100) DEFAULT "PENDING",
Last_Update Time);


delimiter //
CREATE TRIGGER roombookinginfo
AFTER INSERT on roombooking
FOR EACH ROW
BEGIN
INSERT INTO booking(Club_Name,Date,Start_Time,End_Time,purpose,Last_Update) VALUES
(new.Club_Name,new.Date,new.Start_Time,new.End_Time,"Room Booking",CURTIME());
END //

delimiter ;



delimiter //
CREATE TRIGGER eventinfo
AFTER INSERT on events
FOR EACH ROW
BEGIN
INSERT INTO booking(Club_Name,Date,Start_Time,End_Time,purpose,Last_Update) VALUES
(new.Club_Name,new.Date,new.Start_Time,new.End_Time,"Event",CURTIME());
END //

delimiter ;




delimiter //

CREATE TRIGGER delinfo
AFTER UPDATE on events
FOR EACH ROW
BEGIN 
IF new.Approval_Status = "Rejected" THEN
UPDATE booking SET Approval_Status = "Rejected" AND Last_Update = CURTIME() WHERE Booking_ID = new.Event_ID;
END IF;
END //
delimiter ;

delimiter //

CREATE TRIGGER addinfo
AFTER UPDATE on events
FOR EACH ROW
BEGIN 
IF new.Approval_Status = "Approved" THEN
UPDATE booking SET Approval_Status = "Approved" AND Last_Update = CURTIME() WHERE Booking_ID = new.Event_ID;
END IF;
END //
delimiter ;



INSERT INTO events(Name,Club_Name, Date, Start_Time,End_Time) VALUES
    ("Mindspark","Entrepreneurship Cell","2023-01-1","17:30","20:30"),
    ("Impressions","Inferno","2022-12-21","15:00","18:00"),
    ("Zest","Snuphoria","2023-02-01","17:00","19:00"),
    ("RE-INIT","Metanoia","2022-11-05","18:30","19:30"),
    ("FlossMeet","Snuphoria","2023-04-11","17:00","19:00"),
    ("Spandan","Feeding India","2022-11-03","11:00","13:00");




Delimiter //

CREATE PROCEDURE insert_event( N varchar(100), CName varchar(100), D date, STime Time, ETime Time, V varchar(100), RegFee int, Des varchar(100))
BEGIN
INSERT INTO events(Name, Club_Name, Date, Start_Time,End_Time,Venue,Registration_Fee,Description)  values(N,CName,D,STime,ETime,V,RegFee,Des);
END //

Delimiter ;




Delimiter //

CREATE PROCEDURE insert_roombooking(CName varchar(100), Block varchar(2), RNo int, D date, STime Time, ETime Time, Des varchar(100))
BEGIN
INSERT INTO roombooking(Club_Name, Acad_Block, Room_No, Date, Start_Time,End_Time,Description) values(CName,Block,RNo,D,STime,ETime,Des);
END //

Delimiter ;