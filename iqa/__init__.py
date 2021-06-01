import os
import shutil
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

# TODO
# YOU NEED TO CHANGE THIS PATHS ACCORDING TO YOUR SYSTEM
UPLOAD_FOLDER = 'E:/FinalYearProject/image_quality_assessment_final_year_project/iqa/static/images'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '7cfdd234688b289af832a382'

from iqa import routes