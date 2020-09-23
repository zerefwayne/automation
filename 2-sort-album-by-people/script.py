#! /usr/bin/env python3

import os
import sys
import face_recognition
import cv2
import numpy as np
import shutil

known_people = []
original_image_path = os.path.join(os.getcwd(), 'photos/friends.jpg')


def read_image(image_name, image_path):

    image = face_recognition.load_image_file(image_path)
    name = image_name.split('.')[0]

    return dict({"name": name, "image": image})


def encode_people(people):

    print("Learning faces of {} people".format(len(people)))

    for i in range(len(people)):

        person = people[i]
        print("Processing face of {} ({}/{})".format(person['name'], i+1, len(people)))
        person["encoding"] = face_recognition.face_encodings(person['image'])[0]

    print("Successfully learnt all faces.")


def recognize_in_image(people, image_path):

    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    known_face_encodings = []
    known_face_names = []

    found_people = []

    for p in people:
        known_face_encodings.append(p['encoding'])
        known_face_names.append(p['name'])

    for face_encoding in face_encodings:

        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        best_match_index = -1
        best_match_name = "unknown"

        if True in matches:
            best_match_index = matches.index(True)
            best_match_name = known_face_names[best_match_index]
        else:
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = int(np.argmin(face_distances))
            best_match_name = known_face_names[best_match_index]

        if best_match_name != "unknown":
            found_people.append(best_match_name)

    return found_people


def add_image_to_directories(image_path, names):

    curr_dir = os.getcwd()
    sorted_album_dir = os.path.join(curr_dir, "testing/album")

    if not os.path.exists(sorted_album_dir):
        os.mkdir(sorted_album_dir)

    for name in names:
        name_path = os.path.join(sorted_album_dir, name)

        if not os.path.exists(name_path) or not os.path.isdir(name_path):
            os.mkdir(name_path)

        shutil.copy(image_path, name_path)


if __name__ == "__main__":

    known_dir = os.path.join(os.getcwd(), 'known')
    photos_dir = os.path.join(os.getcwd(), 'photos')

    if not os.path.exists(known_dir) or not os.path.exists(photos_dir):
        print("Directory of known people: {} doesn't exist.".format('known'))
        sys.exit(1)

    for person in os.listdir(known_dir):

        path = os.path.join(known_dir, person)
        person_detail = read_image(person, path)
        known_people.append(person_detail)

    encode_people(known_people)

    print("Sorting images")

    found_photos = os.listdir(photos_dir)

    for i, photo in zip(range(len(found_photos)), found_photos):

        print("Processing ({}/{}): {}".format(i+1, len(found_photos), photo))

        original_image_path = os.path.join(photos_dir, photo)

        recognized_names = recognize_in_image(known_people, original_image_path)

        add_image_to_directories(original_image_path, recognized_names)

    print("Successfully sorted all photos.")
