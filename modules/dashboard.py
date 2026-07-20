import streamlit as st
import pandas as pd
import os

def dashboard():

    st.title("🐔 Smart Livestock & Poultry Farm Dashboard")

    os.makedirs("data", exist_ok=True)

    files = {
        "poultry": "data/poultry.csv",
        "goat": "data/goats.csv",
        "cow": "data/cows.csv",
        "income": "data/income.csv",
        "expense": "data/expenses.csv"
    }

    poultry_cols = [
        "Batch ID","Breed","Purchase Date",
        "Purchased","Sold","Dead","Rate"
    ]

    goat_cols = [
        "Goat ID","Breed","Purchase Date",
        "Purchased","Sold","Dead","Rate"
    ]

    cow_cols = [
        "Cow ID","Breed","Purchase Date",
        "Purchased","Sold","Dead","Rate"
    ]

    money_cols = [
        "Date",
        "Category",
        "Amount",
        "Remarks"
    ]

    if not os.path.exists(files["poultry"]):
        pd.DataFrame(columns=poultry_cols).to_csv(files["poultry"], index=False)

    if not os.path.exists(files["goat"]):
        pd.DataFrame(columns=goat_cols).to_csv(files["goat"], index=False)

    if not os.path.exists(files["cow"]):
        pd.DataFrame(columns=cow_cols).to_csv(files["cow"], index=False)

    if not os.path.exists(files["income"]):
        pd.DataFrame(columns=money_cols).to_csv(files["income"], index=False)

    if not os.path.exists(files["expense"]):
        pd.DataFrame(columns=money_cols).to_csv(files["expense"], index=False)

    poultry = pd.read_csv(files["poultry"], dtype=str, keep_default_na=False)
    goat = pd.read_csv(files["goat"], dtype=str, keep_default_na=False)
    cow = pd.read_csv(files["cow"], dtype=str, keep_default_na=False)
    income = pd.read_csv(files["income"], dtype=str, keep_default_na=False)
    expense = pd.read_csv(files["expense"], dtype=str, keep_default_na=False)

    def total(df, col):
        if df.empty or col not in df.columns:
            return 0
        return pd.to_numeric(df[col], errors="coerce").fillna(0).sum()

    poultry_purchase = total(poultry, "Purchased")
    poultry_sold = total(poultry, "Sold")
    poultry_dead = total(poultry, "Dead")
    poultry_available = poultry_purchase - poultry_sold - poultry_dead

    goat_purchase = total(goat, "Purchased")
    goat_sold = total(goat, "Sold")
    goat_dead = total(goat, "Dead")
    goat_available = goat_purchase - goat_sold - goat_dead

    cow_purchase = total(cow, "Purchased")
    cow_sold = total(cow, "Sold")
    cow_dead = total(cow, "Dead")
    cow_available = cow_purchase - cow_sold - cow_dead

    total_income = total(income, "Amount")
    total_expense = total(expense, "Amount")
    profit = total_income - total_expense

    st.subheader("🐔 Poultry")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Purchased", poultry_purchase)
    c2.metric("Sold", poultry_sold)
    c3.metric("Dead", poultry_dead)
    c4.metric("Available", poultry_available)

    st.subheader("🐐 Goats")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Purchased", goat_purchase)
    c2.metric("Sold", goat_sold)
    c3.metric("Dead", goat_dead)
    c4.metric("Available", goat_available)

    st.subheader("🐄 Cows")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Purchased", cow_purchase)
    c2.metric("Sold", cow_sold)
    c3.metric("Dead", cow_dead)
    c4.metric("Available", cow_available)

    st.markdown("---")

    c1,c2,c3 = st.columns(3)

    c1.metric("💰 Total Income", f"₹ {total_income:,.0f}")
    c2.metric("💸 Total Expense", f"₹ {total_expense:,.0f}")
    c3.metric("📈 Net Profit", f"₹ {profit:,.0f}")

    st.markdown("---")

    estimated_value = (
        poultry_available*650 +
        goat_available*12000 +
        cow_available*65000
    )

    st.metric(
        "💎 Estimated Farm Value",
        f"₹ {estimated_value:,.0f}"
    )

    st.markdown("---")

    st.subheader("🚨 Smart Alerts")

    if poultry_available < 100:
        st.warning("⚠ Poultry stock is below 100.")

    if goat_available < 10:
        st.warning("⚠ Goat stock is getting low.")

    if cow_available < 5:
        st.warning("⚠ Cow stock is getting low.")

    if profit < 0:
        st.error("⚠ Farm is currently running at a loss.")

    if profit >= 0:
        st.success("✅ Farm is making a profit.")

    st.markdown("---")

    st.subheader("📊 Farm Summary")

    summary = pd.DataFrame({
        "Animal":[
            "Poultry",
            "Goat",
            "Cow"
        ],
        "Available":[
            poultry_available,
            goat_available,
            cow_available
        ]
    })

    st.bar_chart(summary.set_index("Animal"))

    st.download_button(
        "📥 Download Farm Summary",
        summary.to_csv(index=False).encode("utf-8"),
        "farm_summary.csv",
        "text/csv"
    )
