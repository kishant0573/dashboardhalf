from flask import Flask, render_template, jsonify
import os
import wave

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('check3.html')

@app.route('/static/wav')
def get_static_wav_files():
    audio_files = []
    static_dir = os.path.join(app.root_path, 'static')
    for filename in os.listdir(static_dir):
        if filename.endswith('.wav'):
            audio_path = os.path.join(static_dir, filename)
            duration = get_audio_duration(audio_path)
            audio_files.append({'file': f'/static/{filename}', 'duration': duration})
    return jsonify({'audioFiles': audio_files})

def get_audio_duration(audio_path):
    try:
        with wave.open(audio_path, 'rb') as audio:
            frames = audio.getnframes()
            rate = audio.getframerate()
            duration = frames / float(rate)
            return round(duration, 2)
    except Exception as e:
        print(f"Error getting duration for {audio_path}: {e}")
        return 0.0

if __name__ == '__main__':
    app.run(debug=True)
