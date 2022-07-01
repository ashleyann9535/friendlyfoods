import re
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
@app.route('/update/food/<int:id>' , methods = ['POST', 'GET'])
def update_food(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if request.method == 'GET':
        this_food = food.Food.view_food(id)
        return render_template('update_food.html', this_food = this_food)
    if food.Food.update_food(request.form) == False:
        return redirect(f'/update/food/{id}')
    else:
        food.Food.update_food(request.form)
        return redirect('/user/profile')
#Delete 