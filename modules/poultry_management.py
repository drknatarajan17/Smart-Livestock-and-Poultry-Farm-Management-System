import streamlit as st
import pandas as pd
import os
from datetime import date

def poultry_management():

    st.title("🐔 Poultry Management")

    os.makedirs("data", exist_ok=True)

    filename = "data/poultry.csv"

    columns = [
        "Batch ID",
        "Purchase Date",
        "Breed",
        "Purchased",
        "Sold",
        "Dead",
        "Average Weight",
        "Purchase Rate",
        "Supplier",
        "Vaccinated",
        "Remarks"
    ]

    if (not os.path.exists(filename)) or os.path.getsize(filename) == 0:
        pd.DataFrame(columns=columns).to_csv(filename, index=False)

    df = pd.read_csv(filename, dtype=str, keep_default_na=False)

    batch_id = f"BAT-{len(df)+1:04d}"

    st.subheader("➕ Add New Poultry Batch")

    with st.form("poultry_form", clear_on_submit=True):

        c1, c2 = st.columns(2)

        with c1:
            st.text_input("Batch ID", value=batch_id, disabled=True)

            purchase_date = st.date_input(
                "Purchase Date",
                value=date.today()
            )

            breed = st.selectbox(
                "Breed",
                [
                    "Nattu Kozhi",
                    "Aseel",
                    "Kadaknath",
                    "Giriraja",
                    "Country Chicken",
                    "Other"
                ]
            )

            purchased = st.number_input(
                "Purchased Quantity",
                min_value=1,
                value=100
            )

            avg_weight = st.number_input(
                "Average Weight (Kg)",
                min_value=0.1,
                value=0.5
            )

        with c2:

            purchase_rate = st.number_input(
                "Purchase Rate (₹)",
                min_value=1,
                value=120
            )

            supplier = st.text_input("Supplier")

            vaccinated = st.selectbox(
                "Vaccinated",
                ["Yes", "No"]
            )

            sold = st.number_input(
                "Sold",
                min_value=0,
                value=0
            )

            dead = st.number_input(
                "Dead",
                min_value=0,
                value=0
            )

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button("💾 Save Batch")

    if submit:

        new = pd.DataFrame([{
            "Batch ID": batch_id,
            "Purchase Date": purchase_date,
            "Breed": breed,
            "Purchased": purchased,
            "Sold": sold,
            "Dead": dead,
            "Average Weight": avg_weight,
            "Purchase Rate": purchase_rate,
            "Supplier": supplier,
            "Vaccinated": vaccinated,
            "Remarks": remarks
        }])

        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(filename, index=False)

        st.success("✅ Poultry batch added successfully.")
        st.balloons()

    st.divider()

    st.subheader("📊 Poultry Summary")

    if not df.empty:

        purchased_total = pd.to_numeric(
            df["Purchased"],
            errors="coerce"
        ).fillna(0).sum()

        sold_total = pd.to_numeric(
            df["Sold"],
            errors="coerce"
        ).fillna(0).sum()

        dead_total = pd.to_numeric(
            df["Dead"],
            errors="coerce"
        ).fillna(0).sum()

        available = purchased_total - sold_total - dead_total

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Purchased", int(purchased_total))
        c2.metric("Sold", int(sold_total))
        c3.metric("Dead", int(dead_total))
        c4.metric("Available", int(available))

        st.divider()

        st.subheader("📋 Poultry Register")

        st.dataframe(df, use_container_width=True)

        st.download_button(
            "📥 Download Poultry Report",
            df.to_csv(index=False).encode("utf-8"),
            file_name="poultry.csv",
            mime="text/csv"
        )

    else:
        st.info("No poultry batches available.")
