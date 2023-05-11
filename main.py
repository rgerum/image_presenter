import json
from pathlib import Path
from flask import Flask, url_for, request, make_response, send_file
from flask import render_template
import numpy as np

#import tensorflow
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import re

app = Flask(__name__)

with app.test_request_context():
    url_for('static', filename='templates/index.html')
    url_for('static', filename='templates/style.css')
    url_for('static', filename='templates/helper_functions.js')
#(x1, y1), (x2, y2) = tensorflow.keras.datasets.cifar10.load_data()

def send_image(im_array):
    imagefile = BytesIO()
    plt.imsave(imagefile, im_array)
    imagedata = imagefile.getvalue()
    return imagedata, 200, {'Content-Type': 'image/png'}

@app.route("/image/<number>.png")
def image(number):
    print("image", number)
    return send_image(x1[int(number)])


@app.route("/data")
def data():
    with open("static/interp_exp_files/interpretability_experiment_formatting.txt", "r") as fp:
        data = json.load(fp)
    # add index
    for i, d in enumerate(data):
        d["index"] = i
    # shuffle the data
    np.random.shuffle(data)
    for d in data:
        # flip a join for the choices and store the original order
        coin1 = np.random.random() > 0.5
        d["choices1_orig"] = d["choices1"]
        d["choices2_orig"] = d["choices2"]
        if coin1:
            d["choices1"], d["choices2"] = d["choices2"], d["choices1"]
        d["choices_flip"] = coin1

        # flip a join for the maps and store the original order
        coin2 = np.random.random() > 0.5
        d["maps1_orig"] = d["maps1"]
        d["maps2_orig"] = d["maps2"]
        if coin2:
            d["maps1"], d["maps2"] = d["maps2"], d["maps1"]
        d["maps_flip"] = coin2
    return data


def make_filename_save(filename):
    return re.sub("[^-_A-z0-9]*", "", filename.strip().replace(" ", "_"))

@app.post('/save')
def save():
    data = request.json
    time = make_filename_save(data["time"])
    name = make_filename_save(data["name"])

    Path("output_json").mkdir(exist_ok=True)
    with open(f"output_json/{time}_{name}.json", "w") as fp:
        json.dump(data, fp, indent=2)

    Path("output_csv").mkdir(exist_ok=True)
    pd.DataFrame(data["data"]).to_csv(f"output_csv/{time}_{name}.csv")
    return "done"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/style.css")
def style():
    return send_file('templates/style.css')

@app.route("/helper_functions.js")
def helper_functions():
    return send_file('templates/helper_functions.js')


import zipfile
from pathlib import Path

def zip_dir(path: Path, zip_file_path: Path):
    """Zip all contents of path to zip_file"""
    files_to_zip = [
        file for file in path.glob('*') if file.is_file()]
    with zipfile.ZipFile(
        zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_f:
        for file in files_to_zip:
            print(file.name)
            zip_f.write(file, file.name)

FILE_SYSTEM_ROOT = "output_csv"
import os
@app.route('/output_csv/<path:urlFilePath>')
@app.route('/output_csv/')
def browser(urlFilePath=""):
    print(browser, urlFilePath)
    nestedFilePath = os.path.join(FILE_SYSTEM_ROOT, urlFilePath)
    print(nestedFilePath)
    if os.path.isdir(nestedFilePath):
        itemList = sorted(os.listdir(nestedFilePath))[::-1]
        if not urlFilePath.startswith("/"):
            urlFilePath = "/" + urlFilePath
        return render_template('browser.html', urlFilePath=urlFilePath, itemList=itemList)
    elif os.path.isfile(nestedFilePath):
        return send_file(nestedFilePath)
    return 'something bad happened'

@app.route('/output_csv.zip')
def browser_zip():
    zip_dir(Path("output_csv"), "output_csv.zip")
    return send_file("output_csv.zip")
