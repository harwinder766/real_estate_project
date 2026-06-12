import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title='Price Prediction')

@st.cache_data
def load_dataset():
    with open('pickle_files/df_new.pkl','rb') as file:
        df = pickle.load(file)
    return df

@st.cache_resource
def load_model():
    with open('pickle_files/pipeline_new.pkl','rb') as file:
        pipeline = pickle.load(file)
    return pipeline

st.header('Enter your inputs')

df = load_dataset()
pipeline = load_model()
property_type = st.selectbox('Property Type', ['flat','house'])
sector = st.selectbox('Sector',df['sector'].unique().tolist())  


bedrooms = float(st.selectbox('Number of Bedroom',sorted(df['bedRoom'].unique().tolist())))

bathroom = float(st.selectbox('Number of Bathrooms',sorted(df['bathroom'].unique().tolist())))

balcony = st.selectbox('Balconies',sorted(df['balcony'].unique().tolist()))

property_age = st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))
# st.text(property_age)
built_up_area =float(st.number_input(
    "Built Up Area",
    min_value=100.0,
    value=1000.0,
    step=50.0
))

servant_room = st.selectbox('Servant Room',['Not Required', 'Required'])
if servant_room == 'Not Required':
    add_room_1 = 0.0
else:
    add_room_1 = 1.0

study_room = st.selectbox('Store Room',['Not Required', 'Required'])
if study_room == 'Not Required':
    add_room_2 = 0.0
else:
    add_room_2 = 1.0

furnishing_type = st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique().tolist()))
luxury_category = st.selectbox('Luxury Category',sorted(df['luxury_category'].unique().tolist()))
floor_category = st.selectbox('Floor Category',sorted(df['floor_category'].unique().tolist()))

import pandas as pd

zone_mapping = {
    # Golf Course Road
    'sector 24': 'Golf Course Road',
    'sector 25': 'Golf Course Road',
    'sector 26': 'Golf Course Road',
    'sector 27': 'Golf Course Road',
    'sector 28': 'Golf Course Road',
    'sector 43': 'Golf Course Road',
    'sector 53': 'Golf Course Road',
    'sector 54': 'Golf Course Road',
    'golf course corridor': 'Golf Course Road',

    # Golf Course Extension
    'sector 55': 'Golf Course Extension',
    'sector 56': 'Golf Course Extension',
    'sector 57': 'Golf Course Extension',
    'sector 58': 'Golf Course Extension',
    'sector 59': 'Golf Course Extension',
    'sector 60': 'Golf Course Extension',
    'sector 61': 'Golf Course Extension',
    'sector 62': 'Golf Course Extension',
    'sector 63': 'Golf Course Extension',
    'sector 63a': 'Golf Course Extension',
    'sector 65': 'Golf Course Extension',
    'sector 66': 'Golf Course Extension',
    'sector 67': 'Golf Course Extension',
    'sector 67a': 'Golf Course Extension',
    'sector 68': 'Golf Course Extension',
    'sector 69': 'Golf Course Extension',
    'sector 70': 'Golf Course Extension',
    'sector 70a': 'Golf Course Extension',
    'sector 71': 'Golf Course Extension',
    'sector 72': 'Golf Course Extension',
    'sector 73': 'Golf Course Extension',
    'sector 74': 'Golf Course Extension',

    # Dwarka Expressway
    'dwarka expressway': 'Dwarka Expressway',
    'sector 36a': 'Dwarka Expressway',
    'sector 37c': 'Dwarka Expressway',
    'sector 37d': 'Dwarka Expressway',
    'sector 99': 'Dwarka Expressway',
    'sector 99a': 'Dwarka Expressway',
    'sector 102': 'Dwarka Expressway',
    'sector 103': 'Dwarka Expressway',
    'sector 104': 'Dwarka Expressway',
    'sector 105': 'Dwarka Expressway',
    'sector 106': 'Dwarka Expressway',
    'sector 107': 'Dwarka Expressway',
    'sector 108': 'Dwarka Expressway',
    'sector 109': 'Dwarka Expressway',
    'sector 110': 'Dwarka Expressway',
    'sector 111': 'Dwarka Expressway',
    'sector 112': 'Dwarka Expressway',
    'sector 113': 'Dwarka Expressway',

    # New Gurgaon
    'sector 76': 'New Gurgaon',
    'sector 77': 'New Gurgaon',
    'sector 78': 'New Gurgaon',
    'sector 79': 'New Gurgaon',
    'sector 80': 'New Gurgaon',
    'sector 81': 'New Gurgaon',
    'sector 82': 'New Gurgaon',
    'sector 82a': 'New Gurgaon',
    'sector 83': 'New Gurgaon',
    'sector 84': 'New Gurgaon',
    'sector 85': 'New Gurgaon',
    'sector 86': 'New Gurgaon',
    'sector 88': 'New Gurgaon',
    'sector 89': 'New Gurgaon',
    'sector 90': 'New Gurgaon',
    'sector 91': 'New Gurgaon',
    'sector 92': 'New Gurgaon',
    'sector 93': 'New Gurgaon',
    'sector 95': 'New Gurgaon',

    # Sohna Road
    'sohna road': 'Sohna Road',
    'sector 33': 'Sohna Road',
    'sector 36': 'Sohna Road',
    'sector 38': 'Sohna Road',
    'sector 47': 'Sohna Road',
    'sector 48': 'Sohna Road',
    'sector 49': 'Sohna Road',
    'sector 50': 'Sohna Road',

    # Central Gurgaon
    'sector 1': 'Central Gurgaon',
    'sector 2': 'Central Gurgaon',
    'sector 3': 'Central Gurgaon',
    'sector 4': 'Central Gurgaon',
    'sector 5': 'Central Gurgaon',
    'sector 6': 'Central Gurgaon',
    'sector 7': 'Central Gurgaon',
    'sector 8': 'Central Gurgaon',
    'sector 9': 'Central Gurgaon',
    'sector 9a': 'Central Gurgaon',
    'sector 10a': 'Central Gurgaon',
    'sector 11': 'Central Gurgaon',
    'sector 12': 'Central Gurgaon',
    'sector 13': 'Central Gurgaon',
    'sector 14': 'Central Gurgaon',
    'sector 15': 'Central Gurgaon',
    'sector 17': 'Central Gurgaon',
    'sector 18': 'Central Gurgaon',
    'sector 21': 'Central Gurgaon',
    'sector 22': 'Central Gurgaon',
    'sector 23': 'Central Gurgaon',
    'sector 30': 'Central Gurgaon',
    'sector 31': 'Central Gurgaon',
    'sector 32': 'Central Gurgaon',
    'sector 39': 'Central Gurgaon',
    'sector 40': 'Central Gurgaon',
    'sector 41': 'Central Gurgaon',
    'sector 45': 'Central Gurgaon',
    'sector 46': 'Central Gurgaon',
    'sector 51': 'Central Gurgaon',
    'sector 52': 'Central Gurgaon',

    # Peripheral
    'manesar': 'Peripheral & Outskirts',
    'bissar': 'Peripheral & Outskirts',
    'farukhnagar': 'Peripheral & Outskirts',
    'delhi ncr': 'Peripheral & Outskirts'
}

