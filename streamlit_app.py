import os
from typing import Optional

import pandas as pd
import streamlit as st
from joblib import load, dump
from sklearn.linear_model import LinearRegression


@st.cache_resource(show_spinner=False)
def load_or_train_model() -> Optional[LinearRegression]:
    """Load trained model if available; otherwise train from local CSV.

    Returns None if neither a model file nor the CSV is available.
    """
    model_path = "SalaryModel.pkl"
    data_path = "Salary_Data.csv"

    # Try loading existing model
    if os.path.exists(model_path):
        try:
            model: LinearRegression = load(model_path)
            return model
        except Exception:
            pass

    # Fallback: train a fresh model from CSV if available
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        if "YearsExperience" in df.columns and "Salary" in df.columns:
            X = df["YearsExperience"].values.reshape(-1, 1)
            y = df["Salary"].values
            model = LinearRegression()
            model.fit(X, y)
            # Best-effort save for next runs
            try:
                dump(model, model_path)
            except Exception:
                pass
            return model

    return None


def main() -> None:
    st.set_page_config(page_title="Salary Prediction", page_icon="💼", layout="centered")
    st.title("💼 Salary Prediction")
    st.caption("Predict salary from years of experience using a linear regression model.")

    model = load_or_train_model()

    with st.expander("Model status", expanded=False):
        if model is None:
            st.error(
                "No trained model or dataset found. Place `SalaryModel.pkl` or `Salary_Data.csv` in the project root."
            )
        else:
            st.success("Model is ready.")
            st.write("You can optionally pre-train via `python Model.py`. This app will train on-the-fly if only the CSV is present.")

    st.subheader("Enter your details")
    years_exp = st.number_input(
        label="Years of Experience",
        min_value=0.0,
        max_value=50.0,
        value=3.0,
        step=0.1,
        help="Provide a non-negative number."
    )

    predict_clicked = st.button("Predict Salary", type="primary")

    if predict_clicked:
        if model is None:
            st.warning("Model is not available. Ensure `SalaryModel.pkl` or `Salary_Data.csv` exists.")
        else:
            try:
                prediction = float(model.predict([[years_exp]])[0])
                salary = round(prediction, 2)
                st.metric(label="Estimated Salary", value=f"$ {salary:,.2f}")
            except Exception as exc:
                st.error(f"Failed to predict salary: {exc}")

    with st.expander("Model details", expanded=False):
        if model is not None:
            coef = float(model.coef_[0]) if getattr(model, "coef_", None) is not None else None
            intercept = float(model.intercept_) if getattr(model, "intercept_", None) is not None else None
            st.write({
                "coefficient_per_year": coef,
                "intercept": intercept,
            })
        else:
            st.write("No model details available.")


if __name__ == "__main__":
    main()

