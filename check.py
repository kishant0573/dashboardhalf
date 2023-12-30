from flask import Flask, render_template, request,jsonify
from openpyxl import load_workbook

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('check.html')

@app.route('/convert', methods=['POST'])
def convert():
    duration = request.form['duration']
    # audio_files = request.form['audio_files']
    asr_solutions = request.form['asr_solutions']
    # transliteration = request.form['transliteration']

    excel_file_path = 'Book1.xlsx'

    try:
        workbook = load_workbook(filename=excel_file_path)
        sheet = workbook.active

        last_row = sheet.max_row + 1

        sheet.cell(row=last_row, column=1).value = duration
        # sheet.cell(row=last_row, column=3).value = audio_files
        sheet.cell(row=last_row, column=2).value = asr_solutions
        # sheet.cell(row=last_row, column=4).value = transliteration

        workbook.save(filename=excel_file_path)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
