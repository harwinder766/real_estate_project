import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import ast

st.set_page_config(page_title="Analytic Module")

@st.cache_data
def load_location_df():
    with open('pickle_files\location_df.pkl','rb') as file:
        location_df = pickle.load(file)
    return location_df

@st.cache_data
def load_link_df():
    with open('pickle_files\link_df.pkl','rb') as file:
        link_df = pickle.load(file)
    return link_df

@st.cache_data
def load_pricedetails():
    with open('pickle_files\cosine_sim_pricedetails.pkl','rb') as file:
        cosine_sim_pricedetails = pickle.load(file)
    return cosine_sim_pricedetails
@st.cache_data
def load_facilities():
    with open('pickle_files\cosine_sim_facilities.pkl','rb') as file:
        cosine_sim_facilities = pickle.load(file)
    return cosine_sim_facilities
@st.cache_data
def load_location():
    with open('pickle_files\cosine_sim_location.pkl','rb') as file:
        cosine_sim_facilities = pickle.load(file)
    return cosine_sim_facilities

cosine_sim_location= load_location()
cosine_sim_pricedetails= load_pricedetails()
cosine_sim_facilities = load_facilities()
link_df = load_link_df()
def recommend_properties_with_scores(property_name, top_n=7):

    cosine_sim_matrix = 30*cosine_sim_facilities + 10*cosine_sim_pricedetails + 15*cosine_sim_location
    # cosine_sim_matrix = cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n+1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df
location_df = load_location_df()
# st.dataframe(location_df)

st.title('Select Location and Radius')

selected_location = st.selectbox(
    'Location',
    sorted(location_df.columns.to_list())
)

radius = st.number_input('Radius in Kms', min_value=1)

# Search button
if st.button('Search'):
    
    if radius>53:
        st.warning("No properties found within the selected radius")
        st.stop()

    result_ser = location_df[
        location_df[selected_location] < radius * 1000
    ][selected_location].sort_values()

    apartments = []

    for key, value in result_ser.items():
        apartments.append(
            f"{key} ---> {round(value/1000,2)} km"
        )
    # Store in session state
    st.session_state.apartments = apartments
    


# Show apartments if available
if 'apartments' in st.session_state:

    if len(st.session_state.apartments)>0:

        selected_apartment = st.radio(
            'Select a property for recommendation',
            st.session_state.apartments,
            key='selected_property',
            index = None
        )
        if selected_apartment:
            property_name = selected_apartment.split('--->')[0].strip()
        
            # Generate recommendations
            recommendations = recommend_properties_with_scores(
                property_name
            )
        
            # Store recommendations
            st.session_state.recommendations = recommendations
    else:
        st.warning("No properties found within the selected radius")

        if 'recommendations' in st.session_state:
            del st.session_state.recommendations

        if 'apartments' in st.session_state:
            del st.session_state.apartments
 
if 'recommendations' in st.session_state:

    st.subheader("🏡 Recommended Properties")

    recommendations_df = pd.DataFrame(
        st.session_state.recommendations
    )

    prop_names = recommendations_df['PropertyName'].tolist()

    recomm_prop = link_df[
        link_df['PropertyName'].isin(prop_names)
    ]

    max_score = recommendations_df['SimilarityScore'].max()

    for _, row in recommendations_df.iterrows():

        property_name = row['PropertyName']
        similarity_score = row['SimilarityScore']

        match_percent = (
            similarity_score / max_score
        ) * 100

        prop_link = recomm_prop[
            recomm_prop['PropertyName'] == property_name
        ]['Link'].values[0]

        with st.container(border=True):

            col1, col2 = st.columns([4,1])

            with col1:

                st.markdown(
                    f"### 🏢 {property_name}"
                )

                st.caption(
                    f"Match Score: {match_percent:.0f}%"
                )

                st.progress(
                    float(match_percent) / 100
                )

            with col2:

                st.metric(
                    "Similarity",
                    f"{similarity_score:.1f}"
                )

            with st.expander("Why Recommended?"):

                st.write(
                    "✓ Similar facilities"
                )

                st.write(
                    "✓ Similar location advantages"
                )

                st.write(
                    "✓ Similar price range"
                )

            st.link_button(
                "🔗 View on 99acres",
                prop_link,
                use_container_width=True
            )

    

