import streamlit as st
import pandas as pd
import os

def reports():

    st.title("📑 Farm Reports")

    os.makedirs("data", exist_ok=True)

    files = {
        "🐔 Poultry Report":"data/poultry.csv",
        "🐐 Goat Report":"data/goats.csv",
        "🐄 Cow Report":"data/cows.csv",
        "🌾 Feed Report":"data/feed.csv",
        "👨‍🌾 Employee Report":"data/employees.csv",
        "💉 Medical Report":"data/medical.csv",
        "💰 Sales Report":"data/sales.csv",
        "💵 Income Report":"data/income.csv",
        "💸 Expense Report":"data/expenses.csv"
    }

    report = st.selectbox(
        "Select Report",
        list(files.keys())
    )

    filename = files[report]

    if os.path.exists(filename):

        df = pd.read_csv(
            filename,
            dtype=str,
            keep_default_na=False
        )

        st.subheader(report)

        if df.empty:

            st.warning("No records available.")

        else:

            st.dataframe(
                df,
                use_container_width=True
            )

            st.success(
                f"Total Records : {len(df)}"
            )

            st.download_button(

                "📥 Download CSV",

                df.to_csv(index=False).encode(),

                filename.split("/")[-1],

                "text/csv"

            )

    else:

        st.error("Report File Not Found")

    st.divider()

    st.subheader("📊 Farm Financial Summary")

    income_file="data/income.csv"
    expense_file="data/expenses.csv"

    income=0
    expense=0

    if os.path.exists(income_file):

        df=pd.read_csv(
            income_file,
            dtype=str,
            keep_default_na=False
        )

        if not df.empty:

            income=pd.to_numeric(
                df["Amount"],
                errors="coerce"
            ).fillna(0).sum()

    if os.path.exists(expense_file):

        df=pd.read_csv(
            expense_file,
            dtype=str,
            keep_default_na=False
        )

        if not df.empty:

            expense=pd.to_numeric(
                df["Amount"],
                errors="coerce"
            ).fillna(0).sum()

    profit=income-expense

    c1,c2,c3=st.columns(3)

    c1.metric(
        "Income",
        f"₹ {income:,.0f}"
    )

    c2.metric(
        "Expense",
        f"₹ {expense:,.0f}"
    )

    c3.metric(
        "Profit",
        f"₹ {profit:,.0f}"
    )

    st.divider()

    summary=pd.DataFrame({

        "Particular":[

            "Total Income",
            "Total Expense",
            "Net Profit"

        ],

        "Amount":[

            income,
            expense,
            profit

        ]

    })

    st.subheader("📈 Profit & Loss Statement")

    st.dataframe(
        summary,
        use_container_width=True
    )

    st.download_button(

        "📥 Download Profit Report",

        summary.to_csv(index=False).encode(),

        "profit_report.csv",

        "text/csv"

    )
