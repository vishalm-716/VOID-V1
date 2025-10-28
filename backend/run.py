import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
os.chdir(current_dir)

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# CORS configuration for production
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

from route.wallet_routes import wallet_bp
from route.analysis_routes import analysis_bp

app.register_blueprint(wallet_bp, url_prefix='/api/wallet')
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')

@app.route('/')
def home():
    return jsonify({
        'message': 'VOIDV1 Crypto Transaction Unmasking System API',
        'version': '1.0',
        'status': 'running',
        'endpoints': {
            'wallet_analysis': '/api/wallet/analyze',
            'network_graph': '/api/analysis/network',
            'classify': '/api/wallet/classify'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
