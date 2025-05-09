

# KrishiGyan 🌱  
A Machine Learning-based web application that recommends the best crop type based on environmental conditions like **temperature, soil type, humidity, and rainfall**.

**Video Demonstration** - https://drive.google.com/file/d/1xYn3qONo-VoFihxZu5hUS98ePzLtIsRZ/view?usp=sharing

## 📌 Features  
- **Crop Recommendation**: Predicts the most suitable crop based on environmental factors.  
- **Machine Learning Model**: Utilizes **Random Forest Classifier** for prediction.  
- **User-friendly Web Interface**: Built with **HTML, CSS, and Flask**.  
- **Dynamic Input Handling**: Users can enter values for soil type, temperature, humidity, and rainfall to get real-time recommendations.  

## 🏗️ Project Structure  
```
KrishiGyan
│── static/                 # Static files (CSS, JS)
│── templates/              # HTML templates for frontend
│── models/                 # Contains trained ML models
│── app.py                  # Main Flask application
│── model.py                # Machine Learning model script
│── rice_irrigation_UP.csv   # Dataset used for training
│── irrigation_model.pkl     # Saved trained model
│── README.md               # Project documentation
│── requirements.txt         # Required Python dependencies
```

## ⚙️ Technologies Used  
- **Frontend**: HTML, CSS  
- **Backend**: Flask  
- **Machine Learning**: Scikit-learn (Random Forest Classifier)  
- **Data Processing**: Pandas, NumPy  
- **Model Serialization**: Pickle  

## 🛠️ Installation & Setup  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/KrishiGyan.git
   cd KrishiGyan
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:  
   ```bash
   python app.py
   ```

## 📊 Model Training  
- The **Random Forest Classifier** was trained using a dataset containing soil properties, temperature, humidity, and rainfall.  
- Model is saved as **model.pkl** and is loaded during prediction.  

## 🎯 Future Enhancements  
- Adding **more environmental factors** like pH level, altitude, and soil texture.  
- Improving UI/UX for a better user experience.  
- Deploying the project on **Heroku or AWS** for public access.  

## 🤝 Contributing  
Feel free to contribute! Fork the repository and submit a pull request.  

## 📜 License  
This project is **open-source** and available under the **MIT License**.  

---

Let me know if you want any modifications!
