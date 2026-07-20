import streamlit as st
import pandas as pd
import os
from datetime import date

def sales_management():

    st.title("💰 Animal Sales Management")

    os.makedirs("data", exist_ok=True)

    sales_file = "data/sales.csv"
    income_file = "data/income.csv"

    sales_columns = [
        "Sale ID",
        "Sale Date",
        "Animal",
        "Animal ID / Batch",
        "Customer Name",
        "Mobile",
        "Quantity",
        "Rate",
        "Total Amount",
        "Amount Received",
        "Pending Amount",
        "Payment Status",
        "Remarks"
    ]

    income_columns = [
        "Date",
        "Category",
        "Amount",
        "Remarks"
    ]

    if not os.path.exists(sales_file):
        pd.DataFrame(columns=sales_columns).to_csv(sales_file,index=False)

    if not os.path.exists(income_file):
        pd.DataFrame(columns=income_columns).to_csv(income_file,index=False)

    sales_df = pd.read_csv(sales_file,dtype=str,keep_default_na=False)
    income_df = pd.read_csv(income_file,dtype=str,keep_default_na=False)

    sale_id = f"SALE-{len(sales_df)+1:05d}"

    st.subheader("➕ New Animal Sale")

    with st.form("sale_form",clear_on_submit=True):

        c1,c2 = st.columns(2)

        with c1:

            st.text_input(
                "Sale ID",
                value=sale_id,
                disabled=True
            )

            sale_date = st.date_input(
                "Sale Date",
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

            animal_id = st.text_input(
                "Animal ID / Batch ID"
            )

            customer = st.text_input(
                "Customer Name"
            )

            mobile = st.text_input(
                "Customer Mobile"
            )

        with c2:

            quantity = st.number_input(
                "Quantity Sold",
                min_value=1,
                value=1
            )

            rate = st.number_input(
                "Selling Rate (₹)",
                min_value=1.0,
                value=500.0
            )

            received = st.number_input(
                "Amount Received (₹)",
                min_value=0.0,
                value=0.0
            )

            remarks = st.text_area("Remarks")

        submit = st.form_submit_button("💾 Save Sale")

    if submit:

        total = quantity * rate
        pending = total - received

        if pending <= 0:
            payment = "Paid"
        else:
            payment = "Pending"

        new_sale = pd.DataFrame([{

            "Sale ID":sale_id,
            "Sale Date":sale_date,
            "Animal":animal,
            "Animal ID / Batch":animal_id,
            "Customer Name":customer,
            "Mobile":mobile,
            "Quantity":quantity,
            "Rate":rate,
            "Total Amount":total,
            "Amount Received":received,
            "Pending Amount":pending,
            "Payment Status":payment,
            "Remarks":remarks

        }])

        sales_df = pd.concat(
            [sales_df,new_sale],
            ignore_index=True
        )

        sales_df.to_csv(
            sales_file,
            index=False
        )

        income = pd.DataFrame([{

            "Date":sale_date,
            "Category":"Animal Sale",
            "Amount":received,
            "Remarks":f"{animal} Sale"

        }])

        income_df = pd.concat(
            [income_df,income],
            ignore_index=True
        )

        income_df.to_csv(
            income_file,
            index=False
        )

        # ---------- AUTO STOCK UPDATE ----------

        if animal=="Poultry":
            stock_file="data/poultry.csv"
            id_col="Batch ID"

        elif animal=="Goat":
            stock_file="data/goats.csv"
            id_col="Goat ID"

        else:
            stock_file="data/cows.csv"
            id_col="Cow ID"

        if os.path.exists(stock_file):

            stock=pd.read_csv(
                stock_file,
                dtype=str,
                keep_default_na=False
            )

            if id_col in stock.columns:

                idx=stock[
                    stock[id_col]==animal_id
                ].index

                if len(idx)>0:

                    i=idx[0]

                    sold=int(
                        float(
                            stock.loc[i,"Sold"]
                        )
                    )

                    stock.loc[i,"Sold"]=sold+quantity

                    stock.to_csv(
                        stock_file,
                        index=False
                    )

        st.success(
            "✅ Sale Saved Successfully"
        )

        st.balloons()

    st.divider()

    if not sales_df.empty:

        sales_df["Total Amount"]=pd.to_numeric(
            sales_df["Total Amount"],
            errors="coerce"
        ).fillna(0)

        sales_df["Pending Amount"]=pd.to_numeric(
            sales_df["Pending Amount"],
            errors="coerce"
        ).fillna(0)

        total_sales=sales_df["Total Amount"].sum()

        pending=sales_df["Pending Amount"].sum()

        paid=total_sales-pending

        c1,c2,c3=st.columns(3)

        c1.metric(
            "Total Sales",
            f"₹ {total_sales:,.0f}"
        )

        c2.metric(
            "Amount Received",
            f"₹ {paid:,.0f}"
        )

        c3.metric(
            "Pending",
            f"₹ {pending:,.0f}"
        )

        st.divider()

        st.subheader("📋 Sales Register")

        st.dataframe(
            sales_df,
            use_container_width=True
        )

        st.download_button(
            "📥 Download Sales Report",
            sales_df.to_csv(index=False).encode(),
            "sales.csv",
            "text/csv"
        )

    else:

        st.info("No sales recorded.")
