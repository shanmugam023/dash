"""
Cryptocurrency information service for mapping symbols to full names
"""

class CoinInfoService:
    def __init__(self):
        # Comprehensive cryptocurrency mapping
        self.coin_mapping = {
            'AVAUSDT': {'name': 'Avalanche', 'symbol': 'AVAX', 'category': 'Layer 1'},
            'STEEMUSDT': {'name': 'Steem', 'symbol': 'STEEM', 'category': 'Social'},
            'ZECUSDT': {'name': 'Zcash', 'symbol': 'ZEC', 'category': 'Privacy'},
            'CHRUSDT': {'name': 'Chromia', 'symbol': 'CHR', 'category': 'Platform'},
            'GHSTUSDT': {'name': 'Aavegotchi', 'symbol': 'GHST', 'category': 'Gaming'},
            'BTCUSDT': {'name': 'Bitcoin', 'symbol': 'BTC', 'category': 'Currency'},
            'ETHUSDT': {'name': 'Ethereum', 'symbol': 'ETH', 'category': 'Layer 1'},
            'ADAUSDT': {'name': 'Cardano', 'symbol': 'ADA', 'category': 'Layer 1'},
            'SOLUSDT': {'name': 'Solana', 'symbol': 'SOL', 'category': 'Layer 1'},
            'DOTUSDT': {'name': 'Polkadot', 'symbol': 'DOT', 'category': 'Layer 0'},
            'LINKUSDT': {'name': 'Chainlink', 'symbol': 'LINK', 'category': 'Oracle'},
            'MATICUSDT': {'name': 'Polygon', 'symbol': 'MATIC', 'category': 'Layer 2'},
            'UNIUSDT': {'name': 'Uniswap', 'symbol': 'UNI', 'category': 'DeFi'},
            'LTCUSDT': {'name': 'Litecoin', 'symbol': 'LTC', 'category': 'Currency'},
            'XRPUSDT': {'name': 'Ripple', 'symbol': 'XRP', 'category': 'Payment'},
            'BCHUSDT': {'name': 'Bitcoin Cash', 'symbol': 'BCH', 'category': 'Currency'},
            'XLMUSDT': {'name': 'Stellar', 'symbol': 'XLM', 'category': 'Payment'},
            'VETUSDT': {'name': 'VeChain', 'symbol': 'VET', 'category': 'Supply Chain'},
            'TRXUSDT': {'name': 'TRON', 'symbol': 'TRX', 'category': 'Platform'},
            'EOSUSDT': {'name': 'EOS', 'symbol': 'EOS', 'category': 'Platform'},
            'XMRUSDT': {'name': 'Monero', 'symbol': 'XMR', 'category': 'Privacy'},
            'DASHUSDT': {'name': 'Dash', 'symbol': 'DASH', 'category': 'Currency'},
            'ETCUSDT': {'name': 'Ethereum Classic', 'symbol': 'ETC', 'category': 'Layer 1'},
            'NEOUSDT': {'name': 'Neo', 'symbol': 'NEO', 'category': 'Platform'},
            'ATOMUSDT': {'name': 'Cosmos', 'symbol': 'ATOM', 'category': 'Layer 0'},
            'ALGOUSDT': {'name': 'Algorand', 'symbol': 'ALGO', 'category': 'Layer 1'},
            'FILUSDT': {'name': 'Filecoin', 'symbol': 'FIL', 'category': 'Storage'},
            'ICPUSDT': {'name': 'Internet Computer', 'symbol': 'ICP', 'category': 'Platform'},
            'FTMUSDT': {'name': 'Fantom', 'symbol': 'FTM', 'category': 'Layer 1'},
            'HBARUSDT': {'name': 'Hedera', 'symbol': 'HBAR', 'category': 'Platform'},
            'EGLDUSDT': {'name': 'MultiversX', 'symbol': 'EGLD', 'category': 'Layer 1'},
            'NEARUSDT': {'name': 'NEAR Protocol', 'symbol': 'NEAR', 'category': 'Layer 1'},
            'FLOWUSDT': {'name': 'Flow', 'symbol': 'FLOW', 'category': 'Platform'},
            'SANDUSDT': {'name': 'The Sandbox', 'symbol': 'SAND', 'category': 'Gaming'},
            'MANAUSDT': {'name': 'Decentraland', 'symbol': 'MANA', 'category': 'Gaming'},
            'AXSUSDT': {'name': 'Axie Infinity', 'symbol': 'AXS', 'category': 'Gaming'},
            'ENJUSDT': {'name': 'Enjin Coin', 'symbol': 'ENJ', 'category': 'Gaming'},
            'CHZUSDT': {'name': 'Chiliz', 'symbol': 'CHZ', 'category': 'Fan Token'},
            'THETAUSDT': {'name': 'Theta Network', 'symbol': 'THETA', 'category': 'Media'},
            'MKRUSDT': {'name': 'Maker', 'symbol': 'MKR', 'category': 'DeFi'},
            'AAVEUSDT': {'name': 'Aave', 'symbol': 'AAVE', 'category': 'DeFi'},
            'COMPUSDT': {'name': 'Compound', 'symbol': 'COMP', 'category': 'DeFi'},
            'SNXUSDT': {'name': 'Synthetix', 'symbol': 'SNX', 'category': 'DeFi'},
            'CRVUSDT': {'name': 'Curve DAO Token', 'symbol': 'CRV', 'category': 'DeFi'},
            'YFIUSDT': {'name': 'yearn.finance', 'symbol': 'YFI', 'category': 'DeFi'},
            'SUSHIUSDT': {'name': 'SushiSwap', 'symbol': 'SUSHI', 'category': 'DeFi'},
            '1INCHUSDT': {'name': '1inch Network', 'symbol': '1INCH', 'category': 'DeFi'},
            'BATUSDT': {'name': 'Basic Attention Token', 'symbol': 'BAT', 'category': 'Utility'},
            'ZRXUSDT': {'name': '0x', 'symbol': 'ZRX', 'category': 'DeFi'},
            'OMGUSDT': {'name': 'OMG Network', 'symbol': 'OMG', 'category': 'Layer 2'},
            'LRCUSDT': {'name': 'Loopring', 'symbol': 'LRC', 'category': 'Layer 2'},
            'BNBUSDT': {'name': 'BNB', 'symbol': 'BNB', 'category': 'Exchange'},
            'CAKEUSDT': {'name': 'PancakeSwap', 'symbol': 'CAKE', 'category': 'DeFi'},
            'DOGEUSDT': {'name': 'Dogecoin', 'symbol': 'DOGE', 'category': 'Meme'},
            'SHIBUSDT': {'name': 'Shiba Inu', 'symbol': 'SHIB', 'category': 'Meme'},
            'FLOKIUSDT': {'name': 'Floki', 'symbol': 'FLOKI', 'category': 'Meme'},
            'PEPEUSDT': {'name': 'Pepe', 'symbol': 'PEPE', 'category': 'Meme'},
        }
    
    def get_coin_info(self, symbol):
        """Get full coin information by symbol"""
        if symbol in self.coin_mapping:
            return self.coin_mapping[symbol]
        
        # Fallback for unknown symbols
        clean_symbol = symbol.replace('USDT', '').replace('BUSD', '').replace('BTC', '')
        return {
            'name': clean_symbol.title(),
            'symbol': clean_symbol,
            'category': 'Unknown'
        }
    
    def get_coin_name(self, symbol):
        """Get just the full name of the coin"""
        return self.get_coin_info(symbol)['name']
    
    def get_coin_symbol(self, symbol):
        """Get the clean symbol (without USDT)"""
        return self.get_coin_info(symbol)['symbol']
    
    def get_coin_category(self, symbol):
        """Get the category of the coin"""
        return self.get_coin_info(symbol)['category']
    
    def format_coin_display(self, symbol):
        """Format coin for display with full name and symbol"""
        info = self.get_coin_info(symbol)
        return f"{info['name']} ({info['symbol']})"