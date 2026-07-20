import streamlit as st
import pandas as pd
import os
from datetime import date

def expense_management():

    st.title("💸 Expense Management")

    os.makedirs("data", exist_ok=True)

    filename = "data/expenses.csv"

    columns = [
        "Expense ID",
        "Date",
        "Category",
        "Sub Category",
        "Amount",
        "Paid To",
        "Payment Mode",
        "Remarks"
    ]

    if (not os.path.exists(filename)) or os.path.getsize(filename) == 0:
        pd.DataFrame(columns=columns).to_csv(filename,index=False)

    df = pd.read_csv(filename,dtype=str,keep_default_na=False)

    expense_id = f"EXP-{len(df)+1:05d}"

    st.subheader("➕ Add Expense")

    with st.form("expense_form",clear_on_submit=True):

        col1,col2 = st.columns(2)

        with col1:

            st.text_input(
                "Expense ID",
                value=expense_id,
                disabled=True
            )

            expense_date = st.date_input(
                "Expense Date",
                value=date.today()
            )

            category = st.selectbox(
                "Category",
                [
                    "Feed",
                    "Employee Salary",
                    "Medical",
                    "Electricity",
                    "Water",
                    "Fuel",
                    "Transport",
                    "Maintenance",
                    "Equipment",
                    "Miscellaneous"
                ]
            )

            sub_category = st.text_input(
                "Sub Category"
            )

        with col2:

            amount = st.number_input(
                "Amount (₹)",
                min_value=1.0,
                value=1000.0
            )

            paid_to = st.text_input(
                "Paid To"
            )

            payment_mode = st.selectbox(
                "Payment Mode",
                [
                    "Cash",
                    "UPI",
                    "Bank Transfer",
                    "Cheque"
                ]
            )

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button(
            "💾 Save Expense"
        )

    if submit:

        new = pd.DataFrame([{

            "Expense ID":expense_id,
            "Date":expense_date,
            "Category":category,
            "Sub Category":sub_category,
            "Amount":amount,
            "Paid To":paid_to,
            "Payment Mode":payment_mode,
            "Remarks":remarks

        }])

        df = pd.concat(
            [df,new],
            ignore_index=True
        )

        df.to_csv(
            filename,
            index=False
        )

        st.success("✅ Expense Saved Successfully")

        st.balloons()

    st.divider()

    if not df.empty:

        df["Amount"] = pd.to_numeric(
            df["Amount"],
            errors="coerce"
        ).fillna(0)

        total_expense = df["Amount"].sum()

        st.subheader("📊 Expense Summary")

        c1,c2 = st.columns(2)

        c1.metric(
            "Total Expenses",
            f"₹ {total_expense:,.0f}"
        )

        c2.metric(
            "Expense Entries",
            len(df)
        )

        st.divider()

        st.subheader("📈 Category-wise Expense")

        category_summary = (
            df.groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(category_summary)

        st.divider()

        st.subheader("📋 Expense Register")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.download_button(
            "📥 Download Expense Report",
            df.to_csv(index=False).encode(),
            "expenses.csv",
            "text/csv"
        )

    else:

        st.info("No expenses recorded.")
