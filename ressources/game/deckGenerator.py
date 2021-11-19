from ressources.game.card import Card, UnoCard

# Standard 52 piece deck
NOS = (1,2,3,4,5,6,7,8,9,10)
SUITS = ["Spades", "Diamonds", "Clubs", "Hearts"]
PICS = ["J", "Q", "K"] # jack, queen, king

# Uno deck
UNO_COLORS = ("Red", "Green", "Blue", "Yellow") # Colors, or suits if you insist
UNO_NOS = (0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9) # one of this tuple for each suit
ACT_CARDS = ["+2", "Reverse", "Skip"] # Four in each suit
WILD_CARDS = ["ChangeColor", "Draw4"] # Four total in deck

def getNewDeck(jokers=0) -> list:
    deck: list = []

    for suit in SUITS:
        for pic in PICS:
            deck.append(Card(suit=suit, pic=pic, no=10))
        
        for no in NOS:
            deck.append(Card(suit=suit, no=no))
        
    if jokers >= 1:
        try:
            deck.append(Card(joker=True) * jokers)
        except Exception as e:
            print("%s\n\nCouldn't create the jokers for some reason look in deckGenerator.py lol fuck you")

    return deck

def getNewUnoDeck() -> list:
    deck: list = []

    for color in UNO_COLORS:

        #generate number cards
        for num in UNO_NOS:
            deck.append(UnoCard(color=color, number=num))

        #generate action type cards
        for actType in ACT_CARDS:
            for i in range(2):
                deck.append(UnoCard(isActionType=True, actionType=actType, color=color))

    for wildType in WILD_CARDS:
        for i in range(4):
            deck.append(UnoCard(isWildType=True, wildType=wildType))

    return deck