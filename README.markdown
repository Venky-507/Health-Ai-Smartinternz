# 🏥 HealthAI - Intelligent Healthcare Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![IBM Watson](https://img.shields.io/badge/IBM%20Watson-AI%20Powered-blue.svg)](https://www.ibm.com/watson)

HealthAI is an AI-powered healthcare assistant built with Streamlit and IBM Watson's Granite model, providing intelligent medical consultations, disease predictions, personalized treatment plans, and comprehensive health analytics.

## 🎥 Demo Video

**[▶️ Watch Demo Video: LOW HEALTH.mp4](LOW%20HEALTH.mp4)**

## ✨ Features

### 🤖 AI-Powered Medical Consultation
- 24/7 intelligent health support using IBM Watson Granite model
- Natural language processing for symptom analysis
- Personalized medical advice based on patient profile
- Real-time chat interface with medical context awareness

### 🔍 Disease Prediction System
- Advanced symptom analysis with likelihood indicators
- Differential diagnosis with multiple condition assessment
- Integration with patient health data for accurate predictions
- Evidence-based medical recommendations

### 📋 Treatment Plan Generator
- Comprehensive, personalized treatment protocols
- Medication recommendations with dosage guidelines
- Lifestyle modification suggestions
- Follow-up care scheduling and monitoring parameters

### 📊 Health Analytics Dashboard
- Interactive health metrics visualization
- Trend analysis and correlation insights
- AI-generated health assessments
- Real-time health score calculation
- Support for CSV and PDF medical report uploads

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- IBM Watson Machine Learning account
- Streamlit

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/healthai-assistant.git
   cd healthai-assistant
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   Create a `.env` file in the root directory with the following content:
   ```env
   WATSONX_API_KEY=your_watson_api_key_here
   WATSONX_PROJECT_ID=your_project_id_here
   WATSONX_URL=https://us-south.ml.cloud.ibm.com
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Access the Application**
   Open your browser and navigate to `http://localhost:8501`.

## 🔧 Configuration

### IBM Watson Setup

1. **Create IBM Cloud Account**
   - Sign up at [IBM Cloud](https://cloud.ibm.com).
   - Create a Watson Machine Learning service instance.

2. **Get API Credentials**
   - Navigate to your Watson ML service.
   - Go to Service Credentials → New Credential.
   - Copy the API key.

3. **Create Watson Studio Project**
   - Go to Watson Studio.
   - Create a new project.
   - Copy the project ID from the project settings.

4. **Update Environment Variables**
   - Add your credentials to the `.env` file.
   - Ensure the project ID and API key are correct.

## 📁 Project Structure

```
healthai-assistant/
├── app.py                 # Main Streamlit application
├── app1.py                # Alternative enhanced version
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── README.md              # Project documentation
├── DOCUMENTATION.md       # Detailed technical documentation
└── assets/                # Project assets (screenshots, etc.)
```

## 🔒 Security & Privacy

- **Data Protection**: All patient data is processed locally and not stored permanently.
- **API Security**: IBM Watson API calls use secure authentication tokens.
- **Privacy Compliance**: No personal health information is logged or transmitted to third parties.
- **Encryption**: All API communications use HTTPS encryption.

## 📖 Usage Guide

### 1. Patient Profile Setup
- Complete the patient profile in the sidebar.
- Add medical history, current medications, and allergies.
- Upload health data files (CSV or PDF) for enhanced analysis.

### 2. Medical Consultation
- Use the chat interface to ask health-related questions.
- Provide detailed symptom descriptions for better analysis.
- Review AI-generated medical advice and recommendations.

### 3. Disease Prediction
- Enter comprehensive symptom information.
- Review differential diagnosis with likelihood indicators.
- Follow recommended next steps and warning signs.

### 4. Treatment Planning
- Input specific medical conditions or diagnoses.
- Generate personalized treatment protocols.
- Review medication recommendations and lifestyle modifications.

### 5. Health Analytics
- Upload health data files for trend analysis.
- Monitor key health metrics over time.
- Review AI-generated health insights and recommendations.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.


## ⚠️ Medical Disclaimer

**IMPORTANT**: This application is for informational and educational purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read in this application.

## 📑 Documentation 

- **Documentation**: [Full Documentation](DOCUMENTATION.md)

## 🏆 Acknowledgments

- **IBM Watson** for providing the AI foundation models.
- **Streamlit** for the excellent web framework.
- **Plotly** for interactive data visualizations.
- **Open Source Community** for various libraries and tools.

## 📊 Project Stats

- **Language**: Python
- **Framework**: Streamlit
- **AI Model**: IBM Watson Granite-13b-instruct-v2
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy

---

<div align="center">
  <p><strong>Built with ❤️ for better healthcare accessibility</strong></p>
  <p>⭐ Star this repository if you found it helpful!</p>
</div>
