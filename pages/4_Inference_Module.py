import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import shap
import pickle

if 'one_df' not in st.session_state:
   st.warning('Please make prediction first')
   st.stop()
st.header('Inference Module')
@st.cache_data
def load_pipeline():
    with open('pickle_files/pipeline_new.pkl','rb') as f:
        pipeline = pickle.load(f)
        return pipeline

@st.cache_data
def load_df_new():
    with open('pickle_files/df_new.pkl','rb') as f:
      df_new = pickle.load(f)
    return df_new

pipeline = load_pipeline()
df_new = load_df_new()  
preprocessor = pipeline.named_steps['preprocessor']
model = pipeline.named_steps['regressor']

X = df_new
X_transformed = preprocessor.transform(X)
explainer = shap.TreeExplainer(model)

feature_names = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
       'agePossession', 'built_up_area', 'study room', 'servant room',
       'furnishing_type', 'luxury_category', 'floor_category', 'zone']

infer_module= st.session_state.infer_module
# st.dataframe(infer_module)

one_df = st.session_state.one_df

user_transformed = preprocessor.transform(one_df)
shap_values = explainer(user_transformed)
display_values = infer_module.iloc[0].values

shap_exp = shap.Explanation(
    values=shap_values.values[0],
    base_values=shap_values.base_values[0],
    data=display_values ,       
    feature_names=feature_names
)

fig = plt.figure(figsize=(10,6))

shap.plots.waterfall(
    shap_exp,
    show=False
)

st.pyplot(fig)

shap_df = pd.DataFrame({
    'Feature': feature_names,
    'Contribution': shap_values.values[0]
})

positive = (
    shap_df
    .sort_values('Contribution', ascending=False)
    .head(5)
)

negative = (
    shap_df
    .sort_values('Contribution')
    .head(5)
)

col1,col2 = st.columns(2)
threshold = 0.001
with col1:
    st.subheader("Factors Increasing Price")
    for _, row in positive.iterrows():
        if abs(row['Contribution'])>threshold:
            st.success(
                f"{row['Feature']} (+{row['Contribution']:.3f} Cr)"
            )
with col2:
    st.subheader("Factors Decreasing Price")
    for _, row in negative.iterrows():
        if abs(row['Contribution'])>threshold: 
            st.error(
                f"{row['Feature']} ({row['Contribution']:.3f} Cr)"
            )
    
    top_features = positive['Feature'].tolist()[:3]

positive_sum = positive[positive['Contribution'] > 0]['Contribution'].sum()

negative_sum = abs(
    negative[negative['Contribution'] < 0]['Contribution'].sum()
)
if positive_sum > negative_sum:
    summary = (
        "The positive factors outweighed the negative factors, "
        "resulting in a higher predicted property value."
    )
else:
    summary = (
        "The negative factors outweighed the positive factors, "
        "reducing the final predicted property value."
    )
st.info(
    f"""
   🏆 Largest Positive Contributor\n
    {positive.head(1).to_dict('records')[0]['Feature']} ({round(positive.head(1).to_dict('records')[0]['Contribution'],3)} Cr)\n
    📉 Largest Negative Contributor\n
    {negative.head(1).to_dict('records')[0]['Feature']} ({round(negative.head(1).to_dict('records')[0]['Contribution'],3)} Cr)\n
    {summary}
    """
)
