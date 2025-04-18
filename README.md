
# 🌫️ Image & Video Dehazer (Flask App)

This is a Flask-based web application for removing haze from images, videos, and real-time webcam input using a custom dehazing model.

---

## 📁 Project Structure

```
DeHazer/
├── app.py
├── model/
│   └── image_dehazer.py
├── static/
│   ├── uploads/
│   └── processed/
├── templates/
│   ├── home.html
│   ├── contact.html
│   ├── about.html
│   ├── image_dehazer.html
│   └── video_dehazer.html
├── README.md
```

---

## 🚀 Features

- Upload and dehaze **images**
- Upload and dehaze **videos**
- Real-time webcam stream dehazing
- Simple UI with separate pages for image, video, and live dehazing

---

## 🛠️ Requirements

- Python 3.7+
- Flask
- OpenCV
- Werkzeug

Install the required packages with:

```bash
pip install -r requirements.txt
```

### Example `requirements.txt`

```
Flask
Werkzeug
opencv-python
numpy

```

---

## 🔧 Configuration

Modify the folder paths in `app.py` if needed:

```python
app.config['UPLOAD_FOLDER'] = r'D:\RnD, CCA\Parichay 2024\DeHazer\static\uploads'
app.config['PROCESSED_FOLDER'] = r'D:\RnD, CCA\Parichay 2024\DeHazer\static\processed'
```

These folders will be created automatically if they don't exist.

---

## 🧠 Haze Removal Logic

The dehazing logic is handled by the `remove_haze()` function located in:

```
model/image_dehazer.py
```

This should return a tuple of:
```python
dehazed_image, other_output
```

You can customize this function as needed based on your haze removal algorithm.

---

## 🖥️ Running the App

Start the Flask server:

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000/
```

---

## 🌐 Available Routes

| Route                 | Description                        |
|----------------------|------------------------------------|
| `/` or `/home`       | Home page                          |
| `/image_dehazer`     | Upload and dehaze an image         |
| `/video_dehazer`     | Upload and dehaze a video          |
| `/realtime_dehazer`  | Real-time webcam dehazing preview  |
| `/about`             | About page                         |
| `/contact`           | Contact page                       |

---

## 📸 Output

- Uploaded media is stored in `static/uploads`
- Dehazed outputs are saved to `static/processed`
- Processed results are shown on the respective result pages

---

## 🧑‍💻 Author

Built with ❤️ by Sukesh Reddy
Feel free to personalize this project and improve upon it.

---
