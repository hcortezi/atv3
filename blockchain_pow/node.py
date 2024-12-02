import random
import time

def simulate_node(blockchain, miner_id):
    """Simula a operação de um nó minerador."""
    while True:
        blockchain.mine_pending_transactions(miner_id)
        time.sleep(random.randint(1, 5))  # Simula o tempo entre tentativas
