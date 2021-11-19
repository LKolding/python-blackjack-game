from ressources.game.card import Card

class Player:

    def __init__(self, name: str):
        self.name = name
        self.hand = []

    def __repr__(self) -> str:
        return "Name: %s\
                Current hand: %s\n" % (self.name, self.hand)

    def __str__(self) -> str:
        return '''Player "%s" with a total of %s card in hand.''' % (self.name, len(self.hand))

    def sortHand(self, uno=False) -> bool:
        try:
            if not uno:

                clubs: list = []
                hearts: list = []
                spades: list = []
                diamonds: list = []
                jokers: list = []

                for card in self.hand:
                    if card.suit == "Hearts":
                        hearts.append(card)

                    elif card.suit == "Spades":
                        spades.append(card)

                    elif card.suit == "Diamonds":
                        diamonds.append(card)

                    elif card.suit == "Clubs":
                        clubs.append(card)

                    elif card.joker:
                        jokers.append(card)

                newHand = []

                # TODO make sort by number as well as suit      

                for suit in [clubs, spades, hearts, diamonds]:
                    for card in suit:
                        newHand.append(card)

                self.hand = newHand

            elif uno:
                    yellows = []
                    reds = []
                    blues = []
                    greens = []

                    actionCards = []
                    wildCards = []

                    for card in self.hand:
                        if card.isActionType: actionCards.append(card)
                        elif card.isWildType: wildCards.append(card)

                        elif card.color == "Red":
                            reds.append(card)

                        elif card.color == "Green":
                            greens.append(card)

                        elif card.color == "Blue":
                            blues.append(card)

                        elif card.color == "Yellow":
                            yellows.append(card)

                        else:
                            raise Exception("Tried to sort uno cards - unsuccesfully. sorry")

                    newHand = []

                    for color in [reds, greens, blues, yellows]:
                        try:
                            color.sort(key=lambda c: c.number) # sorts colorgroups cards by number
                            
                            for card in color:
                                newHand.append(card)

                        except Exception as e:
                            print("%s\nsomething went wrong when sorting the number in the uno deck sorry homeboi" % (e))

                        finally:
                            for group in [actionCards, wildCards]:
                                for card in group:
                                    newHand.append(card)
                            
        except Exception as e:
            print(e)
            return False

        else: return True

    def hasCard(self, s_card: int) -> bool:
        for card in self.hand:
            # returns true if card is found
            if card.no == s_card: return True
            # checks if aces values doesnt match and
            # returns true to correct that error if so
            if card.no == 1 and s_card == 11: return True
            elif s_card == 1 and card == 11: return True

        return False

    def hasBJ(self) -> bool:
        '''Returns true if player has blackjack'''
        card_values = []
        for card in self.hand: card_values.append(card.no)
        if len(card_values) == 2:
            if 10 in card_values and 11 in card_values: return True
            elif 10 in card_values and 1 in card_values: return True
            else: return False
        else: return False

    def getHand(self) -> list: return self.hand
    
    def getHandSum(self) -> int:
        sum = 0
        for card in self.hand:
            if card.no: sum += card.no
            else: sum += 10

        return sum

    def addCard(self, card: Card): self.hand.append(card)
