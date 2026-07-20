import streamlit as st
import pandas as pd
import os
from datetime import date

def employee_management():

    st.title("👨‍🌾 Employee Management")

    os.makedirs("data", exist_ok=True)

    filename="data/employees.csv"

    columns=[
        "Employee ID",
        "Employee Name",
        "Mobile",
        "Aadhaar",
        "Address",
        "Designation",
        "Joining Date",
        "Monthly Salary",
        "Attendance Days",
        "Salary Status",
        "Remarks"
    ]

    if (not os.path.exists(filename)) or os.path.getsize(filename)==0:
        pd.DataFrame(columns=columns).to_csv(filename,index=False)

    df=pd.read_csv(filename,dtype=str,keep_default_na=False)

    emp_id=f"EMP-{len(df)+1:04d}"

    st.subheader("➕ Add Employee")

    with st.form("employee_form",clear_on_submit=True):

        col1,col2=st.columns(2)

        with col1:

            st.text_input(
                "Employee ID",
                value=emp_id,
                disabled=True
            )

            name=st.text_input("Employee Name")

            mobile=st.text_input("Mobile Number")

            aadhaar=st.text_input("Aadhaar Number")

            designation=st.selectbox(
                "Designation",
                [
                    "Farm Manager",
                    "Supervisor",
                    "Farm Worker",
                    "Driver",
                    "Watchman",
                    "Veterinary Assistant",
                    "Cleaner",
                    "Other"
                ]
            )

        with col2:

            address=st.text_area("Address")

            joining_date=st.date_input(
                "Joining Date",
                value=date.today()
            )

            salary=st.number_input(
                "Monthly Salary (₹)",
                min_value=5000,
                max_value=100000,
                value=15000
            )

            attendance=st.number_input(
                "Attendance Days",
                min_value=0,
                max_value=31,
                value=30
            )

            salary_status=st.selectbox(
                "Salary Status",
                [
                    "Paid",
                    "Pending"
                ]
            )

        remarks=st.text_area("Remarks")

        submit=st.form_submit_button(
            "💾 Save Employee"
        )

    if submit:

        new=pd.DataFrame([{

            "Employee ID":emp_id,
            "Employee Name":name,
            "Mobile":mobile,
            "Aadhaar":aadhaar,
            "Address":address,
            "Designation":designation,
            "Joining Date":joining_date,
            "Monthly Salary":salary,
            "Attendance Days":attendance,
            "Salary Status":salary_status,
            "Remarks":remarks

        }])

        df=pd.concat([df,new],ignore_index=True)

        df.to_csv(filename,index=False)

        st.success("✅ Employee Saved Successfully")

        st.balloons()

    st.divider()

    if not df.empty:

        df["Monthly Salary"]=pd.to_numeric(
            df["Monthly Salary"],
            errors="coerce"
        ).fillna(0)

        total_salary=df["Monthly Salary"].sum()

        total_emp=len(df)

        paid=(df["Salary Status"]=="Paid").sum()

        pending=(df["Salary Status"]=="Pending").sum()

        c1,c2,c3,c4=st.columns(4)

        c1.metric("Employees",total_emp)

        c2.metric("Salary Expense",
                  f"₹ {total_salary:,.0f}")

        c3.metric("Paid",paid)

        c4.metric("Pending",pending)

        st.divider()

        st.subheader("👨‍🌾 Employee Register")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.bar_chart(
            df.groupby("Designation").size()
        )

        st.download_button(
            "📥 Download Employee Report",
            df.to_csv(index=False).encode(),
            "employees.csv",
            "text/csv"
        )

    else:

        st.info("No employee records available.")
