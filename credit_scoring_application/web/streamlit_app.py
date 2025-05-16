# streamlit_app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import joblib
from glob import glob

st.title("Credit Scoring Web App")

# Load the trained model with a loader
@st.cache_resource
def load_model():
    return joblib.load("../credit_scoring_model.joblib")

with st.spinner("Loading model..."):
    model = load_model()

# Define your feature lists (should match those used in training)
varc = [v for v in model.data.columns if v[:2] == 'C_']
vard = [v for v in model.data.columns if v[:2] == 'D_']

st.write("Upload a CSV file with the same features as the training data (excluding the target column).")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
    st.write("Input Data Preview:")
    st.dataframe(input_df.head())

    # Ensure only the required columns are present
    missing_cols = [col for col in (varc + vard) if col not in input_df.columns]
    if missing_cols:
        st.error(f"Missing columns in uploaded data: {missing_cols}")
    else:
        # Apply the same transformations as in the notebook
        with st.spinner("Scoring data..."):
            try:
                input_data = input_df[varc + vard].copy()
                scored = model.credit_scoring.transform(
                    model.woe_encoder.inverse_transform(
                        model._AutoCreditScoring__apply_pipeline(input_data)
                    )
                )
                st.success("Scoring complete!")
                st.write("Scored Data:")
                st.dataframe(scored[['score']])
                st.download_button(
                    label="Download scored data as CSV",
                    data=scored.to_csv(index=False),
                    file_name="scored_data.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error scoring data: {e}")

        # Display report images with a loader
        with st.spinner("Loading report images..."):
            report_dir = "../reports"
            image_files = sorted(glob(os.path.join(report_dir, "*.png")))
            if image_files:
                st.subheader("Generated Reports")
                for img_path in image_files:
                    st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)
            else:
                st.info("No report images found in the reports directory.")
else:
    st.info("Awaiting CSV file upload.")