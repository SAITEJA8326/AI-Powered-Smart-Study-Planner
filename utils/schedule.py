def generate_smart_schedule(weakest_subtopic, student_type="Steady Learner"):
    """
    Generates a highly engaging, sub-topic specific 7-day study plan.
    """
    intensity_map = {
        "Top Performer": 1.2,
        "Steady Learner": 1.0,
        "At-Risk": 0.8,
        "Low Engagement": 0.7
    }
    
    multiplier = intensity_map.get(student_type, 1.0)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    schedule = {}
    
    for day in days:
        if day in ["Monday", "Wednesday", "Friday"]:
            schedule[day] = {
                "Main Focus": f"🎯 {weakest_subtopic} Mastery",
                "Morning (2h)": "Concept Deep-Dive & Theory Video",
                "Evening (1.5h)": f"Solve 25 Problems in {weakest_subtopic}",
                "Strategy": "Active Recall & Blurting Method",
                "Priority": "🔥 High"
            }
        elif day in ["Tuesday", "Thursday"]:
            schedule[day] = {
                "Main Focus": "🔄 Cross-Subject Revision",
                "Morning (1.5h)": "Formula Sheet Updates",
                "Evening (1h)": "Quick Quiz on Strong Subjects",
                "Strategy": "Spaced Repetition",
                "Priority": "⚡ Medium"
            }
        elif day == "Saturday":
            schedule[day] = {
                "Main Focus": "⚔️ Challenge Day",
                "Block (3h)": f"Previous Year Questions: {weakest_subtopic}",
                "Strategy": "Timed Practice (No notes)",
                "Priority": "🚨 Critical"
            }
        else: # Sunday
            schedule[day] = {
                "Main Focus": "🧘 Review & Recharge",
                "Morning (2h)": "Weekly Mock Test (All Topics)",
                "Afternoon": "Analyze Error Log",
                "Strategy": "Mental Reset",
                "Priority": "🟢 Low"
            }
            
    return schedule