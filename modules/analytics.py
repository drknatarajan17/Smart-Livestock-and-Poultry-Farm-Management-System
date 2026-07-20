import streamlit as st
import pandas as pd
import os

def analytics():

    st.title("📊 Farm Analytics Dashboard")

    os.makedirs("data", exist_ok=True)

    files = {
        "Poultry":"data/poultry.csv",
        "Goat":"data/goats.csv",
        "Cow":"data/cows.csv",
        "Income":"data/income.csv",
        "Expense":"data/expenses.csv",
        "Feed":"data/feed.csv",
        "Medical":"data/medical.csv",
        "Employees":"data/employees.csv"
    }

    def load_csv(path):
        if os.path.exists(path):
            return pd.read_csv(path,dtype=str,keep_default_na=False)
        return pd.DataFrame()

    poultry = load_csv(files["Poultry"])
    goat = load_csv(files["Goat"])
    cow = load_csv(files["Cow"])
    income = load_csv(files["Income"])
    expense = load_csv(files["Expense"])
    feed = load_csv(files["Feed"])
    medical = load_csv(files["Medical"])
    employees = load_csv(files["Employees"])

    def total(df,col):
        if df.empty or col not in df.columns:
            return 0
        return pd.to_numeric(df[col],errors="coerce").fillna(0).sum()

    poultry_stock = total(poultry,"Purchased")-total(poultry,"Sold")-total(poultry,"Dead")
    goat_stock = total(goat,"Purchased")-total(goat,"Sold")-total(goat,"Dead")
    cow_stock = total(cow,"Purchased")-total(cow,"Sold")-total(cow,"Dead")

    total_income = total(income,"Amount")
    total_expense = total(expense,"Amount")
    total_feed = total(feed,"Total Cost")
    total_medical = total(medical,"Medical Cost")
    salary = total(employees,"Monthly Salary")

    total_expense = total_expense + total_feed + total_medical + salary

    profit = total_income-total_expense

    st.subheader("📈 Farm Overview")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Income",f"₹ {total_income:,.0f}")
    c2.metric("Expense",f"₹ {total_expense:,.0f}")
    c3.metric("Profit",f"₹ {profit:,.0f}")
    c4.metric("Employees",len(employees))

    st.divider()

    st.subheader("🐔 Livestock Availability")

    livestock = pd.DataFrame({

        "Animal":[
            "Poultry",
            "Goat",
            "Cow"
        ],

        "Available":[
            poultry_stock,
            goat_stock,
            cow_stock
        ]

    })

    st.bar_chart(
        livestock.set_index("Animal")
    )

    st.divider()

    st.subheader("💰 Income vs Expense")

    finance = pd.DataFrame({

        "Category":[
            "Income",
            "Expense"
        ],

        "Amount":[
            total_income,
            total_expense
        ]

    })

    st.bar_chart(
        finance.set_index("Category")
    )

    st.divider()

    st.subheader("🌾 Feed Cost")

    st.metric(
        "Feed Expense",
        f"₹ {total_feed:,.0f}"
    )

    st.divider()

    st.subheader("💉 Medical Expense")

    st.metric(
        "Medical Expense",
        f"₹ {total_medical:,.0f}"
    )

    st.divider()

    st.subheader("👨‍🌾 Salary Expense")

    st.metric(
        "Salary",
        f"₹ {salary:,.0f}"
    )

    st.divider()

    st.subheader("💎 Estimated Farm Value")

    value = (
        poultry_stock*650 +
        goat_stock*12000 +
        cow_stock*65000
    )

    st.metric(
        "Farm Value",
        f"₹ {value:,.0f}"
    )

    st.divider()

    st.subheader("🚨 AI Insights")

    if profit > 0:
        st.success("✅ Farm is running in Profit.")

    else:
        st.error("⚠ Farm is running in Loss.")

    if poultry_stock < 100:
        st.warning("⚠ Poultry stock is getting low.")

    if goat_stock < 10:
        st.warning("⚠ Goat stock is low.")

    if cow_stock < 5:
        st.warning("⚠ Cow stock is low.")

    if total_feed > total_income*0.40:
        st.warning("⚠ Feed expense exceeds 40% of income.")

    st.divider()

    st.download_button(

        "📥 Download Analytics",

        livestock.to_csv(index=False).encode(),

        "analytics.csv",

        "text/csv"

    )
