import json

from flask import Flask, url_for, request, make_response
from flask import render_template

#import tensorflow
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import re

app = Flask(__name__)

with app.test_request_context():
    url_for('static', filename='templates/index.html')
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
    return [
        {
            'image': "00000.png",
            'choices1': "toad",
            'choices2': "tree",
            'maps1': "00000.png",
            'maps2': "00000.png",
        },
        {
            'image': "00001.png",
            'choices1': "road",
            'choices2': "water",
            'maps1': "00010.png",
            'maps2': "00020.png",
        },
        {
            'image': "00002.png",
            'choices1': "car",
            'choices2': "train",
            'maps1': "00003.png",
            'maps2': "00005.png",
        }
    ]

def make_filename_save(filename):
    return re.sub("[^-_A-z0-9]*", "", filename.strip().replace(" ", "_"))

@app.post('/save')
def save():
    data = request.json
    time = make_filename_save(data["time"])
    name = make_filename_save(data["name"])
    with open(f"output_json/{time}_{name}.json", "w") as fp:
        json.dump(data, fp, indent=2)
    pd.DataFrame(data["data"]).to_csv(f"output_csv/{time}_{name}.csv")
    return "done"

@app.route("/")
def index():
    return render_template('index.html')
