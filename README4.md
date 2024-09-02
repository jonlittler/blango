# Advanced Django External API

## Module 1

Welcome to Week 1 of the Advanced Django: External APIs and Task Queuing course. These assignments cover working with APIs including OMDB and GitHub. The module ends with graded coding exercises.

Learning Objectives

- Get and parse content from an API with the Requests library
- Raise an exception if the status code indicates an error
- Use Requests to PUT and POST information to an API
- Add a header for authenticating against an API
- Use the params argument to simplify searching with URL parameters
- Create an app that stores information about movies
- Use the OMDb API to fetch information about movies
- Conceptualize how the user and site will behave
- Increase efficiency by limiting the number of times the API is queried
- Identify the benefits of keeping Python logic separate from Django
- Identify the pros and cons of using a third-party library
- Generate a GitHub access token and integrate it with Django
- Use Python to query GitHub and render the response in HTML

### Requests Module

https://docs.python-requests.org/en/latest/user/advanced/#request-and-response-objects

```bash
git clone git@github.com:jonlittler/blango.git
pip3 install requests
python3 manage.py shell

# testing
python3 requests_test.py
```

```python
import requests
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code)
print(response.text)
print(response.json())
print(response.headers)
print(response.headers["Content-Type"])

response = requests.get("https://jsonplaceholder.typicode.com/invalidurl")
response.raise_for_status()

# json
import json

post_data = { "id": 1, "title": "New Title", "body": "Updated Body", "userId": 1}

resp = requests.put("https://jsonplaceholder.typicode.com/posts/1", data=json.dumps(post_data))

# or let requests do it for you
resp = requests.put("https://jsonplaceholder.typicode.com/posts/1", json=post_data)
```

### OMDB

1. Go to the course4_proj repo. This repo contains the starting point for this project.
2. Click on the “Fork” button in the top-right corner.
3. Click the green “Code” button.
4. Copy the SSH information.

https://github.com/codio-templates/course4_proj

```bash
git clone git@github.com:jonlittler/course4_proj.git
```
