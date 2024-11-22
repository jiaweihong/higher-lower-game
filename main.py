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
        return self.name

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
    # Jersey Numbers, though value is not relevant
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
            "JACK" : "J",
            "QUEEN" : "Q",
            "KING" : "K",
            "ACE" : "A",
            "MJ": "MJ",
            "RODMAN": "ROD"
        }

        return nameToSymbol[self.name]

class Constraints(Enum):
    NUM_MJ_WIN_REQUIRED = 6
    NUM_MJ_CHANCES = 8
    NUM_MJ_CARDS = 2
    NUM_RODMAN_CARDS = 4
    # 5th card and 20th card which is not equivalent to index = 5 or 20 since we are using a stack
    MJ_LOCATIONS = [5,20]

class Card:
    def __init__(self, rank, suit):
        self.rank: Rank = rank
        self.suit: Suit = suit
        self.value: int = rank.value + suit.value
    
    def getName(self) -> str:
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self, isBullsEdition):
        self.cards: list[Card] = []
        self.numberPlayingCards: int = 0
        self.totalCards: int = 0

        # initialise the playing cards according to the enum classes, skipping the special cards
        for rank in Rank:
            if rank in (Rank.MJ, Rank.RODMAN):
                continue
            for suit in Suit:
                if suit == Suit.BULLS:
                    continue
                
                self.numberPlayingCards += 1
                self.cards.append(Card(rank, suit))

        self.totalCards = self.numberPlayingCards
        # insert special cards
        if isBullsEdition:
            for _ in range(Constraints.NUM_MJ_CARDS.value):
                self.totalCards += 1
                self.cards.append(Card(Rank.MJ, Suit.BULLS))

            for _ in range(Constraints.NUM_RODMAN_CARDS.value):
                self.totalCards += 1
                self.cards.append(Card(Rank.RODMAN, Suit.BULLS))
    
    # for debuggin purposes
    def printDeck(self) -> None:
        res: list[str] = []
        for card in self.cards:
            res.append(f"{card.getName()}")
        print(res)
    
    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def drawCard(self) -> Card:
        return self.cards.pop() if self.cards else None
    
    def seeTopCard(self) -> Card:
        return self.cards[self.totalCards-1] if self.cards else None
    
    def setMjCards(self):
        currentMjLocations: list[int] = []

        for i, card in enumerate(self.cards):
            if card.rank == Rank.MJ:
                currentMjLocations.append(i)
        
        for i, currentMjIdx in enumerate(currentMjLocations):
            # if MJ is not in the correct position
            correctMjLocations: list[int] = Constraints.MJ_LOCATIONS.value
            if currentMjIdx not in correctMjLocations:
                # swap with the card that is currently in MJ's location
                self.cards[currentMjIdx], self.cards[self.totalCards-correctMjLocations[i]] = self.cards[self.totalCards-correctMjLocations[i]], self.cards[currentMjIdx]

        self.printDeck()


class HigherLowerGame:
    def __init__(self, isBullsEdition=False):
        self.currentCard: Card = None
        self.cardsDrawned: int = 0
        self.deck: Deck = None
        self.isBullsEdition: bool = isBullsEdition
        self.currentRodmanCards: int = 0
        self.currentMjRound: int = 0
        self.isRodmanActivated: bool = False
        self.isBullsEdition: bool = False
        self.cardsDrawned: int = 0
        self.score: int = 0
    
    def configureSettings(self):
        isSpecialRound: str = self.getSpecialRoundInput()
        if isSpecialRound == "Y":
            print("Bulls Edition enabled! Special MJ and Rodman cards are in play!")
            self.isBullsEdition = True
        
        
        self.deck = Deck(self.isBullsEdition)
        self.deck.shuffle()

        # assuming we are playing the special mode, this ensure the 1st card we draw is always a normal card.
        while self.isBullsEdition and self.deck.seeTopCard().rank in (Rank.MJ, Rank.RODMAN):
            self.deck.shuffle()
        # after ensuring top card is a normal card, grab the mj cards and place them in the appropriate place
        if self.isBullsEdition:
            self.deck.setMjCards()
        
        self.currentCard = self.deck.drawCard()
        self.cardsDrawned = 1


    def compareCards(self, currentCard: Card, nextCard: Card, userInput: str) -> bool:
        if (nextCard.value > currentCard.value and userInput == "H") or (nextCard.value < currentCard.value and userInput == "L"):
            return True
        else:
            return False
    
    def getHigherLowerInput(self, card: Card) -> str:
        res: str = input(f"Your current card is {card.getName()}, is the next card Higher (H) or Lower (L)? ").strip().upper()

        while res not in ("H", "L"):
            res = input("Please input the characters: H or L. ").strip().upper()

        return res

    def getSpecialRoundInput(self) -> str:
        res: str = input("Do you want to enable the special Chicago Bulls Edition of the Game? Yes (Y) or No (N) ").strip().upper()

        while res not in ("Y", "N"):
            res = input("Please input the characters: Y or N. ").strip().upper()

        return res
    
    def playRound(self) -> bool:
        self.deck.printDeck()
        userInput: str = self.getHigherLowerInput(self.currentCard)
        
        nextCard: Card = self.deck.drawCard()

        if nextCard.rank == Rank.MJ:
            # if mj round is selected
            # mj round requires atleast 8 cards remaining, so mj cannot be in the last 8 cards

            # what happens if rodman card is activated, then mj is picked, rodman card will still be active 
            # what if there are rodman cards within mj rounds, they do not contribute as a win only non special cards
                # so if during mj round, we encounter rodman, we save it but dont increment currentmjround 
            pass
        elif nextCard.rank == Rank.RODMAN:
            # Drawing a rodman card does not update the currentCard since it is only meant to hold playing cards 
            self.currentRodmanCards += 1
            print(f"Congratulations you got a Rodman Card, you currently have {self.currentRodmanCards} Rodman Cards")

            return True
        else: # next card is NOT a special card
            print(f"The card was a {nextCard.getName()}")
            isCorrect: bool = self.compareCards(self.currentCard, nextCard, userInput)
            
            # need to increment before if statements so, if we are on the last card, the game needs to know that this is the last round
            self.cardsDrawned += 1

            if isCorrect and self.isRodmanActivated:
                print("Correct you got 2 points, thanks to Rodman!")

                self.score += 2
                self.isRodmanActivated = False
            elif isCorrect:
                print("Correct you got 1 points!")
                self.score += 1
            else:
                print("Incorrect!")

                if self.isBullsEdition and self.currentRodmanCards > 0 and self.cardsDrawned < self.deck.numberPlayingCards:
                    self.currentRodmanCards -= 1
                    print("You activated a Rodman card! You get a second chance and the next card right to win double points!")
                    self.isRodmanActivated = True
                else: # this means u either have no rodman cards or u are playing normal version of the game
                    return False

            if self.cardsDrawned == self.deck.numberPlayingCards:                
                return False

            self.currentCard = nextCard
            print(f"Your current score is: {self.score}")

            return True

    def mainLoop(self) -> None:
        print("Welcome to the Higher/Lower Card Game!")

        while self.playRound():
            pass

        print(f"Your final score is: {self.score}")

        print("Thanks for playing!")

if __name__ == "__main__":
    game = HigherLowerGame()
    game.configureSettings()
    game.mainLoop()

    
    
    



