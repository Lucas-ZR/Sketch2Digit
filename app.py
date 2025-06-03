import pandas as pd
from flask import Flask, render_template, request, jsonify

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
    df.to_csv("C:\\Users\\L_W\\Documents\\code\\Sketch2Num\\data\\record.csv")
    return jsonify({"message": "csv saved!"}), 200