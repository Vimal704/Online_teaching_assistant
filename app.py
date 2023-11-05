from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
import re
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
f = open("wordlist.10000.txt", "r")
wordlist = f.read().split()
wordlist+=','+'\''+'\"'+'.'+'+'+'1'+'2'+'3'+'4'+'5'+'6'+'7'+'8'+'9'+'0'+' '+'-'

app = Flask(__name__)

# Configuration for file upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
errors=[]
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(app.config['UPLOAD_FOLDER'] + '/' + filename)
        img = Image.open(app.config['UPLOAD_FOLDER'] + '/' + filename)
        text = pytesseract.image_to_string(img)

        errortext = re.sub('[^A-Za-z0-9 ]+', '', text)
        errortext = errortext.lower().split(' ')
        for t in errortext:
            if(t not in wordlist):
                errors.append(t)
        return jsonify({'text': text})
    else:
        return jsonify({'error': 'Invalid file type'})

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/get_text')
def get_text():
    text = errors
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)
