import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from utils.database import *
from utils.analysis import analyze
from utils.engine_dl import get_dl_insights
from utils.schedule import generate_smart_schedule

# ---------------- INIT ----------------
init_db()
st.set_page_config(page_title="Scholar Pro", layout="wide")

if "login" not in st.session_state:
    st.session_state.login = False

# ---------------- LOGIN ----------------
if not st.session_state.login:
    st.title("🔐Scholar Login")

    mode = st.radio("Mode", ["Login", "Register"])
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Enter"):
        if mode == "Register":
            if register_user(user, pwd):
                st.success("Registered!")
            else:
                st.error("User exists")
        else:
            if login_user(user, pwd):
                st.session_state.login = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid login")

# ---------------- DASHBOARD ----------------
else:
    st.title(f"🎓 Dashboard - {st.session_state.user}")

    if st.button("Logout"):
        st.session_state.login = False
        st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Add New Week",
        "📈 Progress",
        "🧠 AI Insights",
        "📅 Schedule"
    ])

    labels = [
        "Algebra","Calculus","Trig","S&P","Coord",
        "Mechanics","Optics","Thermo","Waves","Elec",
        "Organic","Inorganic","Physical"
    ]

    max_marks_map = {
        "Algebra":20, "Calculus":20, "Trig":20, "S&P":20, "Coord":20,
        "Mechanics":20, "Optics":20, "Thermo":20, "Waves":20, "Elec":20,
        "Organic":32, "Inorganic":32, "Physical":36
    }

    # ---------------- TAB 1: ADD WEEK ----------------
    with tab1:
        st.subheader("➕ Add Weekly Marks")

        week = st.number_input("Week Number", 1, 52)

        scores = []
        cols = st.columns(3)

        for i, label in enumerate(labels):
            with cols[i % 3]:
                max_marks = max_marks_map[label]
                val = st.slider(label, 0, max_marks, max_marks//2)
                scores.append(val)

        if st.button("💾 Save Data"):
            history = get_history(st.session_state.user)

            if not history.empty and week in history["week"].values:
                st.warning("⚠️ Overwriting existing week")

            save_week(st.session_state.user, week, scores)
            st.success("Saved successfully!")

            # ---------------- BAR GRAPH ----------------
            max_values = [max_marks_map[label] for label in labels]

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=labels,
                y=scores,
                name="Your Marks"
            ))

            fig.add_trace(go.Bar(
                x=labels,
                y=max_values,
                name="Max Marks",
                opacity=0.4
            ))

            fig.update_layout(
                title="📊 Marks Analysis",
                barmode='group'
            )

            st.plotly_chart(fig, use_container_width=True)

            # ---------------- PERFORMANCE ----------------
            total_score = sum(scores)
            total_max = sum(max_values)
            percentage = (total_score / total_max) * 100

            st.metric("📊 Overall Percentage", f"{percentage:.2f}%")

            st.subheader("🧠 AI Recommendation")

            if percentage < 35:
                st.error("🚨 Critical Performance")
                st.write("""
                - Focus heavily on weak topics
                - Study fundamentals daily
                - Minimum 3 hours practice
                """)

            elif percentage <= 70:
                st.warning("⚡ Moderate Performance")
                st.write("""
                - Improve consistency
                - Practice mixed questions
                - Weekly revisions needed
                """)

            else:
                st.success("🔥 Strong Performance")
                st.write("""
                - Focus on advanced problems
                - Solve PYQs
                - Improve speed
                """)

    # ---------------- TAB 2: PROGRESS ----------------
    with tab2:
        st.subheader("📈 Progress Tracker")

        df = get_history(st.session_state.user)

        if df.empty:
            st.info("No data yet")
        else:
            df_plot = df.drop(columns=["username"])

            df_plot["Maths"] = df_plot.iloc[:,1:6].mean(axis=1)
            df_plot["Physics"] = df_plot.iloc[:,6:11].mean(axis=1)
            df_plot["Chemistry"] = df_plot.iloc[:,11:14].mean(axis=1)

            df_bar = df_plot.melt(
                id_vars="week",
                value_vars=["Maths","Physics","Chemistry"],
                var_name="Subject",
                value_name="Score"
            )

            fig = px.bar(
                df_bar,
                x="week",
                y="Score",
                color="Subject",
                barmode="group",
                title="📊 Weekly Progress"
            )

            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df)

    # ---------------- TAB 3: AI ----------------
    with tab3:
        st.subheader("🧠 Deep Learning Insights")

        df = get_history(st.session_state.user)

        if df.empty:
            st.warning("No data available")
        else:
            latest = df.iloc[-1]
            scores = latest.drop(["username","week"]).values.astype(float)

            prediction, mse = get_dl_insights(scores)

            if prediction is None:
                st.error("Models not found")
            else:
                st.metric("🎯 Predicted Score", round(prediction,2))

                if mse > 0.05:
                    st.error("⚠️ Inconsistent performance")
                else:
                    st.success("✅ Stable learning")

    # ---------------- TAB 4: SCHEDULE ----------------
    with tab4:
        st.subheader("📅 Smart Study Plan")

        df = get_history(st.session_state.user)

        if df.empty:
            st.info("Add data first")
        else:
            latest = df.iloc[-1]
            scores = latest.drop(["username","week"]).values.tolist()

            weak, strong, avg, level = analyze(scores, labels)

            st.write(f"🎯 Focus Topic: {weak}")

            plan = generate_smart_schedule(weak)
            st.table(pd.DataFrame(plan).T)