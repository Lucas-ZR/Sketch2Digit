import pandas as pd
from flask import Flask, render_template, request, jsonify

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import numpy as np

import os
import sys
sys.path.append("static/py")
from py_file import Model_CNN
import torch

model = Model_CNN()
model.load_state_dict(torch.load("static/py/sketch2num_weights.pth"))
model.eval()

app = Flask(__name__)

#minimal rate limiting
limiter = Limiter(
    app = app,
    key_func = get_remote_address,
    default_limits=["100 per hour"]
)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/run_model", methods = ["POST"])
@limiter.limit("10 per minute")
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
@limiter.limit("5 per minute")
def append_to_df():
    data = request.get_json()

    row = data["grid_data"] + [data["label"]]

    df.loc[len(df)] = row
    return jsonify({"message": "data saved!"}), 201
    

@app.route("/export_csv", methods = ["GET"])
@limiter.limit("1 per minute")
def export_csv():
    df.to_csv("data/record.csv")
    return jsonify({"message": "csv saved!"}), 200


#needs this to run on server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))