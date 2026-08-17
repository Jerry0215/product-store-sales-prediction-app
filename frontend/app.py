
import streamlit as st
import pandas as pd
import requests

# Flask backend URL inside the Docker network
BACKEND_URL = "http://backend:7860"

st.title("Product Store Sales Prediction")
st.write(
    "Enter product and store information below to predict total product store sales."
)

st.subheader("Online Prediction")

# Numerical inputs
product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.65,
    step=0.1
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.069,
    step=0.001,
    format="%.3f"
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=147.03,
    step=1.0
)

store_establishment_year = st.number_input(
    "Store Establishment Year",
    min_value=1980,
    max_value=2026,
    value=2009,
    step=1
)

# Categorical inputs
product_sugar_content = st.selectbox(
    "Product Sugar Content",
    [
        "Low Sugar",
        "Regular",
        "No Sugar"
    ]
)

product_type = st.selectbox(
    "Product Type",
    [
        "Fruits and Vegetables",
        "Snack Foods",
        "Frozen Foods",
        "Dairy",
        "Household",
        "Baking Goods",
        "Canned",
        "Health and Hygiene",
        "Meat",
        "Soft Drinks",
        "Breads",
        "Hard Drinks",
        "Others",
        "Starchy Foods",
        "Breakfast",
        "Seafood"
    ]
)

store_size = st.selectbox(
    "Store Size",
    [
        "Small",
        "Medium",
        "High"
    ]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    [
        "Tier 1",
        "Tier 2",
        "Tier 3"
    ]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Supermarket Type1",
        "Supermarket Type2",
        "Departmental Store",
        "Food Mart"
    ]
)

# Create input dataframe
input_data = pd.DataFrame([{
    "Product_Weight": product_weight,
    "Product_Allocated_Area": product_allocated_area,
    "Product_MRP": product_mrp,
    "Store_Establishment_Year": store_establishment_year,
    "Product_Sugar_Content": product_sugar_content,
    "Product_Type": product_type,
    "Store_Size": store_size,
    "Store_Location_City_Type": store_location_city_type,
    "Store_Type": store_type
}])

# Single prediction
if st.button("Predict Sales", type="primary"):

    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/sales",
            json=input_data.to_dict(orient="records")[0]
        )

        if response.status_code == 200:

            prediction = response.json()[
                "Predicted Product Store Sales"
            ]

            st.success(
                f"Predicted Product Store Sales: ${prediction:,.2f}"
            )

        else:
            st.error(
                f"Prediction failed. Status code: {response.status_code}"
            )

    except requests.exceptions.RequestException:
        st.error(
            "Unable to connect to the prediction API."
        )


# Batch prediction section
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV file for batch prediction",
    type=["csv"]
)

if uploaded_file is not None:

    if st.button("Predict Batch", type="primary"):

        try:
            response = requests.post(
                f"{BACKEND_URL}/v1/salesbatch",
                files={"file": uploaded_file}
            )

            if response.status_code == 200:

                predictions = response.json()

                st.success(
                    "Batch predictions completed successfully."
                )

                st.write(predictions)

            else:
                st.error(
                    f"Batch prediction failed. Status code: {response.status_code}"
                )

        except requests.exceptions.RequestException:
            st.error(
                "Unable to connect to the prediction API."
            )
