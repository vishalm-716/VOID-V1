import requests
from datetime import datetime

class BlockchainAPI:
    def __init__(self):
        # Get free API keys from:
        # Etherscan: https://etherscan.io/apis
        # Blockchain.com: https://www.blockchain.com/api
        self.etherscan_api_key = "YOUR_ETHERSCAN_API_KEY"  # Register at etherscan.io
        self.base_urls = {
            'ethereum': 'https://api.etherscan.io/api'
        }
    
    def get_wallet_info(self, address):
        try:
            # Get ETH balance
            balance_url = f"{self.base_urls['ethereum']}?module=account&action=balance&address={address}&tag=latest&apikey={self.etherscan_api_key}"
            balance_response = requests.get(balance_url, timeout=10)
            balance_data = balance_response.json()
            
            # Get transaction count
            txcount_url = f"{self.base_urls['ethereum']}?module=proxy&action=eth_getTransactionCount&address={address}&tag=latest&apikey={self.etherscan_api_key}"
            txcount_response = requests.get(txcount_url, timeout=10)
            txcount_data = txcount_response.json()
            
            balance_eth = int(balance_data['result']) / 1e18 if balance_data['status'] == '1' else 0
            tx_count = int(txcount_data['result'], 16) if 'result' in txcount_data else 0
            
            return {
                'address': address,
                'balance': balance_eth,
                'transaction_count': tx_count,
                'blockchain': 'ethereum',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            print(f"Error fetching real data: {e}")
            # Fallback to demo data
            return self._get_demo_data(address)
    
    def _get_demo_data(self, address):
        import random
        return {
            'address': address,
            'balance': random.randint(1000, 1000000),
            'transaction_count': random.randint(10, 500),
            'blockchain': 'ethereum (demo mode)'
        }
