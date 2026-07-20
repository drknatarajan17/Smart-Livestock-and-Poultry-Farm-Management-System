import streamlit as st
import pandas as pd
import os
from datetime import date

def goat_management():

    st.title("🐐 Goat Management")

    os.makedirs("data", exist_ok=True)

    filename = "data/goats.csv"

    columns = [
        "Goat ID",
        "Purchase Date",
        "Breed",
        "Gender",
        "Age (Months)",
        "Weight (Kg)",
        "Purchased",
        "Sold",
        "Dead",
        "Purchase Rate",
        "Vaccinated",
        "Breeding",
        "Supplier",
        "Remarks"
    ]

    if not os.path.exists(filename):
        pd.DataFrame(columns=columns).to_csv(filename, index=False)

    df = pd.read_csv(filename, dtype=str, keep_default_na=False)

    goat_id = f"GOAT-{len(df)+1:04d}"

    st.subheader("➕ Register Goat")

    with st.form("goat_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:

            st.text_input("Goat ID", value=goat_id, disabled=True)

            purchase_date = st.date_input(
                "Purchase Date",
                value=date.today()
            )

            breed = st.selectbox(
                "Breed",
                [
                    "Kanni Adu",
                    "Salem Black",
                    "Boer",
                    "Jamunapari",
                    "Osmanabadi",
                    "Other"
                ]
            )

            gender = st.selectbox(
                "Gender",
                ["Male","Female"]
            )

            age = st.number_input(
                "Age (Months)",
                1,
                120,
                6
            )

            weight = st.number_input(
                "Weight (Kg)",
                1.0,
                150.0,
                12.0
            )

        with col2:

            purchased = st.number_input(
                "Purchased Count",
                1,
                100,
                1
            )

            purchase_rate = st.number_input(
                "Purchase Price (₹)",
                1000,
                100000,
                12000
            )

            supplier = st.text_input("Supplier Name")

            vaccinated = st.selectbox(
                "Vaccinated",
                ["Yes","No"]
            )

            breeding = st.selectbox(
                "Breeding Status",
                [
                    "Breeding",
                    "Not Breeding",
                    "Young"
                ]
            )

            sold = st.number_input(
                "Sold",
                0,
                100,
                0
            )

            dead = st.number_input(
                "Dead",
                0,
                100,
                0
            )

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button(
            "💾 Save Goat"
        )

    if submit:

        new = pd.DataFrame([{

            "Goat ID": goat_id,
            "Purchase Date": purchase_date,
            "Breed": breed,
            "Gender": gender,
            "Age (Months)": age,
            "Weight (Kg)": weight,
            "Purchased": purchased,
            "Sold": sold,
            "Dead": dead,
            "Purchase Rate": purchase_rate,
            "Vaccinated": vaccinated,
            "Breeding": breeding,
            "Supplier": supplier,
            "Remarks": remarks

        }])

        df = pd.concat([df,new],ignore_index=True)

        df.to_csv(filename,index=False)

        st.success("✅ Goat Registered Successfully")

        st.balloons()

    st.divider()

    st.subheader("📊 Goat Summary")

    if not df.empty:

        purchased = pd.to_numeric(
            df["Purchased"],
            errors="coerce"
        ).fillna(0).sum()

        sold = pd.to_numeric(
            df["Sold"],
            errors="coerce"
        ).fillna(0).sum()

        dead = pd.to_numeric(
            df["Dead"],
            errors="coerce"
        ).fillna(0).sum()

        available = purchased-sold-dead

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Purchased",int(purchased))
        c2.metric("Sold",int(sold))
        c3.metric("Dead",int(dead))
        c4.metric("Available",int(available))

        st.divider()

        st.subheader("🐐 Goat Register")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.download_button(
            "📥 Download Goat Report",
            df.to_csv(index=False).encode(),
            "goats.csv",
            "text/csv"
        )

    else:

        st.info("No goat records found.")
