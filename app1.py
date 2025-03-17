
import streamlit as st
import numpy as np
import xgboost
import joblib 

model = joblib.load("cal_burned.pkl")

st.set_page_config(page_title="Fitness Tracker", layout="centered")
st.title("🔥 Personal Fitness Tracker 🔥")
st.markdown("### Predict Your Calories Burned")

# Sidebar 
st.sidebar.header("User Inputs")
st.sidebar.image("fitness.jpeg", use_container_width=True)

#Inputs
age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=25, step=1)
gender = st.sidebar.radio("Gender", ("Male", "Female"))

#cm or feet & inches
height_unit = st.sidebar.radio("Height Unit", ("cm", "feet & inches"))
if height_unit == "cm":
    height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170, step=1)
else:
    height_feet = st.sidebar.number_input("Feet", min_value=3, max_value=8, value=5, step=1)
    height_inches = st.sidebar.number_input("Inches", min_value=0, max_value=11, value=7, step=1)
    height = (height_feet * 30.48) + (height_inches * 2.54)  # Convert to cm

weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70, step=1)

#BMI
bmi = weight / ((height / 100) ** 2)
st.sidebar.write(f"**BMI:** {bmi:.2f}")

duration = st.sidebar.slider("Exercise Duration (mins)", min_value=5, max_value=180, value=30, step=5)
heart_rate = st.sidebar.slider("Heart Rate (bpm)", min_value=60, max_value=200, value=100, step=5)
body_temp = st.sidebar.slider("Body Temperature (°C)", min_value=35.0, max_value=42.0, value=37.0, step=0.1)

gender_numeric = 0 if gender == "Male" else 1

# prediction
if st.sidebar.button("Predict Calories Burned 🔥"):
    try:
        input_data = np.array([[age, gender_numeric, height, weight, duration, heart_rate, body_temp]], dtype=np.float32)
        prediction = model.predict(input_data)
        st.success(f"💪 Estimated Calories Burned: **{prediction[0]:.2f} kcal**")

        
        avg_age = 30  
        avg_duration = 45
        avg_heart_rate = 90
        avg_body_temp = 36.5
        avg_bmi = 24.0

        comparisons = [
            f"You are {'older' if age > avg_age else 'younger'} than **{min(abs(age - avg_age) / avg_age * 100, 100):.1f}%** of people.",
            f"You exercise **{min(abs(duration - avg_duration) / avg_duration * 100, 100):.1f}%** {'more' if duration > avg_duration else 'less'} than the average person.",
            f"Your heart rate is **{min(abs(heart_rate - avg_heart_rate) / avg_heart_rate * 100, 100):.1f}%** {'higher' if heart_rate > avg_heart_rate else 'lower'} than average.",
            f"Your body temperature is **{min(abs(body_temp - avg_body_temp) / avg_body_temp * 100, 100):.1f}%** {'higher' if body_temp > avg_body_temp else 'lower'} than average.",
            f"Your BMI is **{min(abs(bmi - avg_bmi) / avg_bmi * 100, 100):.1f}%** {'higher' if bmi > avg_bmi else 'lower'} than the average."
        ]

        st.markdown("### 🔍 How You Compare:")
        for comp in comparisons:
            st.markdown(f"- {comp}")
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")


# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Maintain a balanced diet and stay hydrated!")
