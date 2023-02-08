from . import db
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from dotenv import load_dotenv
import os

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')

# this is the user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    firstName = db.Column(db.String(150), nullable=False)

    # this method is used to get a token for the user to reset their password
    def get_reset_token(self, expires_sec=300):

        # create a serializer object with the secret key and expiration time
        s = Serializer(SECRET_KEY, expires_sec)
        # return the token and decode it to a string
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # this method is used to verify the token
    # it is a static method because it does not need to be called on an instance of the class
    @staticmethod
    def verify_reset_token(token):
        # create a serializer object with the secret key
        s = Serializer(SECRET_KEY)
        # try to load the token
        try:
            # load the token
            user_id = s.loads(token)['user_id']
        except:
            # if it fails, return None
            return None
        # if it succeeds, return the user with the id
        return User.query.get(user_id)
