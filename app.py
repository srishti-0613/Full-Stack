from flask import Flask, render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required,current_user,LoginManager,is_authenticated
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = u"Please login to access this page"
login_manager.login_message_category = "info"
login_manager.login_view = 'login'

local_server =False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/brilliant_zone'
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = parameter['prod_uri
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

class Contact(db.Model):

    sno = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(300), nullable=False)

class Users(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

@login_manager.user_loader  
def load_user(user_id): 
    return Users.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html",is_authenticated=is_authenticated)

@app.route("/register",methods = ['GET','POST'])
def register():
    if(request.method ==  'POST'):
        
        name = request.form.get('signupName')
        email = request.form.get('signupEmail')
        phone = request.form.get('signupPhone')
        password = request.form.get('signupPassword')
        user = Users.query.filter_by(phone=phone).first()
        if user:
            flash('phone/Email address already exists')
            return redirect(url_for('home'))
        entry = Users(name=name, email=email, phone=phone,password=password)
        db.session.add(entry)
        db.session.commit()
    return render_template("index.html",is_authenticated=is_authenticated)

@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method == ['GET','POST']:
        phone = request.form.get('loginPhone')
        name = request.form.get('loginName')
        password = request.form.get('loginPassword')
        user = Users.query.filter_by(phone=phone).first()
        if not user or not password==user.password:
            flash("Either you are not registered or your password is incorrect")
            return redirect(url_for('home'))
        else:
            login_user(user)
            flash("Loggedin succesfully")
            return redirect(url_for('home'))
    return render_template('index.html',is_authenticated=is_authenticated)

@app.route("/logout",methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/about")
def about():
    return render_template("about.html",is_authenticated=is_authenticated)
@app.route("/courses")
@login_required
def courses():
    return render_template("courses.html",name=current_user.name,is_authenticated=is_authenticated)
@app.route("/contact",methods = ['GET','POST'])
def contact():
    if(request.method ==  'POST'):
    
        '''add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('mail')
        subject = request.form.get('subject')
        message = request.form.get('message')

        '''upload sno, name, email, subject, messageon database'''
        entry = Contact(name=name, email=email, subject=subject,message=message)
        db.session.add(entry)
        db.session.commit()
    return render_template("contact.html",is_authenticated=is_authenticated)
@app.route("/leaderboard")
@login_required
def events():
    return render_template("leaderboard.html",name=current_user.name,is_authenticated=is_authenticated)
@app.route("/notice")
@login_required
def notice():
    return render_template("notice.html",name=current_user.name,is_authenticated=is_authenticated)
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
# app.run(debug=True)