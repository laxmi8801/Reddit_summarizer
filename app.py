from flask import Flask, request, jsonify,url_for,render_template
import praw
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI 
from langchain.chains import RetrievalQA
import re

api_key  = 'sk-****************************************'

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
    
@app.route('/summarize-reddit', methods=['GET'])
def summarize_reddit_endpoint():
    url = request.args.get('url')
    scrape_reddit_comments(url)
    text = read_file('comments.txt')
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=50,
            length_function=len
            )
    chunks = text_splitter.split_text(text=text)
    print("chunks created")
    embeddings =OpenAIEmbeddings(api_key=api_key,model="text-embedding-3-small")
    print("embeddings created")
    VectorStore = FAISS.from_texts(chunks, embeddings)
    llm = ChatOpenAI(api_key=api_key,model_name='gpt-4o-mini')
    print("llm initialized")
    query = "summarize the give document"
    
    qa_chain = RetrievalQA.from_chain_type(
            llm=llm ,
            chain_type="stuff", 
            retriever=VectorStore.as_retriever()
    )
    print("qa chain ")
    summary = qa_chain.run({"query": f"You are a tech savy reddit user. Your task is to summarize the reddit discussion. Behave like a techology lover. Keep the feel of the content. ANd respond in bullet points. Question: {query}"})
    if isinstance(summary, dict):
        answer = summary.get('result', 'No result found')  # Ensure to extract the result
    else:
        answer = str(summary)  # Convert to string if it's not a dictionary
        
    return jsonify({'summary': answer})
if __name__ == '__main__':
   app.run()
