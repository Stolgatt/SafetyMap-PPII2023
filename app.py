from flask import Flask, g, render_template, request, make_response, jsonify, redirect, url_for
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from flask_wtf.csrf import CSRFProtect, CSRFError
import sqlite3
import secrets
from traitement import cluster
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import hashlib


app = Flask(__name__)
app.secret_key = 'wakanda_f0rever'
DATABASE = 'db/database.db'
bcrypt = Bcrypt(app)
cle_hyper_secrete_ne_pas_toucher = b'\x883\xfb\x8b\n\xcep\xbb2\x9cP\x8f\xa0\xc9\xae\xd3'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'safetymap.mail@gmail.com'
app.config['MAIL_PASSWORD'] = 'zbbb uqht dkrr feeo'

mail = Mail(app)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#-----------------------ROUTES--------------------------------#

@app.route('/')
def home():
    total_incident = total_incidents()
    incidents_by_type_list = incidents_by_type()
    incidents_over_time_nb = incidents_over_time('weekly')
    incident_stat = percentage_incidents_by_type()
    return render_template('home.html', loggedin=check_session(), total=total_incident, incidents_by_type=incidents_by_type_list, incidents_over_time=incidents_over_time_nb, incident_stat=incident_stat, nb_users = nb_users(), admin=check_admin())
    


@app.route('/a_propos')
def about():
    return render_template('a_propos.html', loggedin=check_session(), admin=check_admin())

@app.route('/legal')
def legal():
    return render_template('legal.html', loggedin=check_session(), admin=check_admin())

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if user is None:
            return render_template('login.html', errors=['Mot de passe ou identifiant incorrect !'])
        c.execute("SELECT verified FROM users WHERE username = ?", (username,))
        verified = c.fetchone()[0]
        if verified == 0:
            return render_template('login.html', errors=['Veuillez confirmer votre adresse mail !'])
        else:
            if bcrypt.check_password_hash(user[2], password):
                if not request.form.get('next') is None :
                    return create_session(user[0], request.form.get('next'))
                return create_session(user[0], '/')
            else:
                return render_template('login.html', errors=['Mot de passe incorrect !'])



@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email= request.form['email']
        password = request.form['password']
        
        db = get_db()
        c = db.cursor()

        c.execute('SELECT COUNT(*) FROM users WHERE username = (?);',(username,))
        check_username = c.fetchone()[0]
        if check_username > 0:
            error_message = "Ce nom d'utilisateur existe déjà !"
            return render_template('register.html', error=error_message)
        
        c.execute('SELECT COUNT(*) FROM users WHERE email=(?);', (email,))
        check_mail = c.fetchone()[0]
        if check_mail > 0 :
            error_message = 'Ce mail existe déjà !'
            return render_template('register.html', error=error_message)
        
        crypted_password = bcrypt.generate_password_hash(password)
        c.execute('INSERT INTO users (username, password, email, name, registration_time) VALUES (?,?,?,?,?);', (username, crypted_password, email, name, datetime.now()))
        db.commit()
        with app.app_context():
            send_confirmation_email(email, username)
        return redirect('/verify/a88b7dcd1a9e3e17770bbaa6d7515b31a2d7e85d')


@app.route('/verify/a88b7dcd1a9e3e17770bbaa6d7515b31a2d7e85d', methods=['GET'])
def verify_email():
    return render_template('email_verif.html')


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        username = URLSafeTimedSerializer(app.config['SECRET_KEY']).loads(token, salt='email-confirm-salt', max_age=3600)
    except:
        return 'Le lien est invalide ou a expiré.'
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = ?;", (username,))
    already_verified = c.fetchone()[6]
    if already_verified == 1:
        return f"<html><body><h2>Le compte pour {username} a déjà été confirmé.</h2><a href='/login'>Connexion</a></body></html>"
    else :
        c.execute("UPDATE users SET verified = 1 WHERE username = ?;", (username,))
        db.commit()
        return f"<html><body><h2>Le compte pour {username} a été confirmé avec succès.</h2><a href='/login'>Connexion</a></body></html>"


