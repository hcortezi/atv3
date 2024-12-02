import unittest
from blockchain_pow.blockchain import Blockchain

class TestBlockchain(unittest.TestCase):
    def test_genesis_block(self):
        blockchain = Blockchain(2)
        self.assertEqual(len(blockchain.chain), 1)
        self.assertEqual(blockchain.chain[0].transactions, "Genesis Block")
