from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
from flask_app.models import food
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# make class, class methods with SQL, and logic
class User:
    db = 'gf_df_foods'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.active_user = 1
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.foods = []


#Create 
    @classmethod
    def create_user(cls, data):
        if not cls.validate_user_reg(data):
            return False
        parsed_data = cls.parse_reg_data(data)
        query = """
        INSERT INTO users(first_name, last_name, email, password)
        VALUES( %(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""

        user_id = connectToMySQL(cls.db).query_db(query, parsed_data)
        session['user_id'] = user_id

        return user_id


#Read 
    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email}
        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        ;"""

        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])

        return result

    @classmethod
    def get_user_by_id(cls, id):
        data = {'id' : id}

        query = """
        SELECT * FROM users
        LEFT JOIN foods
        ON users.id = foods.user_id
        WHERE users.id = %(id)s
        ;"""

        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            this_result = cls(result[0])
            for one_user in result:
                info = {
                    'id' : one_user['foods.id'],
                    'name' : one_user['name'],
                    'description' : one_user['description'],
                    'location' : one_user['location'],
                    'gluten_free' : one_user['gluten_free'],
                    'dairy_free' : one_user['dairy_free'],
                    'user_id' : one_user['user_id'],
                    'active_food' : one_user['active_food'],
                    'created_at' : one_user['foods.created_at'],
                    'updated_at' : one_user['foods.updated_at']
                }
                this_result.foods.append(food.Food(info))

        return this_result


#Update 


#Delete 

#Validate 
    #validate registration data
    @staticmethod
    def validate_user_reg(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2:
            flash('Your name must be at least 2 characters.', 'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Your name must be at least 2 characters.', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address!', 'register')
            is_valid = False
        if User.get_user_by_email(data['email'].lower()):
            flash('Email already exits', 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash('Your password must contain at least 8 characters.', 'register')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Your password does not match', 'register')
            is_valid = False
        return is_valid


    #parse data to be used
    @staticmethod
    def parse_reg_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['email'] = data['email'].lower()
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parsed_data

    #validate login data
    @staticmethod
    def login(data):
        this_user = User.get_user_by_email(data['email'].lower())
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                return True
        flash('Your login information is incorrect', 'login')
        return False