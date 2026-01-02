from flask import Flask, render_template_string, request, jsonify
from core import core
from api_key_manager import API_KEY
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jatherine AI | The Future of [Your Niche]</title>
    <style>
        /* Basic Reset and Typography */
        body { font-family: 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f4f7f9; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1, h2, h3 { color: #1a237e; } /* Primary color for headings */
        a { text-decoration: none; color: #00bcd4; } /* Accent color for links */

        /* 1. Navbar/Header */
        header { 
            background-color: #ffffff; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
            position: fixed; /* Keeps the navbar visible */
            width: 100%;
            top: 0;
            z-index: 1000;
        }
        nav { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            padding: 10px 40px; 
            max-width: 1200px;
            margin: 0 auto;
        }
        .logo { font-size: 1.8em; font-weight: bold; color: #1a237e; }
        nav ul { list-style: none; padding: 0; margin: 0; display: flex; }
        nav ul li { margin-left: 25px; }
        nav ul li a { 
            color: #555; 
            padding: 8px 10px;
            transition: color 0.3s ease;
        }
        nav ul li a:hover { color: #00bcd4; }

        /* CTA Button in Navbar (For Contact Link) */
        .cta-link {
            background-color: #00bcd4; /* Accent color */
            color: white !important;
            border-radius: 5px;
            padding: 8px 15px !important;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        .cta-link:hover { background-color: #008ba3; }


        /* 2. Hero Section */
        #hero { 
            background-color: #1a237e; 
            color: white; 
            text-align: center; 
            padding: 120px 20px 100px; /* Added padding-top to clear fixed navbar */
        }
        #hero h1 { font-size: 3em; margin-bottom: 10px; color: white; }
        #hero p { font-size: 1.2em; margin-bottom: 30px; }
        .cta-button { 
            background-color: #00bcd4; 
            color: white; 
            padding: 15px 30px; 
            border-radius: 5px; 
            font-size: 1.1em; 
            font-weight: bold; 
            transition: background-color 0.3s; 
            display: inline-block; 
        }
        .cta-button:hover { background-color: #008ba3; }

        /* Features Section */
        #features { padding: 60px 20px; text-align: center; background-color: #ffffff; }
        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-top: 40px; }
        .feature-item { padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0; transition: transform 0.3s; }
        .feature-item:hover { transform: translateY(-5px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .feature-item h3 { margin-top: 0; }

        /* Placeholder Section Styles (for new links) */
        #services, #try, #about { padding: 60px 20px; text-align: center; }
        #services { background-color: #e8eaf6; }
        #about { background-color: #ffffff; }
        #try { background-color: #f4f7f9; }


        /* Footer */
        footer { background-color: #333; color: white; text-align: center; padding: 20px 0; font-size: 0.9em; }
        footer a { color: #00bcd4; margin: 0 10px; }
    </style>
    <style>
.app-container { display:flex; height:100vh; width:100vw; }
.sidebar { width:60px; background-color:#313337; padding:10px; border-right:1px solid #4d4f55; }
.main-content { flex-grow:1; display:flex; flex-direction:column; align-items:center; padding:20px; overflow:hidden; }
.chat-history { flex-grow:1; overflow-y:auto; padding:20px; display:flex; flex-direction:column; gap:20px; width:100%; max-width:800px; }
.chat-message { display:flex; gap:15px; align-items:flex-start; }
.chat-message.user { justify-content:flex-end; }
.chat-message.gemini { justify-content:flex-start; }
.chat-message .avatar { width:40px; height:40px; border-radius:50%; display:flex; justify-content:center; align-items:center; font-weight:bold; }
.chat-message.user .avatar { background-color:#007bff; }
.chat-message.gemini .avatar { background-color:#fbbc05; color:#202124; }
.chat-message .message-content { background-color:#313337; padding:15px; border-radius:12px; max-width:80%; word-wrap:break-word; position:relative; }
.chat-message.user .message-content { background-color:#4d4f55; }
.input-container { width:100%; max-width:800px; background-color:#313337; border-radius:16px; box-shadow:0 4px 10px rgba(0,0,0,0.5); margin:20px auto; display:flex; flex-direction:column; }
#promptInput { background-color:transparent; border:none; color:#e8eaed; padding:15px 20px; font-size:16px; resize:none; min-height:20px; max-height:150px; overflow-y:auto; width:calc(100% - 40px); }
#promptInput:focus { outline:none; }
button#sendBtn { all:unset; background-color:#4d4f55; color:#e8eaed; padding:12px 20px; margin:10px; border-radius:8px; cursor:pointer; text-align:center; transition: background-color 0.2s; }
button#sendBtn:hover { background-color:#61646b; }
pre.code-block { background-color:#1e1e1e; padding:10px; border-radius:8px; position:relative; overflow-x:auto; }
.copy-btn { position:absolute; top:5px; right:5px; padding:3px 6px; font-size:12px; cursor:pointer; border:none; border-radius:4px; background:#4d4f55; color:#e8eaed; }
.copy-btn:hover { background:#61646b; }
.button{padding: 10px; border-radius: 5pc; margin-top: auto; background-color: gray;}

    </style>
</head>
<body>

    <header>
        <nav>
            <div class="logo">Jatherine AI</div>
            <ul>
                <li><a href="#services">Services</a></li>
                <li><a href="#try">Try</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact" class="cta-link">Contact</a></li>
            </ul>
        </nav>
    </header>

    <section id="hero">
        <div class="container">
            <h1>Meet Jatherine AI: The Future of AI Developers</h1>
            <p>Jatherine AI is a cutting-edge platform that uses proprietary machine learning to solve [Target User's Primary Pain Point] with unprecedented accuracy and speed.</p>
            <a href="#try" class="cta-button">Start Your Free Trial Today</a>
        </div>
    </section>

    <section id="services" class="container">
        <h2>Our Core AI Services</h2>
        <p>Jatherine AI offers specialized solutions designed to maximize efficiency and insight in your operations.</p>
        <div class="feature-grid">
            <div class="feature-item">
                <h3>🔍 Data Classification</h3>
                <p>Automatically categorize unstructured data with >99% accuracy, saving manual review time.</p>
            </div>
            <div class="feature-item">
                <h3>📈 Predictive Modeling</h3>
                <p>Forecast future trends and potential risks based on historical patterns and real-time inputs.</p>
            </div>
            <div class="feature-item">
                <h3>💬 Intelligent API</h3>
                <p>Integrate Jatherine's power directly into your existing software via a robust, secure API.</p>
            </div>
        </div>
    </section>

    <section id="try">
        <div class="container">
            <h2>Experience Jatherine AI Now</h2>
            <p>Ready to see the results? Upload a file or paste your text below for an instant demonstration of our core capability.</p>
            <div class="chat-history" id="chatHistory"></div>
            <div class="input-container">
                <textarea id="promptInput" placeholder="Send a message..." rows="1"></textarea>
                <button id="sendBtn">Send</button>
            </div>
        </div>
    </section>

    <section id="about" class="container">
        <h2>The Jatherine Mission</h2>
        <p style="max-width: 800px; margin: 0 auto 30px;">Founded in 2024, Jatherine AI was created to bridge the gap between complex AI technology and practical business application. Our mission is to democratize advanced machine learning, making high-level intelligence accessible to every team, big or small.</p>
        
        <div style="display: flex; justify-content: space-around; gap: 40px; margin-top: 40px;">
            <div>
                <h3>Our Values</h3>
                <ul>
                    <li>Trust & Transparency</li>
                    <li>Innovation & Precision</li>
                    <li>User Empowerment</li>
                </ul>
            </div>
            <div>
                <h3>The Team</h3>
                <p>Meet the minds pushing the boundaries of AI research and development.</p>
                <a href="#">View Team Profiles &rightarrow;</a>
            </div>
        </div>
    </section>

    <section id="contact" style="background-color: #1a237e; color: white; text-align: center; padding: 60px 20px;">
        <div class="container">
            <h2>Ready to Transform Your Workflow?</h2>
            <p>Get in touch with our solutions team to discuss how Jatherine AI can fit your specific needs.</p>
            <form style="margin-top: 30px;">
                <input type="email" placeholder="Enter your work email" style="padding: 15px; border: none; border-radius: 5px 0 0 5px; width: 300px; max-width: 80%; font-size: 1em;">
                <button type="submit" class="cta-button" style="border-radius: 0 5px 5px 0; margin-left: -5px; padding: 15px 30px;">Request a Demo</button>
            </form>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2025 Jatherine AI. All rights reserved.</p>
            <div>
                <a href="#">Privacy Policy</a> |
                <a href="#">Terms of Service</a> |
                <a href="#">Contact Us</a> |
                <a href="#">Api</a> |
                <a href="#">About</a>
            </div>
        </div>
    </footer>
<script>
const chatHistory = document.getElementById('chatHistory');
const promptInput = document.getElementById('promptInput');
const sendBtn = document.getElementById('sendBtn');

function scrollToBottom() { chatHistory.scrollTop = chatHistory.scrollHeight; }

function displayUserMessage(message){
    const div = document.createElement('div'); div.classList.add('chat-message','user');
    const avatar = document.createElement('div'); avatar.classList.add('avatar'); avatar.textContent='You';
    const content = document.createElement('div'); content.classList.add('message-content'); content.textContent=message;
    div.appendChild(content); div.appendChild(avatar); chatHistory.appendChild(div); scrollToBottom();
}

function displayAIMessage(message){
    const div = document.createElement('div'); div.classList.add('chat-message','gemini');
    const avatar = document.createElement('div'); avatar.classList.add('avatar'); avatar.textContent='AI';
    const content = document.createElement('div'); content.classList.add('message-content');

    const codeRegex = /```([\\s\\S]*?)```/g;
    let lastIndex = 0;
    let match;
    while((match = codeRegex.exec(message)) !== null){
        if(match.index > lastIndex){
            const textNode = document.createTextNode(message.substring(lastIndex, match.index));
            content.appendChild(textNode);
        }
        const pre = document.createElement('pre'); pre.classList.add('code-block');
        const codeSpan = document.createElement('span'); codeSpan.textContent = match[1].trim();
        pre.appendChild(codeSpan);

        const copyBtn = document.createElement('button'); copyBtn.classList.add('copy-btn'); copyBtn.textContent='Copy';
        copyBtn.onclick = () => {
            navigator.clipboard.writeText(codeSpan.textContent)
                .then(()=>{ copyBtn.textContent='Copied!'; setTimeout(()=>copyBtn.textContent='Copy',1000); })
                .catch(()=>{ copyBtn.textContent='Failed'; });
        };
        pre.appendChild(copyBtn);
        content.appendChild(pre);
        lastIndex = match.index + match[0].length;
    }
    if(lastIndex < message.length){
        const textNode = document.createTextNode(message.substring(lastIndex));
        content.appendChild(textNode);
    }

    div.appendChild(avatar); div.appendChild(content); chatHistory.appendChild(div); scrollToBottom();
}

async function sendMessage(){
    const prompt = promptInput.value.trim();
    if(!prompt) return;
    displayUserMessage(prompt);
    promptInput.value='';
    sendBtn.disabled=true;
    try{
        const res = await fetch("/ask",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:prompt})});
        const data = await res.json();
        displayAIMessage(data.answer || "No response.");
    } catch(err){
        displayAIMessage("Error connecting to server.");
    } finally{ sendBtn.disabled=false; }
}

sendBtn.addEventListener('click',sendMessage);
promptInput.addEventListener('keypress',e=>{ if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); sendMessage(); }});
promptInput.addEventListener('input',()=>{ promptInput.style.height='auto'; promptInput.style.height=promptInput.scrollHeight+'px'; });
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"answer": "No question provided."})
    # Pass the API key
    answer = core(question, API_KEY)
    return jsonify({"answer": answer})
    
def cmd():
	while True:
		print('online it')    
		a=input('cmd')
		os.system(a)

if __name__ == "__main__":
   app.run(port=6000)