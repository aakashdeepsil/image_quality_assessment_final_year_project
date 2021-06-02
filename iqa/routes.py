from iqa import app
from iqa import UPLOAD_FOLDER
from iqa.main import main
import os
import shutil
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# TODO
# YOU NEED TO CHANGE THESE PATHS ACCORDING TO YOUR SYSTEM
GOOD_IMAGES_PATH = 'E:/FinalYearProject/good_images'
BAD_IMAGES_PATH = 'E:/FinalYearProject/bad_images'
IMAGE_SUGGESTED_FOR_DELETION_PATH = 'E:/FinalYearProject/image_suggested_for_deletion'

good_images = []
bad_images = []
image_suggested_for_deletion = []

def check_directory_exists(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global good_images
    global bad_images
    global image_suggested_for_deletion

    check_directory_exists(UPLOAD_FOLDER)
    check_directory_exists(GOOD_IMAGES_PATH)
    check_directory_exists(BAD_IMAGES_PATH)
    check_directory_exists(IMAGE_SUGGESTED_FOR_DELETION_PATH)

    os.mkdir(UPLOAD_FOLDER)
    os.mkdir(GOOD_IMAGES_PATH)
    os.mkdir(BAD_IMAGES_PATH)
    os.mkdir(IMAGE_SUGGESTED_FOR_DELETION_PATH)

    good_images.clear()
    bad_images.clear()
    image_suggested_for_deletion.clear()

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        images = request.files.getlist("file")
        
        for image in images:
            if image.filename == '':
                flash('You need to select atleast one image to get the results.')
                return redirect(request.url)
            
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('Please select .jpg or .png or .jpeg.')
                return redirect(request.url)
        
        good_images, bad_images, image_suggested_for_deletion = main()

        for good_image in good_images:
            FileStorage().save(os.path.join(GOOD_IMAGES_PATH, good_image))
        
        for bad_image in bad_images:
            FileStorage().save(os.path.join(BAD_IMAGES_PATH, bad_image))
        
        for image_deletion in image_suggested_for_deletion:
            FileStorage().save(os.path.join(IMAGE_SUGGESTED_FOR_DELETION_PATH, image_deletion))
        
        return redirect(url_for('results'))

    return  render_template('home.html')

@app.route('/results')
def results():
    return render_template('results.html', goodImages=good_images, badImages=bad_images, imageSuggestedForDeletion=image_suggested_for_deletion)

@app.route('/uploads/<name>')
def uploads(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)