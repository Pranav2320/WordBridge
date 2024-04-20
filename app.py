from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy
from googletrans import Translator, LANGUAGES
import speech_recognition as sr
from gtts import gTTS
import os
from forms import LoginForm,RegistrationForm  

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tWqqAeuhvq'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
  
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create an instance of the LoginForm
    if form.validate_on_submit():  # Check if the form is submitted and valid
        # Handle form submission (login logic)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)  # Pass the form object to the template

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Create an instance of the RegisterForm
    if form.validate_on_submit():  # Check if the form is submitted and valid
        # Handle form submission (registration logic)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)  # Pass the form object to the template

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('login'))

@app.route('/users')
def users():
    users = User.query.all()  # Fetch all users from the database
    return render_template('users.html', users=users)

language_codes = list(LANGUAGES.keys())
language_names = list(LANGUAGES.values())

#<-------------------------------------------------  Index Page  ------------------------------------------------------------------------->
@app.route('/')
def index():
    return render_template('index.html')
#<-----------------------------------       Text - to - Text   -----------------------------------------------------------------------------------> 

@app.route('/text-to-text', methods=['GET'])
def text_to_text():
    return render_template('text-to-text.html', source_languages = zip(language_codes, language_names), target_languages=zip(language_codes, language_names))

@app.route('/translate', methods=['POST'])
def translate_text():
    text_to_translate = request.form.get('text')
    source_language = request.form.get( 'source_language' )
    target_language = request.form.get( 'target_language' )

    if not text_to_translate or not source_language or not target_language:
        return jsonify({'translation': 'Please provide valid input.'})

    translator = Translator()
    try:
        translation = translator.translate(text_to_translate, src=source_language, dest=target_language).text
    except Exception as e:
        print(f"Translation error: {e}")
        translation = "Translation failed. Please try refreshing the page."

    return jsonify({'translation': translation})


    

#<-------------------------------------        Text-to-speech              ----------------------------------------------------------------------->
@app.route('/text-to-speech', methods=['GET'])
def text_to_speech():
    return render_template('text_to_audio.html', source_languages = zip(language_codes, language_names), target_languages=zip(language_codes, language_names))

@app.route('/translate-text-to-audio', methods=['POST'])
def translate_text_to_audio():
    text_to_translate = request.form.get('text')
    source_language = request.form.get('source_language')
    target_language = request.form.get('target_language')

    if not text_to_translate or not source_language or not target_language:
        return jsonify({'translation': 'Please provide valid input.'})

    translator = Translator()

    try:
        translated_text = translator.translate(text_to_translate, dest=target_language).text
        
    except Exception as e:
        print(f"Translation error: {e}")
       



#<---------------------------------------------------- Audio-to-Text ----------------------------------------------------------------->

@app.route('/speech-to-text', methods=['GET'])
def speech_to_text():
    return render_template('audio_to_text.html', source_languages = zip(language_codes, language_names), target_languages=zip(language_codes, language_names))

@app.route('/translate-audio-to-text', methods=['POST'])
def translate_audio_to_text():
    try:
        selected_language = request.form['source_language']
        audio_data = request.form['text']

        recognizer = sr.Recognizer()

        # Recognize speech using the selected language
        with sr.AudioData(audio_data, 44100) as source:
            text_result = recognizer.recognize_google(audio_data, language=f'{selected_language}-IN')

        return jsonify({'translation': text_result})
    except Exception as e:
        return jsonify({'error': str(e)})

#<---------------------------------------------------- Audio-to-Audio ----------------------------------------------------------------->
@app.route('/audio-to-audio', methods=['GET'])
def audio_to_audio():
    return render_template('audio.html', source_languages = zip(language_codes, language_names), target_languages=zip(language_codes, language_names))

@app.route('/translate-audio-to-audio', methods=['POST'])
def translate_audio_to_audio():
    try:
        # Get the audio data from the request
        audio_data = request.form['audio_data']
        source_language = request.form['source_language']
        target_language = request.form['target_language']

        if not audio_data or not source_language or not target_language:
            return jsonify({'translation': 'Please provide valid input.'})

       
        recognizer = sr.Recognizer()
        with sr.AudioData(audio_data, 44100) as source:
            transcribed_text = recognizer.recognize_google(source, language=source_language)

        translator = Translator()
        translated_text = translator.translate(transcribed_text, src=source_language, dest=target_language).text


        speak = gTTS(text=translated_text, lang=target_language, slow=False)
        audio_filepath = os.path.join('static', 'audio', f'translated_audio_{source_language}_to_{target_language}.mp3')
        speak.save(audio_filepath)

        return jsonify({'translation': translated_text, 'audio_url': audio_filepath})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
