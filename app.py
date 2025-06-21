import pandas as pd
from flask import Flask, render_template, request, jsonify

import sys
sys.path.append("static/py")
from py_file import Model_CNN
import torch

model = Model_CNN()
model.load_state_dict(torch.load("static/py/sketch2num_weights.pth"))
model.eval()

import numpy as np
import torch

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/run_model", methods = ["POST"])
def run_model():
    data = request.get_json()

    row = data["grid_data"]

    sketch = np.array(row).reshape(28,28)

    sketch_tensor = torch.tensor(sketch, dtype=torch.float32).unsqueeze(0).unsqueeze(0)

    pred = model(sketch_tensor)
    probabilities = torch.softmax(pred.detach(), dim=1)[0]
    round_prob = probabilities.numpy().round(2).tolist()

    return jsonify({"prediction" : round_prob, "message" : "success"}), 202

@app.route("/developer")
def render_dev():
    return render_template("index_dev.html")


#routes used in development (buttons only on /developer)

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