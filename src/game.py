from enum import Enum
import random

class Suit(Enum):
    CLUBS = 0.025
    DIAMONDS = 0.5
    HEARTS = 0.75
    SPADES = 0.99
    BULLS = 1
    
    # Override the function to return just the name
    def __str__(self):
        nameToSymbol = {
            "CLUBS" : "clubs",
            "DIAMONDS" : "diamonds",
            "HEARTS" : "hearts",
            "SPADES" : "spades",
            "BULLS" : "bulls",
        }

        return nameToSymbol[self.name]
class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    # Jersey numbers, though value is irrelevant
    MJ = 23
    RODMAN = 91

    def __str__(self):
        nameToSymbol = {
            "TWO" : "2",
            "THREE" : "3",
            "FOUR" : "4",
            "FIVE" : "5",
            "SIX" : "6",
            "SEVEN" : "7",
            "EIGHT" : "8",
            "NINE" : "9",
            "TEN" : "10",
            "JACK" : "jack",
            "QUEEN" : "queen",
            "KING" : "king",
            "ACE" : "ace",
            "MJ": "mj",
            "RODMAN": "rodman"
        }

        return nameToSymbol[self.name]

class Constant(Enum):
    NUM_MJ_CARDS = 2
    NUM_RODMAN_CARDS = 4
    # (Note: 0-indexed) 
    MJ_LOCATIONS = (4,19)
    MJ_WINNING_SEQUENCE = [1,1,1,0,0,1,1,1]
    MJ_BONUS_POINTS = 10
    RODMAN_BONUS_POINTS = 2

class Card:
    def __init__(self, rank: Rank, suit: Suit, count: int = None):
        """
        Initialises a playing card (can be normal or special card)
        
        :param value: the value of the card to allow comparison
        :param count: the ith special card (MJ/RODMAN), Ideally Card should be a base class then have PlayingCard and SpecialCard extend it.
        """
        self.rank: Rank = rank
        self.suit: Suit = suit
        self.value: int = rank.value + suit.value
        self.count: int = count
    
    def getName(self) -> str:
        """
        Returns the card's name
        """
        return f"{self.rank}_of_{self.suit}" if self.suit != Suit.BULLS else f"{self.rank}_of_{self.suit}_{self.count}"

class Deck:
    def __init__(self, isBullsEdition: bool):
        """
        Initialises a deck of, already shuffled and ready to use, playing cards

        :param isBullsEdition: if true, adds the corresponding special cards
        """
        self.cards: list[Card] = []
        self.startingNumPlayingCards: int = 0
        
        # initialise the playing cards according to the enum classes, skipping the special cards
        for rank in Rank:
            if rank in (Rank.MJ, Rank.RODMAN):
                continue
            for suit in Suit:
                if suit == Suit.BULLS:
                    continue
                
                self.startingNumPlayingCards += 1
                self.cards.append(Card(rank, suit))

        # insert Rodman cards
        if isBullsEdition:
            for i in range(Constant.NUM_RODMAN_CARDS.value):
                self.cards.append(Card(Rank.RODMAN, Suit.BULLS, i + 1))
        
        self.shuffle()

        # assuming we are playing the special mode, this ensure the 1st card we draw is always a normal card.
        while isBullsEdition and self.seeTopCard().rank in (Rank.MJ, Rank.RODMAN):
            self.shuffle()

        # after ensuring top card is a normal card, insert MJ cards into appropriate places
        if isBullsEdition:
            self.insertMjCards()
    
    def printDeck(self) -> None:
        """
        For debugging purposes, prints the entire deck
        """
        res: list[str] = []
        for card in self.cards:
            res.append(f"{card.getName()}")

        print(res)

    def shuffle(self) -> None:
        """
        Shuffles the cards
        """
        random.shuffle(self.cards)

    def drawCard(self) -> Card:
        """
        Returns the top card from the deck (removing it from the deck)
        """
        return self.cards.pop() if self.cards else None
    
    def seeTopCard(self) -> Card:
        """
        See the top card without removing it 
        """
        return self.cards[-1] if self.cards else None
    
    def insertMjCards(self) -> None:
        """
        Inserts MJ cards into the predefined locations
        """
        for i, pos in enumerate(Constant.MJ_LOCATIONS.value):
            self.cards.insert(len(self.cards)-pos, Card(Rank.MJ, Suit.BULLS, i + 1))

