import pandas as pd
from flask import Flask, render_template, request, jsonify

import sys
import os

sys.path.append("static/py")

from py_file import Model_CNN
import torch

model = Model_CNN()
model.load_state_dict(torch.load("static/py/sketch2num_weights.pth"))
model.eval()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

cols = []
for i in range(0,28*28):
    cols.append(str(i))
cols.append("label")

df = pd.DataFrame(columns = cols)


@app.route("/save_drawing", methods=["POST"])
def append_to_df():
    data = request.get_json()

    row = data["grid_data"] + [data["label"]]

    df.loc[len(df)] = row
    return jsonify({"message": "data saved!"}), 201
    

@app.route("/export_csv", methods = ["GET"])
def export_csv():
    df.to_csv("data/record.csv")
    return jsonify({"message": "csv saved!"}), 200