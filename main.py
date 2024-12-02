from threading import Thread
from blockchain_pow.blockchain import Blockchain
from blockchain_pow.node import simulate_node
import time

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
