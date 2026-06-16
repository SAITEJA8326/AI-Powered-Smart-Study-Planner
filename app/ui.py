import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os

# Fix pathing
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.database import init_db, manage_user, save_weekly_entry, get_student_trend
from utils.schedule import generate_granular_schedule

init_db()

st.set_page_config(page_title="AI Scholar Pro", layout="wide", page_icon="🎓")

if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 AI Scholar Portal")
    choice = st.radio("Mode", ["Login", "Register"], horizontal=True)
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Enter Dashboard"):
        if choice == "Register":
            if manage_user(user, pwd, "reg"): st.success("Registered successfully!")
            else: st.error("User already exists.")
        else:
            if manage_user(user, pwd):
                st.session_state.auth = True
                st.session_state.username = user
                st.rerun()
            else: st.error("Invalid credentials.")
else:
    st.title(f"🚀 Dashboard: {st.session_state.username}")
    
    with st.sidebar:
        week = st.number_input("Tracking Week", 1, 52, 1)
        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()

    st.subheader(f"📊 Enter Week {week} Marks")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.info("### 📐 Maths")
        m1 = st.slider("Algebra", 0, 20, 10); m2 = st.slider("Calculus", 0, 20, 10)
        m3 = st.slider("Trig", 0, 20, 10); m4 = st.slider("S&P", 0, 20, 10); m5 = st.slider("Coord", 0, 20, 10)
    with c2:
        st.info("### ⚛️ Physics")
        p1 = st.slider("Mechanics", 0, 20, 10); p2 = st.slider("Optics", 0, 20, 10)
        p3 = st.slider("Thermo", 0, 20, 10); p4 = st.slider("Waves", 0, 20, 10); p5 = st.slider("Elec", 0, 20, 10)
    with c3:
        st.info("### 🧪 Chemistry")
        ch1 = st.slider("Organic", 0, 20, 10); ch2 = st.slider("Inorganic", 0, 20, 10); ch3 = st.slider("Physical", 0, 20, 10)

    labels = ["Algebra", "Calculus", "Trig", "S&P", "Coord", "Mechanics", "Optics", "Thermo", "Waves", "Elec", "Organic", "Inorganic", "Physical"]
    scores = [m1, m2, m3, m4, m5, p1, p2, p3, p4, p5, ch1, ch2, ch3]

    if st.button("🔥 Run Analysis"):
        save_weekly_entry(st.session_state.username, week, scores)
        history = get_student_trend(st.session_state.username)

        # Step 6: Comparison
        if week > 1:
            st.divider()
            st.subheader(f"🔄 Comparison: Week {week-1} vs {week}")
            prev = history[history['week'] == week - 1]
            if not prev.empty:
                m_cols = st.columns(4)
                for i in range(4):
                    diff = scores[i] - prev.iloc[0, i+2]
                    m_cols[i].metric(labels[i], f"{scores[i]}/20", delta=f"{diff}")

        # Visuals & Schedule
        st.divider()
        v1, v2 = st.columns([1, 1])
        with v1:
            df_radar = pd.DataFrame(dict(r=scores, theta=labels))
            fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, title="Mastery Aura")
            fig.update_traces(fill='toself', line_color='#FF4B4B')
            st.plotly_chart(fig, use_container_width=True)
        with v2:
            weakest_idx = scores.index(min(scores))
            weakest_topic = labels[weakest_idx]
            st.error(f"🎯 Critical Focus: {weakest_topic}")
            # Calling the detailed schedule
            plan = generate_granular_schedule(weakest_topic)
            st.table(pd.DataFrame(plan).T)