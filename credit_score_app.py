import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

# Set Streamlit layout
st.set_page_config(page_title="Credit Score Segmentation", layout="wide")

# Load data
data = pd.read_csv("credit_scoring.csv")

# Define the mapping for categorical features
education_level_mapping = {'High School': 1, 'Bachelor': 2, 'Master': 3, 'PhD': 4}
employment_status_mapping = {'Unemployed': 0, 'Employed': 1, 'Self-Employed': 2}

# Apply mapping to categorical features
data['Education Level'] = data['Education Level'].map(education_level_mapping)
data['Employment Status'] = data['Employment Status'].map(employment_status_mapping)

# Calculate credit scores
data['Credit Score'] = (data['Payment History'] * 0.35) + (data['Credit Utilization Ratio'] * 0.30) + (data['Number of Credit Accounts'] * 0.15) + (data['Education Level'] * 0.10) + (data['Employment Status'] * 0.10)

# Clustering using KMeans
X = data[['Credit Score']]
kmeans = KMeans(n_clusters=4, n_init=10, random_state=42)
data['Segment'] = kmeans.fit_predict(X)
data['Segment'] = data['Segment'].map({2: 'Very Low', 0: 'Low', 1: 'Good', 3: 'Excellent'})

# Streamlit UI
st.title("Customer Segmentation based on Credit Scores")
st.write("Explore different segments of customers based on their credit scores.")

# Display the DataFrame
st.write("Data Sample:")
st.dataframe(data)

# Create a scatter plot using Plotly Express
fig = px.scatter(data, x=data.index, y='Credit Score', color='Segment',
                 color_discrete_sequence=['green', 'blue', 'yellow', 'red'])
fig.update_layout(
    xaxis_title='Customer Index',
    yaxis_title='Credit Score',
    title='Customer Segmentation based on Credit Scores'
)

# Display the Plotly figure using Streamlit
st.plotly_chart(fig, use_container_width=True)
