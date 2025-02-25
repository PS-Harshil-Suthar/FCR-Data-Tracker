# from flask import Flask, request, jsonify, render_template
# from jira import JIRA
# import pandas as pd
# import pickle
# import datetime
# import json

# app = Flask(__name__)

# # Jira Authentication (Replace these with actual credentials)
# JIRA_URL = "https://3eco.atlassian.net"
# USERNAME = "harshil.suthar@3eco.com"
# API_TOKEN = "ATATT3xFfGF0NgF-kBeLZppNwvEGNrcSTbyyhLCZUNPckZUsdQp7K9cA0DJEV0KXHpGr95kLkFqMmdUL4xOR2y0-m7JiasaS93uUvT14MMbaqNSdRoT26OU2iVlL9q7BV6vjXWbEEhNRRa25aqo_SC0vKt8b5HMmERVTjGyDCvj6faJnFRh6wvg=2A0A7DAB"
# PROJECT_KEY = "SD"

# jira = JIRA(basic_auth=(USERNAME, API_TOKEN), options={'server': JIRA_URL})

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/fetch_issues", methods=["POST"])
# def fetch_issues():
#     data = request.json
#     from_date = data.get("from_date")
#     to_date = data.get("to_date")

#     if not from_date or not to_date:
#         return jsonify({"error": "Both From Date and To Date are required"}), 400

#     jql_query = (
#         f'project = {PROJECT_KEY} AND resolution IS NOT EMPTY '
#         f'AND resolved >= "{from_date}" AND resolved <= "{to_date}" '
#         f'AND "IT-Team[Dropdown]" = "Service Desk" '
#         f'AND issuetype IN ("[System] Incident", "[System] Service request") '
#         f'ORDER BY resolved DESC'
#     )

#     issues = jira.search_issues(jql_query, maxResults=, expand='changelog')

#     issue_data = []
#     for issue in issues:
#         comments = jira.comments(issue)
#         user_comments = [
#             comment for comment in comments 
#             if comment.author and issue.fields.reporter and 
#             comment.author.displayName == issue.fields.reporter.displayName
#         ]

#         issue_data.append({
#             'Issue Key': issue.key,
#             'Reporter': issue.fields.reporter.displayName if issue.fields.reporter else "Unassigned",
#             'Summary': issue.fields.summary,
#             'Created': issue.fields.created,
#             'Resolved': issue.fields.resolutiondate,
#             'Type': issue.fields.issuetype.name,
#             'Assignee': issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
#             'Status': issue.fields.status.name,
#             'Number of User Comments': len(user_comments)
#         })

#     total_issues = len(issue_data)
    
#     # Save to CSV
#     df = pd.DataFrame(issue_data)
#     current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     csv_filename = f"fcr_{current_time}.csv"
#     df.to_csv(csv_filename, index=False)

#     # Compute FCR metrics
#     frc_results = {
#         "total_issues": total_issues,
#         "csv_filename": csv_filename
#     }

#     return jsonify({
#         "status": "success",
#         "issues_fetched": total_issues,
#         "issue_data": issue_data,  # Updated: Send issues in response
#         "frc_results": frc_results,
#         "message": "FRC data generated successfully!"
#     })

# @app.route("/download_csv")
# def download_csv():
#     with open("frc_results.json", "r") as json_file:
#         frc_results = json.load(json_file)
#     return jsonify({"csv_filename": frc_results["csv_filename"]})

# if __name__ == "__main__":
#     app.run(debug=True)








from flask import Flask, request, jsonify, render_template # type: ignore
from jira import JIRA # type: ignore
import pandas as pd # type: ignore
import pickle
import datetime
import json

app = Flask(__name__)

# Jira Authentication (Replace these with actual credentials)
JIRA_URL = "https://3eco.atlassian.net"
USERNAME = "harshil.suthar@3eco.com"
API_TOKEN = "ATATT3xFfGF0cSukWaA-CqRFrhagm6QaZO32w66gKrCtwHUvf56MmWivBa7BPvOWaMHfNLouPqUyVKlOTi8FhMKQLPu3V5IrOn3klzQLxmHTwnQodjIcJN3EF_9h4iCsdCoN2I00trlcLoL1vlZ_vaFuaFmGq6nycPKfKOWTegYWcIp3iV0ygyw=8F4ACB6A"
PROJECT_KEY = "SD"

jira = JIRA(basic_auth=(USERNAME, API_TOKEN), options={'server': JIRA_URL})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/fetch_issues", methods=["POST"])
def fetch_issues():
    data = request.json
    from_date = data.get("from_date")
    to_date = data.get("to_date")

    if not from_date or not to_date:
        return jsonify({"error": "Both From Date and To Date are required"}), 400

    jql_query = (
        f'project = {PROJECT_KEY} AND resolution IS NOT EMPTY '
        f'AND resolved >= "{from_date}" AND resolved <= "{to_date}" '
        f'AND "IT-Team[Dropdown]" = "Service Desk" '
        f'AND issuetype IN ("[System] Incident", "[System] Service request") '
        f'ORDER BY resolved DESC'
    )

    issues = jira.search_issues(jql_query, maxResults=10000, expand='changelog')

    issue_data = []
    for issue in issues:
        comments = jira.comments(issue)
        user_comments = [
            comment for comment in comments 
            if comment.author and issue.fields.reporter and 
            comment.author.displayName == issue.fields.reporter.displayName
        ]
        
        # Only include issues where user comments are <= 3
        if len(user_comments) <= 3:
            issue_data.append({
                'Issue Key': issue.key,
                'Reporter': issue.fields.reporter.displayName if issue.fields.reporter else "Unassigned",
                'Summary': issue.fields.summary,
                'Created': issue.fields.created,
                'Resolved': issue.fields.resolutiondate,
                'Type': issue.fields.issuetype.name,
                'Assignee': issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
                'Status': issue.fields.status.name,
                'Number of User Comments': len(user_comments)
            })

    total_issues = len(issue_data)
    
    # Save to CSV
    df = pd.DataFrame(issue_data)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = f"fcr_{current_time}.csv"
    df.to_csv(csv_filename, index=False)

    # Compute FCR metrics
    frc_results = {
        "total_issues": total_issues,
        "csv_filename": csv_filename
    }

    return jsonify({
        "status": "success",
        "issues_fetched": total_issues,
        "issue_data": issue_data,  # Updated: Send issues in response
        "frc_results": frc_results,
        "message": "FRC data generated successfully!"
    })

@app.route("/download_csv")
def download_csv():
    with open("frc_results.json", "r") as json_file:
        frc_results = json.load(json_file)
    return jsonify({"csv_filename": frc_results["csv_filename"]})

if __name__ == "__main__":
    app.run(debug=True)