@app.route('/dashboard')
def dashboard():
    try :
        if not check_session():
            return redirect(url_for('login', next=request.url))
        user_id = get_user_id()
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE user_id = (?);", (user_id,))
        data = c.fetchone()
        c.execute("SELECT * FROM incident_reports WHERE user_id = ?;", (data[0],))
        reports = c.fetchall()
        c.execute("SELECT * FROM incident_types;")
        types = c.fetchall()
        incident_types = {key: value for (key, value) in types}
        total_incident = total_incidents_for_user(user_id)
        weekly_incident = incidents_over_time_user('weekly', user_id)
        monthly_incident = incidents_over_time_user('monthly', user_id)[0][1]
        most_reported_incident = most_reported_incident_type_user(user_id)
        return render_template('dashboard.html', posts = data, reports=reports, types_dict=incident_types, admin=check_admin(), total=total_incident, weekly=weekly_incident, monthly=monthly_incident, most_reported_incident=most_reported_incident, id=get_user_id(), loggedin=check_session())
    except TypeError as e:
        return redirect('/login')


@app.route('/edit_password', methods=['GET', 'POST'])
def edit_password_page():
    if not check_session():
        return redirect(url_for('login', next=request.url))
    if request.method == 'GET':
        return render_template('edit_password.html')
    elif request.method == 'POST':
        user_id = get_user_id()
        data = request.form
        old_password = data['old_password']
        new_password = data['new_password']
        new_password_verif = data['new_password_verif']
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE user_id = ?;", (user_id,))
        user = c.fetchone()
        if not bcrypt.check_password_hash(user[2], old_password):
            return render_template('edit_password.html', errors=['Mot de passe incorrect !'])
        if bcrypt.check_password_hash(user[2], new_password):
            return render_template('edit_password.html', errors=['Le nouveau mot de passe doit être différent de l\'ancien !'])
        if new_password != new_password_verif:
            return render_template('edit_password.html', errors=['Les mots de passe ne correspondent pas !'])
        modify_password(user_id, new_password)
        return redirect('/dashboard')




@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')
    elif request.method == 'POST':
        email = request.form['email']
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE email = ?;", (email,))
        user = c.fetchone()
        if user is None:
            return render_template('forgot_password.html', errors=['Aucun compte n\'est associé à cet email !'])
        else:
            username = user[1]
            with app.app_context():
                send_forgot_password_email(email, username)
                return redirect('/verify/5bcf368dbf6ae2399bcf2d648ce8583d')
        

@app.route('/verify/5bcf368dbf6ae2399bcf2d648ce8583d', methods=['GET'])
def verify_email_forgot_password():
    return render_template('email_verif_forgot_password.html')


@app.route('/change_password/<token>', methods=['GET', 'POST'])
def change_password(token):
    if request.method == 'GET':
        try:
            username = URLSafeTimedSerializer(app.config['SECRET_KEY']).loads(token, salt='password-recovery-salt', max_age=3600)
        except:
            return 'Le lien est invalide ou a expiré.'
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE username = ?;", (username,))
        user = c.fetchone()
        if user is None:
            return 'Cet utilisateur n\'existe pas !'
        else:
            return render_template('change_password.html', token=token, username=username)
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_verif = request.form['password_verif']
        if password != password_verif:
            return render_template('change_password.html', errors=['Les mots de passe ne correspondent pas !'])
        else:
            modify_password_bis(username, password)
            return f"<html><body><h2>Le mot de passe a été modifié avec succès.</h2><a href='/login'>Connexion</a></body></html>"

@app.route('/report_incident', methods=['GET', 'POST'])
def report_incident():
    if not check_session():
        return redirect(url_for('login', next=request.url))
    if request.method == 'GET':
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM incident_types;")
        types = c.fetchall()
        return render_template('report_incident.html', types=types)
    elif request.method == 'POST':
        session_key = request.cookies.get('session')
        data = request.form
        type_agression = data['type']
        long = data['long']
        lat = data['lat']
        date = data['date']
        hour = data['time']
        time = date + ' ' + hour
        time = datetime.strptime(time, '%Y-%m-%d %H:%M')
        db = get_db()
        c = db.cursor()
        user_id = get_user_id()
        c.execute("INSERT INTO incident_reports (time, user_id, lat, long, type_id) VALUES (?, ?, ?, ?, ?)", (time, user_id, lat, long, type_agression))
        db.commit()
        return redirect('/dashboard')

@app.route('/None')
def none():
    return redirect('/')


@app.route("/all_markers/<string:etat>")
def markers(etat):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT lat,long, type_id, time FROM incident_reports;")
    markers = c.fetchall()
    c.execute("SELECT * FROM incident_types;")
    types = c.fetchall()
    db.close()
    incident_types = {key: value for (key, value) in types}
    markers_list = [{"long": lng, "lat": lat, "incident_type" : incident_types[incident], "time" : time} for lat, lng, incident, time in markers]
    if etat == "on":
        return jsonify(markers_list)
    elif etat == "off":
        markers_list = cluster(markers_list)
        return jsonify(markers_list)






