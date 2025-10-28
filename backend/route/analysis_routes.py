from flask import Blueprint, request, jsonify
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from model.transaction_classifier import TransactionAnalyzer

analysis_bp = Blueprint('analysis', __name__)
analyzer = TransactionAnalyzer()

@analysis_bp.route('/network', methods=['POST'])
def get_network_graph():
    try:
        data = request.get_json()
        wallet_address = data.get('wallet_address')
        depth = data.get('depth', 2)
        
        if not wallet_address:
            return jsonify({'error': 'Wallet address is required'}), 400
        
        network_data = analyzer.build_network_graph(wallet_address, depth)
        
        return jsonify({
            'success': True,
            'network': network_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/timeline', methods=['POST'])
def get_timeline():
    try:
        data = request.get_json()
        wallet_address = data.get('wallet_address')
        
        if not wallet_address:
            return jsonify({'error': 'Wallet address is required'}), 400
        
        timeline_data = analyzer.analyze_timeline(wallet_address)
        
        return jsonify({
            'success': True,
            'timeline': timeline_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/test')
def test():
    return jsonify({'message': 'Analysis routes working!', 'status': 'ok'})