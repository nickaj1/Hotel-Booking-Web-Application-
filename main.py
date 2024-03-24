from flask import Flask, render_template, redirect, request , jsonify, flash, url_for
from dateutil import parser
from flask_mail import Mail, Message
import os
# from flask_wtf import FlaskForm
# from wtforms import StringField
import smtplib
from flask_pymongo import PyMongo
from bson import ObjectId
from pymongo import UpdateOne
from datetime import datetime 
import secrets
from dotenv import load_dotenv





load_dotenv()
app = Flask(__name__)
                                        #    [FLASK MAIL]
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')  # Replace with your mail server
app.config['MAIL_PORT'] = (os.getenv('MAIL_PORT'))  # Replace with the appropriate port number
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Replace with your email address
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') # Replace with your email password or app password
mail = Mail(app)

                                        #  [DATABASE FLASK]
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)
 
#  [FLASH ERROR]
app.secret_key = secrets.token_hex(16) 

                                    #  [HOME]
@app.route('/' , methods = ['GET','POST'])
def home():
    if request.method == "GET":

        rooms = mongo.db.rooms
    
        getdb = rooms.find()
        output = []

        # for j in getdb:
        #     try:
        #         new = {'roomid':str(j['_id']),'check_out':str(j.get('Check_out'))}
        #         output.append(new)
        #     except Exception as e:
        #         print(e)

        # for i in output:
        #     print(i)
        #     try:
        #         update = (datetime.today() - datetime.strptime(i['Check_out'],'%m/%d/%Y')).days
        #         if update >= 0:
        #             mongo.db.rooms.update_one({'_id':ObjectId(i['roomid'])}, {'$set' : {'Status': 'Available'}})
        #         else:
        #             print('less')
                    
        #     except Exception as e:
        #         print(i['roomid'])
            
        # return render_template('home.html')


        for i in getdb:
            new = {'roomid':str(i['_id']),'check_out':str(i.get('Check_out'))}
            output.append(new)
            print(output[0])

            if i.get('Check_out') != None:
                update = (datetime.today() - datetime.strptime(str(i.get('Check_out')),'%Y-%m-%d %H:%M:%S')).days
                print(update)

                if update >= 0:
                    mongo.db.rooms.update_one({'_id':ObjectId(i['_id'])}, {'$set' : {'Status': 'Available'}})
                
                else:
                    print('less')
        
        return render_template('home.html')








    
    else: 

        room = request.form['room']

        # Accessing document in the database 
        rooms = mongo.db.rooms

        # Querying for each room detail in the database
        dbrooms = rooms.find({'Rooms':room})

        

        pictures = {'Single Bedroom':'/static/image/1bedroom.jpg',
                    'Queensize Bedroom':'/static/image/queensize.jpg',
                    'Kingsize Bedroom':'/static/image/kingsize.jpg',
                    'Executive Bedroom':'/static/image/executive.jpg',
                    }

        result = []

        for i in dbrooms:
            if i['Status'] == 'Available':
                x = {'roomid':str(i['_id']), 'price':i['Price'], 'status':i['Status'].strip(), 'image':pictures[i['Rooms']]}
                result.append(x)  
            
            
            if result == '':
               return render_template('error_page.html' )

        # try:

        #     if update >= 0:
        #        mongo.db.rooms.update_one({'_id':ObjectId(i['_id'])}, {'$set' : {'Status': 'Available'}})
            
        # except Exception as e:
        #     pass 
        
        return jsonify({'dbresults':result})

         


        # for each in reservered.keys():
        #     if room == each:
        #         print(calander, calander2)
        #         if calander in reservered[room] or calander2 in reservered[room]:
        #             return render_template('home.html', Errormessage='Room not available')
                     

        #     else:
        #         return render_template('error_page.html')
                    

                    # return reservered

                    # [BOOK]
