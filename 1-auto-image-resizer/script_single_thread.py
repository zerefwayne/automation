import os
from PIL import Image, UnidentifiedImageError
import uuid
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from threading import Thread

start = -1
root_dir = os.getcwd()
pending_dir = os.path.join(os.getcwd(), 'pending')

if not os.path.exists(pending_dir):
    os.mkdir(pending_dir)

converted_dir = os.path.join(os.getcwd(), 'converted')

if not os.path.exists(converted_dir):
    os.mkdir(converted_dir)

allowed_extensions = ['.jpg', '.png', '.jpeg', '.svg']


class FileCreatedHandler(FileSystemEventHandler):
    def on_created(self, event):
        global start
        if start == -1:
            start = time.time()
        prev_size = -1
        while prev_size != os.path.getsize(event.src_path):
            prev_size = os.path.getsize(event.src_path)
            time.sleep(0.1)

        process_image(event.src_path)


def process_image(image_path):
    # Sleeps for 1 second to simulate large file
    time.sleep(1)
    print("Processing Image:", image_path)
    print(os.getcwd())

    unique_file_code = str(uuid.uuid4()).split('-')[-1]
    image_ext = os.path.splitext(image_path)[-1]

    if image_ext not in allowed_extensions:
        print("Invalid extension:", image_path)
        return

    try:
        image = Image.open(image_path)
    except UnidentifiedImageError:
        print("Cannot identify image: {}".format(image_path))
        return

    os.remove(image_path)

    width, height = image.size

    ratios = [75, 50, 25]

    reduced_images = []

    for ratio in ratios:
        new_width = int(width * (ratio / 100))
        new_height = int(height * (ratio / 100))

        new_image = image.copy()
        new_image.thumbnail((new_width, new_height))
        reduced_images.append(dict({"ratio": ratio, "image": new_image}))

    original_file_name = unique_file_code + image_ext

    converted_path = os.path.join(converted_dir, unique_file_code)

    if not os.path.exists(converted_path):
        print("Creating new directory: {}".format(converted_path))
        os.mkdir(converted_path)

    image.save(os.path.join(converted_path, original_file_name))

    for conv_image in reduced_images:
        ratio_file_name = unique_file_code + "_" + str(conv_image['ratio']) + image_ext
        ratio_abs_path = os.path.join(converted_path, ratio_file_name)
        conv_image['image'].save(ratio_abs_path)


def process_pending_images():
    files = os.listdir(pending_dir)

    for image_file in files:
        image_path = os.path.join(pending_dir, image_file)
        if os.path.isfile(image_path):
            process_image(image_path)

    print("\nAll pending images processed. Starting watchdog!\n")


if __name__ == "__main__":

    process_pending_images()

    event_handler = FileCreatedHandler()
    observer = Observer()
    observer.schedule(event_handler, path=pending_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.unschedule_all()
        observer.stop()
    observer.join()
