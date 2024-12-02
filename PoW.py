import hashlib
import random
import time
from threading import Thread, Lock

class Block:
    """Representa um bloco na blockchain."""
    def __init__(self, index, previous_hash, transactions, difficulty):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = None

    def mine_block(self):
        """Realiza a mineração do bloco ao encontrar um hash válido."""
        target = '0' * self.difficulty
        while True:
            self.hash = self.calculate_hash()
            if self.hash[:self.difficulty] == target:
                break
            self.nonce += 1

    def calculate_hash(self):
        """Calcula o hash do bloco."""
        block_data = f"{self.index}{self.previous_hash}{self.transactions}{self.nonce}"
        return hashlib.sha256(block_data.encode()).hexdigest()

class Blockchain:
    """Simula uma blockchain."""
    def __init__(self, difficulty):
        self.chain = []
        self.difficulty = difficulty
        self.pending_transactions = []
        self.lock = Lock()
        self.create_genesis_block()

    def create_genesis_block(self):
        """Cria o bloco gênesis."""
        genesis_block = Block(0, "0", "Genesis Block", self.difficulty)
        genesis_block.mine_block()
        self.chain.append(genesis_block)

    def get_last_block(self):
        """Retorna o último bloco da cadeia."""
        return self.chain[-1]

    def add_transaction(self, transaction):
        """Adiciona uma transação à lista de transações pendentes."""
        self.lock.acquire()
        try:
            self.pending_transactions.append(transaction)
        finally:
            self.lock.release()

    def mine_pending_transactions(self, miner_id):
        """Minera as transações pendentes e adiciona um novo bloco."""
        if not self.pending_transactions:
            print(f"Miner {miner_id}: Não há transações pendentes.")
            return
        
        new_block = Block(
            len(self.chain),
            self.get_last_block().hash,
            self.pending_transactions,
            self.difficulty
        )
        print(f"Miner {miner_id}: Mineração iniciada.")
        new_block.mine_block()

        self.lock.acquire()
        try:
            self.chain.append(new_block)
            self.pending_transactions = []
        finally:
            self.lock.release()

        print(f"Miner {miner_id}: Bloco minerado com sucesso! Hash: {new_block.hash}")

    def validate_chain(self):
        """Valida a integridade da blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

def simulate_node(blockchain, miner_id):
    """Simula a operação de um nó minerador."""
    while True:
        blockchain.mine_pending_transactions(miner_id)
        time.sleep(random.randint(1, 5))  # Simula o tempo entre tentativas

if __name__ == "__main__":
    difficulty = 4  # Define a dificuldade para mineração
    blockchain = Blockchain(difficulty)

    # Adiciona transações pendentes
    blockchain.add_transaction("Alice paga 10 BTC para Bob")
    blockchain.add_transaction("Bob paga 5 BTC para Charlie")

    # Simula múltiplos nós mineradores
    nodes = []
    for miner_id in range(1, 4):
        node_thread = Thread(target=simulate_node, args=(blockchain, miner_id))
        nodes.append(node_thread)
        node_thread.start()

    # Monitora a blockchain
    time.sleep(20)  # Tempo de simulação
    for node in nodes:
        node.join(timeout=1)  # Aguarda a finalização dos threads

    # Validação e exibição da blockchain
    if blockchain.validate_chain():
        print("\nBlockchain validada com sucesso.")
    else:
        print("\nErro: Blockchain inválida.")

    print("\nBlocos na Blockchain:")
    for block in blockchain.chain:
        print(f"Índice: {block.index}, Hash: {block.hash}, Transações: {block.transactions}")
