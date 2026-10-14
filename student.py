import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

 # page configuration
st.set_page_config(page_title="Student Proformence Systeam",layout="wide")
st.title("🎓Student Performance System")

with st.sidebar:
    st.header("📁upload your data")
    uploaded_file = st.file_uploader("Choose a file", type=["csv"])

    st.markdown("---")

    seleted = option_menu(
        menu_title="Main Menu",
        options=[
            "Row Data",
            "student Results",
            "Topper",
            "Search Student",
            "Subject Wise Performance",
            "Fail/Pass Students",
            "Pivot Table",
            "student Performance"
            
            ],
        icons=[
            "table",
            "bar-chart-line",
            "trophy",
            "search",
            "book",
            "check-circle",
            "grid",
           
        ],
        menu_icon="Main Menu-button-wide",
        default_index=0
    )
if uploaded_file is  None:
    st.warning("Please upload a CSV file to continue...")
    st.stop()


df = pd.read_csv(uploaded_file)

if seleted == "Row Data":
    st.subheader("Row Data")
    st.dataframe(df)


elif seleted == "student Results":
    total=df.groupby("Name")["Marks"].sum()
    avg=df.groupby("Name")["Marks"].mean()

    result=pd.DataFrame({
        "Total":total,
        "Average":avg
        }).reset_index()
    
    st.dataframe(result)

elif seleted == "Topper":
    total=df.groupby("Name")["Marks"].sum().sort_values(ascending=False)

    n=st.number_input("Enter the number of toppers to display",min_value=1,max_value=len(total),value=3)
    st.subheader(f"Top{n} Students")
    st.dataframe(total.head(n))

elif seleted=="Search Student":
    st.subheader("Search Student")
    name=st.text_input("Enter the student name to search")
    
    if name:
        filtered_df=df[df["Name"].str.lower()==name.lower()]

        if not filtered_df.empty:
            st.success(f"Showing result for {name}")
            st.dataframe(filtered_df)

            total=filtered_df["Marks"].sum()
            avg=filtered_df["Marks"].mean()

            st.write(f"Total Marks: {total}")
            st.write(f"Percentage: {avg}")

        else:
            st.error("Student not found." 
            " Please check the name and try again..")

elif seleted=="Subject Wise Performance":
     subject_avg=df.groupby("Subject")["Marks"].mean()
     st.subheader("Subject Wise Performance")
     st.dataframe(subject_avg)

elif seleted=="Fail/Pass Students":
    pass_marks=st.slider("Select the passing marks",0,100,40)

    df["Result"]=df["Marks"].apply(lambda x: "Pass" if x >= pass_marks else "Fail")

    st.subheader("Results of Students")
    st.dataframe(df)

    st.subheader("Summary of Results")
    st.dataframe(df["Result"].value_counts())
                 

elif seleted=="Pivot Table":
    pivot=df.pivot_table(
        values="Marks",
        index="Name",
        columns="Subject"
    )

    st.subheader("student VS Subject")
    st.dataframe(pivot)

elif seleted=="student Performance":
    st.subheader("student Performance")
    student_name=st.selectbox("Select a student",df["Name"].unique())

    student_df=df[df["Name"]==student_name]

    st.write(f"Performance of {student_name}")
    st.dataframe(student_df)

    st.bar_chart(student_df.set_index("Subject")["Marks"])

else:
    st.error("🐌Invalid option selected.")


    
            