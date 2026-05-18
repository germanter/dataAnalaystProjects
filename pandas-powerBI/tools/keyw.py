import pandas as pd
import re
import numpy as np

keywords = [
    # Languages
    "Python",
    "SQL",
    "Java",
    "SAS",
    "Scala",
    "C++",
    "Linux",
    "JavaScript",
    "HTML",
    "CSS",
    "Matlab",
    "Julia",
    # Cloud & Big Data Infrastructure
    "AWS",
    "Spark",
    "Hadoop",
    "Hive",
    "Azure",
    "NoSQL",
    "ETL",
    "GCP",
    "Kubernetes",
    "Docker",
    "Kafka",
    "MapReduce",
    "Cloud",
    # BI & Analytics Tools
    "Tableau",
    "Excel",
    "Power BI",
    "Looker",
    "Qlik",
    # ML / Deep Learning Frameworks
    "TensorFlow",
    "PyTorch",
    "Scikit-Learn",
    "Keras",
    "NLTK",
    "SpaCy",
    "OpenCV",
    # Core Methodologies & Concepts
    "Machine Learning",
    "ML",
    "AI",
    "Artificial Intelligence",
    "Deep Learning",
    "NLP",
    "Natural Language Processing",
    "Predictive Modeling",
    "Statistics",
    "Mathematics",
    "Computer Science",
    "Data Science",
    "Exploratory Data Analysis",
    "Regression",
    "Clustering",
    "Time Series",
    "Data Mining",
    "Big Data",
    # Security Clearance / Government Context
    "Security Clearance",
    "Clearance",
    "TS/SCI",
    "Secret Clearance",
]

keywords = [i.lower() for i in keywords]


def kw_match(text):
    if pd.isna(text):
        return
    
    txt = str(text).lower()

    return [kw for kw in keywords if kw in txt]


def jt_stizer(title):
    if pd.isna(title) or not isinstance(title, str):
        return np.nan
    
    t = title.lower().strip()
    
    t = re.sub(r'\(position added.*\)', '', t) 
    t = re.sub(r'\(ts/sci.*\)|ts/sci|fsp|ci required', '', t) 
    t = re.sub(r'\(remote\)|remote', '', t) 
    t = re.sub(r'-\s*saturday.*shift|shift', '', t) 
    t = re.sub(r'\d+-\d+|\(\d+\)|\b\d+\b', '', t) 

    t = re.sub(r'\b(bay area|ca|nyc|portland|usa|san antonio or)\b', '', t) 
    t = re.sub(r'–.*novartis.*|unilever prestige', '', t) 
    
    seniority_pattern = r'\b(sr|jr|senior|junior|lead|principal|staff|associate|experienced|chief|vp|vice president|director|manager|ii|iii|i|v|iv|level|track|early career|mid-career)\b'
    t = re.sub(seniority_pattern, '', t)

    t = t.replace('â€“', '').replace('(', '').replace(')', '').strip()
    
    t = re.split(r'[-–/,]', t)[0].strip()
    
    t = re.sub(r'\s+', ' ', t).strip()
    
    if len(t) <= 4 or t in ['data', 'analytics', 'scientist', 'engineer']:
        return np.nan

    if any(kw in t for kw in ['machine learning', 'ml', 'computer vision', 'deep learning', 'ai/ml', 'ai ops', 'applied ai']):
        return 'Machine Learning Engineer'
    
    elif any(kw in t for kw in ['molecular', 'lab', 'purification', 'biomarker', 'cytometry', 'toxicologist', 'ngs', 'cancer biology', 'metabolic']):
        return 'Biomedical & Lab Scientist'
    
    elif 'scientist' in t or 'science' in t or 'statistician' in t or 'statistical' in t or 'decision' in t:
        return 'Data Scientist'
    
    elif any(kw in t for kw in ['engineer', 'architect', 'big data', 'cloud', 'integration', 'modeler', 'tableau', 'kafka']):
        return 'Data Engineer'
    
    elif any(kw in t for kw in ['analyst', 'analytics', 'bi', 'business intelligence', 'insights', 'report writer', 'tableau', 'portfolio']):
        return 'Data Analyst'
    
    elif 'software' in t or 'developer' in t or 'computer scientist' in t:
        return 'Software Engineer'
    
    return t.title()