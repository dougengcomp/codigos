import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
          'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

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
        self.balance= int (bal)
        self.hand=[]

    def hit (self,card):
        self.hand.append(card)

    def reset_hand (self):
        self.hand=[]
    
    def current_hand (self):
        total=0
        for item in self.hand:
            total+=item.value
        return total

    def __str__(self):
        stringofcards=''
        for item in self.hand:
            stringofcards+=item.rank + ' of ' + item.suit
        return f'Player {self.name} balance is {self.balance} has {len(self.hand)} cards as follows:\n {stringofcards}'

class Dealer:
    def __init__(self):
        self.name="Dealer"
        self.hand=[]
    
    def hit (self,card):
        self.hand.append(card)
    
    def reset_hand (self):
        self.hand=[]

    def current_hand (self):
        total=0
        for item in self.hand:
            total+=item.value
        return total

    def __str__(self):
        stringofcards=''
        for item in self.hand:
            stringofcards+=item.rank + ' of ' + item.suit
        return f'Dealer {self.name} has {len(self.hand)} cards as follows:\n {stringofcards}'
    

mydeck=None
print ("bem vindo ao blackjack")
nome=input ("qual seu nome:")
balanco=input ("qual seu balanco:")
jogador=Player(nome,balanco)
dealer=Dealer ()
gameison=True
while gameison:
    del mydeck
    mydeck=Deck()
    mydeck.shuffle()
    jogador.reset_hand()
    dealer.reset_hand()
    print (f"jogador balance atual é: {jogador.balance} ")
    bet= int (input ("faça sua aposta:"))
    jogador.balance-=  (bet)
    if jogador.balance < 0:
        #checafundos
        print (f"jogador nao tem fundos suficientes")
        jogador.balance+=  (bet)
        print (f"saldo atual {jogador.balance}")
        continue
    print (f"jogador balance is: {jogador.balance} ")
    #1o round
    jogador.hand.append(mydeck.deal_one())
    dealer.hand.append(mydeck.deal_one())
    jogador.hand.append(mydeck.deal_one())
        
    print (f"valor da mao do jogador é: {jogador.current_hand()}")
    print (f"situacao do jogador é : {jogador}")
    #print (f"valor da mao do Dealer é: {dealer.current_hand()}")
    #print (f"situacao total do dealer é : {dealer}")
    print (f"{dealer}")
    dealer.hand.append(mydeck.deal_one())
    #check if blackjack:
    if (len(jogador.hand)==2) and ((jogador.hand[0].rank=='Ace' and jogador.hand[1].value==10)or (jogador.hand[1].rank=='Ace' and jogador.hand[0].value==10)):
        #check if delaer also has a BJ:
        if (len(dealer.hand)==2) and ((dealer.hand[0].rank=='Ace' and dealer.hand[1].value==10)or (dealer.hand[1].rank=='Ace' and dealer.hand[0].value==10)):
            print (f"mao do do dealer é : {dealer}")
            print ("Tie, both player and dealer have a BJ")
        else:
            print (f"mao do do dealer é : {dealer}")
            print (f"Jogador {jogador.name} has a won with a blackjack!")
            jogador.balance+=bet+(1.5*bet)
            continue
    else:
        action=input ("choose 'H' for hit or 'S' for stand: ")
        if action.upper () == 'S':
            ## vez do dealer jogar ate o fim, hits up to 16, stands on 17 or above:
            print ("vez do dealer jogar")
            if (dealer.current_hand()>16):#dealer stands, check who wins
                if (dealer.current_hand() > 21 ): #if dealer busts
                        print (f"mao do do dealer é : {dealer}")
                        print (f"valor da mao do jogador é: {jogador.current_hand()}")
                        print (f"situacao do jogador é : {jogador}")    
                        print ("Dealer Busts, you Win")
                        jogador.balance+=2*bet
                        continue
                elif dealer.current_hand() > jogador.current_hand():# dealer wins
                            print (f"valor da mao do jogador é: {jogador.current_hand()}")
                            print (f"situacao do jogador é : {jogador}")
                            print (f"mao do do dealer é : {dealer}")
                            print ("you loose")
                            continue
                elif dealer.current_hand() == jogador.current_hand():# tie 
                            print (f"valor da mao do jogador é: {jogador.current_hand()}")
                            print (f"situacao do jogador é : {jogador}")
                            print (f"mao do do dealer é : {dealer}")
                            print ("Tie")
                            jogador.balance+=bet
                            continue
            else:
                while dealer.current_hand() < 17:
                    dealer.hand.append(mydeck.deal_one())
                    if (dealer.current_hand() > 21 ): #if dealer busts
                        print (f"valor da mao do jogador é: {jogador.current_hand()}")
                        print (f"situacao do jogador é : {jogador}")
                        print (f"mao do do dealer é : {dealer}")
                        print ("Dealer Busts, you Win")
                        jogador.balance+=2*bet
                        continue
                    elif dealer.current_hand() > 16: #dealer must stand, check who's won
                        if dealer.current_hand() > jogador.current_hand():# dealer wins
                            print (f"valor da mao do jogador é: {jogador.current_hand()}")
                            print (f"situacao do jogador é : {jogador}")
                            print (f"mao do do dealer é : {dealer}")
                            print ("you loose")
                            continue
                        elif dealer.current_hand() == jogador.current_hand():# tie 
                            print (f"valor da mao do jogador é: {jogador.current_hand()}")
                            print (f"situacao do jogador é : {jogador}")
                            print (f"mao do do dealer é : {dealer}")
                            print ("tie")
                            jogador.balance+=bet
                            continue
                        else:
                            print (f"valor da mao do jogador é: {jogador.current_hand()}")
                            print (f"situacao do jogador é : {jogador}")
                            print (f"mao do do dealer é : {dealer}")
                            print ("you win!")
                            jogador.balance+=2*bet
                            continue
        elif action.upper()=='H':
            is_player_turn=True
            while is_player_turn and action.upper()=='H':
                jogador.hand.append(mydeck.deal_one())
                if (jogador.current_hand()> 21 ): #check if jogador busts and has an ace
                    for item in jogador.hand():
                        if item.rank=='Ace':
                            jogador.hand.pop(item)
                            jogador.hand.append()

                    print (f"mao do dealer é : {dealer}")
                    print (f"valor da mao do jogador é: {jogador.current_hand()}")
                    print (f"situacao do jogador é : {jogador}")
                    print ("Jogador Busts!")
                    is_player_turn=False
                    break
                if (jogador.current_hand()> 21 ): #check if jogador busts
                    print (f"mao do dealer é : {dealer}")
                    print (f"valor da mao do jogador é: {jogador.current_hand()}")
                    print (f"situacao do jogador é : {jogador}")
                    print ("Jogador Busts!")
                    is_player_turn=False
                    break
                elif (jogador.current_hand()== 21 ): #check who wins
                    if dealer.current_hand() < jogador.current_hand():# player wins
                            print (f"mao do do dealer é : {dealer}")
                            print (f"valor da mao do jogador é: {jogador.current_hand()}")
                            print (f"situacao do jogador é : {jogador}")
                            print ("you win")
                            jogador.balance+=2*bet
                            is_player_turn=False
                            break
                    elif dealer.current_hand() == jogador.current_hand():# tie 
                        print (f"mao do do dealer é : {dealer}")
                        print (f"valor da mao do jogador é: {jogador.current_hand()}")
                        print (f"situacao do jogador é : {jogador}")
                        print ("tie")
                        jogador.balance+=bet
                        is_player_turn=False
                        break
                else:
                    print (f"valor da mao do jogador é: {jogador.current_hand()}")
                    print (f"situacao do jogador é : {jogador}")
                    action=input ("choose 'H' for hit or 'S' for stand: ")
                    if action.upper()=='H':
                        is_player_turn=True
                        continue
                    if action.upper () == 'S':
                        #vez do dealer jogar ate o fim, primeiro checa se a mao >16
                        if dealer.current_hand()>16:
                            #compare dealer x player
                            if dealer.current_hand() > jogador.current_hand():# dealer wins
                                print (f" {dealer}")
                                print (f"valor da mao do jogador é: {jogador.current_hand()}")
                                print (f"situacao do jogador é : {jogador}")
                                print ("you loose")
                                continue
                            elif dealer.current_hand() == jogador.current_hand():# tie 
                                print (f" {dealer}")
                                print (f"valor da mao do jogador é: {jogador.current_hand()}")
                                print (f"situacao do jogador é : {jogador}")
                                print ("tie")
                                jogador.balance+=bet
                                continue
                            else: #player wins
                                print (f" {dealer}")
                                print (f"valor da mao do jogador é: {jogador.current_hand()}")
                                print (f"situacao do jogador é : {jogador}")
                                print ("you win!")
                                jogador.balance+=2*bet
                                continue
                        ## se o dealer tem menos que 17 vez do dealer jogar ate o fim, hits up to 16, stands on 17 or above:
                        while dealer.current_hand() < 17:
                            dealer.hand.append(mydeck.deal_one())
                            if (dealer.current_hand() > 21 ): #if dealer busts
                                print (f" {dealer}")
                                print (f"valor da mao do jogador é: {jogador.current_hand()}")
                                print (f"situacao do jogador é : {jogador}")
                                print ("Dealer Busts, you Win")
                                jogador.balance+=2*bet
                                continue
                            elif dealer.current_hand() > 16: #dealer must stand, check who's won
                                if dealer.current_hand() > jogador.current_hand():# dealer wins
                                    print (f" {dealer}")
                                    print (f"valor da mao do jogador é: {jogador.current_hand()}")
                                    print (f"situacao do jogador é : {jogador}")
                                    print ("you loose")
                                    continue
                                elif dealer.current_hand() == jogador.current_hand():# tie 
                                    print (f" {dealer}")
                                    print (f"valor da mao do jogador é: {jogador.current_hand()}")
                                    print (f"situacao do jogador é : {jogador}")
                                    print ("tie")
                                    jogador.balance+=bet
                                    continue
                                else:
                                    print (f" {dealer}")
                                    print (f"valor da mao do jogador é: {jogador.current_hand()}")
                                    print (f"situacao do jogador é : {jogador}")
                                    print ("you win!")
                                    jogador.balance+=2*bet
                                    continue
            is_player_turn=False

                        

                    
            




#mydeck=Deck()
#print (mydeck)
#mycard=mydeck.deal_one()
#print (f"\n my card is {mycard}")
#mydeck.shuffle()
#print (mydeck)
#print (len(mydeck.all_cards))
#mycard=mydeck.deal_one()
#print (f"\n my card is {mycard}")