import streamlit as st
import pandas as pd
import os
from datetime import date

def feed_management():

    st.title("🌾 Feed Management")

    os.makedirs("data", exist_ok=True)

    filename = "data/feed.csv"

    columns = [
        "Feed ID",
        "Date",
        "Animal",
        "Feed Type",
        "Quantity (Kg)",
        "Rate per Kg",
        "Total Cost",
        "Supplier",
        "Remarks"
    ]

    if (not os.path.exists(filename)) or os.path.getsize(filename) == 0:
        pd.DataFrame(columns=columns).to_csv(filename,index=False)

    df = pd.read_csv(filename,dtype=str,keep_default_na=False)

    feed_id = f"FD-{len(df)+1:05d}"

    st.subheader("➕ Add Feed Purchase")

    with st.form("feed_form",clear_on_submit=True):

        col1,col2 = st.columns(2)

        with col1:

            st.text_input("Feed ID",value=feed_id,disabled=True)

            feed_date = st.date_input(
                "Purchase Date",
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

            feed_type = st.selectbox(
                "Feed Type",
                [
                    "Starter Feed",
                    "Grower Feed",
                    "Layer Feed",
                    "Green Grass",
                    "Dry Fodder",
                    "Concentrate Feed",
                    "Maize",
                    "Rice Bran",
                    "Groundnut Cake",
                    "Other"
                ]
            )

        with col2:

            quantity = st.number_input(
                "Quantity (Kg)",
                min_value=1.0,
                value=50.0
            )

            rate = st.number_input(
                "Rate per Kg (₹)",
                min_value=1.0,
                value=35.0
            )

            supplier = st.text_input("Supplier Name")

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button("💾 Save Feed")

    if submit:

        total_cost = quantity * rate

        new = pd.DataFrame([{

            "Feed ID":feed_id,
            "Date":feed_date,
            "Animal":animal,
            "Feed Type":feed_type,
            "Quantity (Kg)":quantity,
            "Rate per Kg":rate,
            "Total Cost":total_cost,
            "Supplier":supplier,
            "Remarks":remarks

        }])

        df = pd.concat([df,new],ignore_index=True)

        df.to_csv(filename,index=False)

        st.success("✅ Feed Entry Saved Successfully")

        st.balloons()

    st.divider()

    if not df.empty:

        df["Quantity (Kg)"] = pd.to_numeric(
            df["Quantity (Kg)"],
            errors="coerce"
        ).fillna(0)

        df["Total Cost"] = pd.to_numeric(
            df["Total Cost"],
            errors="coerce"
        ).fillna(0)

        total_feed = df["Quantity (Kg)"].sum()
        total_expense = df["Total Cost"].sum()

        poultry_feed = df[df["Animal"]=="Poultry"]["Quantity (Kg)"].sum()
        goat_feed = df[df["Animal"]=="Goat"]["Quantity (Kg)"].sum()
        cow_feed = df[df["Animal"]=="Cow"]["Quantity (Kg)"].sum()

        st.subheader("📊 Feed Summary")

        c1,c2,c3,c4,c5 = st.columns(5)

        c1.metric("Total Feed",f"{total_feed:.1f} Kg")
        c2.metric("Poultry",f"{poultry_feed:.1f} Kg")
        c3.metric("Goat",f"{goat_feed:.1f} Kg")
        c4.metric("Cow",f"{cow_feed:.1f} Kg")
        c5.metric("Expense",f"₹ {total_expense:,.0f}")

        st.divider()

        st.subheader("🌾 Feed Register")

        st.dataframe(df,use_container_width=True)

        st.bar_chart(
            df.groupby("Animal")["Quantity (Kg)"].sum()
        )

        st.download_button(
            "📥 Download Feed Report",
            df.to_csv(index=False).encode(),
            "feed.csv",
            "text/csv"
        )

    else:

        st.info("No feed records available.")
