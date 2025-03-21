import pandas as pd
import numpy as np
import streamlit as st
import tensorflow as tf
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder

import pickle


model=tf.keras.models.load_model('Salaryregression.h5')

with open('onehot_encoder_geo_regression.pkl','rb') as file:
    onehot_encoder_geo_regression=pickle.load(file)

with open('label_encoder_gneder_regression.pkl','rb') as file:
    label_encoder_gneder_regression=pickle.load(file)


with open('scaler_regression.pkl','rb') as file:
    scaler_regression=pickle.load(file)


st.title("Customer Salary Prediction")



geography = st.selectbox('Geography', onehot_encoder_geo_regression.categories_[0])
gender = st.selectbox('Gender', label_encoder_gneder_regression.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
Exited= st.selectbox('Has Exited or Not', [0, 1])
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])




input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder_gneder_regression.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'Exited': [Exited]
})



geo_encoded = onehot_encoder_geo_regression.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns=onehot_encoder_geo_regression.get_feature_names_out(['Geography']))

# Combine one-hot encoded columns with input data
input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)

# Scale the input data
input_data_scaled = scaler_regression.transform(input_data)


# Predict churn
prediction = model.predict(input_data_scaled)
predicted=prediction[0][0]

st.write(f'Estimated Salary: {predicted:.2f}')




