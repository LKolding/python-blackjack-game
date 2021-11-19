'''
Blackjack game written in python using the graphics module (based on Tkinter) for GUI components
Game logic written by: 
Louis Kolding (c) 2021
'''

from ressources.game.deckGenerator import getNewDeck
from ressources.game.player import Player
import ressources.graphics.graphics
# from ressources.graphics.widgets import Graph # only includes a selfwritten Graph class to present a graph over a given time
from graphical_components.sprites import *

import random
from time import sleep
from datetime import date
import csv

GameStats = {
    "games_played": 0,
    "player_wins" : 0,
    "dealer_wins" : 0,
    "ties" : 0,
    "datetime": ""
}
deck = []

class DefaultValues:
    window_width = 400
    window_height = 370
    decks = 1
    init_deck_size = len(getNewDeck()*decks)
    shuffle_amount = 3

def print_scene(graphwin, dealer: Player, player: Player, dealerTurn=False):
    global deck
    components = []
    clean_sheet = Rectangle(Point(0,0), Point(DefaultValues.window_width, DefaultValues.window_height))
    clean_sheet.setFill("white")
    room = Room(DefaultValues.window_width, DefaultValues.window_height*0.8, 0,0)
    components.append(clean_sheet)
    components.append(room)
    ###                 ##
    #  PRINT DEALER HAND #
    ##                  ##
    dealer_hand_xpos = DefaultValues.window_width/2-50
    dealer_hand_ypos = DefaultValues.window_height*0.2

    if len(dealer.getHand()) > 2: dealer_hand_xpos -= len(dealer.getHand())*12
    for i, card in enumerate(dealer.getHand()):
        if dealerTurn:
            randomText = Text(Point(dealer_hand_xpos-50, dealer_hand_ypos), dealer.getHandSum())
            components.append(randomText)
        if not dealerTurn:
            if i==0:
                if card.no:
                    random_card = CardSprite(card.no, card.suit, dealer_hand_xpos+i*45, dealer_hand_ypos)
                    components.append(random_card)
                else:
                    random_card = CardSprite(card.pic, card.suit, dealer_hand_xpos+i*45, dealer_hand_ypos)
                    components.append(random_card)

            else:
                if card.no: components.append(CardSprite(card.no, card.suit, dealer_hand_xpos+i*45, dealer_hand_ypos,flipped=True))
                else: components.append(CardSprite(card.pic, card.suit, dealer_hand_xpos+i*45, dealer_hand_ypos,flipped=True))
        else:
            if card.no:
                random_card = CardSprite(card.no, card.suit, dealer_hand_xpos+i*45, dealer_hand_ypos)
                components.append(random_card)
            else:
                random_card = CardSprite(card.pic, card.suit, dealer_hand_xpos+i*45, dealer_hand_ypos)
                components.append(random_card)

    ###                 ##
    #  PRINT PLAYER HAND #
    ##                  ##
    player_hand_xpos = DefaultValues.window_width/2-50
    player_hand_ypos = DefaultValues.window_height*0.6

    hand = player.getHand()
    player_sum_text = Text(Point(player_hand_xpos-50, player_hand_ypos-18), player.getHandSum())
    components.append(player_sum_text)
    if len(hand) > 2: player_hand_xpos -= len(hand)*12
    for i, card in enumerate(hand):
        if not card.pic:
            random_card = CardSprite(card.no, card.suit, player_hand_xpos+i*45, player_hand_ypos)
            components.append(random_card)
        else:
            random_card = CardSprite(card.pic, card.suit, player_hand_xpos+i*45, player_hand_ypos)
            components.append(random_card)

    ###                 ##
    #     PRINT STATS    #
    ##                  ##

    stats_position = (DefaultValues.window_width*0.15, DefaultValues.window_height*0.85)
    for k,i in enumerate(GameStats):
        randomText = Text(Point(stats_position[0], stats_position[1]+k*12), f"{i} : {GameStats[i]}")
        randomText.setSize(14)
        components.append(randomText)

    deck_size_text = Text(Point(stats_position[0]+170, stats_position[1]), f"Deck size: {len(deck)}")
    components.append(deck_size_text)

    for comp in components:
        comp.draw(graphwin)

