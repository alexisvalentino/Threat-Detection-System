import os
import pickle
import cv2
import face_recognition

# Initialize the known faces dictionary
known_faces = {}

# Iterate through the dataset folder
dataset_path = "C:/Users/ACER/Desktop/Real time threat detection/homeowner"
print("Processing dataset...")

for person_name in os.listdir(dataset_path):
    print(f"Processing {person_name}...")
    person_path = os.path.join(dataset_path, person_name)
    if os.path.isdir(person_path):
        known_faces[person_name] = []
        
        # Iterate through the images of each person
        for image_name in os.listdir(person_path):
            print(f"Processing image {image_name}...")
            image_path = os.path.join(person_path, image_name)
            image = cv2.imread(image_path)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Compute the face embedding for each image
            face_locations = face_recognition.face_locations(rgb_image, model="cnn")
            if face_locations:
                face_embedding = face_recognition.face_encodings(rgb_image, face_locations)[0]
                known_faces[person_name].append(face_embedding)

# Save the known faces model as a pickle file
known_faces_model_path = "C:/Users/ACER/Desktop/Real time threat detection/models/home_owners.pkl"
os.makedirs(os.path.dirname(known_faces_model_path), exist_ok=True)
print("Saving known faces model...")

with open(known_faces_model_path, 'wb') as f:
    pickle.dump(known_faces, f)

print("Done.")