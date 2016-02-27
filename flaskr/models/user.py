from werkzeug.security import check_password_hash, generate_password_hash
# from flaskr import errors
import errors


class User():
    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def register(input_dict, collection):
        user_doc = collection.find_one({"username": input_dict['username']})
        if None == input_dict['username'] or None == input_dict['password']:
            raise errors.RegistrationError("Invalid username or password")

        if user_doc:
            raise errors.UsernameAlreadyExists("")
        else:
            try:
                collection.insert({"username": input_dict['username'],
                                   "password": generate_password_hash(input_dict['password']),
                                   "credentials": {
                                       "gmc": {
                                           "auth_key": input_dict.get('gmc_auth_key', None)
                                       }
                                   }})
                return User(input_dict['username'])
            except Exception:
                raise errors.RegistrationError("")

    @staticmethod
    def get(username, collection):
        user_doc = collection.find_one({"username": username})
        if user_doc:
            return user_doc
        return None

    @staticmethod
    def validate_login(password_hash, password):

        return check_password_hash(password_hash, password)