def save_game_stats():
    GameStats["datetime"] = str(date.today())
    with open("stats.csv", "a", newline="") as f:
        csvwriter = csv.writer(f, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        row = []
        for v in GameStats:
            row.append(f"{v}:{GameStats[v]}")

        csvwriter.writerow(row)

def view_game_stats():
    stats = []
    element = {}
    with open("stats.csv", newline="") as f:
        csvreader = csv.reader(f,delimiter=" ", quotechar="|")
        for row in csvreader:
            for stat in row:
                k, v = stat.split(":")
                try: element[k] = int(v)
                except: element[k] = v

            stats.append(element)
            element = {}

    p_wins = 0
    d_wins = 0
    ties = 0
    games_played = 0
    for i in stats:
        p_wins += i["player_wins"]
        d_wins += i["dealer_wins"]
        ties += i["ties"]
        games_played += i["games_played"]

    class StatsWindow:
        width = 290
        height = 270

    stats_window = GraphWin("Overall Statistics", width=StatsWindow.width, height=StatsWindow.height)

    games_played_txt = Text(Point(StatsWindow.width/2, 20), f"Total games played: {games_played}").draw(stats_window)
    p_wins_txt = Text(Point(StatsWindow.width/2, 40), f"Total player wins: {p_wins}").draw(stats_window)
    d_wins_txt = Text(Point(StatsWindow.width/2, 60), f"Total dealer wins: {d_wins}").draw(stats_window)
    ties_txt = Text(Point(StatsWindow.width/2, 80), f"Total ties: {ties}").draw(stats_window)
    try: win_perc_txt = Text(Point(StatsWindow.width/2, 100), "Win percentage: {:.1%}".format(p_wins/games_played)).draw(stats_window)
    except: pass
    # graph = Graph(w=360, h=200, x=25, y=25, values=tuple(wins))
    # graph.show(stats_window, options=("drawLabels", "drawLines", "drawGraphLabel"))
    stats_window.getMouse()
    stats_window.close()

def print_end_scene(graphwin):
    view_game_stats()
    components = []
    clean_sheet = Rectangle(Point(0,0), Point(DefaultValues.window_width, DefaultValues.window_height))
    clean_sheet.setFill("grey")
    components.append(clean_sheet)
    if GameStats["games_played"] != 0:
        scoreboard_location = (DefaultValues.window_width/2-20, DefaultValues.window_height/2)
        txts = {}
        txts["Player win percentage"] = GameStats["player_wins"]/GameStats["games_played"]
        txts["Dealer win percentage"] = GameStats["dealer_wins"]/GameStats["games_played"]
        txts["Ties percentage"] = GameStats["ties"]/GameStats["games_played"]

        for i,k in enumerate(txts):
            p = Point(*scoreboard_location)
            p.y += i*15
            randomText = Text(p, "{}: {:.1%}".format(k, txts[k]))
            components.append(randomText)

    for comp in components: comp.draw(graphwin)
    save_game_stats()
    graphwin.getMouse()
    exit()

def print_blackjack_msg(graphwin, who):
    randomText = Text(Point(DefaultValues.window_width/2, DefaultValues.window_height/2), f"{who} got BlackJack!")
    randomText.setSize(24)
    randomText.setTextColor("white")
    randomText.setStyle("italic")
    randomText.draw(graphwin)

def has_blackjack(hand):
    cards_values = []

    for card in hand:
        if card.no == 1: cards_values.append(11)
        else: cards_values.append(card.no)

    if len(cards_values) == 2:
        if 11 in cards_values and 10 in cards_values: return True
    else: return False

def evaluate_result(dealer, player1):
    # Dealer has blackjack and player doesnt and vice versa
    if has_blackjack(dealer.getHand()) and not has_blackjack(player1.getHand()): GameStats["dealer_wins"]+=1
    elif has_blackjack(player1.getHand()) and not has_blackjack(dealer.getHand()): GameStats["player_wins"]+=1
    # Tie
    elif player1.getHandSum() > 21 and dealer.getHandSum() > 21: GameStats["ties"] += 1
    elif (player1.getHandSum() < 21 and dealer.getHandSum() < 21) and player1.getHandSum() == dealer.getHandSum(): GameStats["ties"] += 1
    # Dealer wins
    elif dealer.getHandSum() > player1.getHandSum() and dealer.getHandSum() <= 21: GameStats["dealer_wins"]+=1
    elif dealer.getHandSum() <= 21 and player1.getHandSum() > 21: GameStats["dealer_wins"] += 1
    # Player wins
    elif player1.getHandSum() > dealer.getHandSum() and player1.getHandSum() <= 21: GameStats["player_wins"]+=1
    elif player1.getHandSum() <= 21 and dealer.getHandSum() > 21: GameStats["player_wins"] += 1
    else: print("CANNOT COMPUTE RESULT")

def run(win):
    global deck
    playerTurn = True
    dealerTurn = True

    dealer = Player("Dealer")
    player1 = Player("Player1")

    for _ in range(DefaultValues.decks): deck += getNewDeck()
    for _ in range(DefaultValues.shuffle_amount): random.shuffle(deck)

    while True:
        # if 69% of deck has been played, reshuffle
        if len(deck) < DefaultValues.init_deck_size*0.31:
            deck = []
            for _ in range(DefaultValues.decks): deck += getNewDeck()
            for _ in range(DefaultValues.shuffle_amount): random.shuffle(deck)

        player1.addCard(deck.pop(0))
        dealer.addCard(deck.pop(0))

        player1.addCard(deck.pop(0))
        dealer.addCard(deck.pop(0))

        while playerTurn:
            # Ace value check
            if player1.hasCard(1) or player1.hasCard(11):
                for i,card in enumerate(player1.getHand()):
                    # checks to see if player has got an ace
                    # and if total sum is less than or equal to
                    # 21 when ace has a value of 11, updates it
                    # and vice versa
                    if card.no == 1 and (player1.getHandSum() + 10 <= 21): player1.hand[i].no = 11
                    elif card.no == 11 and player1.getHandSum() > 21: player1.hand[i].no = 1

            print_scene(win, dealer, player1)

            # BJ check
            if player1.hasBJ():
                print_blackjack_msg(win, "Player1")
                sleep(2)
                break

            if player1.getHandSum() > 21:   
                print("busted!")
                break

            if player1.getHandSum() == 21:
                print("nice one!")
                break

            ans = input("Type d to draw: (or q to quit)")
            if  ans == "d": player1.addCard(deck.pop(0))
            elif ans == "q": print_end_scene(win)
            else: playerTurn = False

        print_scene(win, dealer, player1, dealerTurn=True)
        while dealerTurn:
            # BJ check
            if dealer.hasBJ():
                print_blackjack_msg(win, "Dealer")
                sleep(1.5)
                break

            while dealer.getHandSum() < 17:
                sleep(1)
                dealer.addCard(deck.pop(0))
                # Sets ace's value to 11 if possible. Otherwise the other way around
                if dealer.hasCard(11):
                    for i,card in enumerate(dealer.getHand()): 
                        if card.no == 11: dealer.hand[i].no = 1

                print_scene(win, dealer, player1, dealerTurn=True)
                
            dealerTurn = False

        evaluate_result(dealer, player1)
        print_scene(win, dealer, player1, dealerTurn=True)
        sleep(1.5)

        GameStats["games_played"] += 1
        player1.hand = []
        dealer.hand = []
        playerTurn = True
        dealerTurn = True

if __name__=="__main__":
    win = ressources.graphics.graphics.GraphWin("BlackJack", DefaultValues.window_width, DefaultValues.window_height)
    run(win)