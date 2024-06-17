from enum import Enum

import requests
from datetime import datetime, timedelta

class TestScenarios(Enum):
    active = "ACTIVE"
    submission = "SUBMISSION"
    voting = "VOTING"
    ended = "ENDED"
    upcoming = "UPCOMING"


def create_contest(data):
    url = "http://localhost:8000/api/contests"
    response = requests.post(url, json=data)
    print(response.status_code)
    if response.status_code == 201:
        print(f"Successfully created contest: {data['title']}")
    else:
        print(f"Failed to create contest: {data['title']} - {response.text}")


def generate_contest_data(type_to_create):
    now = datetime.utcnow()
    if type_to_create == TestScenarios.active:
        contest = {
            "title": "Active Contest",
            "description": "This contest is currently active.",
            "start_date": (now - timedelta(days=2)).isoformat(),
            "end_date": (now + timedelta(days=2)).isoformat(),
            "submission_start_date": (now - timedelta(days=2)).isoformat(),
            "submission_end_date": (now + timedelta(days=1)).isoformat(),
            "voting_start_date": (now + timedelta(days=1)).isoformat(),
            "voting_end_date": (now + timedelta(days=2)).isoformat(),
            "stem_url": "http://example.com/stems"
        }
    elif type_to_create == TestScenarios.submission:
        contest = {
            "title": "Submission Phase Contest",
            "description": "This contest is in the submission phase.",
            "start_date": (now - timedelta(days=5)).isoformat(),
            "end_date": (now + timedelta(days=5)).isoformat(),
            "submission_start_date": (now - timedelta(days=5)).isoformat(),
            "submission_end_date": (now + timedelta(days=3)).isoformat(),
            "voting_start_date": (now + timedelta(days=3)).isoformat(),
            "voting_end_date": (now + timedelta(days=5)).isoformat(),
            "stem_url": "http://example.com/stems"
        }
    elif type_to_create == TestScenarios.voting:
        contest = {
            "title": "Voting Phase Contest",
            "description": "This contest is in the voting phase.",
            "start_date": (now - timedelta(days=15)).isoformat(),
            "end_date": (now + timedelta(days=1)).isoformat(),
            "submission_start_date": (now - timedelta(days=15)).isoformat(),
            "submission_end_date": (now - timedelta(days=5)).isoformat(),
            "voting_start_date": (now - timedelta(days=5)).isoformat(),
            "voting_end_date": (now + timedelta(days=1)).isoformat(),
            "stem_url": "http://example.com/stems"
        }
    elif type_to_create == TestScenarios.ended:
        contest = {
            "title": "Ended Contest",
            "description": "This contest has ended.",
            "start_date": (now - timedelta(days=45)).isoformat(),
            "end_date": (now - timedelta(days=15)).isoformat(),
            "submission_start_date": (now - timedelta(days=45)).isoformat(),
            "submission_end_date": (now - timedelta(days=30)).isoformat(),
            "voting_start_date": (now - timedelta(days=30)).isoformat(),
            "voting_end_date": (now - timedelta(days=15)).isoformat(),
            "stem_url": "http://example.com/stems"
        }
    elif type_to_create == TestScenarios.upcoming:
        contest = {
            "title": "Upcoming Contest",
            "description": "This contest will start soon.",
            "start_date": (now + timedelta(days=10)).isoformat(),
            "end_date": (now + timedelta(days=20)).isoformat(),
            "submission_start_date": (now + timedelta(days=10)).isoformat(),
            "submission_end_date": (now + timedelta(days=15)).isoformat(),
            "voting_start_date": (now + timedelta(days=15)).isoformat(),
            "voting_end_date": (now + timedelta(days=20)).isoformat(),
            "stem_url": "http://example.com/stems"
        }

    return contest

if __name__ == "__main__":
    type_to_create = TestScenarios.voting
    contest = generate_contest_data(type_to_create)
    print(contest)
    create_contest(contest)
