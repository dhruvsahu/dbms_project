# ClubHub

## Overview

This repository contains the source code for an Event Management System developed using Python (Flask) and MySQL. The system allows administrators, clubs, and users to manage and participate in events, book rooms, and handle administrative tasks.

## Features

1. **User Registration and Authentication:**
   - Users can register and authenticate using a username and password.
   - Two types of users: Admin and Club Members.

2. **Event Management:**
   - Admins and Club Members can create and manage events.
   - Events have details such as date, time, venue, registration fee, and approval status.

3. **Room Booking:**
   - Club Members can book rooms for various purposes.
   - Room bookings include details like date, time, venue, and approval status.

4. **Admin Panel:**
   - Admins have access to an admin panel where they can view and manage events and room bookings.

5. **Club Management:**
   - Clubs have dedicated login functionality and can manage their club-specific events and room bookings.

## ER Diagram
![ER-Diagram](https://github.com/dhruvsahu/dbms_project/assets/140328175/f02a69d2-3e57-441d-88fb-0da0244dc61f)

## Installing Dependencies

```
$ pip install -r requirements.txt
```

## Usage

- **Home Page:** View available events and room bookings.
- **Admin Panel:** Manage events, room bookings, and handle administrative tasks.
- **Club Members:** Manage club-specific events, room bookings, and participant registrations.
- **Event Registration:** Users can register for events with relevant details.
- **Validation:** System performs checks for mobile numbers, email formats, and registration availability.
- **Room Booking:** Club members can book rooms; requests undergo an approval process.
- **Admin Approval:** Admins can approve or reject event registrations and room booking requests.

## Database Structure

The database structure is defined by the SQL script (`dbmsproj.sql`). Key tables include:

- **`admin` Table:** Contains credentials for system administrators.
- **`club` Table:** Stores information about different clubs.
- **`events` Table:** Details of events organized by clubs.
- **`roombooking` Table:** Information about room bookings.
- **`booking` Table:** Records general booking information.

These tables are interconnected to manage events, participants, room bookings, and approvals in the system.