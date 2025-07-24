import os
from flask import Flask, render_template, flash, redirect, url_for, request
import requests
from dotenv import load_dotenv
from datetime import datetime
import base64
import frontmatter
import markdown

load_dotenv()

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.urandom(24)  # For flash messages
GITHUB_TOKEN = os.getenv('GHTOKEN')
REPO_OWNER = os.getenv('REPO_OWNER')
REPO_NAME = os.getenv('REPO_NAME')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/blog')
def blog():
    posts = []
    contents_path = 'api/contents'
    if os.path.exists(contents_path):
        for filename in os.listdir(contents_path):
            if filename.endswith('.md'):
                filepath = os.path.join(contents_path, filename)
                with open(filepath, 'r') as f:
                    post = frontmatter.load(f)
                    posts.append({
                        'id': filename.replace('.md', ''),
                        'title': post.get('title', 'No Title'),
                        'date': post.get('date', 'No Date')
                    })
    return render_template('blog.html', posts=posts)

@app.route('/blog/<post_name>')
def blog_post(post_name):
    filepath = f'api/contents/{post_name}.md'
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            post_data = frontmatter.load(f)
            html_content = markdown.markdown(post_data.content)
            post = {
                'title': post_data.get('title', 'No Title'),
                'date': post_data.get('date', 'No Date'),
                'content': html_content
            }
            return render_template('post.html', post=post)
    return 'Post not found', 404

@app.route('/newpost')
def new_post():
    return render_template('new_post.html')

@app.route('/create_post', methods=['POST'])
def create_post():
    title = request.form.get('title')
    content = request.form.get('content')

    if not title or not content:
        flash('Title and content are required.', 'error')
        return redirect(url_for('new_post'))

    # Create frontmatter
    frontmatter = f"""---
title: {title}
date: {datetime.utcnow().isoformat()}
---
"""
    
    # Full content with frontmatter
    full_content = f"{frontmatter}\n{content}"
    
    # Create a filename from the current date and time
    now = datetime.utcnow()
    filename = f"api/contents/{now.strftime('%Y-%m-%d-%H-%M-%S')}.md"
    
    if not GITHUB_TOKEN:
        flash('GitHub token not found. Please set the GHTOKEN environment variable.', 'error')
        return redirect(url_for('new_post'))

    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filename}'
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {GITHUB_TOKEN}',
    }
    
    encoded_content = base64.b64encode(full_content.encode('utf-8')).decode('utf-8')
    
    data = {
        'message': f'Create {filename}',
        'content': encoded_content,
        'branch': 'main'
    }

    try:
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 201:
            flash(f'Successfully created file {filename}!', 'success')
            # Optionally, trigger another workflow here if needed
        else:
            flash(f'Error creating file: Received status code {response.status_code} - {response.text}', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('new_post'))


@app.route('/about')
def about():
    return 'About'
