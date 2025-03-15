import requests

url = "http://127.0.0.1:5000/users"

# List of users to add
users = [
    {"username": "isa", "age": 29, "country": "USA"}
]

# Send `POST` request and check response
for user in users:
    response = requests.post(url, json=user)
    
    # Print raw response to debug issues
    print("Raw Response:", response.text)  # <-- This helps debug

    try:
        print(response.json())  # Parse response if valid JSON
    except requests.exceptions.JSONDecodeError:
        print("❌ Error: Response is not valid JSON. Check if API is running.")
