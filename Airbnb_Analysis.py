import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import os
from PIL import Image
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="AirBnb-Analysis by ARUNKUMAR BAIRAVAN!!!", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart:   AirBnb-Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)





st.header("Explore Data")
fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="ISO-8859-1")
else:
    os.chdir(r"C:\\Users\\jithe\\Downloads\\")
    df = pd.read_csv("AirBnb_data.csv", encoding="ISO-8859-1")

st.sidebar.header("Choose your filter: ")

 # Create for neighbourhood_group
city = st.sidebar.multiselect("Pick your neighbourhood_group", df["city"].unique())
if not city:
     df2 = df.copy()
else:
     df2 = df[df["city"].isin(city)]

 # Create for neighbourhood
neighbourhood = st.sidebar.multiselect("Pick the neighbourhood", df2["neighbourhood"].unique())
if not neighbourhood:
     df3 = df2.copy()
else:
     df3 = df2[df2["neighbourhood"].isin(neighbourhood)]

 # Filter the data based on neighbourhood_group, neighbourhood

if not city and not neighbourhood:
     filtered_df = df
elif not neighbourhood:
     filtered_df = df[df["city"].isin(city)]
elif not city:
     filtered_df = df[df["neighbourhood"].isin(neighbourhood)]
elif neighbourhood:
     filtered_df = df3[df["neighbourhood"].isin(neighbourhood)]
elif city:
     filtered_df = df3[df["city"].isin(city)]
elif city and neighbourhood:
     filtered_df = df3[df["city"].isin(city) & df3["neighbourhood"].isin(neighbourhood)]
else:
     filtered_df = df3[df3["city"].isin(city) & df3["neighbourhood"].isin(neighbourhood)]

room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

col1, col2 = st.columns(2)
with col1:
    st.subheader("room_type_ViewData")
    fig = px.bar(room_type_df, x="room_type", y="price", text=['${:,.2f}'.format(x) for x in room_type_df["price"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("city_ViewData")
    fig = px.pie(filtered_df, values="price", names="city", hole=0.5)
    fig.update_traces(text=filtered_df["city"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("room_type wise price"):
        st.write(room_type_df.style.background_gradient(cmap="Blues"))
        csv = room_type_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

with cl2:
    with st.expander("city wise price"):
        city = filtered_df.groupby(by="city", as_index=False)["price"].sum()
        st.write(city.style.background_gradient(cmap="Oranges"))
        csv = city.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="city.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

 # Create a scatter plot
data1 = px.scatter(filtered_df, x="city", y="neighbourhood", color="room_type")
data1['layout'].update(title="Room_type in the Neighbourhood and city wise data using Scatter Plot.",
                        titlefont=dict(size=20), xaxis=dict(title="city", titlefont=dict(size=20)),
                        yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
st.plotly_chart(data1, use_container_width=True)

with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
     st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

# Download orginal DataSet
csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

import plotly.figure_factory as ff

st.subheader(":point_right: city wise Room_type and Minimum stay nights")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["city", "neighbourhood", "room_type", "price", "minimum_nights", "host_name"]]
    fig = ff.create_table(df_sample, colorscale="Cividis")
    st.plotly_chart(fig, use_container_width=True)

# map function for room_type

# If your DataFrame has columns 'Latitude' and 'Longitude':
st.subheader("Airbnb Analysis in Map view")
df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})

st.map(df)

