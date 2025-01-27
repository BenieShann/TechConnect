
import json
import os
from datetime import timedelta    
# the below is for unix time
import datetime
from collections import defaultdict


class DataController:
    def __init__(self):
        self.users_data_path = 'user_data/customers_db.json'
        self.users_data = self.load_or_create_users_data()
    
    def get_all_users(self):
        return self.users_data 
    
    def save_users_data(self):
        with open(self.users_data_path, "w") as file:
            # json.dump(self.user_model, file, indent=4)
            json.dump(self.users_data, file, indent=4)

    def load_users_data(self):
        with open(self.users_data_path, "r") as file:
            return json.load(file)

    def load_or_create_users_data(self):
        directory = os.path.dirname(self.users_data_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self.users_data_path):
            self.users_data = []
            self.save_users_data()
        else:
            self.users_data = self.load_users_data()
        return self.users_data


    def register_user(self, user_model):
        
        if any(user["username"] == user_model.username for user in self.users_data):
            return False
        else:
            # user_model.customer_number = self.generate_customer_number()
            self.users_data.append(vars(user_model))
            self.save_users_data()
            return True 
    
    def authenticate_user(self, username, password):
        for user in self.users_data:
            if user["username"] == username and user["password"] == password:
                return True, user["user_id"], user.get("role", "user")  
        return False, None, None
    