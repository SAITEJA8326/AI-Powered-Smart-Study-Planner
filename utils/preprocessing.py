import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def load_data(path):
    # Added support for both CSV and Excel for robustness
    if path.endswith('.csv'):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()
    return df

def preprocess_nn(df):
    # FEATURE ENGINEERING: Adding derived metrics
    # Efficiency: Score per hour studied
    # Consistency: Attendance * Study Hours
    df['efficiency'] = (df['maths_total'] + df['physics_total'] + df['chemistry_total']) / (df['no_of_hours_studied'] + 1)
    df['consistency'] = (df['attendance'] / 100) * df['study_hours']
    
    features = ['attendance', 'study_hours', 'no_of_hours_studied', 'efficiency', 'consistency']
    targets = ['maths_total', 'physics_total', 'chemistry_total']
    
    X = df[features]
    y = df[targets]

    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()

    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)

    return X_scaled, y_scaled, scaler_X, scaler_y

def get_subtopics(df):
    subtopic_keywords = ['s&p','trigonometry','calculus','algebra','coordinate',
                         'optics','mechanics','thermodynamics','waves','electricity',
                         'inorganic','organic','physical']
    subtopics = [col for col in df.columns if any(x in col for x in subtopic_keywords)]
    return df[subtopics]