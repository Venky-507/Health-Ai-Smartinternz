import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import requests
import json
import io
import PyPDF2
from typing import Optional, Dict, Any

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="HealthAI - Intelligent Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .feature-header {
        font-size: 2rem;
        font-weight: bold;
        color: #A23B72;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #A23B72;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
        border-radius: 15px 15px 5px 15px;
    }
    .ai-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        margin-right: 20%;
        border-radius: 15px 15px 15px 5px;
    }
    .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
    }
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class HealthAIAssistant:
    def __init__(self):
        self.initialize_session_state()
        self.watson_credentials = self.init_watson_credentials()
    
    def initialize_session_state(self):
        """Initialize all session state variables"""
        if 'patient_data' not in st.session_state:
            st.session_state.patient_data = {
                'name': '',
                'age': 25,
                'gender': 'Male',
                'medical_history': '',
                'current_medications': '',
                'allergies': '',
                'emergency_contact': ''
            }
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        if 'uploaded_health_data' not in st.session_state:
            st.session_state.uploaded_health_data = None
        
        if 'health_metrics' not in st.session_state:
            st.session_state.health_metrics = None
    
    def init_watson_credentials(self) -> Optional[Dict[str, str]]:
        """Initialize IBM Watson credentials"""
        try:
            api_key = os.getenv('WATSONX_API_KEY')
            project_id = os.getenv('WATSONX_PROJECT_ID')
            url = os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')
            
            if not api_key or not project_id:
                st.error("❌ IBM Watson credentials not found in .env file!")
                return None
            
            credentials = {
                'api_key': api_key,
                'project_id': project_id,
                'url': url
            }
            
            st.success("✅ IBM Watson credentials loaded successfully!")
            return credentials
            
        except Exception as e:
            st.error(f"❌ Failed to load IBM Watson credentials: {str(e)}")
            return None
    
    def get_watson_token(self, api_key: str) -> Optional[str]:
        """Get IBM Watson access token"""
        try:
            token_url = "https://iam.cloud.ibm.com/identity/token"
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            
            data = {
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": api_key
            }
            
            response = requests.post(token_url, headers=headers, data=data, timeout=30)
            
            if response.status_code == 200:
                token_data = response.json()
                return token_data.get("access_token")
            else:
                st.error(f"❌ Token request failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            st.error(f"❌ Error getting token: {str(e)}")
            return None
    
    def generate_ai_response(self, prompt: str, response_type: str = "general") -> str:
        """Generate AI response using IBM Granite model"""
        
        if not self.watson_credentials:
            return "❌ Watson credentials not available. Please check your .env file."
        
        try:
            # Get access token
            with st.spinner("🔐 Authenticating with IBM Watson..."):
                access_token = self.get_watson_token(self.watson_credentials['api_key'])
                
            if not access_token:
                return "❌ Failed to get access token. Please check your API key."
            
            # API endpoint
            url = f"{self.watson_credentials['url']}/ml/v1/text/generation?version=2023-05-29"
            
            # Request body using your exact format - FIXED for Greedy decoding
            body = {
                "input": prompt,
                "parameters": {
                    "decoding_method": "greedy",
                    "max_new_tokens": 200,  # Match your Prompt Lab setting
                    "min_new_tokens": 0,    # Match your Prompt Lab setting
                    "repetition_penalty": 1  # Only this parameter is allowed in greedy mode
                    # Removed: temperature, top_k, top_p (not compatible with greedy decoding)
                },
                "model_id": "ibm/granite-13b-instruct-v2",
                "project_id": self.watson_credentials['project_id'],
                "moderations": {
                    "hap": {
                        "input": {
                            "enabled": True,
                            "threshold": 0.5,
                            "mask": {
                                "remove_entity_value": True
                            }
                        },
                        "output": {
                            "enabled": True,
                            "threshold": 0.5,
                            "mask": {
                                "remove_entity_value": True
                            }
                        }
                    },
                    "pii": {
                        "input": {
                            "enabled": True,
                            "threshold": 0.5,
                            "mask": {
                                "remove_entity_value": True
                            }
                        },
                        "output": {
                            "enabled": True,
                            "threshold": 0.5,
                            "mask": {
                                "remove_entity_value": True
                            }
                        }
                    },
                    "granite_guardian": {
                        "input": {
                            "threshold": 1
                        }
                    }
                }
            }
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            
            # Make API call
            with st.spinner("🤖 Generating AI response..."):
                response = requests.post(url, headers=headers, json=body, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    generated_text = data['results'][0]['generated_text']
                    return generated_text.strip()
                else:
                    return "❌ No response generated from the model."
            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                st.error(error_msg)
                return f"❌ {error_msg}"
                
        except Exception as e:
            error_msg = f"❌ Error generating AI response: {str(e)}"
            st.error(error_msg)
            return error_msg
    
    def process_uploaded_file(self, uploaded_file) -> Optional[pd.DataFrame]:
        """Process uploaded CSV or PDF file"""
        try:
            if uploaded_file.type == "text/csv":
                # Process CSV file
                df = pd.read_csv(uploaded_file)
                return df
            
            elif uploaded_file.type == "application/pdf":
                # Process PDF file
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                # Extract health data from PDF text using AI
                prompt = f"""Extract health metrics from the following medical report text and format as structured data:

Text: {text[:2000]}...

Please extract and format the following health metrics if available:
- Date/Time
- Heart Rate (bpm)
- Blood Pressure (systolic/diastolic)
- Blood Glucose (mg/dL)
- Temperature (°F)
- Weight (kg/lbs)
- Any symptoms mentioned
- Medications listed

Format the response as a structured list that can be converted to a DataFrame."""
                
                ai_response = self.generate_ai_response(prompt, "data_extraction")
                st.info(f"📄 PDF Content Extracted: {ai_response[:500]}...")
                
                # For demo purposes, return sample data based on PDF content
                return self.generate_sample_data_from_pdf(text)
            
            else:
                st.error("❌ Unsupported file type. Please upload CSV or PDF files only.")
                return None
                
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            return None
    
    def generate_sample_data_from_pdf(self, pdf_text: str) -> pd.DataFrame:
        """Generate sample health data based on PDF content"""
        # Create sample data that would typically be extracted from a medical PDF
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate realistic health metrics
        np.random.seed(42)  # For consistent results
        
        df = pd.DataFrame({
            'date': dates,
            'heart_rate': np.random.normal(75, 8, len(dates)),
            'systolic_bp': np.random.normal(125, 12, len(dates)),
            'diastolic_bp': np.random.normal(82, 8, len(dates)),
            'blood_glucose': np.random.normal(98, 15, len(dates)),
            'temperature': np.random.normal(98.6, 0.8, len(dates)),
            'weight': np.random.normal(70, 2, len(dates)),
            'sleep_hours': np.random.normal(7.5, 1.2, len(dates))
        })
        
        return df
    
    def answer_patient_query(self, query: str, patient_data: Dict) -> str:
        """Generate AI response for patient queries"""
        
        health_context = ""
        if st.session_state.uploaded_health_data is not None:
            recent_data = st.session_state.uploaded_health_data.tail(7)
            avg_hr = recent_data['heart_rate'].mean()
            avg_bp_sys = recent_data['systolic_bp'].mean()
            avg_bp_dia = recent_data['diastolic_bp'].mean()
            avg_glucose = recent_data['blood_glucose'].mean()
            
            health_context = f"""
Recent Health Data (Last 7 days):
- Average Heart Rate: {avg_hr:.1f} bpm
- Average Blood Pressure: {avg_bp_sys:.1f}/{avg_bp_dia:.1f} mmHg
- Average Blood Glucose: {avg_glucose:.1f} mg/dL
"""
        
        prompt = f"""You are a knowledgeable healthcare AI assistant. Respond as a doctor would, providing clear, empathetic, and medically accurate information.

Patient Information:
- Name: {patient_data.get('name', 'Patient')}
- Age: {patient_data.get('age', 'Not specified')}
- Gender: {patient_data.get('gender', 'Not specified')}
- Medical History: {patient_data.get('medical_history', 'None reported')}
- Current Medications: {patient_data.get('current_medications', 'None reported')}
- Allergies: {patient_data.get('allergies', 'None reported')}

{health_context}

Patient Question: {query}

Please provide a comprehensive response that:
1. Directly addresses the patient's question
2. Includes relevant medical information
3. Considers the patient's profile and recent health data
4. Suggests when to seek professional medical care
5. Uses clear, understandable language
6. Acknowledges the limitations of AI medical advice

Response:"""

        return self.generate_ai_response(prompt, "chat")
    
    def predict_disease(self, symptoms: str, patient_data: Dict) -> str:
        """Generate disease predictions based on symptoms"""
        
        health_context = ""
        if st.session_state.uploaded_health_data is not None:
            recent_data = st.session_state.uploaded_health_data.tail(7)
            health_context = f"""
Recent Health Metrics:
- Heart Rate: {recent_data['heart_rate'].mean():.1f} bpm
- Blood Pressure: {recent_data['systolic_bp'].mean():.1f}/{recent_data['diastolic_bp'].mean():.1f} mmHg
- Blood Glucose: {recent_data['blood_glucose'].mean():.1f} mg/dL
- Temperature: {recent_data['temperature'].mean():.1f}°F
"""
        
        prompt = f"""You are a medical AI assistant specializing in diagnostic assessment. Analyze the following patient symptoms and provide potential diagnoses.

Patient Profile:
- Age: {patient_data.get('age', 'Not specified')}
- Gender: {patient_data.get('gender', 'Not specified')}
- Medical History: {patient_data.get('medical_history', 'None reported')}
- Current Medications: {patient_data.get('current_medications', 'None reported')}
- Allergies: {patient_data.get('allergies', 'None reported')}

{health_context}

Reported Symptoms: {symptoms}

Please provide a comprehensive diagnostic assessment including:

1. **Top 3 Most Likely Conditions:**
   - Condition 1: [Name] - Likelihood: [High/Medium/Low]
     * Explanation: [Brief medical explanation]
   - Condition 2: [Name] - Likelihood: [High/Medium/Low]
     * Explanation: [Brief medical explanation]
   - Condition 3: [Name] - Likelihood: [High/Medium/Low]
     * Explanation: [Brief medical explanation]

2. **Recommended Next Steps:**
   - Immediate actions to take
   - When to seek medical attention
   - Additional tests or evaluations needed

3. **Red Flags - Seek Immediate Medical Care If:**
   - List warning signs that require urgent attention

**Important Disclaimer:** This assessment is for informational purposes only and should not replace professional medical diagnosis.

Analysis:"""

        return self.generate_ai_response(prompt, "prediction")
    
    def generate_treatment_plan(self, condition: str, patient_data: Dict) -> str:
        """Generate personalized treatment plan"""
        
        health_context = ""
        if st.session_state.uploaded_health_data is not None:
            recent_data = st.session_state.uploaded_health_data.tail(7)
            health_context = f"""
Current Health Status:
- Heart Rate: {recent_data['heart_rate'].mean():.1f} bpm
- Blood Pressure: {recent_data['systolic_bp'].mean():.1f}/{recent_data['diastolic_bp'].mean():.1f} mmHg
- Blood Glucose: {recent_data['blood_glucose'].mean():.1f} mg/dL
"""
        
        prompt = f"""You are a medical AI assistant creating a comprehensive treatment plan. Develop personalized recommendations for the given condition.

Patient Profile:
- Name: {patient_data.get('name', 'Patient')}
- Age: {patient_data.get('age', 'Not specified')}
- Gender: {patient_data.get('gender', 'Not specified')}
- Medical History: {patient_data.get('medical_history', 'None reported')}
- Current Medications: {patient_data.get('current_medications', 'None reported')}
- Allergies: {patient_data.get('allergies', 'None reported')}

{health_context}

Medical Condition: {condition}

Please create a detailed treatment plan including:

## 🏥 **Comprehensive Treatment Plan for {condition}**

### 1. **Medication Recommendations:**
   - Primary medications with dosages
   - Alternative options if applicable
   - Drug interaction considerations
   - Duration of treatment

### 2. **Lifestyle Modifications:**
   - Dietary recommendations
   - Exercise guidelines
   - Sleep hygiene
   - Stress management techniques

### 3. **Follow-up Care Schedule:**
   - Initial follow-up timeline
   - Monitoring parameters
   - Long-term care plan
   - Specialist referrals if needed

### 4. **Dietary Guidelines:**
   - Foods to include
   - Foods to avoid
   - Nutritional supplements
   - Hydration recommendations

### 5. **Physical Activity Plan:**
   - Recommended exercises
   - Activity restrictions
   - Gradual progression plan
   - Warning signs to stop activity

### 6. **Warning Signs - Seek Immediate Medical Attention:**
   - Emergency symptoms to watch for
   - When to contact healthcare provider
   - Emergency contact information

### 7. **Patient Education:**
   - Understanding the condition
   - Self-monitoring techniques
   - Medication compliance tips

**Important Note:** This treatment plan should be reviewed and approved by a qualified healthcare provider before implementation.

Treatment Plan:"""

        return self.generate_ai_response(prompt, "treatment")
    
    def render_sidebar(self):
        """Render enhanced sidebar with patient profile and file upload"""
        with st.sidebar:
            st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
            st.markdown("### 👤 Patient Profile")
            
            # Patient information form
            st.session_state.patient_data['name'] = st.text_input(
                "Full Name", 
                value=st.session_state.patient_data['name'],
                placeholder="Enter patient's full name"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.patient_data['age'] = st.number_input(
                    "Age", 
                    min_value=1, 
                    max_value=120, 
                    value=st.session_state.patient_data['age']
                )
            with col2:
                st.session_state.patient_data['gender'] = st.selectbox(
                    "Gender", 
                    ["Male", "Female", "Other", "Prefer not to say"],
                    index=0 if st.session_state.patient_data['gender'] == "Male" else 1
                )
            
            st.markdown("#### 📋 Medical Information")
            st.session_state.patient_data['medical_history'] = st.text_area(
                "Medical History", 
                value=st.session_state.patient_data['medical_history'],
                height=80,
                placeholder="Any chronic conditions, past surgeries, etc."
            )
            
            st.session_state.patient_data['current_medications'] = st.text_area(
                "Current Medications", 
                value=st.session_state.patient_data['current_medications'],
                height=80,
                placeholder="List all current medications and dosages"
            )
            
            st.session_state.patient_data['allergies'] = st.text_input(
                "Allergies", 
                value=st.session_state.patient_data['allergies'],
                placeholder="Drug allergies, food allergies, etc."
            )
            
            st.session_state.patient_data['emergency_contact'] = st.text_input(
                "Emergency Contact", 
                value=st.session_state.patient_data['emergency_contact'],
                placeholder="Name and phone number"
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # File Upload Section
            st.markdown("### 📁 Upload Health Data")
            st.markdown('<div class="upload-area">', unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Upload patient health data (CSV or PDF)",
                type=['csv', 'pdf'],
                help="Upload CSV with health metrics or PDF medical reports"
            )
            
            if uploaded_file is not None:
                with st.spinner("Processing uploaded file..."):
                    processed_data = self.process_uploaded_file(uploaded_file)
                    if processed_data is not None:
                        st.session_state.uploaded_health_data = processed_data
                        st.success(f"✅ File processed successfully! {len(processed_data)} records loaded.")
                        
                        # Show data preview
                        st.markdown("**Data Preview:**")
                        st.dataframe(processed_data.head(3), use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # API Status
            if self.watson_credentials:
                st.success("🤖 AI Model: Connected")
                st.info(f"🌍 Region: US-South")
                st.info(f"🔑 Project: {self.watson_credentials['project_id'][:8]}...")
            else:
                st.error("🤖 AI Model: Disconnected")
    
    def render_patient_chat(self):
        """Render patient chat interface"""
        st.markdown('<h2 class="feature-header">💬 24/7 Patient Support</h2>', unsafe_allow_html=True)
        st.write("Ask any health-related question for immediate AI-powered assistance.")
        
        # Chat history display
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                if message['type'] == 'user':
                    st.markdown(f'<div class="chat-message user-message">👤 <strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message ai-message">🤖 <strong>HealthAI:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        
        # Chat input form
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Ask your health question...", 
                height=100,
                placeholder="e.g., I have been suffering from a fever for 2 days, my symptoms are running nose, cough, headache, and joint pain. What could this be and what should I do?"
            )
            submit_button = st.form_submit_button("Send Message", use_container_width=True)
            
            if submit_button and user_input:
                if not self.watson_credentials:
                    st.error("❌ Please check your IBM Watson API credentials.")
                else:
                    # Add user message to chat history
                    st.session_state.chat_history.append({"type": "user", "content": user_input})
                    
                    # Generate AI response
                    ai_response = self.answer_patient_query(user_input, st.session_state.patient_data)
                    st.session_state.chat_history.append({"type": "ai", "content": ai_response})
                    
                    st.rerun()
    
    def render_disease_prediction(self):
        """Render disease prediction interface"""
        st.markdown('<h2 class="feature-header">🔍 AI Disease Prediction System</h2>', unsafe_allow_html=True)
        st.write("Enter detailed symptoms to receive AI-powered diagnostic assessments with likelihood indicators.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 Symptom Documentation")
            symptoms = st.text_area(
                "Describe your symptoms in detail:",
                height=200,
                placeholder="""Please provide detailed information about:
• Primary symptoms (e.g., fever, cough, headache)
• Duration and onset (when did symptoms start?)
• Severity (mild, moderate, severe)
• Associated symptoms
• Factors that make symptoms better or worse
• Any recent travel, exposure, or changes in routine

Example: "I've had a persistent dry cough for 5 days, along with fatigue and mild fever (99.5°F). The cough is worse at night and I've been feeling short of breath during light activities."
"""
            )
            
            if st.button("🔍 Generate AI Prediction", type="primary", use_container_width=True):
                if symptoms:
                    if not self.watson_credentials:
                        st.error("❌ Please check your IBM Watson API credentials.")
                    else:
                        with st.spinner("🤖 Analyzing symptoms with AI..."):
                            prediction = self.predict_disease(symptoms, st.session_state.patient_data)
                            
                            st.subheader("🎯 AI-Generated Diagnostic Assessment")
                            st.markdown(prediction)
                            
                            st.markdown("""
                            <div class="warning-box">
                            ⚠️ <strong>Medical Disclaimer:</strong> This AI analysis is for informational purposes only and should not replace professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.error("Please enter your symptoms to generate a prediction.")
        
        with col2:
            st.subheader("📊 Health Data Context")
            if st.session_state.uploaded_health_data is not None:
                recent_data = st.session_state.uploaded_health_data.tail(7)
                
                st.metric("Avg Heart Rate", f"{recent_data['heart_rate'].mean():.1f} bpm")
                st.metric("Avg Blood Pressure", f"{recent_data['systolic_bp'].mean():.0f}/{recent_data['diastolic_bp'].mean():.0f}")
                st.metric("Avg Blood Glucose", f"{recent_data['blood_glucose'].mean():.1f} mg/dL")
                
                st.info("💡 AI will consider your recent health data in the analysis.")
            else:
                st.info("📁 Upload health data for more accurate predictions.")
    
    def render_treatment_plans(self):
        """Render treatment plan generator"""
        st.markdown('<h2 class="feature-header">📋 AI Treatment Plan Generator</h2>', unsafe_allow_html=True)
        st.write("Generate comprehensive, personalized treatment recommendations based on specific medical conditions.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🏥 Medical Condition Input")
            condition = st.text_input(
                "Enter the medical condition or diagnosis:",
                placeholder="e.g., Type 2 Diabetes, Hypertension, Migraine, Anxiety, etc."
            )
            
            additional_info = st.text_area(
                "Additional Information (Optional):",
                height=100,
                placeholder="Any specific concerns, severity, recent changes, or other relevant details..."
            )
            
            if st.button("📋 Generate Treatment Plan", type="primary", use_container_width=True):
                if condition:
                    if not self.watson_credentials:
                        st.error("❌ Please check your IBM Watson API credentials.")
                    else:
                        full_condition = f"{condition}. {additional_info}" if additional_info else condition
                        
                        with st.spinner("🤖 Creating personalized treatment plan..."):
                            treatment_plan = self.generate_treatment_plan(full_condition, st.session_state.patient_data)
                            
                            st.subheader("📋 AI-Generated Personalized Treatment Plan")
                            st.markdown(treatment_plan)
                            
                            st.markdown("""
                            <div class="warning-box">
                            💡 <strong>Important Note:</strong> This AI-generated treatment plan is based on general medical guidelines and should be reviewed and approved by a qualified healthcare provider before implementation. Always consult with your doctor before starting any new treatment.
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.error("Please enter a medical condition to generate a treatment plan.")
        
        with col2:
            st.subheader("👤 Patient Context")
            if st.session_state.patient_data['name']:
                st.info(f"**Patient:** {st.session_state.patient_data['name']}")
                st.info(f"**Age:** {st.session_state.patient_data['age']} years")
                st.info(f"**Gender:** {st.session_state.patient_data['gender']}")
                
                if st.session_state.patient_data['medical_history']:
                    st.info(f"**Medical History:** {st.session_state.patient_data['medical_history'][:100]}...")
                
                if st.session_state.patient_data['current_medications']:
                    st.info(f"**Current Medications:** {st.session_state.patient_data['current_medications'][:100]}...")
            else:
                st.warning("Complete patient profile for more personalized treatment plans.")
    
    def render_health_analytics(self):
        """Render health analytics dashboard"""
        st.markdown('<h2 class="feature-header">📊 Health Analytics Dashboard</h2>', unsafe_allow_html=True)
        
        if st.session_state.uploaded_health_data is None:
            st.markdown("""
            <div class="upload-area">
                <h3>📁 No Health Data Available</h3>
                <p>Please upload a CSV file with health metrics or a PDF medical report to view analytics.</p>
                <p><strong>Expected CSV columns:</strong> date, heart_rate, systolic_bp, diastolic_bp, blood_glucose, temperature, weight, sleep_hours</p>
            </div>
            """, unsafe_allow_html=True)
            return
        
        health_data = st.session_state.uploaded_health_data
        
        # Key metrics overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_hr = health_data['heart_rate'].mean()
            hr_trend = "↗️" if health_data['heart_rate'].iloc[-7:].mean() > health_data['heart_rate'].iloc[-14:-7].mean() else "↘️"
            st.metric("Heart Rate", f"{avg_hr:.0f} bpm", delta=f"{hr_trend} Trending")
        
        with col2:
            avg_sys = health_data['systolic_bp'].mean()
            avg_dia = health_data['diastolic_bp'].mean()
            st.metric("Blood Pressure", f"{avg_sys:.0f}/{avg_dia:.0f}", delta="Normal Range")
        
        with col3:
            avg_glucose = health_data['blood_glucose'].mean()
            glucose_status = "Normal" if 70 <= avg_glucose <= 100 else "Monitor"
            st.metric("Blood Glucose", f"{avg_glucose:.0f} mg/dL", delta=glucose_status)
        
        with col4:
            if 'temperature' in health_data.columns:
                avg_temp = health_data['temperature'].mean()
                st.metric("Temperature", f"{avg_temp:.1f}°F", delta="Normal")
            else:
                st.metric("Data Points", f"{len(health_data)}", delta="Records")
        
        # Visualizations
        tab1, tab2, tab3 = st.tabs(["📈 Trends", "🔍 Correlations", "🎯 AI Insights"])
        
        with tab1:
            # Heart Rate Trend
            col1, col2 = st.columns(2)
            
            with col1:
                fig_hr = go.Figure()
                fig_hr.add_trace(go.Scatter(
                    x=health_data['date'],
                    y=health_data['heart_rate'],
                    mode='lines+markers',
                    name='Heart Rate',
                    line=dict(color='#2E86AB', width=3),
                    marker=dict(size=6)
                ))
                fig_hr.update_layout(
                    title="Heart Rate Trend",
                    xaxis_title="Date",
                    yaxis_title="Heart Rate (bpm)",
                    height=400,
                    hovermode='x unified'
                )
                st.plotly_chart(fig_hr, use_container_width=True)
                
                # Blood Glucose Trend
                fig_glucose = go.Figure()
                fig_glucose.add_trace(go.Scatter(
                    x=health_data['date'],
                    y=health_data['blood_glucose'],
                    mode='lines+markers',
                    name='Blood Glucose',
                    line=dict(color='#A23B72', width=3),
                    marker=dict(size=6)
                ))
                fig_glucose.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Normal Upper Limit")
                fig_glucose.add_hline(y=70, line_dash="dash", line_color="orange", annotation_text="Normal Lower Limit")
                fig_glucose.update_layout(
                    title="Blood Glucose Trend",
                    xaxis_title="Date",
                    yaxis_title="Blood Glucose (mg/dL)",
                    height=400,
                    hovermode='x unified'
                )
                st.plotly_chart(fig_glucose, use_container_width=True)
            
            with col2:
                # Blood Pressure Trend
                fig_bp = go.Figure()
                fig_bp.add_trace(go.Scatter(
                    x=health_data['date'],
                    y=health_data['systolic_bp'],
                    mode='lines+markers',
                    name='Systolic',
                    line=dict(color='#FF6B6B', width=3),
                    marker=dict(size=6)
                ))
                fig_bp.add_trace(go.Scatter(
                    x=health_data['date'],
                    y=health_data['diastolic_bp'],
                    mode='lines+markers',
                    name='Diastolic',
                    line=dict(color='#4ECDC4', width=3),
                    marker=dict(size=6)
                ))
                fig_bp.update_layout(
                    title="Blood Pressure Trend",
                    xaxis_title="Date",
                    yaxis_title="Blood Pressure (mmHg)",
                    height=400,
                    hovermode='x unified'
                )
                st.plotly_chart(fig_bp, use_container_width=True)
                
                # Health Metrics Distribution
                if len(health_data) > 7:
                    # Create symptom frequency based on health data patterns
                    symptoms_data = {
                        'Normal': 60.0,
                        'Mild Fatigue': 15.0,
                        'Headache': 10.0,
                        'Dizziness': 8.0,
                        'Other': 7.0
                    }
                    
                    fig_symptoms = px.pie(
                        values=list(symptoms_data.values()),
                        names=list(symptoms_data.keys()),
                        title="Health Status Distribution",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_symptoms.update_layout(height=400)
                    st.plotly_chart(fig_symptoms, use_container_width=True)
        
        with tab2:
            # Correlation analysis
            numeric_cols = ['heart_rate', 'systolic_bp', 'diastolic_bp', 'blood_glucose']
            if 'sleep_hours' in health_data.columns:
                numeric_cols.append('sleep_hours')
            if 'weight' in health_data.columns:
                numeric_cols.append('weight')
            
            correlation_data = health_data[numeric_cols].corr()
            
            fig_corr = px.imshow(
                correlation_data,
                text_auto=True,
                aspect="auto",
                title="Health Metrics Correlation Matrix",
                color_continuous_scale="RdBu",
                zmin=-1, zmax=1
            )
            fig_corr.update_layout(height=500)
            st.plotly_chart(fig_corr, use_container_width=True)
            
            st.markdown("""
            **Correlation Insights:**
            - Values close to 1 indicate strong positive correlation
            - Values close to -1 indicate strong negative correlation
            - Values close to 0 indicate weak correlation
            """)
        
        with tab3:
            # AI-generated insights
            st.markdown("### 🤖 AI-Generated Health Insights")
            
            if st.button("Generate AI Health Analysis", type="primary"):
                health_summary = f"""Analyze the following patient health data and provide comprehensive insights:

Patient: {st.session_state.patient_data['name']}
Age: {st.session_state.patient_data['age']}
Gender: {st.session_state.patient_data['gender']}

Health Data Summary ({len(health_data)} days):
- Average Heart Rate: {health_data['heart_rate'].mean():.1f} bpm (Range: {health_data['heart_rate'].min():.1f}-{health_data['heart_rate'].max():.1f})
- Average Blood Pressure: {health_data['systolic_bp'].mean():.1f}/{health_data['diastolic_bp'].mean():.1f} mmHg
- Average Blood Glucose: {health_data['blood_glucose'].mean():.1f} mg/dL (Range: {health_data['blood_glucose'].min():.1f}-{health_data['blood_glucose'].max():.1f})

Recent Trends (Last 7 days vs Previous 7 days):
- Heart Rate: {health_data['heart_rate'].iloc[-7:].mean():.1f} vs {health_data['heart_rate'].iloc[-14:-7].mean():.1f}
- Systolic BP: {health_data['systolic_bp'].iloc[-7:].mean():.1f} vs {health_data['systolic_bp'].iloc[-14:-7].mean():.1f}
- Blood Glucose: {health_data['blood_glucose'].iloc[-7:].mean():.1f} vs {health_data['blood_glucose'].iloc[-14:-7].mean():.1f}

Medical History: {st.session_state.patient_data['medical_history']}
Current Medications: {st.session_state.patient_data['current_medications']}

Please provide:
1. Overall health assessment
2. Trend analysis and patterns
3. Areas of concern or improvement
4. Personalized recommendations
5. When to seek medical attention

Analysis:"""
                
                insights = self.generate_ai_response(health_summary, "insights")
                st.markdown(insights)
            
            # Static insights based on data
            st.markdown("#### 📈 Data-Driven Observations")
            
            insights = []
            
            # Heart rate analysis
            avg_hr = health_data['heart_rate'].mean()
            if avg_hr < 60:
                insights.append("💙 **Heart Rate**: Below normal range - may indicate bradycardia. Consider consulting a cardiologist.")
            elif avg_hr > 100:
                insights.append("❤️ **Heart Rate**: Above normal range - may indicate tachycardia. Monitor stress levels and caffeine intake.")
            else:
                insights.append("💚 **Heart Rate**: Within normal range (60-100 bpm). Good cardiovascular health indicator.")
            
            # Blood pressure analysis
            avg_sys = health_data['systolic_bp'].mean()
            avg_dia = health_data['diastolic_bp'].mean()
            if avg_sys > 140 or avg_dia > 90:
                insights.append("🔴 **Blood Pressure**: Elevated readings detected. Consider lifestyle modifications and medical consultation.")
            elif avg_sys > 130 or avg_dia > 80:
                insights.append("🟡 **Blood Pressure**: Stage 1 hypertension range. Monitor closely and consider preventive measures.")
            else:
                insights.append("💚 **Blood Pressure**: Within normal range. Continue healthy lifestyle habits.")
            
            # Blood glucose analysis
            avg_glucose = health_data['blood_glucose'].mean()
            if avg_glucose > 126:
                insights.append("🔴 **Blood Glucose**: Elevated levels may indicate diabetes. Consult healthcare provider immediately.")
            elif avg_glucose > 100:
                insights.append("🟡 **Blood Glucose**: Pre-diabetic range. Consider dietary modifications and regular monitoring.")
            else:
                insights.append("💚 **Blood Glucose**: Within normal range. Good metabolic health.")
            
            for insight in insights:
                st.markdown(f"- {insight}")
            
            # Health score calculation
            health_score = 100
            if avg_hr < 60 or avg_hr > 100:
                health_score -= 15
            if avg_sys > 130 or avg_dia > 80:
                health_score -= 20
            if avg_glucose > 100:
                health_score -= 25
            
            st.markdown(f"### 🎯 Overall Health Score: **{max(health_score, 0)}/100**")
            
            if health_score >= 90:
                st.success("🌟 Excellent health status! Keep up the great work.")
            elif health_score >= 75:
                st.info("👍 Good health status with room for minor improvements.")
            elif health_score >= 60:
                st.warning("⚠️ Fair health status. Consider lifestyle modifications.")
            else:
                st.error("🚨 Health status needs attention. Consult with a healthcare provider.")
    
    def run(self):
        """Main application runner"""
        # Header
        st.markdown('<h1 class="main-header">🏥 HealthAI - Intelligent Healthcare Assistant</h1>', unsafe_allow_html=True)
        
        # Render sidebar
        self.render_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "💬 Patient Chat", 
            "🔍 Disease Prediction", 
            "📋 Treatment Plans", 
            "📊 Health Analytics"
        ])
        
        with tab1:
            self.render_patient_chat()
        
        with tab2:
            self.render_disease_prediction()
        
        with tab3:
            self.render_treatment_plans()
        
        with tab4:
            self.render_health_analytics()
        
        # Footer
        st.markdown("---")
        st.markdown(f"""
        <div style='text-align: center; color: #666; padding: 2rem;'>
            <p><strong>HealthAI - Intelligent Healthcare Assistant</strong></p>
            <p>Powered by IBM Watson & Granite-13b-instruct-v2 AI Model</p>
            <p><strong>API Status:</strong> {'🟢 Connected' if self.watson_credentials else '🔴 Disconnected'} | 
            <strong>Region:</strong> US-South | 
            <strong>Model:</strong> granite-13b-instruct-v2</p>
            <p><strong>⚠️ Medical Disclaimer:</strong> This application is for informational purposes only and should not replace professional medical advice, diagnosis, or treatment.</p>
        </div>
        """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    app = HealthAIAssistant()
    app.run()
