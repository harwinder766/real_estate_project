import streamlit as st

st.title("🏠 Real Estate Intelligence Platform")
st.markdown("""
### AI-Powered Property Valuation, Analytics & Recommendations

An end-to-end real estate analytics platform built using Machine Learning,
Explainable AI, and Recommendation Systems to help users estimate property
prices, explore market insights, discover similar properties, and understand
the reasoning behind every prediction.
""")

# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     st.metric("Properties", "250+")

# with col2:
#     st.metric("Sectors Covered", "120+")

# with col3:
#     st.metric("ML Model", "XGBoost")

# with col4:
#     st.metric("Modules", "4")

# st.divider()

st.header("🚀 Platform Features")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    ### 🏠 Price Prediction

    Estimate property prices using an XGBoost-based machine learning model
    trained on Gurgaon real estate data.

    ✓ Instant valuation
    ✓ Price per Sq.Ft estimation
    ✓ Confidence range
    """)

    st.info("""
    ### 🎯 Recommendation Engine

    Discover properties similar to your preferred property based on:

    • Location Advantages
    • Amenities & Facilities
    • Price Characteristics
    """)

with col2:
    st.info("""
    ### 📊 Analytics Dashboard

    Explore interactive market insights including:

    • Geo Maps
    • Price Distribution
    • Sector Analysis
    • BHK Comparisons
    • Area vs Price Trends
    """)

    st.info("""
    ### 🔍 Explainable AI

    Understand why the model predicted a specific price using SHAP.

    ✓ Feature Contributions
    ✓ Price Drivers
    ✓ Positive & Negative Factors
    """)
st.divider()

st.header("⚙ Technology Stack")

st.markdown("""
- **Machine Learning:** XGBoost
- **Explainable AI:** SHAP
- **Recommendation System:** Cosine Similarity
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly, Matplotlib
- **Web Framework:** Streamlit
""")


st.divider()

st.header("🔄 How It Works")

st.markdown("""
1. Enter property details in the Prediction Module.
2. Get an AI-powered property valuation.
3. Explore factors affecting the prediction.
4. Analyze market trends using interactive dashboards.
5. Discover similar properties through the Recommendation System.
""")

st.divider()

st.caption(
    "Built with Machine Learning, Explainable AI and Data Analytics for Real Estate Intelligence."
)