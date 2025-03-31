import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid import GridOptionsBuilder, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode
import io

st.set_page_config(layout="wide")
st.title("Data Glide Management")

file_path = "/Users/shrutisharma/PycharmProjects/Batch8/mypandasmodule/annual-enterprise-survey.csv"

df = pd.read_csv(file_path)

menu = ["Year", "Value", "Industry_aggregation_NZSIOC", "Industry_code_NZSIOC", "Industry_name_NZSIOC", "Units",
        "Variable_code", "Variable_name", "Variable_category", "Industry_code_ANZSIC06"]
choice = st.sidebar.selectbox("Select an option", menu)

col1, col2 = st.columns([1, 3])
with col1:
    st.subheader("Annual Enterprise Survey Data")

with col2:
    selected_year = st.selectbox('Select Year', df['Year'].unique(), key='year')

filtered_df = df[df['Year'] == selected_year]

column_order = ['Year', 'Value', 'Industry_aggregation_NZSIOC', 'Industry_code_NZSIOC', 'Industry_name_NZSIOC',
                'Units', 'Variable_code', 'Variable_name', 'Variable_category', 'Industry_code_ANZSIC06']

filtered_df = filtered_df[column_order]

# Displaying the data table with AgGrid
AgGrid(filtered_df)

if choice == "Year":
    st.subheader("Bar Chart for Year-wise data")
    chart_data = df.groupby('Year')['Value'].sum().reset_index()
    st.bar_chart(chart_data.set_index('Year'))

elif choice == "Industry_aggregation_NZSIOC":
    st.subheader("Bar Chart for Industry Aggregation")
    chart_data = df.groupby('Industry_aggregation_NZSIOC')['Value'].sum().reset_index()
    st.bar_chart(chart_data.set_index('Industry_aggregation_NZSIOC'))

elif choice == "Industry_code_NZSIOC":
    st.subheader("Bar Chart for Industry Code")
    chart_data = df.groupby('Industry_code_NZSIOC')['Value'].sum().reset_index()
    st.bar_chart(chart_data.set_index('Industry_code_NZSIOC'))

elif choice == "Industry_name_NZSIOC":
    st.subheader("Bar Chart for Industry Name")
    chart_data = df.groupby('Industry_name_NZSIOC')['Value'].sum().reset_index()
    st.bar_chart(chart_data.set_index('Industry_name_NZSIOC'))

elif choice == "Units":
    st.subheader("Bar Chart for Units")
    chart_data = df.groupby('Units')['Value'].sum().reset_index()
    st.bar_chart(chart_data.set_index('Units'))

elif choice == "Variable_code":
    st.subheader("Bar Chart for Variable Code")
    chart_data = df.groupby('Variable_code')['Value'].sum().reset_index()
    st.bar_chart(chart_data.set_index('Variable_code'))

elif choice == "Variable_name":
    st.subheader("Bar Chart for Variable Name")
    chart_data = df.groupby('Variable_name')['Value'].sum().reset_index()
    st.bar_chart(chart_data.set_index('Variable_name'))

elif choice == "Variable_category":
    st.subheader("Bar Chart for Variable Category")
    chart_data = df.groupby('Variable_category')['Value'].sum().reset_index()
    st.bar_chart(chart_data.set_index('Variable_category'))

elif choice == "Industry_code_ANZSIC06":
    st.subheader("Bar Chart for Industry Code ANZSIC06")
    chart_data = df.groupby('Industry_code_ANZSIC06')['Value'].sum().reset_index()
    st.bar_chart(chart_data.set_index('Industry_code_ANZSIC06'))

else:
    st.write("Select a valid column to plot the bar chart.")


#Download button

@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_df)

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',

)


