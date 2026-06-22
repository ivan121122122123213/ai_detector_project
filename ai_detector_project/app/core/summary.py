def build_summary(risk_score, summary, classifications, files):
    if risk_score >= 75:
        level = "High"
    elif risk_score >= 40:
        level = "Medium"
    else:
        level = "Low"

    top_entities = sorted(summary.items(), key=lambda x: x[1], reverse=True)[:6]
    top_files = sorted(files, key=lambda f: f.risk, reverse=True)[:5]
    lines = []
    lines.append(f"Risk level: {level}. Overall score: {risk_score}/100.")
    if top_entities:
        lines.append("Most frequent entities: " + ", ".join([f"{k}: {v}" for k, v in top_entities]) + ".")
    if top_files:
        lines.append("Most important files: " + ", ".join([f.path for f in top_files]) + ".")
    if summary.get("api_like_keys") or summary.get("jwt_like") or summary.get("ssh_private_key_marker"):
        lines.append("Sensitive credentials-like patterns were detected. Rotate exposed secrets and remove them from archives before sharing.")
    if classifications.get("Databases") or classifications.get("Backups"):
        lines.append("Database or backup files were detected. Check whether they contain personal or production data.")
    if not top_entities and not top_files:
        lines.append("No obvious sensitive indicators were detected in readable files.")
    return " ".join(lines)
