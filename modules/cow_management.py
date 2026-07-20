import streamlit as st
import pandas as pd
import os
from datetime import date

def cow_management():

    st.title("🐄 Cow Management")

    os.makedirs("data", exist_ok=True)

    filename = "data/cows.csv"

    columns = [
        "Cow ID",
        "Purchase Date",
        "Breed",
        "Gender",
        "Age (Years)",
        "Weight (Kg)",
        "Purchased",
        "Sold",
        "Dead",
        "Purchase Price",
        "Milk Per Day (L)",
        "Pregnancy Status",
        "Vaccinated",
        "Health Status",
        "Supplier",
        "Remarks"
    ]

    if not os.path.exists(filename):
        pd.DataFrame(columns=columns).to_csv(filename,index=False)

    df = pd.read_csv(filename,dtype=str,keep_default_na=False)

    cow_id = f"COW-{len(df)+1:04d}"

    st.subheader("➕ Register Cow")

    with st.form("cow_form",clear_on_submit=True):

        col1,col2 = st.columns(2)

        with col1:

            st.text_input("Cow ID",value=cow_id,disabled=True)

            purchase_date = st.date_input(
                "Purchase Date",
                value=date.today()
            )

            breed = st.selectbox(
                "Breed",
                [
                    "Jersey",
                    "HF",
                    "Kangayam",
                    "Gir",
                    "Sahiwal",
                    "Other"
                ]
            )

            gender = st.selectbox(
                "Gender",
                ["Male","Female"]
            )

            age = st.number_input(
                "Age (Years)",
                1,
                20,
                3
            )

            weight = st.number_input(
                "Weight (Kg)",
                50,
                1200,
                350
            )

        with col2:

            purchased = st.number_input(
                "Purchased",
                1,
                100,
                1
            )

            purchase_price = st.number_input(
                "Purchase Price (₹)",
                10000,
                500000,
                65000
            )

            milk = st.number_input(
                "Milk Per Day (Litres)",
                0.0,
                60.0,
                10.0
            )

            pregnancy = st.selectbox(
                "Pregnancy Status",
                [
                    "Pregnant",
                    "Not Pregnant",
                    "N/A"
                ]
            )

            vaccinated = st.selectbox(
                "Vaccinated",
                ["Yes","No"]
            )

            health = st.selectbox(
                "Health Status",
                [
                    "Healthy",
                    "Under Treatment",
                    "Critical"
                ]
            )

            supplier = st.text_input("Supplier")

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
            "💾 Save Cow"
        )

    if submit:

        new = pd.DataFrame([{

            "Cow ID":cow_id,
            "Purchase Date":purchase_date,
            "Breed":breed,
            "Gender":gender,
            "Age (Years)":age,
            "Weight (Kg)":weight,
            "Purchased":purchased,
            "Sold":sold,
            "Dead":dead,
            "Purchase Price":purchase_price,
            "Milk Per Day (L)":milk,
            "Pregnancy Status":pregnancy,
            "Vaccinated":vaccinated,
            "Health Status":health,
            "Supplier":supplier,
            "Remarks":remarks

        }])

        df = pd.concat([df,new],ignore_index=True)

        df.to_csv(filename,index=False)

        st.success("✅ Cow Registered Successfully")

        st.balloons()

    st.divider()

    st.subheader("📊 Cow Summary")

    if not df.empty:

        purchased = pd.to_numeric(df["Purchased"],errors="coerce").fillna(0).sum()
        sold = pd.to_numeric(df["Sold"],errors="coerce").fillna(0).sum()
        dead = pd.to_numeric(df["Dead"],errors="coerce").fillna(0).sum()
        milk = pd.to_numeric(df["Milk Per Day (L)"],errors="coerce").fillna(0).sum()

        available = purchased - sold - dead

        c1,c2,c3,c4,c5 = st.columns(5)

        c1.metric("Purchased",int(purchased))
        c2.metric("Sold",int(sold))
        c3.metric("Dead",int(dead))
        c4.metric("Available",int(available))
        c5.metric("Milk/Day",f"{milk:.1f} L")

        st.divider()

        st.subheader("🐄 Cow Register")

        st.dataframe(df,use_container_width=True)

        st.download_button(
            "📥 Download Cow Report",
            df.to_csv(index=False).encode("utf-8"),
            "cows.csv",
            "text/csv"
        )

    else:
        st.info("No cow records available.")
