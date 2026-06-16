def analyze(scores, labels):
    avg = sum(scores) / len(scores)

    weak = labels[scores.index(min(scores))]
    strong = labels[scores.index(max(scores))]

    if avg > 80:
        level = "🔥 Top Performer"
    elif avg > 60:
        level = "⚡ Good Performer"
    elif avg > 40:
        level = "⚠️ Needs Improvement"
    else:
        level = "🚨 At Risk"

    return weak, strong, avg, level