from flask import Flask, jsonify, request, render_template_string
import random
import base64
import re

app = Flask(__name__)

# HTML template for the frontend
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SecretFinder Test App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .section { margin-bottom: 30px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        button { padding: 8px 15px; margin: 5px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; }
        pre { background: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>SecretFinder Test Application</h1>
        <p>Click buttons to generate responses containing different types of secrets</p>
        
        <div class="section">
            <h2>API Keys</h2>
            <button onclick="fetchResponse('/api-keys')">Get API Keys</button>
            <div id="api-keys-result"></div>
        </div>
        
        <div class="section">
            <h2>Authentication Tokens</h2>
            <button onclick="fetchResponse('/tokens')">Get Auth Tokens</button>
            <div id="tokens-result"></div>
        </div>
        
        <div class="section">
            <h2>Database Connections</h2>
            <button onclick="fetchResponse('/db-connections')">Get DB Connections</button>
            <div id="db-connections-result"></div>
        </div>
        
        <div class="section">
            <h2>Hidden Endpoints</h2>
            <button onclick="fetchResponse('/hidden/.env')">Get .env File</button>
            <button onclick="fetchResponse('/hidden/config.json')">Get Config</button>
            <div id="hidden-result"></div>
        </div>
        
        <div class="section">
            <h2>Encoded Secrets</h2>
            <button onclick="fetchResponse('/encoded')">Get Encoded Secrets</button>
            <div id="encoded-result"></div>
        </div>
    </div>

    <script>
        async function fetchResponse(endpoint) {
            const resultDiv = document.getElementById(endpoint.substring(1).replace('/', '-') + '-result');
            resultDiv.innerHTML = 'Loading...';
            
            try {
                const response = await fetch(endpoint);
                const data = await response.json();
                resultDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            } catch (error) {
                resultDiv.innerHTML = `Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>
"""

# Sample secrets data
SECRETS = {
    "google_api_key": "AIza" + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=35)),
    "aws_access_key": "AKIA" + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=16)),
    "aws_secret_key": "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=", k=40)),
    "github_token": "ghp_" + "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=36)),
    "slack_token": "xoxb-" + "".join(random.choices("0123456789", k=12)) + "-" + 
                   "".join(random.choices("0123456789", k=12)) + "-" + 
                   "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=24)),
    "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." + 
                 "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ." + 
                 "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
    "firebase_key": "AAAA" + "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_", k=7)) + 
                   ":" + "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_", k=140)),
    "stripe_key": "sk_live_" + "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=24)),
    "database_url": f"postgres://user:{''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12))}@localhost:5432/dbname",
    "private_key": "-----BEGIN RSA PRIVATE KEY-----\n" + 
                  "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=\n", k=500)) + 
                  "\n-----END RSA PRIVATE KEY-----"
}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api-keys')
def api_keys():
    return jsonify({
        "google_api_key": SECRETS["google_api_key"],
        "aws_keys": {
            "access_key": SECRETS["aws_access_key"],
            "secret_key": SECRETS["aws_secret_key"]
        },
        "github_token": SECRETS["github_token"],
        "message": "This response contains various API keys that should be detected"
    })

@app.route('/tokens')
def tokens():
    return jsonify({
        "slack_token": SECRETS["slack_token"],
        "jwt_token": SECRETS["jwt_token"],
        "firebase_key": SECRETS["firebase_key"],
        "stripe_key": SECRETS["stripe_key"],
        "message": "This response contains authentication tokens"
    })

@app.route('/db-connections')
def db_connections():
    return jsonify({
        "database_url": SECRETS["database_url"],
        "message": "This response contains database connection strings"
    })

@app.route('/hidden/.env')
def dotenv():
    env_content = f"""
    # Database configuration
    DB_HOST=localhost
    DB_USER=admin
    DB_PASS={''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))}
    DB_NAME=production
    
    # API keys
    GOOGLE_API_KEY={SECRETS["google_api_key"]}
    AWS_ACCESS_KEY={SECRETS["aws_access_key"]}
    AWS_SECRET_KEY={SECRETS["aws_secret_key"]}
    
    # Encryption
    SECRET_KEY={''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32))}
    """
    return jsonify({
        "content": env_content,
        "message": "This simulates a .env file disclosure"
    })

@app.route('/hidden/config.json')
def config_json():
    return jsonify({
        "database": {
            "host": "localhost",
            "port": 5432,
            "username": "admin",
            "password": "".join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16)),
            "name": "production"
        },
        "api_keys": {
            "google": SECRETS["google_api_key"],
            "stripe": SECRETS["stripe_key"]
        },
        "jwt_secret": "".join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32))
    })

@app.route('/encoded')
def encoded_secrets():
    # Create some base64 encoded secrets
    encoded_aws = base64.b64encode(f"AWS_ACCESS={SECRETS['aws_access_key']};AWS_SECRET={SECRETS['aws_secret_key']}".encode()).decode()
    encoded_db = base64.b64encode(SECRETS['database_url'].encode()).decode()
    
    return jsonify({
        "encoded_aws": encoded_aws,
        "encoded_db": encoded_db,
        "private_key": SECRETS["private_key"],
        "message": "This response contains encoded secrets and a private key"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
