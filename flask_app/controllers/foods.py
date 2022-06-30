from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import food

# put in routes


#Create 
@app.route('/add/food', methods = ['GET', 'POST'])
def add_food():
    if 'user_id' not in session:
        return redirect('/')
    if request.method == 'GET':
        return render_template('add_food.html')
    if food.Food.create_food(request.form):
        return redirect('/user/profile')
    return redirect('/add/food')

#Read 



#Update 


#Delete 