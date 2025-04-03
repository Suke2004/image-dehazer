from flask import Flask, render_template, request, redirect, url_for, send_file,Response
import cv2
import os
from werkzeug.utils import secure_filename
from model.image_dehazer import remove_haze

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r'D:\RnD, CCA\Parichay 2024\DeHazer\static\uploads'
app.config['PROCESSED_FOLDER'] = r'D:\RnD, CCA\Parichay 2024\DeHazer\static\processed'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'bmp', 'mp4'}

# Ensure upload and processed folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/image_dehazer', methods=['GET', 'POST'])
def image_dehazer_route():
    original_image = None
    dehazed_image = None
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            haze_img = cv2.imread(filepath)
            original_image = url_for('static', filename='uploads/' + filename)
            dehazed_img, _ = remove_haze(haze_img)

            
            # Save the processed image
            processed_filename = 'processed_' + filename
            processed_filepath = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
            cv2.imwrite(processed_filepath, dehazed_img)
            dehazed_image = url_for('static', filename='processed/' + processed_filename)
            
    return render_template('image_dehazer.html', original_image=original_image, dehazed_image=dehazed_image)


@app.route('/video_dehazer', methods=['GET', 'POST'])
def video_dehazer_route():
    original_video = None
    dehazed_video = None
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the video
            cap = cv2.VideoCapture(filepath)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out_filename = 'processed_' + filename
            out_filepath = os.path.join(app.config['PROCESSED_FOLDER'], out_filename)
            out = None
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if out is None:
                    height, width, layers = frame.shape
                    out = cv2.VideoWriter(out_filepath, fourcc, 20.0, (width, height))
                HazeCorrectedImg, _ = remove_haze(frame)
                out.write(HazeCorrectedImg)
            
            cap.release()
            out.release()
            
            original_video = url_for('static', filename='uploads/' + filename)
            dehazed_video = url_for('static', filename='processed/' + out_filename)
            
    return render_template('video_dehazer.html', original_video=original_video, dehazed_video=dehazed_video)


@app.route('/realtime_dehazer')
def realtime_dehazer():
    def gen():
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Processing dehazed frame
            HazeCorrectedImg, _ = remove_haze(frame)  # Assuming remove_haze is defined elsewhere
            _, dehazed_frame = cv2.imencode('.jpg', HazeCorrectedImg)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + dehazed_frame.tobytes() + b'\r\n\r\n')
        cap.release()
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
    

if __name__ == '__main__':
    app.run(debug=True)
