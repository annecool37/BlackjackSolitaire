### author Chia-An Chen       ###
### CIT 590, Spring 2015, hw6 ###
### 03/06/2015                ###

### SolBlackjack.py ###

# import cards for the use of Card class and Deck class.
from cards import *

# create class Blackjack
class BlackJack(object):

    def __init__(self):
        '''initialize BlackJack()'''
        # create deck
        self.deck = Deck()
        
        # create table and discardList
        self.table = {'row1':range(1,6), 'row2':range(6,11), 'row3': range(11,14), 'row4': range(14,17)}
        self.table_reference = {'row1':range(1,6), 'row2':range(6,11), 'row3': range(11,14), 'row4': range(14,17)}
        self.discardList = range(17,21)

        # handler for one-time printing
        self.isPrint = False

        # create empty dictionary
        self.hand = {}
        self.theSum = {}

        # create highestScore.txt
        self.highScore = open('highScore.txt', 'w')
        self.highScore.write('0')
        self.highScore.close()

    def __str__(self):
        '''to print out the table in proper alignment'''
        lst = []
        for row in self.table.keys():
            string =''
            for card in self.table[row]:
                if row =='row1' or row =='row2':
                    if type(card) == int:
                        string = string + ' '+ str(card) + ' '
                    else:
                        string = string + ' '+ str(card)
                else:
                    string = string + ' '+ str(card)
            # central alignment (space as filler)
            lst.append(string.center(18,' '))           
        return '\n'+lst[0]+'\n'+lst[1]+'\n'+lst[2]+'\n'+lst[3]+'\n'
        
    ### card handling functions ###
    def check_full_discard(self):
        '''check is the discarList is full'''
        if self.discardList[3] != 20:
            return True
        return False
            
    def add_to_discard(self, card):
        '''add card to discardList if the the discardList'''
        for i in range(0,4):
            if type(self.discardList[i]) == int:
                # place the card to discardList
                self.discardList[i]=card
                break
    
    def place_card(self, card, position):
        '''place the card in table'''           
        for row, grid_nums in self.table.items():
            if grid_nums.count(int(position)) != 0:
                # get the values in dictionary
                lst = self.table[row]
                # replace the value with card
                lst[lst.index(int(position))] = card
                # update table
                self.table[row] = lst
                break
        
    def check_full_table(self):
        '''check if the table is full'''
        checkList=[]
        for grid_nums in self.table.values():
            for num in grid_nums:
                if type(num) != int:
                    checkList.append(0)
                else:
                    checkList.append(1)
        if checkList.count(0) == 16:
            return True
        return False
        
    def check_input(self, position):
        '''check the validity of an input position'''
        # non-number        
        try:
            int(position)
        except ValueError:
            return 'non_number'

        # out-of-range number
        position = int(position)
        if position > 16 or position < 1 :
            return 'out_of_range'
  
        # check if place is already occupied
        for row, grid_nums in self.table_reference.items():
            if grid_nums.count(position) != 0:
                idx = self.table_reference[row].index(position)
                if self.table[row][idx] != position:
                    return 'occupied'

        return 'valid'

    ### scoring-related functions ###
    def store_hands(self):
        '''create new dictionary to store each hands'''
        ###        hand5 hand6 hand7 hand8 hand9   ###
        ###  hand1  1     2     3     4     5      ###
        ###  hand2  6     7     8     9     10     ###
        ###  hand3        11    12    13           ###
        ###  hand4        14    15    14           ###
        
        for row in self.table.keys():
            key = row.replace('row', 'hand')
            self.hand[key]=self.table[row]

        self.hand['hand5']=[self.table['row1'][0],self.table['row2'][0]]
        self.hand['hand9']=[self.table['row1'][4],self.table['row2'][4]]
        self.hand['hand6']=[self.table['row1'][1],self.table['row2'][1], self.table['row3'][0],self.table['row4'][0]]
        self.hand['hand7']=[self.table['row1'][2],self.table['row2'][2], self.table['row3'][1],self.table['row4'][1]]
        self.hand['hand8']=[self.table['row1'][3],self.table['row2'][3], self.table['row3'][2],self.table['row4'][2]]

    def store_rank(self, cards):
        '''store cards' ranks for a row/colomn into rankList'''
        rankList=[]
        for i in range(0, len(cards)):
            rankList.append(cards[i].get_rank())
        return rankList

    def to_rank_only(self):
        ''''update hand's values to rank only'''
        for hand, cards in self.hand.items():
            theRank = self.store_rank(cards) 
            self.hand[hand] = theRank
            
    def convert_to_number_and_sort(self, lst):
        '''convert the rank to numeric form in integer'''
        for i in range (0,len(lst)):
            if lst[i] == 'A':
                # for now, we convert A into 1
                lst[i] = 1
            elif lst[i] == 'J' or lst[i] == 'Q' or lst[i] == 'K':
                lst[i] = 10
            else:
                lst[i] = int(lst[i])
        lst.sort()
        return lst   

    def ace_oriented_score_sum(self, lst):
        '''check how many aces are there in the list and convert the score to 11 if needed'''
        # since we already converted A into 1, we will just count the number of '1'
        # if the remaining sum (excluding 1's) <= the threshold
        # for example if ace_num == 1 and sum(lst[1:]) <= 10, then convert the first ace's score from 1 to 11
        ace_num = lst.count(1)
        if  sum(lst[ace_num:]) <= 11-ace_num:
            lst[0] = 11    
        return sum(lst)

    def assign_points(self, score):
        '''assign points according to score in the hand'''
        # ignore the Blackjack case for now
        if score == 21:
            return 7
        elif score <= 16:
            return 1
        elif score >= 22:
            return 0
        else:
            return score-15

    def hand_to_score(self):
        '''store the sum of score for each hand to a new dictionary'''
        for hand in self.hand.keys():
            sortedList = self.convert_to_number_and_sort(self.hand[hand])
            self.theSum[hand] = self.ace_oriented_score_sum(sortedList)

    def score_to_points(self):
        '''convert score into corresponding points'''
        point=[]
        for hand in self.theSum.keys():
            if self.theSum[hand] == 21 and len(self.hand[hand]) ==2:
                point.append(10) # Blackjack!
            else:
                point.append(self.assign_points(self.theSum[hand]))
        return point
       
    def check_highest_score(self,totalPoints):
        '''check if the user's score is the highest so far. If yes, update the file'''
        self.highScore = open('highScore.txt', 'r+')
        current_high = int(self.highScore.readline())
        if totalPoints < current_high:
            return False
        elif totalPoints == current_high:
            return True
        else:
            self.highScore.seek(0)
            self.highScore.truncate()
            self.highScore.write(str(totalPoints))
            self.highScore.close()
            return True
        
    def print_intro(self):
        '''print introduction'''
        intro = '''Hello there!
This is a modified Blackjack game and you will have to place the card onto the table below.
Scores will be calculated for each column/row, representing nine independent hands.
 
Scoring Table (score:criteria)
10: Two cards that total 21
 7: 3,4,5 cards total 21
 5: Hand totals 20
 4: Hand totals 19
 3: Hand totals 18
 2: Hand totals 17
 1: Hand totals 16 or less
 0: Hand totals 22 or more

In case you are not familiar with the rule:
Ace can take as 1 or 11, and J,Q,K will count for 10
The rest of the cards count as the number displayed

Note that you can only discard four cards in total and you can not move the card once placed.
(p.s. for a yes/no question, enter n for no or else we will take it as a yes)

Enjoy the game!!! :)
'''
        return intro
        
    ### main play function ###
    def play(self):
        '''main play method'''
        print self.print_intro()
        
        start = True
        while start:
            # display initial state of game
            print self
            
            # shuffle deck
            self.deck.shuffle()

            run = True
            while run:
                
                keepCard = True
                while keepCard == True:
                    # deal a card and allow user to make a move
                    card = self.deck.deal()
                    print 'the card you get is', card

                    # check if the discardList is full
                    isDiscardFull = self.check_full_discard()
                    if isDiscardFull == False:
                        decision = raw_input("Do you want this card? ")      
                        if decision == 'n':
                            # discard the card
                            self.add_to_discard(card)
                        else:
                            keepCard = False
                    elif isDiscardFull == True:
                        if self.isPrint == False:
                            # if the discard pile is full, print the statement only once
                            print "The discard pile is full. You have to place the card in your hands from now on."
                            self.isPrint = True
                        keepCard = False

                # check input validity
                isValid = False
                while isValid == False:
                    position = raw_input("Where do you want to place the card? ")
                    # isValid = self.check_input(position)
                    checker = self.check_input(position)
                    if checker == 'non_number':
                        print "Please enter a number."
                    elif checker =='out_of_range':
                        print "Please enter a number that is being displayed above"
                    elif checker =='occupied':
                        print "The place is already occupied with another card."
                    else:
                        isValid = True

                # place the card
                self.place_card(card, position)
                
                # display current state of game
                print self
                
                # check if the table is full 
                tableIsFull= self.check_full_table()
                if tableIsFull == True:
                    run = False

            print "game ends, score calculating..."
            
            # store nine hands, update to rank-only, and convert to score
            self.store_hands()
            self.to_rank_only()
            self.hand_to_score()
            
            # convert score to points and sum them up
            totalPoints = sum(self.score_to_points())        
            print "your score is:", totalPoints
            
            # check highest score (if it's the first round, the score is the highest score)
            isHighest = self.check_highest_score(totalPoints)
            if isHighest == True:
                print 'Congrats! You have the highest score so far!'

            # print game is done and ask if the use wants to restart
            response = raw_input("Do you wish to restart the game? ")
            if response == 'n':
                start = False
            else:
                # reset all variables back to initial conditions
                self.table = {'row1':range(1,6), 'row2':range(6,11), 'row3': range(11,14), 'row4': range(14,17)}
                self.discardList = range(17,21)
                self.isPrint = False
                self.deck = Deck()
                self.hand = {}
                self.theSum = {}
     
### execute the game ###
# still wrote a main() to avoid running the game while unittesting
def main():   
    bj_solitaire = BlackJack()
    bj_solitaire.play()

if __name__=="__main__":
    main()

