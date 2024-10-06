from flask import Flask, request, jsonify,url_for,render_template
import requests
import re
import praw
import os
import openai
import textwrap

openai.api_key  = 'sk-**********'


app = Flask(__name__)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def search_reddit(query, limit=5):
    
    reddit = praw.Reddit(
        client_id='II237Mryzext2vqt5VJ0gg',
        client_secret='Hlb0Y4YGC2dW2w3hzc9AgElJmuTOdg',
        user_agent='python:comment_scraper:v1.0 (by /u/Alert_Passenger8)',
    )
    """Search Reddit for posts related to a query."""
    results = []
    for submission in reddit.subreddit('all').search(query, limit=limit):
        results.append({
            'title': submission.title,
            'url': submission.url
        })
    return results
    
def scrape_reddit_comments(url):
    reddit = praw.Reddit(
        client_id='II237Mryzext2vqt5VJ0gg',
        client_secret='Hlb0Y4YGC2dW2w3hzc9AgElJmuTOdg',
        user_agent='python:comment_scraper:v1.0 (by /u/Alert_Passenger8)',
    )

    # Get the submission from the URL
    submission = reddit.submission(url=url)

    # Expand all comments
    submission.comments.replace_more(limit=None)

    # Initialize lists to store comment data
    comments = []
    # Define a regular expression to detect image URLs (e.g., .jpg, .png)
    image_pattern = re.compile(r"(https?:\/\/.*\.(?:png|jpg|jpeg|gif|bmp|svg))")
    # Iterate through comments and extract data
    for comment in submission.comments.list():
        if not image_pattern.search(comment.body) and '[removed]' not in comment.body:
            comments.append(comment.body)

    with open("comments.txt", "w", encoding="utf-8") as file:
            comment_count = 0
            for comment in submission.comments.list():
                file.write(comment.body + "\n\n---\n\n")  # Add separators between comments
                comment_count += 1
    print("comments added in the file")

def summarize_chunk(chunk):
    try:
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {   "role" : "system","content": "You are a tech savy reddit user. Your task is to summarize the reddit discussion. Behave like a techology lover. Keep the feel of the content. ANd respond in bullet points ",
                    "role": "user", "content": f"Please summarize the following text:\n\n{chunk}"}
            ],
            max_tokens=150,  # Adjust the token limit as needed
            temperature=0.5,
        )

        summary = response['choices'][0]['message']['content'].strip()
        return summary

    except Exception as e:
        print(f"An error occurred while summarizing a chunk: {e}")
        return None

def summarize_document(document_text, chunk_size=3000):
    # Split the document into chunks based on the specified chunk size
    wrapped_text = textwrap.fill(document_text, width=chunk_size)
    chunks = wrapped_text.split('\n')
    
    # Summarize each chunk
    summaries = []
    for chunk in chunks:
        summary = summarize_chunk(chunk)
        if summary:
            summaries.append(summary)
    
    # Combine summaries and summarize again
    combined_summary = ' '.join(summaries)
    final_summary = summarize_chunk(combined_summary)
    
    return final_summary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search-reddit', methods=['GET'])
def search_reddit_endpoint():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is missing'}), 400

    results = search_reddit(query)
    return jsonify({'results': results})


def summarize_reddit(url):
    try:
        # Scrape Reddit post content using BeautifulSoup
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        page = requests.get(url, headers=headers)
        
        if page.status_code != 200:
            return "Error fetching the Reddit post"

        scrape_reddit_comments(url)
        document_text = read_file('comments.txt')
        final_summary = summarize_document(document_text)
        return final_summary
        
    except Exception as e:
        print(f"Error while summarizing: {e}")
        return "Error summarizing content."
    
@app.route('/summarize-reddit', methods=['GET'])
def summarize_reddit_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is missing'}), 400

    summary = summarize_reddit(url)
    return jsonify({'summary': summary})
    
if __name__ == '__main__':
   app.run()
