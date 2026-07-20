import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta

def medical_management():

    st.title("💉 Medical & Vaccination Management")

    os.makedirs("data", exist_ok=True)

    filename = "data/medical.csv"

    columns = [
        "Record ID",
        "Treatment Date",
        "Animal",
        "Animal ID",
        "Disease",
        "Medicine",
        "Veterinary Doctor",
        "Vaccination",
        "Next Vaccination",
        "Medical Cost",
        "Health Status",
        "Remarks"
    ]

    if (not os.path.exists(filename)) or os.path.getsize(filename)==0:
        pd.DataFrame(columns=columns).to_csv(filename,index=False)

    df = pd.read_csv(filename,dtype=str,keep_default_na=False)

    record_id = f"MED-{len(df)+1:05d}"

    st.subheader("➕ Medical Entry")

    with st.form("medical_form",clear_on_submit=True):

        col1,col2 = st.columns(2)

        with col1:

            st.text_input(
                "Record ID",
                value=record_id,
                disabled=True
            )

            treatment_date = st.date_input(
                "Treatment Date",
                value=date.today()
            )

            animal = st.selectbox(
                "Animal",
                [
                    "Poultry",
                    "Goat",
                    "Cow"
                ]
            )

            animal_id = st.text_input("Animal / Batch ID")

            disease = st.text_input("Disease")

            medicine = st.text_input("Medicine")

        with col2:

            doctor = st.text_input(
                "Veterinary Doctor"
            )

            vaccination = st.selectbox(
                "Vaccination Given",
                [
                    "Yes",
                    "No"
                ]
            )

            next_vaccine = st.date_input(
                "Next Vaccination Date",
                value=date.today()+timedelta(days=30)
            )

            medical_cost = st.number_input(
                "Medical Cost (₹)",
                min_value=0.0,
                value=500.0
            )

            health = st.selectbox(
                "Health Status",
                [
                    "Healthy",
                    "Recovering",
                    "Critical"
                ]
            )

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button(
            "💾 Save Medical Record"
        )

    if submit:

        new = pd.DataFrame([{

            "Record ID":record_id,
            "Treatment Date":treatment_date,
            "Animal":animal,
            "Animal ID":animal_id,
            "Disease":disease,
            "Medicine":medicine,
            "Veterinary Doctor":doctor,
            "Vaccination":vaccination,
            "Next Vaccination":next_vaccine,
            "Medical Cost":medical_cost,
            "Health Status":health,
            "Remarks":remarks

        }])

        df = pd.concat([df,new],ignore_index=True)

        df.to_csv(filename,index=False)

        st.success("✅ Medical Record Saved Successfully")

        st.balloons()

    st.divider()

    if not df.empty:

        df["Medical Cost"] = pd.to_numeric(
            df["Medical Cost"],
            errors="coerce"
        ).fillna(0)

        total_cost = df["Medical Cost"].sum()

        poultry = (df["Animal"]=="Poultry").sum()
        goat = (df["Animal"]=="Goat").sum()
        cow = (df["Animal"]=="Cow").sum()

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Medical Records",len(df))
        c2.metric("Total Expense",f"₹ {total_cost:,.0f}")
        c3.metric("Vaccinations",len(df[df["Vaccination"]=="Yes"]))
        c4.metric("Critical Cases",len(df[df["Health Status"]=="Critical"]))

        st.divider()

        st.subheader("📊 Animal-wise Medical Records")

        animal_summary = pd.DataFrame({
            "Animal":["Poultry","Goat","Cow"],
            "Records":[poultry,goat,cow]
        })

        st.bar_chart(animal_summary.set_index("Animal"))

        st.divider()

        st.subheader("📋 Medical Register")

        st.dataframe(df,use_container_width=True)

        st.download_button(
            "📥 Download Medical Report",
            df.to_csv(index=False).encode(),
            "medical.csv",
            "text/csv"
        )

        st.divider()

        st.subheader("🚨 Vaccination Reminder")

        today = pd.Timestamp.today().normalize()

        df["Next Vaccination"] = pd.to_datetime(
            df["Next Vaccination"],
            errors="coerce"
        )

        due = df[df["Next Vaccination"] <= today + pd.Timedelta(days=7)]

        if due.empty:
            st.success("✅ No vaccinations due in the next 7 days.")
        else:
            st.warning("⚠ Upcoming Vaccinations")
            st.dataframe(
                due[
                    [
                        "Animal",
                        "Animal ID",
                        "Next Vaccination",
                        "Veterinary Doctor"
                    ]
                ],
                use_container_width=True
            )

    else:

        st.info("No medical records available.")
