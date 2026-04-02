# 🌫️ Single Image & Video Dehazing via Dark Channel Prior

**Computer Vision Final Year Project**  
*Developed by Sukesh Reddy*

This repository contains a Flask-based web application implementing an environmental dehazing system. The core algorithm estimates atmospheric light and transmission maps using the **Dark Channel Prior (DCP)** method, allowing the system to recover geometry and intrinsic contrast from static imagery, video files, and real-time streams without relying on external deep learning checkpoints.

---

## 📁 Project Structure

```text
DeHazer/
├── app.py                 # Main Flask server and API routing architecture
├── model/
│   └── image_dehazer.py   # Core OpenCV logic (DCP Algorithm implementation)
├── static/
│   ├── uploads/           # Raw input payload directory
│   └── processed/         # Solved outputs with UUIDs
├── templates/
│   ├── home.html          # Web application UI views
│   └── ...
├── requirements.txt
└── README.md
```

---

## 🚀 Key Academic Features

- **Dark Channel Prior Implementation**: Realization of physical scattering models entirely mathematically.
- **Robust Concurrency**: Safely handles file ingest via UUID normalization and backend thread management.
- **Automatic Garbage Collection**: Employs a daemon worker thread to prevent disk overflows during inference validation.
- **Academic Dashboard UI**: Sleek, distraction-free HTML/CSS interface focused on result evaluation.

---

## 🛠️ Environment Prerequisites

- Python 3.7+
- Flask >= 3.0.0
- OpenCV (`opencv-python`)
- Werkzeug >= 3.0.0
- NumPy

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧠 Methodology Detail

The algorithm logic resides entirely within `model/image_dehazer.py`. The fundamental pipeline includes:
1. **Airlight Estimation**: Calculating global atmospheric light using morphological erosions on the input matrices.
2. **Transmission Matrix Formulation**: Solving boundary conditions using the Kirsch Edge Filter bank for localized approximations.
3. **Radiance Recovery**: Generating the definitive Haze-corrected output structure array.

It returns:
```python
dehazed_image_matrix, transmission_map
```

---

## 🖥️ Running the Validation Server

Initialize the local Flask environment:

```bash
python app.py
```

The application interface will bind to standard localhost port 5000:
`http://127.0.0.1:5000/`

---

## 🧑‍💻 Author

This repository represents the culmination of a Computer Vision Final Year Project crafted by **Sukesh Reddy**. 
