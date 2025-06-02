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
    try:
        data = request.get_json()
        print("Recieved data:",data)

        row = data["grid_data"] + [data["label"]]
        print("row data length:", len(row))

        df.loc[len(df)] = row
        return jsonify({"message": "data saved!"}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}),500