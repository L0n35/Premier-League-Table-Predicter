from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship



@login.user_loader
def load_user(userID):
    return users.query.get(int(userID))

# TO DO -> in create form incoporate flask msging to ensure all fields are completed
class users(db.Model, UserMixin):
    userID = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(50), nullable=False)
    fullName = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    passwordHash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return 'User: {}{}{}{}'.format(self.fullName, self.passwordHash, self.userID, self.email)
    
    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)
    
    def get_id(self):
        return (self.userID)
    
    def get_name(self):
        return(self.fullName)
    
    def get_email(self):
        return(self.email)

class predictions(db.Model):
    predictionID = db.Column(db.Integer, primary_key=True)
    prediction = db.Column(db.Text, nullable=False)
    season = db.Column(db.String(10), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)
    points = db.Column(db.Integer, nullable=True)

    user = relationship('users', backref='predictions')


    def __repr__(self):
        return '"{}","{}","{}","{}"'.format(self.predictionID, self.user.userName, self.user.fullName, self.points)
    
    def get_array(self):
        return [self.predictionID,self.user.userName,self.user.fullName,self.points]

    def get_id(self):
        return (self.predictionID)
    
    def get_prediction(self):
        return (self.prediction)
    
    def get_points(self):
        return (self.points)
    
    def get_userName(self):
        return (self.user.userName)
    
    def set_points(self, points):
        self.points = points

class seasons(db.Model):
    season = db.Column(db.Integer, primary_key=True)
    teams = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '"{}", "{}"'.format(self.season, self.teams)
    
    def get_teams(self):
        return (self.teams)



