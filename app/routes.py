from flask import render_template, jsonify, session, redirect, request, url_for, flash
from app import app, db
from app.forms import LoginForm, CreateForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import users, predictions, seasons
import json
from sqlalchemy import select

currentSeason = 2023

@app.route('/')
def base():
    return redirect(url_for('home'))

@app.route('/home', methods = ['GET','POST'])
def home():
    # Makes current user variables global
    global currentUserID
    global currentUserName

    form = LoginForm()

    if form.validate_on_submit():
          # Sets current user information
          currentUser = users.query.filter_by(email=form.email.data).first()
          currentUserID = currentUser.get_id()
          currentUserName = currentUser.get_name()
          session['username'] = currentUserName

          if currentUser is None:
            print('email is not in DB')
            return redirect(url_for('home'))
          elif not currentUser.check_password(form.password.data):
               print('password is incorrect')
               flash('password is incorrect')
            #    return redirect(url_for('home'))
          else:
            login_user(currentUser)
            return redirect(url_for('predict'))

    return render_template('home-page.html', form=form)

@app.route('/create', methods = ['GET','POST'])
def create():
    if current_user.is_authenticated:
        return redirect(url_for('predict'))
    
    form = CreateForm()

    if form.validate_on_submit():
         currentUser = users(userName=form.userName.data, fullName=form.fullName.data, email=form.email.data)
         currentUser.set_password(form.password.data)
         db.session.add(currentUser)
         db.session.commit()
         flash('Account created successfully!')
         return redirect(url_for('home'))

    return render_template("create.html", form=form)

# WORKS!!
@app.route('/login', methods = ['GET','POST'])
def login():
    # Makes current user variables global
    global currentUserID
    global currentUserName

    # if current_user.is_authenticated:
    #     currentUserName = current_user.name
    #     return redirect(url_for("history"))

    form = LoginForm()

    if form.validate_on_submit():
          # Sets current user information
          currentUser = users.query.filter_by(email=form.email.data).first()
          currentUserID = currentUser.get_id()
          currentUserName = currentUser.get_name()
          session['username'] = currentUserName

          if currentUser is None:
            flash('email is not in DB')
            return redirect(url_for('login'))
          elif not currentUser.check_password(form.password.data):
               flash('password is incorrect')
               return redirect(url_for('login'))
          login_user(currentUser)
          return redirect(url_for('index'))
    else:
        flash("unsuccessful")
    return render_template('login.html', form=form)    

@app.route('/logout')
def logout():
     logout_user()
     return redirect(url_for('home'))

# testing if base template changes depending on if user is logged in
@app.route('/test', methods = ['GET','POST'])
def test():
    form = LoginForm()
    return render_template('base.html', form=form)

@app.route('/predict')
def predict():
    return render_template('index.html')

@app.route('/submit_prediction', methods=['POST'])
def submit_prediction():
    prediction = request.form['prediction']
    predictionData = predictions(prediction=prediction, season=currentSeason, userID=currentUserID)
    db.session.add(predictionData)
    db.session.commit()
    print('pred',prediction)
    return redirect(url_for('home'))

@app.route('/points')
def points():
    return render_template('points.html')



@app.route('/get_prediction', methods=['POST','GET'])
def get_prediction():
    prediction = predictions.query.filter_by(userID=currentUserID, season=currentSeason).first()
    predictionRAA = prediction.get_prediction()
    # prediction1 = json.loads(predictionJSON)
    print('gp',predictionRAA)
    return predictionRAA

@app.route('/points/<id>', methods=['POST','GET'])
def view_points(id):
    print('heya',id)
    prediction = predictions.query.filter_by(predictionID=id).first()
    u = prediction.get_userName();
    return render_template('view_points.html', viewingUser=u)

@app.route('/view_prediction/<id>', methods=['POST','GET'])
def view_prediction(id):
    print(id)
    prediction = predictions.query.filter_by(predictionID=id).first()
    predictionRAA = prediction.get_prediction()
    return predictionRAA

@app.route('/get_teams', methods=['POST','GET'])
def get_teams():
    season = seasons.query.first()
    teams = season.get_teams()
    teams = teams.replace('[','')
    teams = teams.replace(']','')
    teamList2 = teams.split(",")
    teamList2.sort()
    print('gt',teamList2)
    return teamList2

@app.route('/get_standings', methods=['POST','GET'])
def get_standings():
    s = seasons.query.first()
    t = s.get_teams()
    t = t.replace('[','')
    t = t.replace(']','')
    print('gs',t)
    return t

@app.route('/update_points', methods=['POST','GET'])
def update_points():
    points = request.form['points']



    # Get the conversations previous messages 
    predictionData = predictions.query.filter_by(userID=currentUserID, season=currentSeason).first()


    # Update changes in database
    predictionData = predictions.query.filter_by(userID=currentUserID, season=currentSeason).first()
    predictionData.set_points(points)

    db.session.commit()

    print('points', points)
    return '!SCORE UPDATED!'

@app.route('/rank')
def rank():
    return render_template('rank.html')

@app.route('/get_leaderboard', methods=['POST','GET'])
def get_leaderboard():
    all = []
    allPredictions = predictions.query.filter_by(season=currentSeason).all()
    for x in allPredictions:
        all.append(x.get_array())
        print(x.get_array())

    print(Sort(all))
    return Sort(all)

def Sort(sub_li):
 
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used

    if (lambda x: x[3] != None):
        return(sorted(sub_li, key=lambda x: x[3],reverse=True))

@app.route('/dash')
def dash():
    return render_template('dashboard.html')