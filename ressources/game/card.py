class UnoCard:

    id = None

    isActionType = False
    isWildType = False

    color = str()
    number = int()

    wildType = str()
    actionType = str()

    def __init__(self, color = None, \
                        number = None, \
                        isActionType: bool = False, \
                        isWildType: bool = False, \
                        actionType: str = None, \
                        wildType: str = None):

        if isActionType:
            self.actionType = actionType
            self.isActionType = True
            self.color = color
            self.id = 1
            pass

        elif isWildType:
            self.wildType = wildType
            self.isWildType = True
            self.id = 2
            pass

        elif color is not None and number is not None:
            self.color = color
            self.number = number
            self.id=3
            pass

        else:
            raise Exception("Wrong initialization with uno card. Check card.py.")

    def __str__(self):
        if self.isWildType:
            return self.wildType

        elif self.isActionType:
            return "A %s %s" % (self.color, self.actionType)

        else:
            return "A %s number %s" % (self.color, self.number)

class Card:
    def __init__(self, suit: str = None, no: int = None, pic: str = None, joker: bool = False):

        try:
            self.suit = suit   # suit type
            self.no = no       # the number/value
            self.pic = pic     # picture type eg. Q, J or K
            self.joker = joker # joker or not?
        
        except Exception as e:
            print("%s\n%s\nTrying to initialize a card. Something wrong w/ the args prolly. \
                Look in card.py/deckGenerator.py" % ("="*15, e))

    def __str__(self) -> str:
        # ANY STANDARD NUMBER CARD
        if self.no and self.no != 1 and self.no != 11: return "%s of %s" % (self.no, self.suit)
        # ACE
        elif self.no == 1 or self.no == 11: return "A of %s" % (self.suit)
        # PICTURE CARD
        elif self.pic: return "%s of %s" % (self.pic, self.suit)
        # JOKER
        elif self.joker: return "Joker"