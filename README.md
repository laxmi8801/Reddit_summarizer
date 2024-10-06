# Reddit Summarizer Application
A web-based application that allows users to search for Reddit posts related to a specific query, select a Reddit post, and get a summary of the discussion.

## Project Overview
This application allows users to input a query, search Reddit posts using the Reddit PRAW API, and select a Reddit post to get a summarized version of the discussion. Users can browse through the relevant posts, choose a post for summarization, and the app generates a concise summary of the content.

## Tech Stack
Backend: <br>
Flask (Python)<br>
Reddit API (for Reddit search)<br>
Python libraries for summarization (e.g., Reddit praw, requests)<br>

Frontend:<br>
HTML<br>
CSS (Bootstrap 5)<br>
JavaScript (for handling frontend logic)<br>

## Setup Instructions
1. Prerequisites<br>
   
Before running this project, ensure you have the following installed on your machine:<br>

Python 3.7+<br>
Reddit API credentials (client ID, client secret, and user agent)<br>
Flask<br>

2. Installation<br>
Follow these steps to install and set up the project on your local machine:<br>

Clone the repository:
```
git clone https://github.com/yourusername/reddit-summarizer.git
cd reddit-summarizer
```

Create a virtual environment (optional but recommended):

```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Install dependencies:

```
pip install -r requirements.txt
Set up your Reddit API credentials:
```

Create a Reddit app to obtain client_id, client_secret, and user_agent from Reddit's developer console.<br>
Create a .env file at the root of the project and add your credentials:<br>

```
PRAW_CLIENT_ID=your_client_id
PRAW_CLIENT_SECRET=your_client_secret
PRAW_USER_AGENT=your_user_agent
```
3. Running the Application<br>
Start the Flask server:
```
flask run
```
Open your browser and navigate to http://127.0.0.1:5000 to access the application.<br>

## API Endpoints
/search-reddit: Takes a query as input and returns a list of relevant Reddit posts (URLs).<br>
Method: GET<br>
Parameters: query<br>
/summarize-reddit: Takes a Reddit URL as input and returns a summary of the content.<br>
Method: GET<br>
Parameters: url<br>
