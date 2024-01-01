from flask import Flask, render_template, request, jsonify
import csv
import os
import wave

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('check4.html')

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

@app.route('/save-all-data', methods=['POST'])
def save_all_data():
    data = request.get_json()

    table_data = data.get('tableData', [])

    headers = table_data[0].keys() if table_data else []

    with open('blank.csv', 'w', newline='') as file:  # Change the file name to 'black.csv'
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(table_data)
    return jsonify({'success': True, 'message': 'Data saved to black.csv file successfully!'})

if __name__ == '__main__':
    app.run(debug=True)