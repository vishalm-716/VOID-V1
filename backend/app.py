from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from route.wallet_routes import wallet_bp
from route.analysis_routes import analysis_bp

app = Flask(__name__)
CORS(app)

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
            'classify': '/api/wallet/classify',
            'timeline': '/api/analysis/timeline'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

if __name__ == '__main__':
    print("Starting VOIDV1 Backend Server...")
    print("Server running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
