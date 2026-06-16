import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# 1. FIX PATHING (Ensures 'utils' folder is found)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import init_db, save_week, get_history
from utils.schedule import generate_smart_schedule

# Initialize Database
init_db()

st.set_page_config(page_title="AI Scholar Pro", layout="wide")
st.title("🎓 AI Student Performance Tracker")

# 2. SIDEBAR INPUTS
with st.sidebar:
    st.header("👤 Profile")
    stu_name = st.text_input("Student Name", "John Doe")
    week_num = st.number_input("Week", 1, 10, 1)
    st.divider()
    attendance = st.slider("Attendance %", 0, 100, 85)
    study_h = st.slider("Daily Study Hours", 1, 15, 6)

# 3. MANUAL SUB-TOPIC INPUTS (Student gives these marks)
st.subheader(f"📝 Week {week_num}: Sub-Topic Marks")
c1, c2, c3 = st.columns(3)

with c1:
    m_alg = st.slider("Algebra", 0, 20, 10)
    m_cal = st.slider("Calculus", 0, 20, 10)
with c2:
    p_mec = st.slider("Mechanics", 0, 20, 10)
    p_opt = st.slider("Optics", 0, 20, 10)
with c3:
    c_org = st.slider("Organic Chem", 0, 20, 10)
    c_phy = st.slider("Physical Chem", 0, 20, 10)

# 4. ANALYZE BUTTON
if st.button("🚀 Submit & Analyze Progress"):
    current_marks = {
        "Algebra": m_alg, "Calculus": m_cal,
        "Mechanics": p_mec, "Optics": p_opt,
        "Organic": c_org, "Physical": c_phy
    }
    
    # Save to Database
    save_week(stu_name, week_num, scores)

    
    # Step 6: Fetch Comparison
    history = get_history(stu_name)
    if week_num > 1:
        st.header(f"🔄 Progress vs Week {week_num-1}")
        prev_week = history[history['week'] == week_num - 1]
        if not prev_week.empty:
            m_cols = st.columns(len(current_marks))
            for i, (topic, score) in enumerate(current_marks.items()):
                old_val = prev_week[prev_week['topic'] == topic]['score'].values[0]
                m_cols[i].metric(label=topic, value=score, delta=float(score - old_val))

    # FIXED DYNAMIC RADAR CHART
    st.divider()
    df_radar = pd.DataFrame({
        'Score': list(current_marks.values()),
        'Topic': list(current_marks.keys())
    })
    fig = px.line_polar(df_radar, r='Score', theta='Topic', line_close=True)
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_container_width=True)

    # SUB-TOPIC SCHEDULE
    weakest = min(current_marks, key=current_marks.get)
    st.subheader(f"📅 Adaptive Plan: Focusing on {weakest}")
    plan = generate_smart_schedule(weakest)
    st.table(pd.DataFrame(plan).T)