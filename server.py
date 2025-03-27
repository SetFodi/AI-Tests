from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/run-model', methods=['POST'])
def run_model():
    # (same as above)
    model_name = request.json.get('model_name', '')
    model_map = {
        'claude haiku': 'claudehaiku.py',
        'deepseek r1': 'deepSeekR1_Llama.py',
        'claude (reasoning model)': 'claudethink.py',
        'gemini 2.5 pro': 'gemini2.5.py',
        'grok thinking model': 'grokthink.py',
        'o3 mini high': 'o3minihigh.py',
        'claude opus': 'claudeopus.py',
        'deepseek v3': 'DeepSeekv3.py',
        'grok 3': 'grok.py',
        'chatgpt default free model': 'chatgpt4omini.py',
        'gemini 2.0 flash': 'geminiflash.py'
    }
    
    python_file = None
    model_name_lower = model_name.lower()
    for key, value in model_map.items():
        if key in model_name_lower:
            python_file = value
            break
    
    if not python_file:
        if 'claude' in model_name_lower:
            python_file = 'claudehaiku.py'
        elif 'gemini' in model_name_lower:
            python_file = 'gemini2.5.py'
        elif 'grok' in model_name_lower:
            python_file = 'grok.py'
        elif 'deepseek' in model_name_lower:
            python_file = 'deepSeekR1_Llama.py'
        elif 'gpt' in model_name_lower or 'chatgpt' in model_name_lower:
            python_file = 'chatgpt4mini.py'
        elif 'o3' in model_name_lower:
            python_file = 'o3minihigh.py'
        else:
            return jsonify({'status': 'error', 'message': f'No Python file found for model: {model_name}'})
    
    try:
        subprocess.Popen(['python3', python_file])
        return jsonify({
            'status': 'success', 
            'message': f'Running {python_file} for model {model_name}'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
