### author Chia-An Chen       ###
### CIT 590, Spring 2015, hw6 ###
### 03/06/2015                ###

### CardsTest.py ###
from cards import *
import unittest

class testCard(unittest.TestCase):

    def setUp(self):
        self.king_spade = Card('k','s')
        self.ace_heart = Card('a','h')
        self.two_club = Card('2','c')
        self.deck = Deck()

    def test__init__(self):
        self.assertEqual('Q', Card('q', 'h').r)
        self.assertEqual('q'.upper(), Card('q', 'h').r)
        self.assertEqual('h'.upper(), Card('q', 'h').s)      

    def testget_rank(self):
        self.assertEqual('K', self.king_spade.r)
        self.assertEqual('2', self.two_club.r)
        self.assertEqual('!', Card('!','?').r) # will still work for random input
        
    def testget_suit(self):
        self.assertEqual('S',self.king_spade.s)
        self.assertEqual('C',self.two_club.s)
        self.assertEqual('?', Card('!','?').s) # will still work for random input        

    def test__str__(self):
        # for class Card
        self.assertEqual('KS', str(self.king_spade))
        self.assertEqual('AH', str(self.ace_heart))
        self.assertEqual('QH', str(Card('q','h' ))) # case not sensitive
        # for class Deck
        expected_print = ['AS\nAC\nAH\nAD\n2S\n2C\n2H\n2D\n3S\n3C\n3H\n3D\n4S\n4C\n4H\n4D\n5S\n5C\n5H\n5D\n6S\n6C\n6H\n6D\n7S\n7C\n7H\n7D\n8S\n8C\n8H\n8D\n9S\n9C\n9H\n9D\n10S\n10C\n10H\n10D\nJS\nJC\nJH\nJD\nQS\nQC\nQH\nQD\nKS\nKC\nKH\nKD\n']
        self.assertEqual(expected_print , [str(self.deck)])
       
    def testget_deck(self):
        expected_deck = self.expected_deck()
        result_deck = [str(card) for card in self.deck.get_deck()]
        self.assertEqual(expected_deck, result_deck) 
    
    def testshuffle(self):
        original_deck = Deck()
        self.deck.shuffle()
        self.assertFalse(str(original_deck) == str(self.deck))
        
    def testdeal(self):
        expected_deck = self.expected_deck()
        # deal three cards
        self.assertEqual(expected_deck[-1], str(self.deck.deal()))
        self.assertEqual(expected_deck[-2], str(self.deck.deal()))
        self.assertEqual(expected_deck[-3], str(self.deck.deal()))

    def expected_deck(self):
        '''helper function to create expected deck'''
        # expectedDeck = ['AS', 'AC', 'AH', 'AD', '2S', '2C', '2H', '2D', '3S', '3C', '3H', '3D', '4S', '4C', '4H', '4D', '5S', '5C', '5H', '5D', '6S', '6C', '6H', '6D', '7S', '7C', '7H', '7D', '8S', '8C', '8H', '8D', '9S', '9C', '9H', '9D', '10S', '10C', '10H', '10D', 'JS', 'JC', 'JH', 'JD', 'QS', 'QC', 'QH', 'QD', 'KS', 'KC', 'KH', 'KD']
        expected_deck=str(self.deck).split('\n')
        expected_deck.pop() # to remove the empty string at the end
        return expected_deck
               
unittest.main()
