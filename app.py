import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load trained model
model = joblib.load("drone_battery_model.pkl")

st.set_page_config(page_title="Aero Energy Optimizer", page_icon="🚁")

st.title("🚁 Aero Energy Optimizer — Mission Intelligence System")
st.write("AI-powered drone battery prediction, endurance estimation, and mission risk analysis")

st.sidebar.header("🛠️ Drone Flight Parameters")

altitude = st.sidebar.slider("Altitude (meters)", 50, 500, 120)
duration = st.sidebar.slider("Planned Flight Duration (minutes)", 1, 60, 15)
distance = st.sidebar.slider("Distance Flown (km)", 0.5, 15.0, 3.5)
payload = st.sidebar.slider("Payload Weight (kg)", 0.1, 15.0, 2.0)
wind = st.sidebar.slider("Wind Speed (m/s)", 0.0, 20.0, 5.0)

input_data = pd.DataFrame(
    [[altitude, duration, distance, payload, wind]],
    columns=[
        "Altitude (meters)",
        "Flight Duration (minutes)",
        "Distance Flown (km)",
        "Actual Carry Weight (kg)",
        "Wind Speed (m/s)"
    ]
)

if st.button("🚀 Analyze Mission"):

    # Predict battery remaining
    prediction = model.predict(input_data)[0]

    # Battery used
    battery_used = 100 - prediction

    # Battery Prediction
    st.subheader("🔋 Battery Prediction")
    st.success(f"Battery Remaining After Mission: **{prediction:.2f}%**")

    # Endurance Estimation
    estimated_total_time = duration * (100 / max(1, battery_used))
    remaining_time = max(0, estimated_total_time - duration)

    st.subheader("⏱️ Mission Endurance Estimation")
    st.write(f"Estimated Maximum Flight Time: **{estimated_total_time:.1f} minutes**")
    st.write(f"Estimated Remaining Flight Time: **{remaining_time:.1f} minutes**")

    if remaining_time <= 0:
        st.error("🚨 MISSION FAILURE RISK — Drone may not complete mission!")
    elif remaining_time < 10:
        st.warning("⚠️ LOW ENDURANCE — Optimize mission parameters")
    else:
        st.info("✅ MISSION SAFE — Drone endurance is sufficient")

    # Efficiency Score
    efficiency = min(100, max(0, prediction))
    st.subheader("⚡ Energy Efficiency Score")
    st.progress(int(efficiency))
    st.write(f"Efficiency Score: **{efficiency:.1f} / 100**")

    # Mission Risk Meter
    st.subheader("🚨 Mission Risk Meter")

    risk_score = 0

    if prediction < 30:
        risk_score += 40
    elif prediction < 50:
        risk_score += 25

    if payload > 3:
        risk_score += 15

    if wind > 10:
        risk_score += 15

    if altitude > 300:
        risk_score += 10

    if duration > estimated_total_time:
        risk_score += 20

    risk_score = min(100, risk_score)

    st.progress(risk_score)
    st.write(f"Risk Score: **{risk_score} / 100**")

    if risk_score > 70:
        st.error("🔴 HIGH RISK — Mission likely to fail!")
    elif risk_score > 40:
        st.warning("🟡 MEDIUM RISK — Optimize before mission")
    else:
        st.success("🟢 LOW RISK — Mission safe to execute")

    # Optimization Suggestions
    st.subheader("💡 Smart Optimization Suggestions")

    if payload > 3:
        st.write("🔹 Reduce payload to extend endurance")
    if altitude > 300:
        st.write("🔹 Lower altitude to reduce energy consumption")
    if wind > 10:
        st.write("🔹 Avoid high wind conditions")
    if duration > estimated_total_time:
        st.write("🔹 Shorten mission duration or split mission")

    st.write("🔹 Maintain balanced speed and altitude")

    # Realistic Battery Drain Graph
    st.subheader("📉 Battery Drain Over Mission Time")

    time = list(range(0, duration + 1))

    # Load impact factor
    load_factor = 1 + (payload * 0.05) + (wind * 0.03) + (altitude / 1000)

    battery_curve = []

    for t in time:
        drain = (battery_used * ((t / max(1, duration)) ** 1.3)) * load_factor
        battery_curve.append(max(0, 100 - drain))

    fig, ax = plt.subplots()
    ax.plot(time, battery_curve, marker="o")
    ax.set_xlabel("Flight Time (minutes)")
    ax.set_ylabel("Battery Remaining (%)")
    ax.set_title("Realistic Drone Battery Drain Curve")
    ax.grid(True)

    st.pyplot(fig)

# after running this file, Type streamlit run app.py to see the dashboard 
