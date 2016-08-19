### author Chia-An Chen       ###
### CIT 590, Spring 2015, hw6 ###
### 03/06/2015                ###


### cards.py ###

import random

class Card(object):
    #the card has a suit which is one of 'S','C','H' or 'D'
    #the card has a rank 
    
    def __init__(self, r, s):
        '''implement rank and suit for card'''
        # where r is the rank, s is suit
        self.r = r.upper()
        self.s = s.upper()
        
    def get_rank(self):
        '''get the rank of the card'''
        return self.r

    def get_suit(self):
        '''get the suit of the card'''
        return self.s

    def __str__(self):
        '''print out the card: rank+suit'''
        return str(self.r)+str(self.s)

class Deck(object):
    """Denote a deck to play cards with"""
     
    def __init__(self):
        """Initialize deck as a list of all 52 cards:
           13 cards in each of 4 suits"""   
        self.__deck = []
        rank = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        suit = 'SCHD'
        for i in range (0, len(rank)):
            for j in range (0, len(suit)):
                self.__deck.append(Card(rank[i],suit[j]))
                       
    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.__deck)
        
    def get_deck(self):
        '''get the deck'''
        return self.__deck
  
    def deal(self):
        '''get the last card in the deck, 
           simulates a pile of cards and getting the top one'''
        # get the last card
        card = self.__deck[-1]
        # modify the deck
        self.__deck.pop()
        return card
   
    def __str__(self):
        """Represent the whole deck as a string for printing -- very useful during code development"""
        printed_deck = ''
        for card in self.__deck:
            printed_deck += str(card)
            printed_deck += '\n'
        return printed_deck

