from flask import Flask, render_template, redirect, request 
from dateutil import parser
from flask_mail import Mail, Message 
import os
from flask_wtf import FlaskForm
from wtforms import StringField
import smtplib


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your mail server
app.config['MAIL_PORT'] =  587  # Replace with the appropriate port number
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nickaj1505@gmail.com'  # Replace with your email address
app.config['MAIL_PASSWORD'] = 'kuzkbotyaygqpden' # Replace with your email password or app password
# app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

                                    #  [HOME]
@app.route('/' , methods = ['GET','POST'])
def home():
    if request.method == "GET":
        return render_template('home.html')
    else:
        print('found') 
        reservered = {
                '1 Bedroom': ['05/26/2023','05/25/2023','06/05/2023','06/01/2023','05/27/2023','05/28/2023','05/29/2023','05/30/2023','05/31/2023'],
                'Queensize': ['05/29/2023','05/30/2023','05/31/2023'],
                'Kingsize': ['06/02/2023','06/01/2023','06/03/2023','06/04/2023'],
                'Executive Bedroom': ['06/05/2023','06/06/2023']
        }
        calander =   request.form['Date2']
        calander2 =   request.form['Date1']
        room = request.form['room']

        for each in reservered.keys():
            if room == each:
                print(calander, calander2)
                if calander in reservered[room] or calander2 in reservered[room]:
                    return render_template('home.html', Errormessage='Room not available')
                else: 
                 return redirect('/booking')
                

            else:
                return render_template('error_page.html')
                    

                    # return reservered

                    # [BOOK]
@app.route('/booking', methods = ['GET','POST'])
def booking():
    if request.method == "GET":
       return render_template('booking.html')
    
    else:
        prices = {
            '1 Bedroom': [550,500],
            'Queensize': [750,700],
            'Kingsize': [950,900],
            'Executive':[1500,1300]
        }
        
        bed1 = request.form['bed1']
        bed2 = request.form['bed2']
        queen1 = request.form['queen1']
        queen2 = request.form['queen2']
        king1 = request.form['king1']
        king2 = request.form['king2']
        exe1 = request.form['exe1']
        exe2 = request.form['exe2']

        rooms = [bed1,bed2,queen1,queen2,king1,king2,exe1,exe2]

        for each in rooms:
            if each:
                return render_template('home.html', success = True) 
    
         
        


                         #[ROOM]
@app.route('/rooms', methods = ['GET','POST'])
def rooms():
    if request.method == "GET":
        return render_template('rooms.html')
    
    else:
        print('found')
        rooms = ['1 Bedroom','Queensize Bedroom','Kingsize Bedroom','Executive  Bedroom']
        dropdown = request.form['dropdown']
        for room in rooms:
            if dropdown in room:
                return render_template('booking.html')
            else:
                return redirect('/home.html')





                              #[RESERVATION]
@app.route('/reservation', methods = ['GET','POST'])
def reservation():
    if request.method == "GET":
        return render_template('reservation.html')
    


                               #[CONTACT]
@app.route('/contact', methods = ['GET','POST'])
def contact():
    if request.method == "GET":
        return render_template('contact.html')
    else:
       fname = request.form['fname']
       lname = request.form['lname']
       email = request.form['email']
       message = request.form['message']

       user = [fname,lname]

       msg = Message(subject=f"Mail from {user}", body=f"First_name: {fname}\n Last_name: {lname}\n E-mail: {email}\n\n\n{message}", sender=email, recipients=['nickaj1505@gmail.com'])
       mail.send(msg)
       return render_template('contact.html', success=True)
    
    

    



                                 #[ABOUT-US]
@app.route('/about-us', methods = ['GET','POST'])
def about_us():
    if request.method == "GET":
        return render_template('about-us.html')
    
    else:
        return redirect('/reviews')
    

                                   #[REVIEWS]
@app.route('/reviews', methods = ['GET','POST'])
def reviews():
    if request.method == "GET":
        return render_template('home.html')



if '__name__' == '__main__':
    app.run(host = '0.0.0.0', debug = True)