@app.route('/markers/<string:hash>')
def markers_hash(hash):
    id = check_hash(hash)
    db = get_db()
    c = db.cursor()
    c.execute(f"SELECT lat,long, type_id, time FROM incident_reports WHERE user_id = ?;", (id,))
    markers = c.fetchall()
    c.execute("SELECT * FROM incident_types;")
    types = c.fetchall()
    db.close()
    incident_types = {key: value for (key, value) in types}
    markers_list = [{"long": lng, "lat": lat, "incident_type" : incident_types[incident], "time" : time} for lat, lng, incident, time in markers]
    return jsonify(markers_list)


@app.route('/get_pourcentage_from_database')
def get_pourcentage_from_database():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT it.name, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM incident_reports) FROM incident_reports ir JOIN incident_types it ON ir.type_id = it.type_id GROUP BY it.name")
    results = c.fetchall()
    res = {'incident_type': [], 'pourcentage': []}
    somme = 0
    for i in range(len(results)):
        res['incident_type'].append(results[i][0])
        res['pourcentage'].append(round(results[i][1], 2))
    for element in res['pourcentage']:
        somme += element
    return jsonify(res)



@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'GET':
        if check_session():
            user_id = get_user_id()
            db = get_db()
            c = db.cursor()
            c.execute("SELECT name, email FROM users WHERE user_id = ?;", (user_id,))
            user = c.fetchone()
            return render_template('feedback.html', user=user)
        else :
            return render_template('feedback.html', user = [])
    elif request.method == 'POST':
        user_id = get_user_id()
        message = request.form['message']
        
        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO feedbacks (user_id, time, content) VALUES (?, ?, ?);", (user_id, datetime.now(), message))
        db.commit()
        return redirect('/')


@app.route('/logout')
def logout():
    return logout_session()


##-----------------------ADMIN---------------------------------##

@app.route('/admin', methods=['GET'])
def admin():
    if not check_admin():
        wait_time = 3000
        seconds = wait_time / 1000
        redirect_url = url_for('home')
        return f"<html><body><p style='color: red;'>Accès interdit ! Vous serez redirigé à la page d'accueil dans { int(seconds) } secondes.</p><script>var timer = setTimeout(function() {{window.location='{ redirect_url }'}}, { wait_time });</script></body></html>"
    if request.method == 'GET':
        return render_template('admin.html')


@app.route('/admin/', methods=['GET'])
def admin_home():
    return redirect('/admin')



@app.route('/admin/users', methods=['GET'])
def admin_users():
    if not check_admin():
        wait_time = 3000
        seconds = wait_time / 1000
        redirect_url = url_for('home')
        return f"<html><body><p style='color: red;'>Accès interdit ! Vous serez redirigé à la page d'accueil dans { int(seconds) } secondes.</p><script>var timer = setTimeout(function() {{window.location='{ redirect_url }'}}, { wait_time });</script></body></html>"
    if request.method == 'GET':
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM users;")
        users = c.fetchall()
        return render_template('admin_users.html', users=users)


@app.route('/admin/reports', methods=['GET'])
def admin_incidents():
    if not check_admin():
        wait_time = 3000
        seconds = wait_time / 1000
        redirect_url = url_for('home')
        return f"<html><body><p style='color: red;'>Accès interdit ! Vous serez redirigé à la page d'accueil dans { int(seconds) } secondes.</p><script>var timer = setTimeout(function() {{window.location='{ redirect_url }'}}, { wait_time });</script></body></html>"
    if request.method == 'GET':
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM incident_reports;")
        reports = c.fetchall()
        c.execute("SELECT * FROM incident_types;")
        types = c.fetchall()
        incident_types = {key: value for (key, value) in types}
        return render_template('admin_incidents.html', reports=reports, types_dict=incident_types)


@app.route('/admin/feedbacks', methods=['GET'])
def admin_feedback():
    if not check_admin():
        wait_time = 3000
        seconds = wait_time / 1000
        redirect_url = url_for('home')
        return f"<html><body><p style='color: red;'>Accès interdit ! Vous serez redirigé à la page d'accueil dans { int(seconds) } secondes.</p><script>var timer = setTimeout(function() {{window.location='{ redirect_url }'}}, { wait_time });</script></body></html>"
    if request.method == 'GET':
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM feedbacks;")
        feedbacks = c.fetchall()
        return render_template('admin_feedbacks.html', feedbacks=feedbacks)



@app.route('/admin/delete_report', methods=['POST']) 
def delete_report():
    if not check_admin():
        return redirect('/login')
    report_id = request.form['report_id']
    db = get_db()
    c = db.cursor()
    c.execute("DELETE FROM incident_reports WHERE report_id = ?;", (report_id,))
    db.commit()
    return redirect('/admin/reports')


