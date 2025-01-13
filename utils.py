from deepface import DeepFace
import cv2

def process_image(image_path):
    """
    Detecta emociones en las caras de una imagen.
    """
    try:
        # Leer la imagen
        img = cv2.imread(image_path)
        
        # Analizar la imagen con DeepFace
        analysis = DeepFace.analyze(img_path=image_path, actions=['emotion'])

        # Extraer datos relevantes
        emotions_detected = []
        for face in analysis:
            emotions_detected.append({
                "dominant_emotion": face["dominant_emotion"],
                "emotion_scores": face["emotion"]
            })

        # Devuelve las emociones detectadas
        return {"emotions": emotions_detected}

    except Exception as e:
        return {"error": str(e)}
