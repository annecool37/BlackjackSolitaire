### author Chia-An Chen       ###
### CIT 590, Spring 2015, hw6 ###
### 03/06/2015                ###

### SolBlackjackTests.py ###

from SolBlackjack import *
import unittest

class testSolBlackjack(unittest.TestCase):

    def setUp(self):
        self.test_bj = BlackJack()
        self.theDiscard = self.test_bj.discardList
        self.theTable = self.test_bj.table       
        self.theHand = self.test_bj.hand
        self.sum = self.test_bj.theSum
        self.theHighScore = self.test_bj.highScore

        self.k_spade = Card('k','s')
        self.q_spade = Card('q', 's')
        self.j_heart = Card('j', 'h')
        self.two_club = Card('2','c')
        self.a_square = Card('a', 's')
        self.a_club = Card('a', 'c')

    def fullTable(self):
        '''helper function that manually creates a full table'''
        ### optimize the full table that contains most varied scenarios ###
        ## 1  2  3  4  5           AC AS  3C 2C KC    ##
        ## 6  7  8  9  10  -->     KS 10C 5C AD JC    ##
        ##    11 12 13                5S  7C 9C       ##
        ##    14 15 16                2S  6C AH       ##
        self.theTable['row1']=[Card('a','c'), Card('a','s'), Card('3','c'), Card('2','c'), Card('k','c')]
        self.theTable['row2']=[Card('k','s'), Card('10','c'), Card('5','c'), Card('a','d'), Card('j','c')]
        self.theTable['row3']=[Card('5','s'), Card('7','c'), Card('9','c')]
        self.theTable['row4']=[Card('2','s'), Card('6','c'), Card('a','h')]
                                   
    def jump_to_rank_only_status(self):
        '''helper function that runs the dictionry to to_rank_only status'''
        self.fullTable()
        self.test_bj.store_hands()
        self.test_bj.to_rank_only()

    def test__init__(self):
        self.assertEqual({'row1':range(1,6), 'row2':range(6,11), 'row3': range(11,14), 'row4': range(14,17)},self.test_bj.table)
        self.assertEqual(range(17,21), self.test_bj.discardList)
        self.assertEqual({}, self.test_bj.hand)
        self.assertEqual({}, self.test_bj.theSum)
        self.assertEqual(False, self.test_bj.isPrint)

    def test__str__(self):
        expected_str = '\n  1  2  3  4  5   \n  6  7  8  9  10  \n     11 12 13     \n     14 15 16     \n'
        self.assertEqual(expected_str,str(self.test_bj))
        self.fullTable()
        expected_str = '\n  AC AS 3C 2C KC  \n  KS 10C 5C AD JC \n     5S 7C 9C     \n     2S 6C AH     \n'
        self.assertEqual(expected_str,str(self.test_bj))

    def testcheck_full_discard(self):
        # when there's only one card in discrdList --> return False
        self.theDiscard[0]= self.two_club
        self.assertEqual(False, self.test_bj.check_full_discard())
        # in the game, we append discard to the list in order
        # when the last element in discardList had been placed w/ a card --> return True
        self.theDiscard[3]= self.a_square
        self.assertEqual(True, self.test_bj.check_full_discard())
        
    def testadd_to_discard(self):
        # add two cards into discardlist and check if the card object is in the list
        self.test_bj.add_to_discard(self.k_spade)
        self.test_bj.add_to_discard(self.two_club)
        self.assertEqual(self.k_spade, self.theDiscard[0])
        self.assertEqual(self.two_club, self.theDiscard[1])
        self.assertEqual(19, self.theDiscard[2]) # card not yet added to this position in discardList
               
    def testplace_card(self):
        # place two card in table and check if the table dictionary is updated
        self.test_bj.place_card(self.k_spade, 2)
        self.test_bj.place_card(self.two_club, 11)
        self.assertEqual(self.k_spade, self.theTable['row1'][1])
        self.assertEqual(self.two_club, self.theTable['row3'][0])
        self.assertEqual(7, self.theTable['row2'][1]) # card not yet placed onto this position in table

    def testcheck_full_table(self):
        self.assertFalse(self.test_bj.check_full_table())
        self.fullTable() # make a full table 
        self.assertTrue(self.test_bj.check_full_table())

    def testcheck_input(self):
        # non-number input
        # internal error won't raise ValueRrror, thus not testing through self.assertRaises()
        self.assertEqual('non_number', self.test_bj.check_input('a'))
        self.assertEqual('non_number', self.test_bj.check_input('11.5'))
        # out-of-range input 
        self.assertEqual('out_of_range', self.test_bj.check_input('25'))
        self.assertEqual('out_of_range', self.test_bj.check_input('-5'))
        # valid input
        self.assertEqual('valid', self.test_bj.check_input('10'))
        self.assertEqual('valid', self.test_bj.check_input('5'))
        # place a card and check the input validity for an occupied space
        self.test_bj.place_card(self.k_spade, '10')
        self.assertEqual('occupied', self.test_bj.check_input('10'))

    ### tests for scoring-related functions ###
    def teststore_hands(self):
        self.test_bj.store_hands()
        hand1 = self.theTable['row1']
        hand5 = [self.theTable['row1'][0], self.theTable['row2'][0]] 
        hand8 = [self.theTable['row1'][3], self.theTable['row2'][3], self.theTable['row3'][2], self.theTable['row4'][2]]
        self.assertEqual(hand1, self.theHand['hand1'])
        self.assertEqual(hand5, self.theHand['hand5'])
        self.assertEqual(hand8, self.theHand['hand8'])

    def teststore_rank(self):
        self.assertEqual(['K','2'], self.test_bj.store_rank([self.k_spade,self.two_club]))
        self.assertEqual(['J','A','A'], self.test_bj.store_rank([self.j_heart, self.a_square, self.a_club]))
        
    def testto_rank_only(self):
        self.jump_to_rank_only_status()
        self.assertEqual(['A', 'A', '3', '2', 'K'], self.theHand['hand1']) 
        self.assertEqual(['5', '7', '9'], self.theHand['hand3'])
        self.assertEqual(['A', 'K'], self.theHand['hand5'])
        self.assertEqual(['3', '5', '7', '6'], self.theHand['hand7']) 

    def testconvert_to_number_and_sort(self):
        self.assertEqual([1,1,2,5,7,8,10,10,10], self.test_bj.convert_to_number_and_sort([7, 'K', 'A', 5, 'Q', 2, 'J', 'A', 8]))
        self.assertEqual([1,1,3,10,10], self.test_bj.convert_to_number_and_sort(['A', 'K', 'A', 'Q', 3]))
        self.assertEqual([7, 10], self.test_bj.convert_to_number_and_sort(['K', 7]))
        
    def testace_oriented_score_sum(self):
        # only passed in sorted list and the number will only range from 1 to 10
        ## 2 cards ##
        self.assertEqual(21, self.test_bj.ace_oriented_score_sum([1,10]))
        self.assertEqual(18, self.test_bj.ace_oriented_score_sum([1,7]))
        self.assertEqual(12, self.test_bj.ace_oriented_score_sum([1,1]))
        ## 3 cards ##
        # all A --> 1 
        self.assertEqual(16, self.test_bj.ace_oriented_score_sum([1,5,10]))
        self.assertEqual(12, self.test_bj.ace_oriented_score_sum([1,1,10]))
        # one A --> 11
        self.assertEqual(19, self.test_bj.ace_oriented_score_sum([1,3,5]))
        self.assertEqual(21, self.test_bj.ace_oriented_score_sum([1,4,6]))
        self.assertEqual(17, self.test_bj.ace_oriented_score_sum([1,1,5]))
        self.assertEqual(21, self.test_bj.ace_oriented_score_sum([1,1,9]))
        self.assertEqual(13, self.test_bj.ace_oriented_score_sum([1,1,1]))       
        ## 4 cards ##
        # all A --> 1 
        self.assertEqual(13, self.test_bj.ace_oriented_score_sum([1,2,4,6]))
        self.assertEqual(14, self.test_bj.ace_oriented_score_sum([1,1,5,7]))
        self.assertEqual(13, self.test_bj.ace_oriented_score_sum([1,1,1,10]))       
        # one A --> 11
        self.assertEqual(17, self.test_bj.ace_oriented_score_sum([1,2,2,2]))
        self.assertEqual(21, self.test_bj.ace_oriented_score_sum([1,2,3,5]))
        self.assertEqual(19, self.test_bj.ace_oriented_score_sum([1,1,3,4]))
        self.assertEqual(21, self.test_bj.ace_oriented_score_sum([1,1,2,7]))
        self.assertEqual(20, self.test_bj.ace_oriented_score_sum([1,1,1,7])) 
        self.assertEqual(21, self.test_bj.ace_oriented_score_sum([1,1,1,8]))
        self.assertEqual(14, self.test_bj.ace_oriented_score_sum([1,1,1,1]))
        ## 5 cards ##
        # all A --> 1 
        self.assertEqual(18, self.test_bj.ace_oriented_score_sum([1,2,3,5,7]))
        self.assertEqual(13, self.test_bj.ace_oriented_score_sum([1,1,2,3,6]))
        self.assertEqual(15, self.test_bj.ace_oriented_score_sum([1,1,1,5,7]))
        self.assertEqual(14, self.test_bj.ace_oriented_score_sum([1,1,1,1,10]))
        # one A --> 11
        self.assertEqual(19, self.test_bj.ace_oriented_score_sum([1,2,2,2,2]))
        self.assertEqual(21, self.test_bj.ace_oriented_score_sum([1,2,2,3,3]))
        self.assertEqual(18, self.test_bj.ace_oriented_score_sum([1,1,2,2,2]))
        self.assertEqual(21, self.test_bj.ace_oriented_score_sum([1,1,2,3,4]))
        self.assertEqual(18, self.test_bj.ace_oriented_score_sum([1,1,1,2,3]))
        self.assertEqual(21, self.test_bj.ace_oriented_score_sum([1,1,1,3,5]))
        self.assertEqual(17, self.test_bj.ace_oriented_score_sum([1,1,1,1,3]))
        self.assertEqual(21, self.test_bj.ace_oriented_score_sum([1,1,1,1,7]))
        self.assertEqual(15, self.test_bj.ace_oriented_score_sum([1,1,1,1,1]))
        ##  no change when there's no A ##
        self.assertEqual(17, self.test_bj.ace_oriented_score_sum([3,5,9]))

    def testassign_points(self):
        self.assertEqual(7, self.test_bj.assign_points(21))
        self.assertEqual(5, self.test_bj.assign_points(20))
        self.assertEqual(4, self.test_bj.assign_points(19))
        self.assertEqual(3, self.test_bj.assign_points(18))
        self.assertEqual(2, self.test_bj.assign_points(17))
        self.assertEqual(1, self.test_bj.assign_points(13))
        self.assertEqual(0, self.test_bj.assign_points(25))
           
    def testhand_to_score(self):
        self.jump_to_rank_only_status()
        self.test_bj.hand_to_score()
        self.assertEqual(17, self.sum['hand1'])
        self.assertEqual(36, self.sum['hand2'])
        self.assertEqual(21, self.sum['hand3'])
        self.assertEqual(19, self.sum['hand4'])
        self.assertEqual(21, self.sum['hand5']) # Blackjack case
        self.assertEqual(18, self.sum['hand6'])
        self.assertEqual(21, self.sum['hand7'])
        self.assertEqual(13, self.sum['hand8'])
        self.assertEqual(20, self.sum['hand9'])

    def testscore_to_points(self):
        self.jump_to_rank_only_status()
        self.test_bj.hand_to_score()
        # hands_num: 4  5  6  7  1  2  3  8  9
        # score    :19 21 18 21 17 36 21 13 20
        expected_points = [4, 10, 3, 7, 2, 0, 7, 1, 5]
        self.assertEqual(expected_points, self.test_bj.score_to_points())

    def testicheck_highest_score(self):
        # assume we get the score in the order of 5,10,7,10,15,13
        self.assertTrue(self.test_bj.check_highest_score(5)) # 5 is the current high
        self.assertTrue(self.test_bj.check_highest_score(10)) # 10 is the current high
        self.assertFalse(self.test_bj.check_highest_score(7))
        self.assertTrue(self.test_bj.check_highest_score(10))
        self.assertTrue(self.test_bj.check_highest_score(15)) # 15 is the current high
        self.assertFalse(self.test_bj.check_highest_score(13)) 
        
        
unittest.main()