@app.route('/admin/delete_user', methods=['POST'])
def delete_user():
    if not check_admin():
        return redirect('/login')
    user_id = request.form['user_id']
    db = get_db()
    c = db.cursor()
    c.execute("DELETE FROM users WHERE user_id = ?;", (user_id,))
    db.commit()
    return redirect('/admin/users')





#-----------------------FUNCTIONS---------------------------------#

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def create_session(user_id, route):
    db = get_db()
    c = db.cursor()
    is_unique = False
    
    while(not is_unique):
        session_key = secrets.token_urlsafe()
        c.execute("SELECT COUNT(*) FROM sessions WHERE key = ?;", (session_key,))
        count = c.fetchone()[0]
        if count == 0:
            is_unique = True
            
    ip_address = request.remote_addr
    expiration_date = datetime.now() + timedelta(weeks=1)
    
    #Partie à vérifier
    c.execute("DELETE FROM sessions WHERE user_id = ? AND ipv4 = ? AND expiration <= ?;", (user_id,ip_address,expiration_date))
    
    c.execute("INSERT INTO sessions (user_id,ipv4,key,expiration) VALUES (?,?,?,?);",(user_id, ip_address, session_key, expiration_date))
    db.commit()
    resp = make_response(redirect(route))
    resp.set_cookie('session', session_key, httponly=True, expires=expiration_date)
    return resp

def check_session():
    session_key = request.cookies.get('session')
    ip_adress = request.remote_addr

    db = get_db()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM sessions WHERE key = ? AND ipv4 = ?;", (session_key,ip_adress))
    session_num = c.fetchone()[0]
    
    if session_num > 0:
        return True
    else:
        return False

def get_user_id():
    session_key = request.cookies.get('session')
    db = get_db()
    c = db.cursor()
    c.execute("SELECT user_id FROM sessions WHERE key = ?;", (session_key,))
    user_id = c.fetchone()[0]
    return user_id

def check_admin():
    try :
        user_id = get_user_id()
        db = get_db()
        c = db.cursor()
        c.execute("SELECT user_id FROM users WHERE user_id IN (SELECT user_id FROM admins);")
        admins = c.fetchall()
        for admin in admins:
            if user_id == admin[0]:
                return True
        return False
    except TypeError:
        return False



def logout_session():
    session_key = request.cookies.get('session')
    db = get_db()
    c = db.cursor()
    c.execute("DELETE FROM sessions WHERE key = ?;",(session_key,))
    db.commit()
    resp = make_response(redirect('/'))
    resp.delete_cookie('session')
    return resp

def modify_password(user_id, password):
    crypted_password = bcrypt.generate_password_hash(password)
    db = get_db()
    c = db.cursor()
    c.execute("UPDATE users SET password = ? WHERE user_id = ?;", (crypted_password, user_id))
    db.commit()


def modify_password_bis(username, password):
    crypted_password = bcrypt.generate_password_hash(password)
    db = get_db()
    c = db.cursor()
    c.execute("UPDATE users SET password = ? WHERE username = ?;", (crypted_password, username))
    db.commit()


def generate_confirmation_token_mail(username):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(username, salt='email-confirm-salt')


def generate_confirmation_token_password(username):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(username, salt='password-recovery-salt')



def send_confirmation_email(user_email, username):
    token = generate_confirmation_token_mail(username)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    email_body = f'Bonjour,\n\nVeuillez cliquer sur le lien suivant pour confirmer votre e-mail : \n{confirm_url}\n\nCordialement,\nL\'équipe SafetyMap.'
    msg = Message('Confirmez votre Email', sender='safetymap.mail@gmail.com', recipients=[user_email])
    msg.body = email_body
    mail.send(msg)

def send_forgot_password_email(user_email, username):
    token = generate_confirmation_token_password(username)
    url = url_for('change_password', token=token, _external=True)
    email_body = f'Bonjour,\n\nVeuillez cliquer sur le lien suivant pour changer votre mot de passe: \n{url}\n\nCordialement,\nL\'équipe SafetyMap.'
    msg = Message('Récupérer votre mot de passe', sender='safetymap.mail@gmail.com', recipients=[user_email])
    msg.body = email_body
    mail.send(msg)


def total_incidents():
    db= get_db()
    cur = db.cursor()
    cur.execute('SELECT COUNT(*) FROM incident_reports;')
    total = cur.fetchone()[0]
    return total

