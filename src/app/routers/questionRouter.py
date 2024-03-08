from flask import Flask, request, jsonify
import asyncio

from app.services.contentService import run_qa_session
from app.services.scrapeService import ascrape_playwright
from app.services.audioService import extract_transcript

from flask import Flask, request, jsonify
from flasgger import Swagger
import asyncio


app = Flask(__name__)
swagger = Swagger(app)

@app.route('/save_document', methods=['POST'])
def save_document():
    """
    Save Document
    ---
    parameters:
      - name: link
        in: formData
        type: string
        required: true
        description: Link to the document
      - name: content
        in: formData
        type: string
        required: true
        description: Content of the document
    responses:
      200:
        description: Document saved successfully
    """
    data = request.json
    link = data.get('link')
    content = data.get('content')
    # Save the link and document content into your database
    return jsonify({'message': 'Document saved successfully'})

@app.route('/generate_qa', methods=['POST'])
def generate_qa():
    """
    Generate Questions and Answers
    ---
    parameters:
      - name: content
        in: formData
        type: string
        required: true
        description: Content for generating questions and answers
      - name: num
        in: formData
        type: integer
        description: Number of questions to generate (default is 5)
    responses:
      200:
        description: Questions and Answers generated successfully
    """
    data = request.json
    content = data.get('content')
    num = data.get('num', 5)
    qa_dict, overall_scores = run_qa_session(num, content)
    return jsonify({'qa_data': qa_dict, 'overall_scores': overall_scores})

@app.route('/scrape_and_qa', methods=['POST'])
def scrape_and_qa():
    """
    Scrape Content and Run QA Session
    ---
    parameters:
      - name: url
        in: formData
        type: string
        required: true
        description: URL to scrape content from
      - name: tags
        in: formData
        type: array
        description: Tags for content scraping (optional)
    responses:
      200:
        description: Scrape and QA session completed successfully
    """
    data = request.json
    url = data.get('url')
    tags = data.get('tags', [])
    html_content = asyncio.run(scrape_with_playwright(url, tags))
    return jsonify({'html_content': html_content})

async def scrape_with_playwright(url: str, tags: list):
    html_content = extract_transcript(url)
    num = 5
    qa_dict, overall_scores = run_qa_session(num, html_content)
    return {'qa_data': qa_dict, 'overall_scores': overall_scores}

if __name__ == '__main__':
    app.run(debug=True)

