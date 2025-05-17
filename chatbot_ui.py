import streamlit as st
import requests

def display_results(data):
    """Display crop prediction results."""
    st.markdown("<h3 style='color: limegreen;'>🌾 Recommended Crops:</h3>", unsafe_allow_html=True)
    if data.get("prediction"):
        prediction = data['prediction'].capitalize()
        st.markdown(f"""
            <div class="recommended-box">
                <h4>Crop Recommendation:</h4>
                <p>{prediction}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: red; font-weight: bold;'>🚫 No recommendations found.</p>", unsafe_allow_html=True)


# UI Setup
st.set_page_config(page_title="KrishiGyan--Smart Crop Advisor", layout="centered")
st.markdown("""
    <style>
        /* Global background and font */
        body {
            background-color: #000;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Input styling */
        .stTextInput>div>div>input,
        .stSelectbox>div>div>div>div {
            background-color: #222;
            color: white;
            border-radius: 8px;
        }

        /* Button styling */
        .stButton>button {
            background-color: limegreen;
            color: black;
            font-weight: bold;
            border-radius: 10px;
            padding: 8px 16px;
            transition: background-color 0.3s, color 0.3s;
        }

        /* Hover effect: use white instead of red */
        .stButton>button:hover {
            background-color: white !important;
            color: black !important;
            font-weight: bold;
        }

        /* Chat bubbles */
        .message {
            background-color: #111;
            padding: 12px 16px;
            border-radius: 10px;
            margin-bottom: 8px;
            line-height: 1.6;
        }

        .message strong {
            color: limegreen;
        }

        /* Crop box */
        .recommended-box {
            background-color: #2c2f36;
            padding: 20px;
            border-radius: 12px;
            margin-top: 15px;
        }

        .recommended-box h4 {
            color: white;
            margin-bottom: 10px;
        }

        .recommended-box p {
            color: lightgreen;
            font-size: 20px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)


st.title("KrishiGyan")

# Session state setup
if "started" not in st.session_state:
    st.session_state.started = False
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# Reset button
if st.session_state.started:
    if st.button("🔄 Start Over"):
        st.session_state.started = False
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()

# Intro screen
# Intro screen
if not st.session_state.started:
    st.subheader("👋 Welcome to KrishiGyan!")
    st.markdown("""
   🤖 **Welcome to KrishiGyan – Your Smart Crop Advisor!**

Are you a farmer wondering which crop to grow this season?  
This intelligent assistant is here to **recommend the most suitable crops** based on your **local farming conditions**.

### 🧠 How it works:
KrishiGyan uses a smart algorithm that considers:
- 🌍 **Your Location (City)**  
- 🌱 **Type of Soil in your area**  
- 🌧️ **Average Rainfall**  
- ☀️ **Live Weather Data** (Temperature & Humidity)

With this information, it predicts the **best crop** to grow in your region to **maximize your yield and profit**.

✅ It's fast, easy, and tailored just for you.  
Ready to discover the best crop for your farm? 😊

    """)

    if st.button("🚀 Start"):
        st.session_state.started = True
        st.rerun()
else:
    questions = [
        ("name", "👋 Hi there! What's your name?"),
        ("city", "🏙️ Which city are you from?"),
        ("soil", "🌍 What type of soil is common there?"),
        ("rainfall", "🌧️ What's the average rainfall there (in mm)?")
    ]

    for i in range(st.session_state.step):
        key, question = questions[i]
        answer = st.session_state.answers.get(key, "")
        st.markdown(f"""
            <div class="message"><strong>🤖 Bot:</strong> {question}</div>
            <div class="message" style="background-color:#222"><strong>🧑 You:</strong> {answer}</div>
        """, unsafe_allow_html=True)

    if st.session_state.step < len(questions):
        key, question = questions[st.session_state.step]

        if key == "soil":
            soil_options = ["-- Select --", "Clay", "Sandy", "Loamy", "Peaty", "Saline", "Chalky"]
            selected_soil = st.selectbox(question, options=soil_options, index=0, key="soil_select")

            if selected_soil != "-- Select --":
                st.session_state.answers[key] = selected_soil
                st.session_state.step += 1
                st.rerun()
        else:
            response = st.text_input(question, key=key)
            if response:
                st.session_state.answers[key] = response
                st.session_state.step += 1
                st.rerun()

    else:
        # All questions answered, fetch weather and recommendation
        city = st.session_state.answers["city"]
        soil_type = st.session_state.answers["soil"]
        rainfall = st.session_state.answers["rainfall"]

        try:
            weather_resp = requests.get(f"http://127.0.0.1:5000/weather?city={city}")
            weather_data = weather_resp.json()
            weather = weather_data.get("temp_c", "Unknown")
            humidity = weather_data.get("humidity", "Unknown")
        except Exception as e:
            st.error(f"❌ Could not fetch weather info: {e}")
            weather = humidity = "Unknown"

        request_data = {
            "soil_type": soil_type,
            "weather": weather,
            "humidity": humidity,
            "rainfall": rainfall
        }

        try:
            rec_resp = requests.post("http://127.0.0.1:5000/predict", json=request_data)
            rec_data = rec_resp.json()
            display_results(rec_data)
        except Exception as e:
            st.error(f"❌ Failed to get recommendation: {e}")
