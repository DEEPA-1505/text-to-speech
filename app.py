from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
from gtts import gTTS
import os
import uuid
import re

app = Flask(__name__)
app.secret_key = 'supersecret'  # Needed to use sessions

OUTPUT_FOLDER = 'output'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def sanitize_text(text):
    return re.sub(r'[^\w\s.,?!]', '', text)

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = session.pop('audio_file', None)  # Retrieve and clear

    if request.method == 'POST':
        text = request.form.get('text', '')
        lang = request.form.get('lang', 'en')

        if text.strip():
            try:
                clean_text = sanitize_text(text)
                filename = f"{uuid.uuid4()}.mp3"
                filepath = os.path.join(OUTPUT_FOLDER, filename)

                # Generate speech
                tts = gTTS(clean_text, lang=lang)
                tts.save(filepath)

                # Save filename in session and redirect
                session['audio_file'] = filename
                return redirect(url_for('index'))

            except Exception as e:
                return f"<h3>Error: {e}</h3>", 500

    return render_template('index.html', audio_file=audio_file)

@app.route('/output/<filename>')
def serve_audio(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)
