
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask application
sales_predictor_api = Flask("Product Store Sales Predictor")

# Load trained preprocessing + model pipeline
model = joblib.load("rental_price_prediction_model_v1_0.joblib")


# Home endpoint
@sales_predictor_api.get("/")
def home():
    return "Welcome to the Product Store Sales Prediction API!"


# Single prediction endpoint
@sales_predictor_api.post("/v1/sales")
def predict_sales():

    # Get JSON input
    product_data = request.get_json()

    # Create input dictionary using the same features used during training
    sample = {
        "Product_Weight": product_data["Product_Weight"],
        "Product_Allocated_Area": product_data["Product_Allocated_Area"],
        "Product_MRP": product_data["Product_MRP"],
        "Store_Establishment_Year": product_data["Store_Establishment_Year"],

        "Product_Sugar_Content": product_data["Product_Sugar_Content"],
        "Product_Type": product_data["Product_Type"],
        "Store_Size": product_data["Store_Size"],
        "Store_Location_City_Type": product_data["Store_Location_City_Type"],
        "Store_Type": product_data["Store_Type"]
    }

    # Convert JSON input to DataFrame
    input_data = pd.DataFrame([sample])

    # Generate prediction
    prediction = model.predict(input_data)[0]

    # Convert NumPy output to regular Python float
    prediction = round(float(prediction), 2)

    return jsonify({
        "Predicted Product Store Sales": prediction
    })


# Batch prediction endpoint
@sales_predictor_api.post("/v1/salesbatch")
def predict_sales_batch():

    # Get uploaded CSV
    file = request.files["file"]

    # Read CSV
    input_data = pd.read_csv(file)

    # Generate predictions
    predictions = model.predict(input_data)

    # Convert predictions to Python floats
    predictions = [
        round(float(prediction), 2)
        for prediction in predictions
    ]

    # Return predictions
    return jsonify({
        "predictions": predictions
    })


# Run Flask application
if __name__ == "__main__":
    sales_predictor_api.run(debug=True)
