# About the project
A Django based event management portal along with REST API. Has the following features
* User registartion, Changing password and accessing the user data in read only mode
* Event creation (submiting a request to the admin)
* Display list of approved events, past events and all user generated events in appropriate sorting orders 
* Admin panel with the option to approve/disprove/add/delete and edit events, users and user groups
* History of events, feedback collection and showing a consolidated feedback set to the event creator
* Polling feature for people coming/not-coming and people who are undecided
* REST API for programmatic access

## What this project doesn't contain
Due to time constraints or unfeasibility of the feature for this level of app, the following features aren't implemented and should be kept in mind:
* Strict HTTPS policy
* Secure login for REST API
* Displaying the base64 image input that can be submitted/retrieved via the API
* Rate limiting in the API
* Automatic management of the event venues (booked/available/under-mantainance/restricted-access etc)

# Info particular to this repo
* Stable and database included
* No migrations needed, just install from the pipfile and start using
* login with username = admin and password = admin (the login page asks for email, it's a typo, just enter the username)
* when creating a new user the email needs to be (username)@iitg.ac.in, (username) will be the username needed for login
* This includes no gitignore so do not send any pull requests, this repo is only for forking/cloning