def get_zone(sector):
    """
    Returns the zone corresponding to a sector.
    """
    sector = str(sector).lower().strip()
    return zone_mapping.get(sector, "Unknown")

zone = get_zone(sector)
count = False
if st.button('Predict'):
    # form a dataframe
    data= [['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
       'agePossession', 'built_up_area', 'study room', 'servant room',
       'furnishing_type', 'luxury_category', 'floor_category', 'zone']]
    
    data = [[property_type, sector, bedrooms, bathroom, balcony,property_age,built_up_area,add_room_2,add_room_1,furnishing_type,luxury_category,floor_category,zone]]
    columns = df.columns
    one_df = pd.DataFrame(data,columns=columns)

    data_inference = [[property_type, sector, bedrooms, bathroom, balcony,property_age,built_up_area,study_room, servant_room,furnishing_type,luxury_category,floor_category,zone]]
    infer_module = pd.DataFrame(data= data_inference,columns= columns)
    st.session_state["infer_module"] = infer_module
    st.session_state["one_df"] = one_df

    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price-0.22
    high = base_price+0.22
    if built_up_area<200:
        st.warning("Built Up Area below 200 sq.ft. is unusual. Please verify the value.")

    price_per_sqft = base_price * 10000000 / built_up_area
    
    st.session_state.prediction_result = {
    "base_price": base_price,
    "low": low,
    "high": high,
    "price_per_sqft": price_per_sqft
}   
    st.session_state.last_inputs = one_df.copy()
    st.session_state.prediction_done = True

if st.session_state.get("prediction_done", False):

    result = st.session_state.prediction_result

    st.success("Prediction Complete")

    st.markdown(f"""
    <div style="
    padding:20px;
    border-radius:10px;
    background-color:#1f2937;
    border:1px solid #374151;
    ">
    <h2>🏠 Estimated Property Value</h2>
    <h1>₹ {result['base_price']:.2f} Cr</h1>
    <p>Expected Range: ₹ {result['low']:.2f} Cr - ₹ {result['high']:.2f} Cr</p>
    </div>
    """, unsafe_allow_html=True)

    st.metric(
        "Estimated Price/Sq.ft.",
        f"₹ {result['price_per_sqft']:,.0f}"
    )

    st.info("Want to know why the model predicted this price?")

    if st.button("Open Inference Module"):
        st.switch_page("pages/4_Inference_Module.py")

current_inputs = pd.DataFrame(
    [[property_type, sector, bedrooms, bathroom, balcony,
      property_age, built_up_area, add_room_2, add_room_1,
      furnishing_type, luxury_category, floor_category, zone]],
    columns=df.columns
)

if "last_inputs" in st.session_state:
    if not current_inputs.equals(st.session_state.last_inputs):

        st.session_state.prediction_done = False

        if "prediction_result" in st.session_state:
            del st.session_state["prediction_result"]
        
        if "infer_module" in st.session_state:
            del st.session_state["infer_module"]
        if "one_df" in st.session_state:
            del st.session_state["one_df"]
        
        