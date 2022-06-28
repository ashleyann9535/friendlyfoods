from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session


# make class, class methods with SQL, and logic
class Food:
    db = 'gf_df_foods '

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.location = data['location']
        self.gluten_free = data['gluten_free']
        self.dairy_free = data['dairy_free']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None


#Create 
    @classmethod
    def create_food(cls, data):
        if not cls.validate_food(data):
            return False
        query = """
        INSERT INTO foods(name, description, location, gluten_free, dairy_free, user_id)
        VALUES (%(name)s, %(description)s, %(location)s, %(gluten_free)s, %(dairy_free)s, %(user_id)s)
        ;"""

        food_id = connectToMySQL(cls.db).query_db(query, data)

        return food_id

#Read 


#Update 


#Delete 

#Validate 
    @staticmethod
    def validate_food(data):
        is_valid = True
        if not data['name']:
            flash('Please give a name to the food', 'create_food')
            is_valid = False
        if not data['location']:
            flash('Please add the place the food can be found', 'create_food')
            is_valid = False
        if not data['description']:
            flash('Please let us about the food', 'create_food')
            is_valid = False
        if not data['gluten_free']:
            flash('Is the food gluten free?', 'create_food')
            is_valid = False
        if not data['dairy_free']:
            flash('Is the food dairy free?', 'create_food')
            is_valid = False
        return is_valid
