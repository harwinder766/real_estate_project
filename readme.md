# 🏠 Gurgaon Real Estate Intelligence Platform

A machine learning-powered real estate platform for Gurgaon that helps users:

- Predict property prices
- Discover similar properties
- Analyze market trends
- Understand model predictions using Explainable AI (SHAP)

---

## 🚀 Features

### 1. Price Prediction Module
Predict the estimated market value of a property based on:

- Property Type
- Sector
- Bedrooms
- Bathrooms
- Balconies
- Property Age
- Built-up Area
- Servant Room
- Study Room
- Furnishing Type
- Luxury Category
- Floor Category
- Zone

The model provides:

- Estimated Property Price
- Expected Price Range
- Price per Square Foot

---

### 2. Analytics Module

Interactive visualizations for Gurgaon real estate data:

- Interactive Geographic Bubble Map
- Top Amenities in Selected Sector using Wordcloud
- Area Vs Price
- Average Price per Sqft by Sector (Top 15)
- Correlation analysis
- Price Distribution

Built using Plotly and Streamlit.

---

### 3. 🏘️ Recommendation Module

The Recommendation Module helps users discover properties that match their preferred location and requirements.

How it works:

Select a Location – The user chooses a landmark or point of interest in Gurgaon.
Enter Radius – The system finds all properties within the specified distance from that location.
Choose a Property – The user selects one of the nearby properties.
Get Recommendations – The system recommends similar properties based on:
Location Advantages
Price Characteristics
Available Amenities
Sector Information

The recommendation engine combines multiple similarity scores using a weighted approach to generate the most relevant suggestions.

Output includes:

Recommended Properties
Similarity Score
Match Percentage
Direct 99acres Listing Link

This hybrid recommendation system combines geographic filtering with property similarity analysis to help users find suitable alternatives quickly and efficiently. 

## 🧠 Machine Learning Model

Model Used:

- XGBoost Regressor

Pipeline Includes:

- Feature preprocessing
- Encoding
- Model training
- Prediction pipeline

Performance:

- R² Score: (0.89)
- MAE: (0.48)

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Machine Learning
- Scikit-Learn
- XGBoost
- SHAP

### Data Processing
- Pandas
- NumPy

### Visualization
- Plotly
- Matplotlib
- Plotly

---

## 📂 Project Structure

```text
real_estate_project/
│
├── pages/
│   ├── 1_Price_Prediction.py
│   ├── 2_Analytic_Module.py
│   ├── 3_Recommendation_System.py
│   └── 4_Inference_Module.py
│
├── pipeline.pkl
├── df.pkl
├── location_df.pkl
├── cosine_sim_facilities.pkl
├── cosine_sim_location.pkl
├── cosine_sim_pricedetails.pkl
│
├── requirements.txt
├── README.md
└── Home.py
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/real_estate_project.git
cd real_estate_project
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run Home.py
```

---

## 📊 Dataset

The dataset contains Gurgaon residential property information including:

- Property Details
- Price Information
- Amenities
- Location Advantages
- Sector Information

Data preprocessing includes:

- Missing value handling
- Feature engineering
- Location standardization
- Text processing
- Recommendation feature generation

---

## 🎯 Future Improvements

- Multi-city support
- Interactive property map
- Rental price prediction
- User authentication
- Property comparison dashboard
- AI-powered property chatbot

---

## 👨‍💻 Author

Harwinder Singh
GitHub:
https://github.com/harwinder766

---

## ⭐ If you found this project useful, please consider giving it a star.