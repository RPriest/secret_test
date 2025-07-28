from flask import Flask, jsonify, request, render_template_string
import random
import base64
import re
import json

app = Flask(__name__)

# HTML template for the frontend
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SecretFinder Pro Test App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .section { margin-bottom: 30px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        button { padding: 8px 15px; margin: 5px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; }
        pre { background: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto; }
        .category { display: flex; flex-wrap: wrap; gap: 10px; }
        .test-case { flex: 1 1 300px; }
        h3 { margin-top: 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>SecretFinder Pro Test Application</h1>
        <p>Click buttons to test all detection capabilities of SecretFinder Pro</p>
        
        <div class="section">
            <h2>API Keys</h2>
            <div class="category">
                <div class="test-case">
                    <h3>Google API Keys</h3>
                    <button onclick="fetchResponse('/google-keys')">Test Google Keys</button>
                    <div id="google-keys-result"></div>
                </div>
                <div class="test-case">
                    <h3>AWS Keys</h3>
                    <button onclick="fetchResponse('/aws-keys')">Test AWS Keys</button>
                    <div id="aws-keys-result"></div>
                </div>
                <div class="test-case">
                    <h3>GitHub Tokens</h3>
                    <button onclick="fetchResponse('/github-tokens')">Test GitHub</button>
                    <div id="github-tokens-result"></div>
                </div>
                <div class="test-case">
                    <h3>Stripe Keys</h3>
                    <button onclick="fetchResponse('/stripe-keys')">Test Stripe</button>
                    <div id="stripe-keys-result"></div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>Authentication Tokens</h2>
            <div class="category">
                <div class="test-case">
                    <h3>JWT Tokens</h3>
                    <button onclick="fetchResponse('/jwt-tokens')">Test JWTs</button>
                    <div id="jwt-tokens-result"></div>
                </div>
                <div class="test-case">
                    <h3>OAuth Tokens</h3>
                    <button onclick="fetchResponse('/oauth-tokens')">Test OAuth</button>
                    <div id="oauth-tokens-result"></div>
                </div>
                <div class="test-case">
                    <h3>Slack Tokens</h3>
                    <button onclick="fetchResponse('/slack-tokens')">Test Slack</button>
                    <div id="slack-tokens-result"></div>
                </div>
                <div class="test-case">
                    <h3>Firebase Keys</h3>
                    <button onclick="fetchResponse('/firebase-keys')">Test Firebase</button>
                    <div id="firebase-keys-result"></div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>Database Connections</h2>
            <div class="category">
                <div class="test-case">
                    <h3>PostgreSQL</h3>
                    <button onclick="fetchResponse('/postgres-conn')">Test PostgreSQL</button>
                    <div id="postgres-conn-result"></div>
                </div>
                <div class="test-case">
                    <h3>MySQL</h3>
                    <button onclick="fetchResponse('/mysql-conn')">Test MySQL</button>
                    <div id="mysql-conn-result"></div>
                </div>
                <div class="test-case">
                    <h3>MongoDB</h3>
                    <button onclick="fetchResponse('/mongodb-conn')">Test MongoDB</button>
                    <div id="mongodb-conn-result"></div>
                </div>
                <div class="test-case">
                    <h3>Redis</h3>
                    <button onclick="fetchResponse('/redis-conn')">Test Redis</button>
                    <div id="redis-conn-result"></div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>Configuration Files</h2>
            <div class="category">
                <div class="test-case">
                    <h3>.env Files</h3>
                    <button onclick="fetchResponse('/dotenv')">Test .env</button>
                    <div id="dotenv-result"></div>
                </div>
                <div class="test-case">
                    <h3>config.json</h3>
                    <button onclick="fetchResponse('/config-json')">Test config.json</button>
                    <div id="config-json-result"></div>
                </div>
                <div class="test-case">
                    <h3>web.config</h3>
                    <button onclick="fetchResponse('/web-config')">Test web.config</button>
                    <div id="web-config-result"></div>
                </div>
                <div class="test-case">
                    <h3>Dockerfiles</h3>
                    <button onclick="fetchResponse('/dockerfile')">Test Dockerfile</button>
                    <div id="dockerfile-result"></div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>Encoded Secrets</h2>
            <div class="category">
                <div class="test-case">
                    <h3>Base64 Encoded</h3>
                    <button onclick="fetchResponse('/base64-encoded')">Test Base64</button>
                    <div id="base64-encoded-result"></div>
                </div>
                <div class="test-case">
                    <h3>Hex Encoded</h3>
                    <button onclick="fetchResponse('/hex-encoded')">Test Hex</button>
                    <div id="hex-encoded-result"></div>
                </div>
                <div class="test-case">
                    <h3>URL Encoded</h3>
                    <button onclick="fetchResponse('/url-encoded')">Test URL Encoded</button>
                    <div id="url-encoded-result"></div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>Private Keys</h2>
            <div class="category">
                <div class="test-case">
                    <h3>RSA Private Key</h3>
                    <button onclick="fetchResponse('/rsa-key')">Test RSA</button>
                    <div id="rsa-key-result"></div>
                </div>
                <div class="test-case">
                    <h3>SSH Private Key</h3>
                    <button onclick="fetchResponse('/ssh-key')">Test SSH</button>
                    <div id="ssh-key-result"></div>
                </div>
                <div class="test-case">
                    <h3>PGP Private Key</h3>
                    <button onclick="fetchResponse('/pgp-key')">Test PGP</button>
                    <div id="pgp-key-result"></div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>Hidden Endpoints</h2>
            <div class="category">
                <div class="test-case">
                    <h3>Common Secret Paths</h3>
                    <button onclick="fetchResponse('/secret-paths')">Test Secret Paths</button>
                    <div id="secret-paths-result"></div>
                </div>
                <div class="test-case">
                    <h3>Admin Interfaces</h3>
                    <button onclick="fetchResponse('/admin-interfaces')">Test Admin</button>
                    <div id="admin-interfaces-result"></div>
                </div>
                <div class="test-case">
                    <h3>Debug Endpoints</h3>
                    <button onclick="fetchResponse('/debug-endpoints')">Test Debug</button>
                    <div id="debug-endpoints-result"></div>
                </div>
                <div class="test-case">
                    <h3>Backup Files</h3>
                    <button onclick="fetchResponse('/backup-files')">Test Backups</button>
                    <div id="backup-files-result"></div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>JavaScript/CSS Secrets</h2>
            <div class="category">
                <div class="test-case">
                    <h3>JavaScript Files</h3>
                    <button onclick="fetchResponse('/js-secrets')">Test JS</button>
                    <div id="js-secrets-result"></div>
                </div>
                <div class="test-case">
                    <h3>CSS Files</h3>
                    <button onclick="fetchResponse('/css-secrets')">Test CSS</button>
                    <div id="css-secrets-result"></div>
                </div>
                <div class="test-case">
                    <h3>HTML Comments</h3>
                    <button onclick="fetchResponse('/html-comments')">Test Comments</button>
                    <div id="html-comments-result"></div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>Test All Features</h2>
            <button onclick="testAll()">Test All Endpoints</button>
            <div id="all-results"></div>
        </div>
    </div>

    <script>
        const endpoints = [
            '/google-keys', '/aws-keys', '/github-tokens', '/stripe-keys',
            '/jwt-tokens', '/oauth-tokens', '/slack-tokens', '/firebase-keys',
            '/postgres-conn', '/mysql-conn', '/mongodb-conn', '/redis-conn',
            '/dotenv', '/config-json', '/web-config', '/dockerfile',
            '/base64-encoded', '/hex-encoded', '/url-encoded',
            '/rsa-key', '/ssh-key', '/pgp-key',
            '/secret-paths', '/admin-interfaces', '/debug-endpoints', '/backup-files',
            '/js-secrets', '/css-secrets', '/html-comments'
        ];
        
        async function fetchResponse(endpoint) {
            const resultId = endpoint.substring(1).replace(/\//g, '-') + '-result';
            const resultDiv = document.getElementById(resultId);
            resultDiv.innerHTML = 'Loading...';
            
            try {
                const response = await fetch(endpoint);
                const data = await response.json();
                resultDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            } catch (error) {
                resultDiv.innerHTML = `Error: ${error.message}`;
            }
        }
        
        async function testAll() {
            const resultsDiv = document.getElementById('all-results');
            resultsDiv.innerHTML = 'Testing all endpoints...<br><br>';
            
            for (const endpoint of endpoints) {
                try {
                    const response = await fetch(endpoint);
                    const data = await response.json();
                    resultsDiv.innerHTML += `<strong>${endpoint}:</strong><br><pre>${JSON.stringify(data, null, 2)}</pre><br>`;
                } catch (error) {
                    resultsDiv.innerHTML += `<strong>${endpoint}:</strong> Error - ${error.message}<br>`;
                }
            }
        }
    </script>
</body>
</html>
"""

def generate_random_string(length, chars=None):
    if chars is None:
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choices(chars, k=length))

# Generate all test secrets
SECRETS = {
    # API Keys
    "google_api_key": "AIza" + generate_random_string(35, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"),
    "google_oauth_token": "ya29." + generate_random_string(129),
    "aws_access_key": "AKIA" + generate_random_string(16, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"),
    "aws_secret_key": generate_random_string(40, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/="),
    "github_token": "ghp_" + generate_random_string(36),
    "gitlab_token": "glpat-" + generate_random_string(20),
    "stripe_key": "sk_live_" + generate_random_string(24),
    "mailgun_key": "key-" + generate_random_string(32),
    "twilio_key": "SK" + generate_random_string(32),
    
    # Authentication Tokens
    "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." + 
                 "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ." + 
                 generate_random_string(43),
    "slack_token": "xoxb-" + generate_random_string(12, "0123456789") + "-" + 
                   generate_random_string(12, "0123456789") + "-" + 
                   generate_random_string(24),
    "firebase_key": "AAAA" + generate_random_string(7) + ":" + generate_random_string(140),
    "heroku_key": "heroku" + generate_random_string(32).lower(),
    
    # Database Connections
    "postgres_url": f"postgres://user:{generate_random_string(12)}@localhost:5432/dbname",
    "mysql_url": f"mysql://user:{generate_random_string(12)}@localhost:3306/dbname",
    "mongodb_url": f"mongodb://user:{generate_random_string(12)}@localhost:27017/dbname",
    "redis_url": f"redis://:{generate_random_string(12)}@localhost:6379/0",
    
    # Private Keys
    "rsa_key": "-----BEGIN RSA PRIVATE KEY-----\n" + 
               generate_random_string(500, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=\n") + 
               "\n-----END RSA PRIVATE KEY-----",
    "ssh_key": "-----BEGIN OPENSSH PRIVATE KEY-----\n" + 
               generate_random_string(500, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=\n") + 
               "\n-----END OPENSSH PRIVATE KEY-----",
    "pgp_key": "-----BEGIN PGP PRIVATE KEY BLOCK-----\n" + 
               generate_random_string(500, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=\n") + 
               "\n-----END PGP PRIVATE KEY BLOCK-----",
    
    # Config values
    "secret_key": generate_random_string(32),
    "encryption_key": generate_random_string(64),
}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# API Key Endpoints
@app.route('/google-keys')
def google_keys():
    return jsonify({
        "google_api_key": SECRETS["google_api_key"],
        "google_oauth_token": SECRETS["google_oauth_token"],
        "message": "Testing Google API keys and OAuth tokens detection"
    })

@app.route('/aws-keys')
def aws_keys():
    return jsonify({
        "aws_access_key": SECRETS["aws_access_key"],
        "aws_secret_key": SECRETS["aws_secret_key"],
        "message": "Testing AWS keys detection"
    })

@app.route('/github-tokens')
def github_tokens():
    return jsonify({
        "github_token": SECRETS["github_token"],
        "gitlab_token": SECRETS["gitlab_token"],
        "message": "Testing GitHub and GitLab tokens detection"
    })

@app.route('/stripe-keys')
def stripe_keys():
    return jsonify({
        "stripe_key": SECRETS["stripe_key"],
        "message": "Testing Stripe keys detection"
    })

# Authentication Token Endpoints
@app.route('/jwt-tokens')
def jwt_tokens():
    return jsonify({
        "jwt_token": SECRETS["jwt_token"],
        "message": "Testing JWT tokens detection"
    })

@app.route('/oauth-tokens')
def oauth_tokens():
    return jsonify({
        "google_oauth_token": SECRETS["google_oauth_token"],
        "message": "Testing OAuth tokens detection"
    })

@app.route('/slack-tokens')
def slack_tokens():
    return jsonify({
        "slack_token": SECRETS["slack_token"],
        "message": "Testing Slack tokens detection"
    })

@app.route('/firebase-keys')
def firebase_keys():
    return jsonify({
        "firebase_key": SECRETS["firebase_key"],
        "message": "Testing Firebase keys detection"
    })

# Database Connection Endpoints
@app.route('/postgres-conn')
def postgres_conn():
    return jsonify({
        "postgres_url": SECRETS["postgres_url"],
        "message": "Testing PostgreSQL connection strings detection"
    })

@app.route('/mysql-conn')
def mysql_conn():
    return jsonify({
        "mysql_url": SECRETS["mysql_url"],
        "message": "Testing MySQL connection strings detection"
    })

@app.route('/mongodb-conn')
def mongodb_conn():
    return jsonify({
        "mongodb_url": SECRETS["mongodb_url"],
        "message": "Testing MongoDB connection strings detection"
    })

@app.route('/redis-conn')
def redis_conn():
    return jsonify({
        "redis_url": SECRETS["redis_url"],
        "message": "Testing Redis connection strings detection"
    })

# Configuration File Endpoints
@app.route('/dotenv')
def dotenv():
    env_content = f"""
# Database configuration
DB_HOST=localhost
DB_USER=admin
DB_PASS={generate_random_string(16)}
DB_NAME=production

# API keys
GOOGLE_API_KEY={SECRETS["google_api_key"]}
AWS_ACCESS_KEY={SECRETS["aws_access_key"]}
AWS_SECRET_KEY={SECRETS["aws_secret_key"]}

# Encryption
SECRET_KEY={SECRETS["secret_key"]}
ENCRYPTION_KEY={SECRETS["encryption_key"]}
"""
    return jsonify({
        "content": env_content,
        "message": "Testing .env file secrets detection"
    })

@app.route('/config-json')
def config_json():
    return jsonify({
        "database": {
            "host": "localhost",
            "port": 5432,
            "username": "admin",
            "password": generate_random_string(16),
            "name": "production"
        },
        "api_keys": {
            "google": SECRETS["google_api_key"],
            "stripe": SECRETS["stripe_key"],
            "mailgun": SECRETS["mailgun_key"],
            "twilio": SECRETS["twilio_key"]
        },
        "jwt_secret": SECRETS["secret_key"]
    })

@app.route('/web-config')
def web_config():
    config_content = f"""
<configuration>
    <connectionStrings>
        <add name="DefaultConnection" 
             connectionString="Server=localhost;Database=production;User Id=admin;Password={generate_random_string(16)};"
             providerName="System.Data.SqlClient" />
    </connectionStrings>
    <appSettings>
        <add key="GoogleApiKey" value="{SECRETS["google_api_key"]}" />
        <add key="AwsAccessKey" value="{SECRETS["aws_access_key"]}" />
        <add key="AwsSecretKey" value="{SECRETS["aws_secret_key"]}" />
    </appSettings>
</configuration>
"""
    return jsonify({
        "content": config_content,
        "message": "Testing web.config secrets detection"
    })

@app.route('/dockerfile')
def dockerfile():
    docker_content = f"""
FROM python:3.9
ENV DB_PASSWORD={generate_random_string(16)}
ENV SECRET_KEY={SECRETS["secret_key"]}
ENV AWS_ACCESS_KEY_ID={SECRETS["aws_access_key"]}
ENV AWS_SECRET_ACCESS_KEY={SECRETS["aws_secret_key"]}
"""
    return jsonify({
        "content": docker_content,
        "message": "Testing Dockerfile secrets detection"
    })

# Encoded Secret Endpoints
@app.route('/base64-encoded')
def base64_encoded():
    encoded_aws = base64.b64encode(f"AWS_ACCESS={SECRETS['aws_access_key']};AWS_SECRET={SECRETS['aws_secret_key']}".encode()).decode()
    encoded_db = base64.b64encode(SECRETS['postgres_url'].encode()).decode()
    
    return jsonify({
        "encoded_aws": encoded_aws,
        "encoded_db": encoded_db,
        "message": "Testing base64 encoded secrets detection"
    })

@app.route('/hex-encoded')
def hex_encoded():
    hex_aws = f"AWS_ACCESS={SECRETS['aws_access_key']};AWS_SECRET={SECRETS['aws_secret_key']}".encode().hex()
    hex_db = SECRETS['postgres_url'].encode().hex()
    
    return jsonify({
        "hex_aws": hex_aws,
        "hex_db": hex_db,
        "message": "Testing hex encoded secrets detection"
    })

@app.route('/url-encoded')
def url_encoded():
    url_aws = f"AWS_ACCESS={SECRETS['aws_access_key']}&AWS_SECRET={SECRETS['aws_secret_key']}"
    url_db = f"DB_URL={SECRETS['postgres_url']}"
    
    return jsonify({
        "url_aws": url_aws,
        "url_db": url_db,
        "message": "Testing URL encoded secrets detection"
    })

# Private Key Endpoints
@app.route('/rsa-key')
def rsa_key():
    return jsonify({
        "rsa_key": SECRETS["rsa_key"],
        "message": "Testing RSA private key detection"
    })

@app.route('/ssh-key')
def ssh_key():
    return jsonify({
        "ssh_key": SECRETS["ssh_key"],
        "message": "Testing SSH private key detection"
    })

@app.route('/pgp-key')
def pgp_key():
    return jsonify({
        "pgp_key": SECRETS["pgp_key"],
        "message": "Testing PGP private key detection"
    })

# Hidden Endpoint Tests
@app.route('/secret-paths')
def secret_paths():
    return jsonify({
        "paths": [
            "/.env",
            "/config.json",
            "/.git/config",
            "/admin/credentials",
            "/api/keys",
            "/v1/secrets"
        ],
        "message": "Testing secret path detection in responses"
    })

@app.route('/admin-interfaces')
def admin_interfaces():
    return jsonify({
        "interfaces": [
            "/admin",
            "/wp-admin",
            "/manager",
            "/administrator",
            "/console"
        ],
        "message": "Testing admin interface path detection"
    })

@app.route('/debug-endpoints')
def debug_endpoints():
    return jsonify({
        "endpoints": [
            "/debug",
            "/phpinfo",
            "/status",
            "/metrics",
            "/actuator"
        ],
        "message": "Testing debug endpoint detection"
    })

@app.route('/backup-files')
def backup_files():
    return jsonify({
        "files": [
            "/backup.zip",
            "/db.sql",
            "/dump.tar.gz",
            "/www.rar",
            "/config.bak"
        ],
        "message": "Testing backup file detection"
    })

# JavaScript/CSS Secret Tests
@app.route('/js-secrets')
def js_secrets():
    js_content = f"""
// API Keys
const googleApiKey = "{SECRETS["google_api_key"]}";
const awsConfig = {{
    accessKeyId: "{SECRETS["aws_access_key"]}",
    secretAccessKey: "{SECRETS["aws_secret_key"]}"
}};

// Database URL
const dbUrl = "{SECRETS["postgres_url"]}";

// JWT Secret
const jwtSecret = "{SECRETS["secret_key"]}";
"""
    return jsonify({
        "content": js_content,
        "message": "Testing JavaScript secrets detection"
    })

@app.route('/css-secrets')
def css_secrets():
    css_content = f"""
/* Secret API endpoints */
.secret-endpoint {{
    background-image: url('https://api.example.com/v1/token?key={SECRETS["google_api_key"]}');
}}

/* Admin interface */
.admin-panel {{
    content: "{SECRETS["aws_access_key"]}";
}}
"""
    return jsonify({
        "content": css_content,
        "message": "Testing CSS secrets detection"
    })

@app.route('/html-comments')
def html_comments():
    html_content = f"""
<!-- 
    Database credentials:
    Username: admin
    Password: {generate_random_string(12)}
    
    API Key: {SECRETS["google_api_key"]}
-->
"""
    return jsonify({
        "content": html_content,
        "message": "Testing HTML comments secrets detection"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
