import requests
import random
from datetime import datetime, timedelta

class BlockchainAPI:
    def __init__(self):
        self.base_urls = {
            'bitcoin': 'https://blockchain.info',
            'ethereum': 'https://api.etherscan.io/api'
        }
    
    def get_wallet_info(self, address, blockchain='ethereum'):
        return {
            'address': address,
            'balance': random.randint(1000, 1000000),
            'transaction_count': random.randint(10, 500),
            'blockchain': blockchain,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_transactions(self, address, limit=10):
        transactions = []
        for i in range(limit):
            transactions.append({
                'hash': f"0x{random.randint(10**15, 10**16):016x}",
                'from': address if random.random() > 0.5 else f"0x{random.randint(10**15, 10**16):016x}",
                'to': f"0x{random.randint(10**15, 10**16):016x}" if random.random() > 0.5 else address,
                'value': random.randint(100, 50000),
                'timestamp': (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d %H:%M:%S')
            })
        return transactions