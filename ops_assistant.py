from flask import Flask, render_template, request, jsonify, send_file
from huggingface_hub import InferenceClient
import os
import markdown
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('HUGGINGFACE_TOKEN')

if not API_KEY:
    raise ValueError("Please set HUGGINGFACE_TOKEN in .env file")

client = InferenceClient(token=API_KEY)

# Load all knowledge base markdown files
def load_knowledge_base():
    kb_path = "knowledge_base"
    knowledge = {}
    
    for filename in os.listdir(kb_path):
        if filename.endswith(".md"):
            filepath = os.path.join(kb_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                knowledge[filename] = content
    
    return knowledge

knowledge_base = load_knowledge_base()

# Web search function
def web_search(query):
    """Simple web search using DuckDuckGo"""
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for result in soup.find_all('div', class_='result')[:3]:
                title_tag = result.find('a', class_='result__a')
                snippet_tag = result.find('a', class_='result__snippet')
                
                if title_tag and snippet_tag:
                    results.append({
                        'title': title_tag.get_text(),
                        'snippet': snippet_tag.get_text()
                    })
            
            if results:
                search_summary = "Web search results:\n\n"
                for i, r in enumerate(results, 1):
                    search_summary += f"{i}. {r['title']}\n{r['snippet']}\n\n"
                return search_summary
        
        return None
    except:
        return None

# Create context from knowledge base
def create_context():
    context = "You are a CSM Operations expert assistant. Use the following documentation to answer questions:\n\n"
    for filename, content in knowledge_base.items():
        context += f"=== {filename} ===\n{content}\n\n"
    return context

SYSTEM_PROMPT = create_context() + """
Instructions:
- First, try to answer based on the documentation provided above
- If the answer is not in the documentation, indicate you'll search the web
- Be specific and cite the relevant document when answering from documentation
- For web search results, summarize the key findings
- For troubleshooting questions, provide step-by-step guidance
- Include SLA information when relevant
- Be concise but thorough
"""

messages = []
last_response = ""

@app.route('/')
def home():
    docs = list(knowledge_base.keys())
    return render_template('ops_assistant.html', documents=docs)

@app.route('/chat', methods=['POST'])
def chat():
    global last_response
    user_input = request.json['message']
    
    if len(messages) == 0:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    
    # Check if question might need web search
    search_keywords = ['latest', 'current', 'new', 'recent', 'update', 'news']
    needs_search = any(keyword in user_input.lower() for keyword in search_keywords)
    
    # Try knowledge base first
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct",
        messages=messages,
        max_tokens=1000
    )
    
    bot_reply = response.choices[0].message.content
    
    # If answer indicates "not in knowledge base" or needs search, do web search
    if "don't have information" in bot_reply.lower() or "not in my knowledge" in bot_reply.lower() or needs_search:
        search_results = web_search(user_input)
        if search_results:
            # Add search results to context and re-query
            messages.append({"role": "assistant", "content": bot_reply})
            messages.append({"role": "user", "content": f"Here are web search results:\n{search_results}\n\nPlease answer the original question using this information."})
            
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.2-3B-Instruct",
                messages=messages,
                max_tokens=1000
            )
            
            bot_reply = "🌐 [Searched the web]\n\n" + response.choices[0].message.content
    
    messages.append({"role": "assistant", "content": bot_reply})
    last_response = bot_reply
    
    return jsonify({'response': bot_reply})

@app.route('/export_report', methods=['POST'])
def export_report():
    """Export the last response as a PDF troubleshooting guide"""
    global last_response
    
    if not last_response:
        return jsonify({'error': 'No response to export'}), 400
    
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#1e3c72',
        spaceAfter=12
    )
    
    # Title
    title = Paragraph("CSM Ops Troubleshooting Guide", title_style)
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # Timestamp
    timestamp = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    story.append(timestamp)
    story.append(Spacer(1, 0.3*inch))
    
    # Content
    content_lines = last_response.split('\n')
    for line in content_lines:
        if line.strip():
            p = Paragraph(line.replace('<', '&lt;').replace('>', '&gt;'), styles['Normal'])
            story.append(p)
            story.append(Spacer(1, 0.1*inch))
    
    doc.build(story)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'troubleshooting_guide_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )

@app.route('/view_doc/<filename>')
def view_doc(filename):
    if filename in knowledge_base:
        html_content = markdown.markdown(knowledge_base[filename])
        return jsonify({'content': html_content})
    return jsonify({'error': 'Document not found'}), 404

if __name__ == '__main__':
    print(f"\nLoaded {len(knowledge_base)} knowledge base documents:")
    for doc in knowledge_base.keys():
        print(f"  - {doc}")
    print("\n✅ Web search enabled (DuckDuckGo)")
    print("✅ PDF export enabled")
    print("\nStarting CSM Ops Assistant...\n")
    app.run(debug=True)