from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import uuid
from deepface import DeepFace
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de carpetas
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}  # Extensiones permitidas

def allowed_file(filename):
    """
    Verifica si el archivo tiene una extensión válida.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """
    Página principal que muestra el formulario para subir imágenes.
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Ruta para cargar la imagen y analizar la emoción.
    """
    if 'image' not in request.files:
        return jsonify({"error": "No se encontró ninguna imagen en la solicitud"}), 400

    file = request.files['image']

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Formato de archivo no permitido. Solo se aceptan: JPG, JPEG, PNG."}), 400

    # Guardar la imagen en el servidor con un nombre único
    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Análisis de emoción con DeepFace
        analysis = DeepFace.analyze(img_path=filepath, actions=['emotion'], enforce_detection=False)

        # Manejar si `analysis` es una lista o un diccionario
        if isinstance(analysis, list):
            analysis = analysis[0]  # Usar el primer elemento si es una lista

        if 'dominant_emotion' in analysis:
            emotion = analysis['dominant_emotion']
        else:
            emotion = "No se pudo detectar una emoción dominante"

        return jsonify({
            "result": f"Emoción detectada: {emotion}",
            "image": f"/static/images/{filename}"
        })
    except Exception as e:
        return jsonify({"error": f"Error al procesar la imagen: {str(e)}"}), 500

@app.route('/static/images/<filename>')
def get_image(filename):
    """
    Ruta para servir las imágenes guardadas.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
