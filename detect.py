import cv2

# Charger le modèle de détection de visage pré-entrainé
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Ouvrir la caméra
cap = cv2.VideoCapture(0)

while True:
    # Lire une image depuis la caméra
    ret, frame = cap.read()

    # Convertir l'image en niveaux de gris pour la détection du visage
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Dessiner un cadre autour de chaque visage détecté
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Afficher l'image avec les cadres de visage
    cv2.imshow('Face Detection', frame)

    # Quitter la boucle si la touche 'q' est pressée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()