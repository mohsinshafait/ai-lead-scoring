# 🎯 AI Lead Scoring & Conversion Prediction System

An end-to-end Machine Learning application that predicts the probability of a lead converting into a customer and automatically assigns a business priority level.

The project demonstrates how a trained Machine Learning model can be integrated into a production-style application using **FastAPI**, **Streamlit**, **GitHub**, and cloud deployment.

---
## 🚀 Live Demo

- 🎯 **Live Streamlit Application:** https://ai-lead-scoring-mohsin.streamlit.app/
- ⚡ **Live FastAPI API:** https://ai-lead-scoring-hvsq.onrender.com/
- 📚 **API Documentation:** https://ai-lead-scoring-hvsq.onrender.com/docs

## Project Overview

Businesses receive many leads every day, but not all leads have the same probability of conversion.

Sales teams can waste valuable time treating every lead equally.

This system helps prioritize leads by:

- Predicting whether a lead is likely to convert
- Calculating the lead's conversion probability
- Categorizing leads as **High, Medium, or Low priority**
- Providing a recommended follow-up action based on lead priority

---

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
````

---

## 📊 Lead Priority Strategy

| Conversion Probability | Priority | Recommended Action                |
| ---------------------- | -------- | --------------------------------- |
| ≥ 70%                  | 🔥 High  | Contact immediately               |
| 40% – 69%              | ⚡ Medium | Targeted follow-up                |
| < 40%                  | 📌 Low   | Automated or lower-cost follow-up |

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   Streamlit User    │
                    │     Interface       │
                    └──────────┬──────────┘
                               │
                               │ HTTPS Request
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    │       Render        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  ML Pipeline Model  │
                    │  lead_scoring_model │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Prediction Response │
                    │ Probability         │
                    │ Lead Priority       │
                    └─────────────────────┘
```

---

## ✨ Key Features

* Machine Learning-based lead conversion prediction
* Conversion probability scoring
* Automatic lead prioritization
* High / Medium / Low priority classification
* Business-oriented follow-up recommendations
* REST API built with FastAPI
* Interactive API documentation using Swagger
* Streamlit web interface
* Deployed backend and frontend
* End-to-end cloud testing

---

## 🛠️ Technologies Used

### Machine Learning

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib

### Backend

* FastAPI
* Uvicorn

### Frontend

* Streamlit
* Requests

### Deployment & Development

* Git
* GitHub
* Render
* Streamlit Community Cloud

---

## 📁 Project Structure

```text
ai-lead-scoring/

├── app/
│   ├── main.py
│   │
│   └── services/
│       └── prediction.py
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
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/mohsinshafait/ai-lead-scoring.git
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

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application Locally

The application has two components:

1. FastAPI Backend
2. Streamlit Frontend

### Start the FastAPI Backend

Run:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### Start the Streamlit Frontend

Open another terminal and run:

```bash
python -m streamlit run streamlit_app.py
```

The Streamlit application will be available at:

```text
http://localhost:8501
```

---

## 📡 API Example

### Sample Request

The `/predict` endpoint accepts lead information such as:

```json
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

```json
{
  "prediction": "Likely to Convert",
  "conversion_probability": 0.9707,
  "lead_priority": "High"
}
```

---

## 🔍 Model Insights

The model uses lead information and website engagement data to estimate the probability of conversion.

Important categories of information include:

* Website engagement
* Total time spent on the website
* Number of website visits
* Lead origin and source
* Lead profile
* Current occupation
* Course selection factors

The goal is not only to generate predictions but also to support better business decisions and lead prioritization.

---

## 🎯 Business Value

This system can help businesses:

* Prioritize high-potential leads
* Improve sales team efficiency
* Reduce time spent on low-potential leads
* Support data-driven follow-up decisions
* Improve lead management workflows

---

## 🚀 Deployment Architecture

```text
User
  ↓
Streamlit Community Cloud
  ↓
HTTPS Request
  ↓
FastAPI on Render
  ↓
Machine Learning Model
  ↓
Prediction Result
```

---

## 🔮 Version 2 Roadmap

The next version of the project will expand the MVP into a more realistic production-style AI/ML system.

Planned improvements include:

* PostgreSQL database integration
* Relational lead data
* Learner and course information
* Lead interaction history
* Sales action tracking
* Synthetic business data generation
* Advanced feature engineering
* Batch lead scoring
* Analytics dashboard
* SHAP-based model explainability
* Model monitoring
* Docker containerization
* Authentication and user management

---

## 📌 Project Status

### Version 1 — MVP Completed ✅

The first version successfully demonstrates an end-to-end deployed Machine Learning system:

```text
Machine Learning Model
        ↓
FastAPI Backend
        ↓
Cloud Deployment
        ↓
Streamlit Frontend
        ↓
Live Prediction
```

---

## 👨‍💻 Author

**Mohsin Shafait**

Aspiring AI/ML Engineer
