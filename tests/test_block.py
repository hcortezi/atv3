import unittest
from blockchain_pow.blockchain import Block

class TestBlock(unittest.TestCase):
    def test_calculate_hash(self):
        block = Block(0, "0", "Test", 2)
        hash_value = block.calculate_hash()
        self.assertIsInstance(hash_value, str)
        self.assertEqual(len(hash_value), 64)

    def test_mine_block(self):
        block = Block(0, "0", "Test", 2)
        block.mine_block()
        self.assertTrue(block.hash.startswith('00'))
