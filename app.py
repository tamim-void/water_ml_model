from flask import Flask, request, jsonify
import os
import pickle
from pathlib import Path

app = Flask(__name__)

# Load model using an absolute path based on this file's location
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "water_model.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


@app.route("/")
def home():
    return "Water Quality Prediction API is running"


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Invalid or missing JSON body."
            }), 400

        ph = float(data["ph"])
        hardness = float(data["Hardness"])
        solids = float(data["Solids"])
        chloramines = float(data["Chloramines"])
        sulfate = float(data["Sulfate"])
        conductivity = float(data["Conductivity"])
        organic_carbon = float(data["Organic_carbon"])
        trihalomethanes = float(data["Trihalomethanes"])
        turbidity = float(data["Turbidity"])

        prediction = model.predict([[
            ph, hardness, solids, chloramines,
            sulfate, conductivity, organic_carbon,
            trihalomethanes, turbidity
        ]])

        if prediction[0] == 1:
            result = "Potable"
            message = "The water is safe to drink."
        else:
            result = "Not Potable"
            message = "The water is not safe for drinking. Treatment is required."

        return jsonify({
            "status": "success",
            "result": result,
            "message": message
        })

    except KeyError as e:
        return jsonify({
            "status": "error",
            "message": f"Missing field: {str(e)}"
        }), 400

    except ValueError:
        return jsonify({
            "status": "error",
            "message": "All input fields must be numeric."
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
