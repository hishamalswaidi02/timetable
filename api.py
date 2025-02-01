import requests
import json


GITHUB_TOKEN = "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"
REPO_OWNER = "hishamalswaidi02"
REPO_NAME = "timetable"

BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def get_lectures():
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code == 200:
        lectures = []
        for issue in response.json():
            lectures.append({
                "id": issue["id"],
                "teacher_name": issue["title"],
                "subject": issue["body"],
                "start_time": issue["created_at"],
                "status": "upcoming" if issue["state"] == "open" else "completed"
            })
        return lectures
    else:
        return {"error": "Failed to fetch lectures"}

def add_lecture(teacher_name, subject, start_time):
    data = {
        "title": teacher_name,
        "body": f"{subject} - {start_time}",
        "labels": ["lecture"]
    }
    response = requests.post(BASE_URL, headers=HEADERS, json=data)
    if response.status_code == 201:
        return {"success": "Lecture added successfully"}
    else:
        return {"error": "Failed to add lecture"}


def notify_students(lecture_id):
    issue_url = f"{BASE_URL}/{lecture_id}/comments"
    data = {"body": "📢 المحاضرة بدأت الآن! انضموا بسرعة!"}
    response = requests.post(issue_url, headers=HEADERS, json=data)
    if response.status_code == 201:
        return {"success": "Notification sent"}
    else:
        return {"error": "Failed to send notification"}


def close_lecture(lecture_id):
    issue_url = f"{BASE_URL}/{lecture_id}"
    data = {"state": "closed"}
    response = requests.patch(issue_url, headers=HEADERS, json=data)
    if response.status_code == 200:
        return {"success": "Lecture ended"}
    else:
        return {"error": "Failed to close lecture"}

if __name__ == "__main__":
    print(get_lectures())
    print(add_lecture("د. محمد", "شبكات الحاسوب", "2025-02-05T10:00:00Z"))
