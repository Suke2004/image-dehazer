from flask import Flask, render_template, request, redirect, url_for, send_file, Response
import cv2
import os
import uuid
import time
import threading
from werkzeug.utils import secure_filename
from model.image_dehazer import remove_haze

app = Flask(__name__)
# Security baseline
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['PROCESSED_FOLDER'] = './static/processed'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'bmp', 'mp4'}

# Ensure upload and processed folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# --------------------------------------------------------------------------
# Background Cleanup Task
# --------------------------------------------------------------------------
def cleanup_old_files():
    """Background thread to remove files older than 1 hour to prevent disk fill-up."""
    while True:
        try:
            current_time = time.time()
            # 3600 seconds = 1 hour
            age_limit = 3600 
            folders_to_clean = [app.config['UPLOAD_FOLDER'], app.config['PROCESSED_FOLDER']]
            
            for folder in folders_to_clean:
                for filename in os.listdir(folder):
                    # We ignore hidden files (like .placeholder if tracking is used)
                    if filename.startswith('.'):
                        continue
                    
                    filepath = os.path.join(folder, filename)
                    if os.path.isfile(filepath):
                        file_age = current_time - os.path.getctime(filepath)
                        if file_age > age_limit:
                            os.remove(filepath)
                            print(f"Cleanup: Removed {filepath}")
        except Exception as e:
            print(f"Cleanup thread error: {e}")
            
        # Sleep for 30 minutes before next check
        time.sleep(1800)

# Start cleanup thread as a daemon automatically on launch
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()
# --------------------------------------------------------------------------

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(filename):
    """Appends a unique UUID to the secure filename to prevent race conditions & overwrites."""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    base = secure_filename(filename.rsplit('.', 1)[0]) if '.' in filename else secure_filename(filename)
    unique_id = uuid.uuid4().hex[:8] # Short 8 char uuid is sufficient
    return f"{base}_{unique_id}.{ext}" if ext else f"{base}_{unique_id}"

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
            unique_filename = generate_unique_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Application of AI Model
            haze_img = cv2.imread(filepath)
            if haze_img is not None:
                original_image = url_for('static', filename='uploads/' + unique_filename)
                dehazed_img, _ = remove_haze(haze_img)
                
                # Save the processed image
                processed_filename = 'processed_' + unique_filename
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
            unique_filename = generate_unique_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            try:
                # Process the video
                cap = cv2.VideoCapture(filepath)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out_filename = 'processed_' + unique_filename
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
                if out is not None:
                    out.release()
                
                original_video = url_for('static', filename='uploads/' + unique_filename)
                dehazed_video = url_for('static', filename='processed/' + out_filename)
            except Exception as e:
                print(f"Error processing video: {e}")
            
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
            HazeCorrectedImg, _ = remove_haze(frame)
            _, dehazed_frame = cv2.imencode('.jpg', HazeCorrectedImg)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + dehazed_frame.tobytes() + b'\r\n\r\n')
        cap.release()
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
    

if __name__ == '__main__':
    # Threaded defaults to True in Flask, improving local concurrency routing 
    app.run(debug=True, threaded=True)
