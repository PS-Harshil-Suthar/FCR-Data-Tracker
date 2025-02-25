from flask import Flask, request, jsonify
import subprocess
from jira import JIRA
import pickle

app = Flask(__name__)

# Your Jira Credentials & URL
JIRA_URL = "https://3eco.atlassian.net"
USERNAME = "harshil.suthar@3eco.com"
API_TOKEN = "ATATT3xFfGF0NgF-kBeLZppNwvEGNrcSTbyyhLCZUNPckZUsdQp7K9cA0DJEV0KXHpGr95kLkFqMmdUL4xOR2y0-m7JiasaS93uUvT14MMbaqNSdRoT26OU2iVlL9q7BV6vjXWbEEhNRRa25aqo_SC0vKt8b5HMmERVTjGyDCvj6faJnFRh6wvg=2A0A7DAB"
PROJECT_KEY = "SD"

# Connect to Jira
jira = JIRA(basic_auth=(USERNAME, API_TOKEN), options={'server': JIRA_URL})

@app.route('/fetch_issues', methods=['POST'])
def fetch_issues():
    data = request.json
    from_date = data.get("from_date")
    to_date = data.get("to_date")

    # JQL Query
    jql_query = f'project = {PROJECT_KEY} AND resolution IS NOT EMPTY AND resolved >= "{from_date}" AND resolved <= "{to_date}" ORDER BY resolved DESC'
    
    issues = jira.search_issues(jql_query, maxResults=None, expand='changelog')

    # Save the issues to a pickle file
    pickle_filename = 'jira_issues_data.pkl'
    with open(pickle_filename, 'wb') as file:
        pickle.dump(issues, file)

    # Convert issues to JSON format
    issue_list = [{"key": issue.key, "summary": issue.fields.summary, "status": issue.fields.status.name} for issue in issues]

    # **Trigger FRC Data Generation**
    process = subprocess.Popen(["python", "generate_fcr.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for script to complete execution
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        return jsonify({"status": "success", "issues": issue_list, "message": "FCR data generated successfully!"})
    else:
        return jsonify({"status": "error", "issues": issue_list, "message": stderr.decode("utf-8")})

if __name__ == '__main__':
    app.run(debug=True)



