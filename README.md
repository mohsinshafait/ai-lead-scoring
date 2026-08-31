# 🎯 AI Lead Scoring & Conversion Prediction System
An end-to-end Machine Learning application that predicts the probability of a lead converting into a customer and automatically assigns a business priority level.

The project demonstrates how a trained Machine Learning model can be integrated into a real-world application using **FastAPI** and **Streamlit**.
## 🚀 Project Overview

Businesses receive many leads every day, but not all leads have the same probability of conversion.

This system helps prioritize leads by:
- Predicting whether a lead is likely to convert
- Calculating the lead's conversion probability
- Categorizing leads as High, Medium, or Low priority
- Providing a recommended business action based on lead priority
## 🧠 Machine Learning Workflow
```text
Raw Lead Data
      ↓
Feature Engineering
      ↓
Data Preprocessing
      ↓
Machine Learning Model
      ↓
Conversion Probability
      ↓
Lead Priority
      ↓
Business Action
```
## 📊 Lead Priority Strategy

| Conversion Probability | Priority | Recommended Action |
| --- | --- | --- |
| ≥ 70% | 🔥 High | Contact immediately |
| 40% – 69% | ⚡ Medium | Targeted follow-up |
| < 40% | 📌 Low | Automated or lower-cost follow-up |

### 🏗️ Project Architecture
```text
User
  ↓
Streamlit Frontend
  ↓
FastAPI Backend
  ↓
Trained ML Pipeline
  ↓
Prediction & Lead Priority
```
## 🛠️ Technologies Used
- Python
- Pandas
- NumPy
- Scikit-learn
- FastAPI
- Uvicorn
- Streamlit
- Requests
- Joblib
## 📁 Project Structure
```text
ai-lead-scoring/
│
├── app/
│   └── main.py
│
├── data/
│   └── raw/
│       └── Lead Scoring.csv
│
├── models/
│   └── lead_scoring_model.pkl
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_model_export.ipynb
│
├── src/
│   ├── __init__.py
│   └── feature_engineering.py
│
├── streamlit_app.py
├── requirements.txt
└── README.md
```
## ⚙️ Installation
### 1. Clone the repository
```bash 
git clone https://github.com/mohsinshafait/ai-lead-scoring
```
### 2. Navigate to the project directory
```bash
cd ai-lead-scoring
```
### 3. Create a Conda environment
```bash
conda create -n lead_scoring python=3.12
```
### 4. Activate the environment
```bash
conda activate lead_scoring
```
### 5. Install the required dependencies
```bash
pip install -r requirements.txt
```
---
## ▶️ Running the Application

This project has two components that need to run simultaneously:

1. FastAPI Backend
2. Streamlit Frontend 

### Start the FastAPI Backend

Open a terminal in the project folder and run:
```bash
python -m uvicorn app.main:app --reload
```

The backend API will run at:
```text
http://127.0.0.1:8000
```
You can access the interactive API documentation at:
```text
http://127.0.0.1:8000/docs
```
### Start the Streamlit Frontend

Open a second terminal in the project folder and run:
python -m streamlit run streamlit_app.py

The Streamlit application will run at:
```text
http://localhost:8501
```

## 📡 API Example
Sample Request

The ```/predict``` endpoint accepts lead information such as:
```JSON
{
  "lead_origin": "Landing Page Submission",
  "lead_source": "Google",
  "country": "India",
  "specialization": "Business Administration",
  "heard_about_x_education": "Online Search",
  "current_occupation": "Working Professional",
  "course_selection_factor": "Better Career Prospects",
  "lead_profile": "Potential Lead",
  "city": "Mumbai",
  "do_not_email": "No",
  "free_mastering_interview_copy": "No",
  "total_visits": 5,
  "total_time_spent_on_website": 1200,
  "page_views_per_visit": 4
}
```
### Sample Response
```JSON
{
  "prediction": "Likely to Convert",
  "conversion_probability": 0.9707,
  "lead_priority": "High"
}
```
---
## 🔍 Model Explainability

The model analysis identified several important factors influencing lead conversion.

Some of the most influential features include:

- Total Time Spent on Website
- Lead Origin
- Lead Profile
- Current Occupation
- Course Selection Factor
- Total Visits
- Website Engagement

These insights help make the system more than just a prediction model by supporting business decision-making and lead prioritization.

## 🎯 Business Value

The system can help businesses:

- Prioritize high-potential leads
- Improve sales team efficiency
- Reduce time spent on low-potential leads
- Support data-driven follow-up decisions
- Optimize lead management strategies

## 🔮 Future Improvements

Possible future improvements include:

- PostgreSQL database integration
- Lead history tracking
- Synthetic lead data generation
- Batch lead scoring
- Dashboard analytics
- SHAP-based model explainability
- Model monitoring
- Docker containerization
- Cloud deployment
- Authentication and user management
## 👨‍💻 Author

**Mohsin Shafait**

Aspiring AI/ML Engineer
## 📌 Project Status

MVP Completed ✅

The application successfully integrates:
```
Machine Learning
      ↓
FastAPI
      ↓
Streamlit
```
and provides an end-to-end system for lead conversion prediction and lead prioritization.