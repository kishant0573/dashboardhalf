from flask import Flask, render_template, jsonify, request
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

    if not table_data:
        return jsonify({'success': False, 'message': 'No data to save.'})

    # Ensure the audioPath key exists in the tableData
    if 'audioPath' not in table_data[0]:
        return jsonify({'success': False, 'message': 'Audio file path missing or incorrect structure.'})

    try:
        audio_path = table_data[0]['audioPath']
        file_name = os.path.basename(audio_path).replace('.wav', '.csv')

        csv_filename = os.path.join(os.getcwd(), file_name)

        headers = table_data[0].keys()

        with open(csv_filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(table_data)
        
        return jsonify({'success': True, 'message': f'Data saved to {csv_filename} successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error saving data: {e}'})

if __name__ == '__main__':
    app.run(debug=True)
