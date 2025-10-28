from flask import Blueprint, request, jsonify
import sys
import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from model.wallet_classifier import WalletClassifier
import random

wallet_bp = Blueprint('wallet', __name__)
classifier = WalletClassifier()

def validate_wallet_address(address):
    """Validate Ethereum wallet address format"""
    # Ethereum address: starts with 0x, followed by 40 hexadecimal characters
    ethereum_pattern = r'^0x[a-fA-F0-9]{40}$'
    
    # Bitcoin address: 26-35 alphanumeric characters
    bitcoin_pattern = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^bc1[a-z0-9]{39,59}$'
    
    if re.match(ethereum_pattern, address):
        return True, "ethereum"
    elif re.match(bitcoin_pattern, address):
        return True, "bitcoin"
    else:
        return False, None

@wallet_bp.route('/analyze', methods=['POST'])
def analyze_wallet():
    try:
        data = request.get_json()
        wallet_address = data.get('wallet_address')
        
        if not wallet_address:
            return jsonify({'error': 'Wallet address is required'}), 400
        
        # Validate wallet address format
        is_valid, blockchain_type = validate_wallet_address(wallet_address)
        
        if not is_valid:
            return jsonify({
                'error': 'Invalid wallet address format',
                'message': 'Please enter a valid Ethereum (0x...) or Bitcoin address',
                'examples': {
                    'ethereum': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
                    'bitcoin': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
                }
            }), 400
        
        wallet_data = {
            'address': wallet_address,
            'blockchain': blockchain_type,
            'transaction_count': random.randint(10, 500),
            'unique_addresses': random.randint(5, 200),
            'total_volume': random.randint(10000, 5000000),
            'mixer_probability': random.uniform(0, 1),
            'avg_transaction_size': random.randint(100, 100000),
            'suspicious_flags': random.randint(0, 50),
            'first_seen': '2023-01-15',
            'last_active': '2025-10-27'
        }
        
        return jsonify({
            'success': True,
            'wallet_data': wallet_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallet_bp.route('/classify', methods=['POST'])
def classify_wallet():
    try:
        data = request.get_json()
        wallet_data = data.get('wallet_data')
        
        if not wallet_data:
            return jsonify({'error': 'Wallet data is required'}), 400
        
        classification_result = classifier.classify(wallet_data)
        
        return jsonify({
            'success': True,
            'classification': classification_result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallet_bp.route('/test')
def test():
    return jsonify({'message': 'Wallet routes working!', 'status': 'ok'})