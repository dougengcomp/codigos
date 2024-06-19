import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
          'Nine':9, 'Ten':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14}

class Card:
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
        self.value=values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit
    
class Deck:
    def __init__(self):
        self.all_cards = []
        for a in suits:
            for b in ranks:
                self.all_cards.append(Card(a,b))
        
    def shuffle (self):
        random.shuffle (self.all_cards)

    def deal_one (self):
        return self.all_cards.pop()
            
    def __str__(self):
        complete_deck=''
        for c in self.all_cards:
            complete_deck+=str (c)
        return str (complete_deck)

class Player:
    def __init__(self,name, bal):
        self.name = name
        self.balance=bal
        self.hand=[]

    def hit (self,card):
        self.hand.append(card)

    def reset_hand (self):
        self.hand=[]

    def __str__(self):
        return f'Player {self.name} has {len(self.hand)} cards.'





    
#mydeck=Deck()
#print (mydeck)
#mycard=mydeck.deal_one()
#print (f"\n my card is {mycard}")
#mydeck.shuffle()
#print (mydeck)
#print (len(mydeck.all_cards))
#mycard=mydeck.deal_one()
#print (f"\n my card is {mycard}")