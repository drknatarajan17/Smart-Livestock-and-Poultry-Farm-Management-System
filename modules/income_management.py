import streamlit as st
import pandas as pd
import os
from datetime import date

def income_management():

    st.title("💰 Income Management")

    os.makedirs("data", exist_ok=True)

    filename = "data/income.csv"

    columns = [
        "Income ID",
        "Date",
        "Category",
        "Customer Name",
        "Mobile",
        "Quantity",
        "Rate",
        "Amount",
        "Payment Mode",
        "Remarks"
    ]

    if (not os.path.exists(filename)) or os.path.getsize(filename)==0:
        pd.DataFrame(columns=columns).to_csv(filename,index=False)

    df = pd.read_csv(filename,dtype=str,keep_default_na=False)

    income_id = f"INC-{len(df)+1:05d}"

    st.subheader("➕ Add Income")

    with st.form("income_form",clear_on_submit=True):

        col1,col2 = st.columns(2)

        with col1:

            st.text_input(
                "Income ID",
                value=income_id,
                disabled=True
            )

            income_date = st.date_input(
                "Income Date",
                value=date.today()
            )

            category = st.selectbox(
                "Income Category",
                [
                    "Poultry Sale",
                    "Goat Sale",
                    "Cow Sale",
                    "Egg Sale",
                    "Milk Sale",
                    "Organic Manure",
                    "Cow Dung",
                    "Feed Sale",
                    "Other Income"
                ]
            )

            customer = st.text_input(
                "Customer Name"
            )

            mobile = st.text_input(
                "Mobile Number"
            )

        with col2:

            quantity = st.number_input(
                "Quantity",
                min_value=1.0,
                value=1.0
            )

            rate = st.number_input(
                "Rate (₹)",
                min_value=1.0,
                value=100.0
            )

            payment = st.selectbox(
                "Payment Mode",
                [
                    "Cash",
                    "UPI",
                    "Bank Transfer",
                    "Cheque"
                ]
            )

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button("💾 Save Income")

    if submit:

        amount = quantity * rate

        new = pd.DataFrame([{

            "Income ID":income_id,
            "Date":income_date,
            "Category":category,
            "Customer Name":customer,
            "Mobile":mobile,
            "Quantity":quantity,
            "Rate":rate,
            "Amount":amount,
            "Payment Mode":payment,
            "Remarks":remarks

        }])

        df = pd.concat([df,new],ignore_index=True)

        df.to_csv(filename,index=False)

        st.success("✅ Income Saved Successfully")

        st.balloons()

    st.divider()

    if not df.empty:

        df["Amount"]=pd.to_numeric(
            df["Amount"],
            errors="coerce"
        ).fillna(0)

        total_income=df["Amount"].sum()

        st.subheader("📊 Income Summary")

        c1,c2=st.columns(2)

        c1.metric(
            "Total Income",
            f"₹ {total_income:,.0f}"
        )

        c2.metric(
            "Income Entries",
            len(df)
        )

        st.divider()

        st.subheader("📈 Category-wise Income")

        chart=df.groupby("Category")["Amount"].sum()

        st.bar_chart(chart)

        st.divider()

        st.subheader("📋 Income Register")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.download_button(
            "📥 Download Income Report",
            df.to_csv(index=False).encode(),
            "income.csv",
            "text/csv"
        )

    else:

        st.info("No income records available.")
