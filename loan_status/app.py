import streamlit as st
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier

# Load the trained model
MODEL_PATH = "./vector.pkl"  # Update this path if needed
if not os.path.exists(MODEL_PATH):
    st.error(f"Model file not found at {MODEL_PATH}. Please check the path.")
else:
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)

# Debug: Show the type of the loaded model
st.write(f"Loaded model type: {type(model)}")

# Title and description
st.title("Loan Status Prediction")
st.write("This application predicts whether a loan will be approved or not based on user inputs.")

# Input fields for user data
st.sidebar.header("Input Features")
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
married = st.sidebar.selectbox("Married", ["Yes", "No"])
dependents = st.sidebar.selectbox("Dependents", ["0", "1", "2", "3+"])
education = st.sidebar.selectbox("Education", ["Graduate", "Not Graduate"])
self_employed = st.sidebar.selectbox("Self Employed", ["Yes", "No"])
applicant_income = st.sidebar.number_input("Applicant Income", min_value=0, step=1000)
coapplicant_income = st.sidebar.number_input("Coapplicant Income", min_value=0, step=1000)
loan_amount = st.sidebar.number_input("Loan Amount (in thousands)", min_value=0, step=1)
loan_amount_term = st.sidebar.number_input("Loan Amount Term (in days)", min_value=0, step=1)
credit_history = st.sidebar.selectbox("Credit History", [1.0, 0.0])
property_area = st.sidebar.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

# Prepare input data for prediction
input_data = pd.DataFrame({
    "Gender": [gender],
    "Married": [married],
    "Dependents": [dependents],
    "Education": [education],
    "Self_Employed": [self_employed],
    "ApplicantIncome": [applicant_income],
    "CoapplicantIncome": [coapplicant_income],
    "LoanAmount": [loan_amount],
    "Loan_Amount_Term": [loan_amount_term],
    "Credit_History": [credit_history],
    "Property_Area": [property_area]
})

# Map categorical values to numerical values (if required by the model)
# Add preprocessing logic here if needed

# Predict button
if st.button("Predict Loan Status"):
    prediction = model.predict(input_data)[0]
    if prediction == 1:
        st.success("Congratulations! Your loan is likely to be approved.")
    else:
        st.error("Unfortunately, your loan is likely to be rejected.")