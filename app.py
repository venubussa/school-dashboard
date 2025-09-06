import streamlit as st
import pandas as pd
import duckdb
import os

st.set_page_config(page_title="School Dashboard - DuckDB", layout="wide")
st.title("📊 School Dashboard - DuckDB Version")

csv_path = r"C:\Users\Venu\Pictures\school-bi\data\students.csv"

if os.path.exists(csv_path):
    # --- Connect to DuckDB ---
    con = duckdb.connect("school.duckdb")

    # --- Read CSV into DuckDB ---
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS students AS
        SELECT * FROM read_csv_auto('{csv_path}')
    """)

    # --- Sidebar Filters ---
    st.sidebar.header("🔧 Filters")
    classes = con.execute("SELECT DISTINCT class FROM students").fetchall()
    subjects = con.execute("SELECT DISTINCT subject FROM students").fetchall()

    selected_class = st.sidebar.multiselect("Select Class:", options=[c[0] for c in classes], default=[c[0] for c in classes])
    selected_subject = st.sidebar.multiselect("Select Subject:", options=[s[0] for s in subjects], default=[s[0] for s in subjects])

    # --- Query filtered data ---
    query = f"""
        SELECT * FROM students
        WHERE class IN ({','.join([f"'{c}'" for c in selected_class])})
        AND subject IN ({','.join([f"'{s}'" for s in selected_subject])})
    """
    filtered_df = con.execute(query).df()

    st.success(f"Filtered data loaded ({len(filtered_df)} rows)")

    # --- KPI Cards ---
    total_students = len(filtered_df)
    highest_marks = filtered_df["marks"].max()
    lowest_marks = filtered_df["marks"].min()
    average_marks = round(filtered_df["marks"].mean(), 2)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("👩‍🎓 Total Students", total_students)
    kpi2.metric("🏆 Highest Marks", highest_marks)
    kpi3.metric("📉 Lowest Marks", lowest_marks)
    kpi4.metric("📊 Average Marks", average_marks)

    # --- Conditional Formatting ---
    def color_marks(val):
        if val >= 90:
            return 'background-color: #b6fcb6'
        elif val <= 70:
            return 'background-color: #fcb6b6'
        else:
            return ''

    # --- Students Table ---
    st.subheader("👩‍🎓 Students Table")
    st.dataframe(filtered_df.style.applymap(color_marks, subset=['marks']))

    # --- Charts ---
    col1, col2 = st.columns(2)
    with col1:
        avg_subject = filtered_df.groupby("subject")["marks"].mean().reset_index()
        st.subheader("📈 Average Marks by Subject")
        st.bar_chart(avg_subject.rename(columns={"marks": "Average Marks"}).set_index("subject"))

    with col2:
        avg_class = filtered_df.groupby("class")["marks"].mean().reset_index()
        st.subheader("🏫 Average Marks by Class")
        st.bar_chart(avg_class.rename(columns={"marks": "Average Marks"}).set_index("class"))

    # --- Drillthrough / Comparison ---
    st.subheader("🔎 Student Drillthrough & Comparison")
    student_name = st.selectbox("Select a student:", filtered_df["name"].unique())
    student_data = filtered_df[filtered_df["name"] == student_name]
    st.table(student_data.style.applymap(color_marks, subset=['marks']))
    st.image(student_data.iloc[0]["photo_url"], width=150)

    selected_students = st.multiselect("Compare Students:", filtered_df["name"].unique())
    compare_data = filtered_df[filtered_df["name"].isin(selected_students)]
    if not compare_data.empty:
        compare_chart = compare_data.pivot(index="subject", columns="name", values="marks")
        st.bar_chart(compare_chart)

else:
    st.error(f"CSV not found at: {csv_path}")
