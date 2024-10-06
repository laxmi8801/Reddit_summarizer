# Reddit Summarizer Application
A web-based application that allows users to search for Reddit posts related to a specific query, select a Reddit post, and get a summary of the discussion.

Project Overview
This application allows users to input a query, search Reddit posts using the Reddit PRAW API, and select a Reddit post to get a summarized version of the discussion. Users can browse through the relevant posts, choose a post for summarization, and the app generates a concise summary of the content.

Tech Stack
Backend:
Flask (Python)
Reddit API (for Reddit search)
Python libraries for summarization (e.g., Reddit praw, requests)

Frontend:
HTML
CSS (Bootstrap 5)
JavaScript (for handling frontend logic)

Setup Instructions
1. Prerequisites
   
Before running this project, ensure you have the following installed on your machine:

Python 3.7+
Reddit API credentials (client ID, client secret, and user agent)
Flask

2. Installation
Follow these steps to install and set up the project on your local machine:

Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/reddit-summarizer.git
cd reddit-summarizer
Create a virtual environment (optional but recommended):

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up your Reddit API credentials:

Create a Reddit app to obtain client_id, client_secret, and user_agent from Reddit's developer console.
Create a .env file at the root of the project and add your credentials:
makefile
Copy code
PRAW_CLIENT_ID=your_client_id
PRAW_CLIENT_SECRET=your_client_secret
PRAW_USER_AGENT=your_user_agent
3. Running the Application
Start the Flask server:

bash
Copy code
flask run
Open your browser and navigate to http://127.0.0.1:5000 to access the application.

API Endpoints
/search-reddit: Takes a query as input and returns a list of relevant Reddit posts (URLs).
Method: GET
Parameters: query
/summarize-reddit: Takes a Reddit URL as input and returns a summary of the content.
Method: GET
Parameters: url
