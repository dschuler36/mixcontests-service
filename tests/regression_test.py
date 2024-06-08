import requests

# Create x users
def create_users(num_users):
    for x in range(0, num_users):
        payload = {
            "email": "example.com"
        }
        response = requests.post(f'{base_url}/api/users', json=payload)
# Create contest
# have each user submit entry to contest
# perform 3 ratings per user


if __name__ == '__main__':
    base_url = 'http://localhost'