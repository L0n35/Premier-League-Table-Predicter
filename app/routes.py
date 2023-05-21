from flask import render_template, jsonify, session, redirect, request, url_for, flash
from app import app, db
from app.forms import LoginForm, CreateForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import user, conversations
import json
import openai
from sqlalchemy import select

# OpenAI API key
openai.api_key = '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'
# OpenAI model 
MODEL_NAME = 'gpt-3.5-turbo'



@app.route('/')
def base():
    return render_template("base.html", title="base")

@app.route('/home', methods = ['GET','POST'])
def home():
    form = LoginForm()

    if form.validate_on_submit():
          currentUser = user.query.filter_by(email=form.email.data).first()
          if currentUser is None:
            flash('email is not in DB')
            return redirect(url_for('home'))
          elif not currentUser.check_password(form.password.data):
               flash('password is incorrect')
               return redirect(url_for('home'))
          login_user(currentUser)
          return redirect(url_for('history'))
    else:
        flash("unsuccessful")
    return render_template('home-page.html', form=form)

@app.route('/history')
@login_required
def history():
      




      return render_template("history-page.html", name=currentUserName)

@app.route('/chat')
def new_chat():
      empty_json = {
        "messages": []
      }
      conversation = conversations(title="", conv_json=json.dumps(empty_json), userID=currentUserID)
      db.session.add(conversation)
      db.session.commit()
      global conversationID
      conversationID = conversation.get_id()
      return render_template("chat.html", name=currentUserName)

@app.route('/chat/<id>')
def chat(id):
      # todo: add check to see if id exists
      global conversationID
      conversationID = id
      return render_template("chat.html")
     
    
@app.route('/get_response', methods=['POST'])
def get_response():
    location = request.form['location']
    message = request.form['message']

    # Prepare the conversation input
    conversation = [
        {'role': 'system', 'content': 'You are a helpful assistant who helps users with travel related questions about ' + location + ' only.'},
        {'role': 'user', 'content': 'In 50 words or less answer the question: ' + message}
    ]

    # Generate TravelBots's response using stream
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=conversation,
        max_tokens=200,
        n=1,
        stop=None
    )
    
    reply = response.choices[0].message.content

    conversationQuery = conversations.query.filter_by(conversationID=conversationID).first()
    conversationJSON = conversationQuery.get_json()
    conversationMessages = json.loads(conversationJSON)
    print(conversationMessages)

    conversationMessages["messages"].append({"author": current_user.name, "message": message})
    conversationMessages["messages"].append({"author": "TravelBot", "message": reply})
    print(conversationMessages)

    conv = conversations.query.filter_by(conversationID=conversationID).first()
    conv.set_title(location)
    conv.set_json(json.dumps(conversationMessages))
    db.session.commit()

    print(conv.get_json())

    

    # messages = {
    #     "messages": [
    #         {"author": current_user.name, "message": message},
    #         {"author": "TravelBot", "message": reply}
    #     ]
    # }

    # print(messages)
    # m = json.dumps(messages)
    # print(m) 

    
    
    return reply

@app.route('/get_conversations', methods=['POST'])
def get_conversations():
    #location#= #request.form['location']#
    #print('currentID',currentUserID)
    convs = conversations.query.filter_by(userID=currentUserID).all()
    str(convs)
    print(convs)

    return str(convs)

    



# WORKS!!
@app.route('/create', methods = ['GET','POST'])
def create():
    if current_user.is_authenticated:
        return redirect(url_for('history'))
    
    form = CreateForm()

    if form.validate_on_submit():
         currentUser = user(name=form.name.data, email=form.email.data)
         currentUser.set_password(form.password.data)
         db.session.add(currentUser)
         db.session.commit()
         flash('Account created successfully!')
         return redirect(url_for('login'))

    return render_template("create.html", form=form)

# WORKS!!
@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        global currentUserName
        currentUserName = current_user.name
        return redirect(url_for("history"))

    form = LoginForm()

    if form.validate_on_submit():
          global currentUserID
          #global currentUserName
          currentUser = user.query.filter_by(email=form.email.data).first()
          currentUserID = currentUser.get_id()
          print('currentuserid',currentUserID)
          currentUserName = currentUser.get_name()
          if currentUser is None:
            flash('email is not in DB')
            return redirect(url_for('login'))
          elif not currentUser.check_password(form.password.data):
               flash('password is incorrect')
               return redirect(url_for('login'))
          login_user(currentUser)
          return redirect(url_for('history'))
    else:
        flash("unsuccessful")
    return render_template('login.html', form=form)    

@app.route('/logout')
def logout():
     logout_user()
     return redirect(url_for('home'))