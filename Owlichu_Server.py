# ========================================================================= #
#    Python Personal Project 
#    student: Pablo Ostos Bollmann
#    professor: Pepe García
#    master: MCSBT (Master in Computer Science and Business Technology)
#   
# ========================================================================= #

# Importing necessary libraries
from flask import Flask, render_template, request, session, redirect, url_for
from sqlalchemy import create_engine
import sqlalchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import requests

# Connecting to database
# engine = create_engine("sqlite:///owlichu_internal.db")

def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    """ Initializes a TCP connection pool for a Cloud SQL instance of MySQL. """
    db_host = ''# e.g. '127.0.0.1' ('172.17.0.1' if deployed to GAE Flex)
    db_user = ''# e.g. 'my-db-user'
    db_pass = ''# e.g. 'my-db-password'
    db_name = ''# e.g. 'my-database'
    db_port =  # e.g. 3306

    engine = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        ),
    )
    return engine

# Creating Flask instance and secret key to sign session data and protect app from attacks
app = Flask(__name__)
app.config["SECRET_KEY"] = "my_secret_key"

engine = connect_tcp_socket()
conn = engine.connect()

# ========================================================================= #
# Handling the dictionary API

api_key = "a34fb0de-1934-49c0-8afa-80d65f0a2856"

def get_word_definition(word):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[0]
        if 'meta' in data and 'id' in data['meta']:
            word_id = data['meta']['id']
            if ('def' in data) and ('sseq' in data['def'][0]) and ('dt' in data['def'][0]['sseq'][0][0][1]):
                definitions = data['def'][0]['sseq'][0][0][1]['dt'][0][1]
                return word_id, definitions
            else:
                return word, None
        else:
            return None
    else:
        return None

# ========================================================================= #
# ========================================================================= #
# index() route: loads main page where user can introduce new word
@app.route("/")
def index():
    if 'username' in session: 
        return render_template("Word_Owlichu.html")
    else: 
        return redirect("/identification")


# ========================================================================= #
# ========================================================================= #
# handle_word() route: handles word restrictions and redirects to next step -> giving the word a definition
@app.route("/handle_word", methods = ["POST"])
def handle_word():
    owlichu = request.form["owly"]

    # RESTRICTION #1: it can only be a word, no spaces in between
    if len(owlichu.split(' ')) != 1:
        return render_template("Restriction1_Owlichu.html")
    # RESTRICTION #2: only lowercase letters
    elif not owlichu[0].islower():
        return render_template("Restriction2_Owlichu.html")
    # RESTRICTION #3: Can't be longer than the longest word in the english dictionary: Pneumonoultramicroscopicsilicovolcanoconiosis [45 letters](thought it was going to be shorter hahahhahahahahah)
    elif len(owlichu) >= 45:
        return render_template("Restriction3_Owlichu.html")
    # RESTRICTION #4: Can't exist in current english dictionary (calling API to check)
    request_dict_api = get_word_definition(owlichu)

    if request_dict_api != None:
        if request_dict_api[1] == None:
            request_dict_api[1] = 'We do not have a definition for this word, but it exists. BAZINGA'
        return render_template("Restriction4_Owlichu.html", word_info = request_dict_api) #, dict_word = request_dict_api
    

    # RESTRICTION #5: a word is considered invalid if it already exists in the Owlichu database. In other words, a word can only be added to the database if it is unique and does not already exist in the database.
    check_owlichu = f'''
    SELECT word, definition 
    FROM words
    WHERE word = '{owlichu}';
    '''
    # Connecting to database to check if word exists
    with engine.connect() as connection: 
        result = connection.execute(check_owlichu).fetchone()
        if result:
            return render_template("/Restriction5_Owlichu.html", owlichu_info = result)
    
    session['owlichu'] = owlichu
    return render_template("Definition_Owlichu.html")

# ========================================================================= #
# definition() route: once a word is introduced, users can introduce a meaning to the word 
@app.route("/handle_definition", methods = ["POST"])
def handle_definition(): 
    owlichu_definichu = request.form["owly"]
    # RESTRICTION 1: definition can't be empty (can't have zero characters)
    if len(owlichu_definichu) == 0:
        return render_template("Empty_Definition_Owlichu.html")
    # RESTRICTION 2: definition can't be longer than 300 words
    elif len(owlichu_definichu) > 300:
        return render_template("Too_Long_Definition_Owlichu.html")

    # RESTRICTION 3: definition can't have weird characters
    for x in owlichu_definichu:
            if not (x.isalpha() or x.isspace()): 
                return render_template("Only_Letters_Owlichu.html")
    else:
        session["owlichu_definichu"] = owlichu_definichu
        return redirect("/handle_owlichu_to_database")

