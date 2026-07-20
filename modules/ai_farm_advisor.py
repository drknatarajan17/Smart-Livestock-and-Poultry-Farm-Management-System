import streamlit as st
import pandas as pd
import os

def ai_farm_advisor():

    st.title("🤖 AI Farm Advisor")

    os.makedirs("data", exist_ok=True)

    def load_csv(file):
        if os.path.exists(file):
            return pd.read_csv(file, dtype=str, keep_default_na=False)
        return pd.DataFrame()

    poultry = load_csv("data/poultry.csv")
    goats = load_csv("data/goats.csv")
    cows = load_csv("data/cows.csv")
    feed = load_csv("data/feed.csv")
    income = load_csv("data/income.csv")
    expense = load_csv("data/expenses.csv")
    medical = load_csv("data/medical.csv")
    employees = load_csv("data/employees.csv")

    def total(df, column):
        if df.empty or column not in df.columns:
            return 0
        return pd.to_numeric(df[column], errors="coerce").fillna(0).sum()

    poultry_available = total(poultry,"Purchased") - total(poultry,"Sold") - total(poultry,"Dead")
    goat_available = total(goats,"Purchased") - total(goats,"Sold") - total(goats,"Dead")
    cow_available = total(cows,"Purchased") - total(cows,"Sold") - total(cows,"Dead")

    total_income = total(income,"Amount")

    total_expense = (
        total(expense,"Amount") +
        total(feed,"Total Cost") +
        total(medical,"Medical Cost") +
        total(employees,"Monthly Salary")
    )

    profit = total_income - total_expense

    farm_value = (
        poultry_available * 650 +
        goat_available * 12000 +
        cow_available * 65000
    )

    st.subheader("📊 Farm Health Dashboard")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Income",f"₹ {total_income:,.0f}")
    c2.metric("Expense",f"₹ {total_expense:,.0f}")
    c3.metric("Profit",f"₹ {profit:,.0f}")
    c4.metric("Farm Value",f"₹ {farm_value:,.0f}")

    st.divider()

    st.subheader("🧠 AI Recommendations")

    if poultry_available < 100:
        st.warning("🐔 Poultry stock is low. Consider purchasing a new batch.")

    if goat_available < 10:
        st.warning("🐐 Goat stock is low.")

    if cow_available < 5:
        st.warning("🐄 Cow stock is low.")

    if total_feed := total(feed,"Total Cost"):
        if total_feed > total_income * 0.35:
            st.warning("🌾 Feed cost is more than 35% of your income. Review feed planning.")

    if total(medical,"Medical Cost") > 20000:
        st.warning("💉 Medical expenses are high this month.")

    pending_salary = 0

    if not employees.empty and "Salary Status" in employees.columns:
        pending_salary = len(
            employees[
                employees["Salary Status"]=="Pending"
            ]
        )

    if pending_salary > 0:
        st.warning(f"👨‍🌾 {pending_salary} employee salaries are pending.")

    if profit > 0:
        st.success("✅ Farm is generating profit. Continue the current strategy.")
    else:
        st.error("❌ Farm is running at a loss. Reduce expenses or increase sales.")

    st.divider()

    st.subheader("📈 Business Suggestions")

    suggestions = []

    if poultry_available > 300:
        suggestions.append("🐔 Large poultry stock available. Plan a sale to improve cash flow.")

    if goat_available > 50:
        suggestions.append("🐐 Mature goats may be ready for sale.")

    if cow_available > 10:
        suggestions.append("🥛 Consider increasing milk sales through local vendors.")

    if total_feed > total_income * 0.30:
        suggestions.append("🌾 Negotiate better feed prices or purchase feed in bulk.")

    if profit > 100000:
        suggestions.append("💰 Farm is performing well. Consider expanding operations.")

    if len(suggestions)==0:
        suggestions.append("✅ Farm performance is stable.")

    for item in suggestions:
        st.info(item)

    st.divider()

    st.subheader("📊 Overall Farm Score")

    score = 100

    if profit < 0:
        score -= 30

    if poultry_available < 100:
        score -= 10

    if goat_available < 10:
        score -= 10

    if cow_available < 5:
        score -= 10

    if pending_salary > 0:
        score -= 10

    score = max(score,0)

    st.progress(score/100)

    st.metric(
        "Farm Health Score",
        f"{score}/100"
    )

    report = pd.DataFrame({
        "Parameter":[
            "Income",
            "Expense",
            "Profit",
            "Farm Value",
            "Farm Health Score"
        ],
        "Value":[
            total_income,
            total_expense,
            profit,
            farm_value,
            score
        ]
    })

    st.download_button(
        "📥 Download AI Report",
        report.to_csv(index=False).encode(),
        "AI_Farm_Report.csv",
        "text/csv"
    )
