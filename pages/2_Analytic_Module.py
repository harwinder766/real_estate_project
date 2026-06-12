import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import ast
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

st.set_page_config(page_title="Plotting Demo")

@st.cache_data
def load_dataset_1():
    with open('pickle_files/data_for_analytic_module.pkl','rb') as file:
        df = pickle.load(file)
    return df

df= load_dataset_1()
st.header("Gurgaon Real Estate Hotspots")

group_df = (
    df.groupby('sector')
    .agg(
        price=('price','mean'),
        price_per_sqft=('price_per_sqft','mean'),
        latitude=('latitude','mean'),
        longitude=('longitude','mean'),
        property_count=('sector','count')
    )
    .reset_index()
)
fig1 = px.scatter_mapbox(
    group_df,
    lat='latitude',
    lon='longitude',
    color='price_per_sqft',
    size='property_count',
    hover_name='sector',
    hover_data={
        'price':':.2f',
        'price_per_sqft':':.0f',
        'property_count':True
    },
    zoom=10,
    mapbox_style='open-street-map',
    color_continuous_scale='Turbo'
)

st.plotly_chart(fig1, use_container_width=True)
st.caption(
    "Bubble size represents number of listings and color indicates average price per sqft."
)

st.header("Top Amenities in Selected Sector")

@st.cache_data
def load_dataset_2():
    with open('pickle_files/wordcloud_df.pkl','rb') as file:
        df = pickle.load(file)
    return df

wordcloud_df = load_dataset_2()

sector_1 = st.selectbox(
    'Sector',
    sorted(wordcloud_df['sector'].unique()),
    key = 'sector_1'
)

def func(sector):
    a = wordcloud_df[wordcloud_df['sector'] == sector]

    main = []

    for item in a['features'].dropna().apply(ast.literal_eval):
        main.extend(item)

    return ' '.join(main)


feature_text = func(sector_1)

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color='black',
    stopwords={'s'},
    min_font_size=10
).generate(feature_text)

# Create figure
fig2, ax = plt.subplots(figsize=(8, 8))

ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')

# Pass figure to streamlit
st.pyplot(fig2)

# Optional: free memory
plt.close(fig2)

st.header('Area Vs Price')

property_type_1 = st.selectbox('Select Property Type', ['flat','house'],key = 'property_type_1')

if property_type_1 == 'house':
    fig3 = px.scatter(df[df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom")

    st.plotly_chart(fig3, use_container_width=True)
else:
    fig3 = px.scatter(df[df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom",)

    st.plotly_chart(fig3, use_container_width=True)

# Average Price Per Sqft of top 15 sectors
st.header('Average Price per Sqft by Sector (Top 15)')

temp_df = df.groupby('sector')['price_per_sqft'].mean().reset_index().sort_values(by = 'price_per_sqft',ascending = False).head(15)
property_type_6= st.selectbox(
    'Select Property Type',
    ['flat', 'house'],
    key = 'property_type_6'
)

if property_type_6 == 'flat':
    temp_df_0 = df[df['property_type'] == 'flat']
    temp_df = temp_df_0.groupby('sector')['price_per_sqft'].mean().reset_index().sort_values(by = 'price_per_sqft',ascending = False).head(15)
    fig9 = px.bar(
    temp_df,
    x='sector',
    y='price_per_sqft',
    color='sector'
)
    fig9.update_layout(
        xaxis_title='Sector',
        yaxis_title='Average Price Per Sqft',
        template='plotly_dark',
        height=500
    )
    st.plotly_chart(fig9, use_container_width=True)
        
else:
    temp_df_0 = df[df['property_type'] == 'house']
    temp_df = temp_df_0.groupby('sector')['price_per_sqft'].mean().reset_index().sort_values(by = 'price_per_sqft',ascending = False).head(15)
    fig9 = px.bar(
    temp_df,
    x='sector',
    y='price_per_sqft',
    color='sector'
)
    fig9.update_layout(
        xaxis_title='Sector',
        yaxis_title='Average Price Per Sqft',
        template='plotly_dark',
        height=500
    )
    st.plotly_chart(fig9, use_container_width=True)
  
# BHK Pie Chart

st.header('BHK Pie Chart')

sector_options = df['sector'].unique().tolist()
sector_options.insert(0,'overall')
selected_sector = st.selectbox('Select Sector',sector_options)

property_type_2 = st.selectbox("Select Property type",['flat','house'],key = 'property_type_2')

if selected_sector == 'overall':
    fig4 = px.pie(df[df['property_type'] == property_type_2],names = 'bedRoom')
    st.plotly_chart(fig4, use_container_width=True)
else:
    fig4 = px.pie(df[(df['sector'] ==selected_sector)& (df['property_type'] == property_type_2)],names = 'bedRoom')
    st.plotly_chart(fig4, use_container_width=True)

st.header('Side by Side BHK price comparison')

fig5= px.box(df[df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig5, use_container_width=True)

house_price = df[df['property_type'] == 'house']['price']
flat_price = df[df['property_type'] == 'flat']['price']

st.header('Price Distribution: House vs Flat')

fig6 = ff.create_distplot(
    [house_price, flat_price],
    ['House', 'Flat'],
    show_hist=False,
    show_rug=False
)

fig6.update_layout(
    xaxis_title='Price (Cr)',
    yaxis_title='Density',
    template='plotly_dark',
    height=500
)

st.plotly_chart(fig6, use_container_width=True)

# Property Age vs Price
st.header('Property Age vs Price')

property_type_3 = st.selectbox(
    'Select Property Type',
    ['flat', 'house']
)

temp_df = (
    df[df['property_type'] == property_type_3]
    .groupby('agePossession')['price']
    .mean()
    .reset_index()
)

fig7 = px.bar(
    temp_df,
    x='agePossession',
    y='price',
    color='agePossession',

)
fig7.update_layout(
    xaxis_title='Property Age',
    yaxis_title='Price (Cr)',
    template='plotly_dark',
    height=500
)
st.plotly_chart(fig7, use_container_width=True)

# Furnishing Type vs Price

st.header('Furnishing Type vs Price')

property_type_4= st.selectbox(
    'Select Property Type',
    ['flat', 'house'],
    key = 'property_type_4'
)

temp_df = (
    df[df['property_type'] == property_type_3]
    .groupby('furnishing_type')['price']
    .mean()
    .reset_index()
)

fig8 = px.bar(
    temp_df,
    x='furnishing_type',
    y='price',
    color='furnishing_type',
    title='Average Price by Furnishing Type'
)
fig8.update_layout(
    xaxis_title='Furnishing Type',
    yaxis_title='Price (Cr)',
    template='plotly_dark',
    height=500
)
st.plotly_chart(fig8, use_container_width=True)

# Heatmap
st.header('Feature Correlation Heatmap')

corr_cols = [
    'price',
    'built_up_area',
    'bedRoom',
    'bathroom',
    'servant room',
    'study room',
    'price_per_sqft',
    'latitude',
    'longitude'
]

corr_matrix = df[corr_cols].corr()

fig = px.imshow(
    corr_matrix,
    text_auto=True,
    aspect='auto',
    color_continuous_scale='RdBu_r',
)

fig.update_layout(height=700)

st.plotly_chart(fig, use_container_width=True)