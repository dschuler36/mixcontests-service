import random

import requests
import uuid
from datetime import datetime, timedelta


def create_users(num_users):
    users = []
    for x in range(0, num_users):
        user_uuid = str(uuid.uuid4())
        payload = {
            "id": str(uuid.uuid4()),
            "email": f"{user_uuid}.com",
            "username": f"{user_uuid} username"
        }
        response = requests.post(url=f'{base_url}/api/users', json=payload)
        if response.status_code != 200:
            raise Exception(response.text)
        users.append(response.json()['id'])
    return users


def create_contest():

    contest_start = datetime.now()
    submission_end = contest_start + timedelta(days=4)
    contest_end = contest_start + timedelta(days=7)
    payload = {
      "title": "The Weekly #1",
      "description": "Our flagship contest",
      "start_date": str(contest_start),
      "end_date": str(contest_end),
      "submission_start_date": str(contest_start),
      "submission_end_date": str(submission_end),
      "voting_start_date": str(submission_end),
      "voting_end_date": str(contest_end),
      "stem_url": "string"
    }
    response = requests.post(url=f'{base_url}/api/contests', json=payload)
    if response.status_code != 200:
        raise Exception(response.text)

    print(f'Contest created')
    return response.json()['id']


def create_submissions(users, contest_id):
    submissions = []
    for user_id in users:
        payload = {
            "submission_file_path": "./tests/test_data/trails.mp3",
            "contest_id": contest_id,
            "user_id": user_id,
            "state": "Enter Contest"
        }
        response = requests.post(url=f'{base_url}/api/submissions', json=payload)
        if response.status_code != 200:
            raise Exception(response.text)
        submissions.append(response.json()['id'])

    print(f'{len(submissions)} submissions created')
    return submissions


def create_feedback(contest_id, users):
    for user_id in users:
        for i in range(0, 2):
            mixes_response = requests.get(url=f'{base_url}/api/feedback/{contest_id}/submissions/{user_id}')
            mix_ids = []
            for mr in mixes_response.json():
                mix_ids.append(mr['id'])

            payload = {
              "contest_id": contest_id,
              "submission_1_id": mix_ids[0],
              "submission_2_id": mix_ids[1],
              "winner_submission_id": mix_ids[random.randint(0, 1)],
              "rater_user_id": user_id,
              "feedback_text_1": "pretty good",
              "feedback_text_2": "pretty good"
            }

            feedback_response = requests.post(url=f'{base_url}/api/feedback', json=payload)
            if feedback_response.status_code != 200:
                raise Exception(feedback_response.text)


if __name__ == '__main__':
    base_url = 'http://localhost:8000'
    users = create_users(50)
    print(f'users: {users}')
    contest_id = create_contest()
    print(f'contest_id: {contest_id}')
    submissions = create_submissions(users, contest_id)
    print(f'submissions: {submissions}')
    create_feedback(contest_id, users)