class HigherLowerGame:
    def __init__(self):
        """
        Initialises the high level game object (However, it does not initilise deck since user needs to decide which version of game to play)

        :parms currentCard: Holds the current normal card (non-special)
        """
        self.deck: Deck = None
        self.currentCard: Card = None
        
        self.normalCardsDrawned: int = 0

        self.isBullsEdition: bool = None
        self.currentRodmanCards: int = 0
        self.currentMjRound: int = 0
        self.currentMjSequence: list[int] = []
        self.isMjActivated = False
        self.isRodmanActivated: bool = False
        self.score: int = 0

    def getNumRemainingNormalCards(self) -> int:
        return self.deck.startingNumPlayingCards - self.normalCardsDrawned
    
    def configureSpecialEdition(self, isBullsEdition: bool) -> None:
        """
        Update the variables relevant to special edition and also initialises the deck of cards accordingly
        """
        self.isBullsEdition = isBullsEdition
        self.deck = Deck(self.isBullsEdition)

    def compareCards(self, currentCard: Card, nextCard: Card, isUserInputHigher: bool) -> bool:
        """
        Returns a boolean depending on if the user correctly guesses the next card's value
        """
        if (nextCard.value > currentCard.value and isUserInputHigher) or (nextCard.value < currentCard.value and not isUserInputHigher):
            return True
        else:
            return False
    
    def isNextCardRodman(self, card: Card) -> bool:
        return True if card.rank == (Rank.RODMAN) else False
    
    def isNextCardMj(self, card: Card) -> bool:
        return True if card.rank == (Rank.MJ) else False

    def resetMjRound(self):
        """
        Resets MJ round related attributes
        """
        self.isMjActivated = False
        self.currentMjRound = 0
        self.currentMjSequence = []

    def playRound(self, isUserInputHigher: bool) -> bool:
        """
        Returns a boolean indicating if the round should continue (logic to handle player's guess and next card scenarios are here)
        """ 
        
        nextCard: Card = self.deck.drawCard()

        if nextCard.rank == Rank.MJ:
            self.isMjActivated = True
            return True
        elif nextCard.rank == Rank.RODMAN:
            self.currentRodmanCards += 1
            return True
        else: # next card is NOT a special card
            isCorrect: bool = self.compareCards(self.currentCard, nextCard, isUserInputHigher)
            
            # need to increment before if statements so, because if we are on the last card, the game needs to know that this is the last round and return false
            self.normalCardsDrawned += 1

            if self.isMjActivated:
                # basically when the current winning number is 1, we need to guess correctly, when it is 0, we need to guess 'wrongly' (note guessing wrongly increments score as well)
                if (isCorrect and Constant.MJ_WINNING_SEQUENCE.value[self.currentMjRound] == 1) or (not isCorrect and Constant.MJ_WINNING_SEQUENCE.value[self.currentMjRound] == 0):
                    self.score += 1
                    self.currentMjSequence.append(Constant.MJ_WINNING_SEQUENCE.value[self.currentMjRound])

                    if self.currentMjSequence == Constant.MJ_WINNING_SEQUENCE.value:
                        self.score += Constant.MJ_BONUS_POINTS.value
                        self.resetMjRound()
                else:
                    self.resetMjRound()
                self.currentMjRound += 1
            elif isCorrect and self.isRodmanActivated:
                self.score += Constant.RODMAN_BONUS_POINTS.value
                self.isRodmanActivated = False
            elif isCorrect:
                self.score += 1
            else:
                if self.isBullsEdition and self.currentRodmanCards > 0 and self.normalCardsDrawned < self.deck.startingNumPlayingCards:
                    self.currentRodmanCards -= 1
                    self.isRodmanActivated = True
                else: # this means u either (have no rodman cards and got it wrong) or (u are playing normal version of the game and got it wrong)
                    return False

            if self.normalCardsDrawned == self.deck.startingNumPlayingCards:
                return False
            
            self.currentCard = nextCard

            return True
            
    def startGame(self) -> None:
        """
        Draws a card to start the game
        """
        # Draws the initial card for the user
        self.currentCard = self.deck.drawCard()
        self.normalCardsDrawned += 1

    
    
    



