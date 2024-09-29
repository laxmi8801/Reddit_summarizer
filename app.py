from flask import Flask, request, redirect,url_for,render_template
import praw
import os
import openai
import textwrap

openai.api_key  = 'sk-**********'

app = Flask(__name__)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

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

    # Iterate through comments and extract data
    for comment in submission.comments.list():
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
                {"role": "user", "content": f"Please summarize the following text:\n\n{chunk}"}
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



@app.route('/reddit_summarizer', methods=['GET', 'POST'])
def summarize():
   
    url = request.form['url']
    scrape_reddit_comments(url)
    document_text = read_file('comments.txt')
    final_summary = summarize_document(document_text)
    print(final_summary)
    return render_template('index.html', summary=final_summary)
  
if __name__ == '__main__':
   app.run()