# ========================================================================= #
# handle_owlichu_to_database() route: this route is in charge of storing the owlichu into the database
@app.route("/handle_owlichu_to_database")
def handle_owlichu_to_database(): 
    my_owlichu = {
        'owlichu': session['owlichu'],
        'owlichu_definichu': session['owlichu_definichu'],
        'user_id': session['user_id'],
        'date': datetime.utcnow()
    }

    add_owlichu = f""" 
     INSERT INTO words (word, definition, user_id, date)
        VALUES (
        '{my_owlichu["owlichu"]}',
        '{my_owlichu["owlichu_definichu"]}',
        '{my_owlichu["user_id"]}',
        '{my_owlichu["date"]}'
    )
    """

    #Connecting to the database and inserting information
    with engine.connect() as connection: 
        connection.execute(add_owlichu)

        return redirect("/congratulations")

# ========================================================================= #
# congratulations() route: shows user a word has been created
@app.route("/congratulations")
def congratulations():
    my_owlichu = [session["username"], session['email'], datetime.utcnow(), session['owlichu'], session['owlichu_definichu']]
    return render_template("Congratulations_Owlichu.html", word_info = my_owlichu)

# ========================================================================= #
# certificate() route: shows users certification
@app.route("/certificate/<username>/<word>")
def certificate(username, word):
    my_owlichu = [username, session['email'], datetime.utcnow(), word, session['owlichu_definichu']]
    return render_template("Certification_Owlichu.html", word_info = my_owlichu)

# ========================================================================= #
#login() route: loads the login page 
@app.route("/login")
def login():
    return render_template("Login_Owlichu.html")

# ========================================================================= #
#sign_in() route: handles login for users
@app.route('/sign_in', methods = ["POST"])
def sign_in():
    #Getting data from HTML form
    username = request.form["username"]
    password = request.form["password"]

    login_query = f"""
        SELECT * 
        FROM users
        WHERE username = "{username}";"""

    
    #Connecting to the database and getting login info
    with engine.connect() as connection: 
        users_info = connection.execute(login_query).fetchone()
        password_matches = check_password_hash(users_info[3], password)

        if users_info and password_matches:
            session["username"] = username
            session["user_id"] = users_info[0]
            session['email'] = users_info[2]
            return redirect("/")
    
        return redirect("/unauthorized")

# ========================================================================= #
#unauthorized() route: if username or password not correct, load this page
@app.route('/unauthorized')
def unauthorized():
    return render_template("Unauthorized_Owlichu.html"), 403

# ========================================================================= #
#identification() route: enables users whether to log in or register if they do not have an account 
@app.route("/identification")
def identification():
    return render_template("Identification_Owlichu.html")

# ========================================================================= #
#registration() route: enables users to create an account
@app.route("/registration")
def registration():
    return render_template("Registration_Owlichu.html")

# ========================================================================= #
#register_user() route: handles registration for users loading their information to database
@app.route("/register_user", methods = ["POST"])
def register_user():
    #Getting data from HTML form
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    rep_password = request.form["rep_password"]
    valid_user_info = [username, email]

    # if password and repeate password fields don't match redirect to "Try_Password_Again_Owlichu.html" so that user tries again
    if password != rep_password:
        return render_template("Try_Password_Again_Owlichu.html", user_info = valid_user_info)

    hashed_password = generate_password_hash(password)

    # QUERY: checking if there exists a user with that username
    username_valid_query = f"""
        SELECT username
        FROM users
        WHERE username = "{username}";
        """
    # QUERY: checking if there exists a user with that username
    email_valid_query = f"""
        SELECT email
        FROM users
        WHERE email = "{email}";
        """
    # QUERY: inserting registration information to create a new user 
    register_query = f""" 
     INSERT INTO users (username, email, password)
        VALUES (
        '{username}',
        '{email}',
        '{hashed_password}'
    )
    """
    #Connecting to the database and checking for usernames
    with engine.connect() as connection: 
        check_valid_username = connection.execute(username_valid_query).fetchone()
        if check_valid_username:
            return render_template("Try_Username_Again_Owlichu.html", user_info = valid_user_info)
        
        check_valid_email = connection.execute(email_valid_query).fetchone()
        if check_valid_email:
            return render_template("Try_Email_Again_Owlichu.html", user_info = valid_user_info)
        
    #Connecting to the database and inserting information
    with engine.connect() as connection: 
        connection.execute(register_query)

        return redirect("/login")

# ========================================================================= #
#register_user() route: handles registration for users loading their information to database
@app.route("/user_profile")
def user_profile():
    if 'username' not in session: 
        return redirect("/identification")
    else: 

        get_owlichus = f"""
        SELECT *
        FROM words
        WHERE user_id = {session['user_id']}
        """
        #Connecting to the database and inserting information
        with engine.connect() as connection: 
            users_words = connection.execute(get_owlichus).fetchall()

        profile_info = [session['username'], session['email'], users_words]

        return render_template("User_Profile_Owlichu.html", profile_info = profile_info)

# =========================================================================
#sign_out() route: signs user out of session
@app.route("/signout")
def sign_out():
    if 'username' in session: 
        session.pop('username')
        return redirect('/')
    else: 
        return redirect('identification')
    

if __name__ == '__main__':
    app.run(debug=True, port=8080)


