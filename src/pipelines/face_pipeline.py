import numpy as np
from insightface.app import FaceAnalysis

from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_lib_models():
    app = FaceAnalysis(name="buffalo_sc", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(640, 640))
    return app


def get_face_embeddings(image_np):
    app = load_lib_models()
    faces = app.get(image_np)
    embeddings = [face.normed_embedding for face in faces]
    return embeddings


@st.cache_resource
def get_trained_model():

    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get('face_embedding')

        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) == 0:
        return 0

    # clf -> SVC model trained on the face embeddings of students with their student_id as labels
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    try:
        clf.fit(X, y)
    except ValueError:
        pass

    return {"clf": clf, "X": X, "y": y}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):

    encodings = get_face_embeddings(class_image_np)

    detected_student = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], len(encodings)

    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:

        if len(all_students) >= 2:
            predicted_id = int(
                clf.predict([encoding])[0]
            )

        else:
            predicted_id = int(
                all_students[0]
            )

        student_embedding = X_train[
            y_train.index(predicted_id)
        ]

        # ArcFace embeddings are normalized; use cosine similarity instead of L2 distance
        cosine_sim = np.dot(student_embedding, encoding) / (
            np.linalg.norm(student_embedding) * np.linalg.norm(encoding)
        )

        resemblance_threshold = 0.4  # ArcFace similarity threshold (tune as needed)

        if cosine_sim >= resemblance_threshold:
            detected_student[predicted_id] = True

    return (
        detected_student,
        all_students,
        len(encodings)
    )