def incidents_by_type():
    db= get_db()
    cur = db.cursor()
    cur.execute('SELECT it.name, COUNT(*) FROM incident_reports ir JOIN incident_types it ON ir.type_id = it.type_id GROUP BY it.name;')
    results = cur.fetchall()
    return results

def incidents_over_time(period='daily'):
    db = get_db()
    cur = db.cursor()
    if period == 'daily':
        cur.execute('SELECT DATE(time), COUNT(*) FROM incident_reports GROUP BY DATE(time);')
    if period == 'weekly':
        end_date = datetime.now()
        start_date = end_date - timedelta(days=6)
        start_date_str = start_date.strftime('%Y-%m-%d')
        cur.execute('SELECT DATE(time) as date, COUNT(*) FROM incident_reports WHERE DATE(time) BETWEEN ? AND ? GROUP BY DATE(time);', (start_date_str, end_date.strftime('%Y-%m-%d')))
        results = cur.fetchall()
        sum = 0
        for element in results:
            sum += element[1]
        return sum
    elif period == 'monthly':
        cur.execute('SELECT strftime("%Y-%m", time), COUNT(*) FROM incident_reports GROUP BY strftime("%Y-%m", time);')
        results = cur.fetchall()
        return results


def percentage_incidents_by_type():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT it.name, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM incident_reports) FROM incident_reports ir JOIN incident_types it ON ir.type_id = it.type_id GROUP BY it.name')
    results = cur.fetchall()
    return results


def nb_users():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT COUNT(*) FROM users;')
    results = cur.fetchone()[0]
    return results


def total_incidents_for_user(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT COUNT(*) FROM incident_reports WHERE user_id = ?', (user_id,))
    total = cur.fetchone()[0]
    return total


def incidents_over_time_user(period='daily', id=0):
    db = get_db()
    cur = db.cursor()
    if period == 'daily':
        cur.execute('SELECT DATE(time), COUNT(*) FROM incident_reports WHERE user_id = ? GROUP BY DATE(time);', (id,))
        results = cur.fetchall()
        return results
    elif period == 'weekly':
        end_date = datetime.now()
        start_date = end_date - timedelta(days=6)
        start_date_str = start_date.strftime('%Y-%m-%d')
        cur.execute('SELECT DATE(time) as date, COUNT(*) FROM incident_reports WHERE user_id = ? AND DATE(time) BETWEEN ? AND ? GROUP BY DATE(time);', (id, start_date_str, end_date.strftime('%Y-%m-%d')))
        results = cur.fetchall()
        sum = 0
        for element in results:
            sum += element[1]
        return sum
    elif period == 'monthly':
        cur.execute('SELECT strftime("%Y-%m", time), COUNT(*) FROM incident_reports WHERE user_id = ? GROUP BY strftime("%Y-%m", time);', (id,))
        results = cur.fetchall()
        return results



def most_reported_incident_type_user(id):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT it.name, COUNT(*) FROM incident_reports ir JOIN incident_types it ON ir.type_id = it.type_id WHERE user_id = ? GROUP BY it.name ORDER BY COUNT(*) DESC LIMIT 1;', (id,))
    results = cur.fetchone()
    return results


def check_hash(hash):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT user_id FROM users')
    results = cur.fetchall()
    for e in results:
        if hashlib.md5(str(e[0]).encode()).hexdigest() == hash:
            return e[0]
    return None


# @app.route('/scores', methods=['GET', 'POST'])
# def create_score():
#     db = get_db()
#     c = db.cursor()
    
#     if request.method == 'GET':
#         c.execute("SELECT * FROM scores;")
#         data = c.fetchall()
        
#         return jsonify(data)
    
#     elif request.method == 'POST':
#         if not check_session():
#             return redirect('/login')
#         data = request.json
#         ip = request.remote_addr
#         score = data['score']
#         date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#         c.execute("INSERT INTO scores (ipv4, score, time) VALUES (?, ?, ?)", (ip, score, date))
#         db.commit()

#         return jsonify(success=True)






#modèle de requête: /search_by_location?latMin=${latMin}&latMax=${latMax}&longMin=${longMin}&longMax=${longMax}
# @app.route('/search_by_location')
# def search_by_location():
#     latMax = request.args.get('latMax')
#     latMin = request.args.get('latMin')
#     longMax = request.args.get('longMax')
#     longMin = request.args.get('longMin')
#     db = get_db()
#     c = db.cursor()
#     c.execute("SELECT * FROM incident_reports WHERE lat BETWEEN ? AND ? AND long BETWEEN ? AND ?", (latMin, latMax, longMin, longMax))
#     incident_reports = c.fetchall()
#     return jsonify(incident_reports)
