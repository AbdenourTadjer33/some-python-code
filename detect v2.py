import cv2

# Charger le modèle de détection de visage pré-entrainé
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Charger le modèle de détection de clignements d'yeux pré-entrainé
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Charger le modèle de détection de clignements d'yeux pré-entrainé
eye_blink_net = cv2.dnn.readNetFromTensorflow('models/eye_blink_detection.pb')


# Ouvrir la caméra
cap = cv2.VideoCapture(0)

while True:
    # Lire une image depuis la caméra
    ret, frame = cap.read()

    # Convertir l'image en niveaux de gris pour la détection du visage
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Pour chaque visage détecté
    for (x, y, w, h) in faces:
        # Dessiner un cadre autour du visage
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Région d'intérêt pour le visage (ROI)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Détecter les yeux dans le ROI
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Pour chaque œil détecté
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

            eye_roi = roi_gray[ey:ey+eh, ex:ex+ew]

            eye_roi = cv2.resize(eye_roi, (64, 64))
            eye_roi = eye_roi / 255.0
            eye_roi = eye_roi.reshape(1, 64, 64, 1)

            predictions = eye_blink_net.predict(eye_roi)

            # Si les yeux sont fermés (prédiction > 0.5), changer la couleur du cadre en rouge
            if predictions[0][0] > 0.5:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)

    # Afficher l'image avec les cadres de visage et d'yeux
    cv2.imshow('Eye Blink Detection', frame)

    # Quitter la boucle si la touche 'q' est pressée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()