@app.route('/booking', methods = ['GET','POST'])
def booking():
    if request.method == "GET":
       selected_room = request.args.get('q')  # Get the room id from the query parameter

     # Pass the selected_room which contains the id to the obj_id
       rooms = mongo.db.rooms
       selected_room_id = rooms.find({'_id': ObjectId(selected_room)})
       print('Room found.')
       
       # Accessing a list of db result index and key
       x = selected_room_id[0]['Rooms']

       

       if x == 'Single Bedroom':
          return render_template('1bedroom.html',selected_room=selected_room,)
       elif x == 'Queensize Bedroom':
          return render_template('queen_bedroom.html', selected_room=selected_room)
       elif x == 'Kingsize Bedroom':
          return render_template('king_bedroom.html', selected_room=selected_room)
       elif x == 'Executive Bedroom':
          return render_template('exe_room.html', selected_room=selected_room)
      # Add more conditions for other room types
       else:
          return render_template('error_page.html')  # Handle invalid room selection
       
    
        
    else:
        # Accessing document in the database 
        rooms = mongo.db.rooms

        data = request.get_json()
        calander = data['date1']
        calander2 = data['date2']
        selected_room = data['selected_room']
        fname = data['fname']
        lname = data['lname']
        cardName = data['cardName']
        cardNum = data['cardNum']
        email = data['email']


        getdb = rooms.find({'_id':ObjectId(selected_room)})
        result = []

        date = datetime.today()
        first_cal = datetime.strptime(calander, "%m/%d/%Y")

        for i in getdb:
           new = {'roomid':str(i['_id']),'room':i['Rooms'] ,'check_in': str(i.get('Check_in')), 'check_out': str(i.get('Check_out'))}
           result.append(new)

            # update = (result[0]['Check_in'] - result[0]['Check_out']).days
            # update = (parser.parse(calander, dayfirst=False) -  parser.parse(calander2, dayfirst=False)).days
        
            # Do something with the data, like updating the database 
           if first_cal != '' and calander2 != '':   
                # current = parser.parse(calander, dayfirst=False) == datetime.now().day
                
               # Check for current date if its equal to the first calander intake [Check_in] date
                if first_cal.date() >= date.date(): 
                
                 # If it matches calculate the days between both calander intake [Check_in] and [Check_out] date
                    update =  (parser.parse(calander2, dayfirst=False) - parser.parse(str(first_cal), dayfirst=False)).days
                    update  # Output returns a negative number. however, assign exponentiation ** to set output to positive 0
                    print('update:', update)
         
                 # Setting a limit for amount of days a user can select
                    if update <= 1:
                        print('less than 1')
                    
                        if fname != '' and lname != '' and cardName != '' and cardNum != '' and email != '':           
                             mongo.db.rooms.update_one({'_id': ObjectId(selected_room)}, 
                             {'$set':{'Check_in': first_cal, 'Check_out': datetime.strptime(calander2, '%m/%d/%Y'),
                                'Status': 'Not Available', 'First Name':fname, 'Last Name':lname, 'Card Name': cardName, 'Card Number': str(cardNum), 'Email': email}})
                             print('You\'ve succefully Booked')
                             return jsonify({'alert': 'You\'ve succefully Booked'})
                        else:
                            return jsonify({'alert':'Enter the right details'}) 

                    else:
                        print('You can not choose more than one day')
                        return jsonify({'alert':'You can not choose more than one day'})
                    
                else:
                    print('Select the right date')
                    return jsonify({'alert':'You can not choose more than one day'})

           else:
               return jsonify({'alert':'Select the right date'})
       
        return jsonify({'dbresults': str(result)})
    
        
        

        # (datetime.today() - parser.parse('', dayfirst=True)).days
                #  (parser.parse(calander, dayfirst=True) -  parser.parse(calander2, dayfirst=True))
        # for i in dbdate:
        #    output = {'Check_in':i['Check_in'], 'Check_out':i['Check_out']}
        #    result = []
        #    result.append(output)

        # selected_room_id = rooms.find({'_id': ObjectId(selected_room)})
        # print(selected_room_id)
        # dbrooms = rooms.update_many({'_id': ObjectId(selected_room)}, {'$set': {'Check_In': date(calander),'Check_Out': date(calander2)}}, return_document= True)

        # if dbrooms:
        #    return jsonify('Document updated successfully:', dbrooms)
        
        # results = []
        # for i in dbrooms:
        #     y = {'roomid':str(i['_id']), 'price':i['Price'], 'status':i['Status'], 'check_in':calander[i['Check_in']], 'check_out':calander2[i['Check_out']]}
        #     results.append(y)
        #     print(results)
        #     return jsonify({'dbresults':results})
       


       

        # calander =   request.get_json()['date1']
        # calander2 =   request.get_json()['date2']
        # selected_room = request.args.get('selected_room')
        


        

    

                         #[ROOM]
@app.route('/rooms', methods = ['GET','POST'])
def rooms():
    if request.method == "GET":
        return render_template('rooms.html')
    
    else:
        print('found')
        rooms = ['Single Bedroom','Queensize Bedroom','Kingsize Bedroom','Executive  Bedroom']
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
        about = request.form['about']

        if about:
            redirect('/reviews')
    

                                   #[REVIEWS]
@app.route('/reviews', methods = ['GET','POST'])
def reviews():
    if request.method == "GET":
        return render_template('reviews.html')
    
    else:
        review_data = request.json()

    # Validate and store the review
        if 'title' in review_data and 'text' in review_data and 'rating' in review_data:
            review = {
                'title': review_data['title'],
                'text': review_data['text'],
                'rating': review_data['rating']
            }
            reviews.append(review)
            return jsonify({'message': 'Review submitted successfully'})
        else:
            return jsonify({'error': 'Invalid review data'}), 400




if '__name__' == '__main__':
    app.run(host = '0.0.0.0', debug = True)
