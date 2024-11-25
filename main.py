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
    # (Note: 0-indexed) 
    MJ_LOCATIONS = [4,19]
    MJ_WINNING_SEQUENCE = [1,1,1,0,0,1,1,1]
    MJ_BONUS_POINTS = 10
    RODMAN_BONUS_POINTS = 2

class Card:
    def __init__(self, rank: Rank, suit: Suit):
        """
        Initialises a playing card (can be normal or special card)

        :param rank: rank of the card
        :param suit: suit of the card
        :param value: the value of the card to allow comparison
        """
        self.rank: Rank = rank
        self.suit: Suit = suit
        self.value: int = rank.value + suit.value
    
    def getName(self) -> str:
        """
        Returns the card's name
        """
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self, isBullsEdition: bool):
        """
        Initialises a deck of, already shuffled and ready to use, playing cards

        :param isBullsEdition: if true, adds the corresponding special cards
        """
        self.cards: list[Card] = []
        self.numberPlayingCards: int = 0
        
        # initialise the playing cards according to the enum classes, skipping the special cards
        for rank in Rank:
            if rank in (Rank.MJ, Rank.RODMAN):
                continue
            for suit in Suit:
                if suit == Suit.BULLS:
                    continue
                
                self.numberPlayingCards += 1
                self.cards.append(Card(rank, suit))

        # insert Rodman cards
        if isBullsEdition:
            for _ in range(Constraints.NUM_RODMAN_CARDS.value):
                self.cards.append(Card(Rank.RODMAN, Suit.BULLS))
        
        self.shuffle()

        # assuming we are playing the special mode, this ensure the 1st card we draw is always a normal card.
        while isBullsEdition and self.seeTopCard().rank in (Rank.MJ, Rank.RODMAN):
            self.shuffle()

        # after ensuring top card is a normal card, insert MJ cards into appropriate places
        if isBullsEdition:
            self.insertMjCards()
    
    def printDeck(self) -> None:
        """
        Prints the entire deck
        """
        res: list[str] = []
        for card in self.cards:
            res.append(f"{card.getName()}")

        print()
        print(res)
        print()

    
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
        for i in Constraints.MJ_LOCATIONS.value:
            self.cards.insert(len(self.cards)-i, Card(Rank.MJ, Suit.BULLS))


class HigherLowerGame:
    def __init__(self, isBullsEdition:bool=False):
        """
        Initialises the high level game object
        """
        self.currentCard: Card = None
        self.cardsDrawned: int = 0
        self.deck: Deck = None
        self.isBullsEdition: bool = isBullsEdition
        self.currentRodmanCards: int = 0
        self.currentMjRound: int = 0
        self.currentMjSequence: list[int] = []
        self.isMjActivated = False
        self.isRodmanActivated: bool = False
        self.isBullsEdition: bool = False
        self.cardsDrawned: int = 0
        self.score: int = 0
    
    def configureSettings(self) -> None:
        """
        Initialises the appropriate deck depending on the user's game preference
        """
        isSpecialRound: str = self.getSpecialRoundInput()
        if isSpecialRound == "Y":
            print("Bulls Edition enabled! Special MJ and Rodman cards are in play!")
            self.isBullsEdition = True
        
        self.deck = Deck(self.isBullsEdition)

    def compareCards(self, currentCard: Card, nextCard: Card, userInput: str) -> bool:
        """
        Returns a boolean depending on if the user correctly guesses the next card's value
        """
        if (nextCard.value > currentCard.value and userInput == "H") or (nextCard.value < currentCard.value and userInput == "L"):
            return True
        else:
            return False
    
    def getHigherLowerInput(self, currentCard: Card) -> str:
        """
        Returns the user's guess on the next card's value

        :params currentCard: the user's current card
        """
        res: str = input(f"Your current card: {currentCard.getName()}, is the next card Higher (H) or Lower (L)? ").strip().upper()

        while res not in ("H", "L"):
            res = input("Please input the characters: H or L. ").strip().upper()

        return res

    def getSpecialRoundInput(self) -> str:
        """
        Returns the user's guess on the next card's value
        """
        res: str = input("Do you want to enable the special Chicago Bulls Edition of the Game? Yes (Y) or No (N) ").strip().upper()

        while res not in ("Y", "N"):
            res = input("Please input the characters: Y or N. ").strip().upper()

        return res
        
    def playRound(self) -> bool:
        """
        Contains the main game logic to handle the players move
        """
        #print(f"Next card is: {self.deck.seeTopCard().getName()}")
        
        if self.isMjActivated:
            print(f"You are currently on MJ round number {self.currentMjRound+1} / f{len(Constraints.MJ_WINNING_SEQUENCE.value)}")

        userInput: str = self.getHigherLowerInput(self.currentCard)
        
        nextCard: Card = self.deck.drawCard()

        if nextCard.rank == Rank.MJ:
            print(f"Congratulations you got the Micheal Jordan card, activating special MJ round...")
            self.isMjActivated = True
            
            return True
        elif nextCard.rank == Rank.RODMAN:
            # Drawing a rodman card does not update the currentCard since it is only meant to hold playing cards 
            self.currentRodmanCards += 1
            print(f"Congratulations you got a Rodman Card, you currently have {self.currentRodmanCards} Rodman Cards")

            return True
        else: # next card is NOT a special card
            print(f"The card was a {nextCard.getName()}")
            isCorrect: bool = self.compareCards(self.currentCard, nextCard, userInput)
            
            # need to increment before if statements so, because if we are on the last card, the game needs to know that this is the last round
            self.cardsDrawned += 1

            if self.isMjActivated:
                if isCorrect:
                    print("Correct you got 1 point!")
                    self.score += 1
                    self.currentMjSequence.append(1)
                else:
                    self.currentMjSequence.append(0)
                
                # Check as soon as we finish playing the final MJ round
                self.currentMjRound += 1

                if self.currentMjRound == len(Constraints.MJ_WINNING_SEQUENCE.value):
                    if self.currentMjSequence == Constraints.MJ_WINNING_SEQUENCE.value:
                        print("Congratulations you won the MJ round! You get 10 extra bonus points!!")
                        self.score += Constraints.MJ_BONUS_POINTS.value
                        self.isMjActivated = False
                    else:
                        print("Unfortunately you did not win any bonus points!")
                        print(f"Your sequence was {self.currentMjSequence}, the required sequence is {Constraints.MJ_WINNING_SEQUENCE.value}")

                    print("Exiting Special MJ Round...")

                    # Reset MJ related attributes
                    self.isMjActivated = False
                    self.currentMjRound = 0
                    self.currentMjSequence = []
            elif isCorrect and self.isRodmanActivated:
                print(f"Rebounded by Rodman and you made the shot! You got {Constraints.RODMAN_BONUS_POINTS.value} points")

                self.score += Constraints.RODMAN_BONUS_POINTS.value
                self.isRodmanActivated = False
            elif isCorrect:
                print("Correct you got 1 point!")
                self.score += 1
            else:
                print("Incorrect!")

                if self.isBullsEdition and self.currentRodmanCards > 0 and self.cardsDrawned < self.deck.numberPlayingCards:
                    self.currentRodmanCards -= 1
                    print("You activated a Rodman card! You get a second chance. Get the next card right to win double points!")
                    self.isRodmanActivated = True
                else: # this means u either have no rodman cards or u are playing normal version of the game
                    print()
                    return False

            if self.cardsDrawned == self.deck.numberPlayingCards:
                print()
                return False

            self.currentCard = nextCard
            print(f"Your current score is: {self.score} \n")

            return True

    def mainLoop(self) -> None:
        """
        Loops indefinitely until the game is done
        """
        print("Welcome to the Higher/Lower Card Game! \n")

        # Draws the initial card for the user
        self.currentCard = self.deck.drawCard()
        self.cardsDrawned = 1

        while self.playRound():
            pass

        print(f"Your final score is: {self.score}")

        print("Thanks for playing!")

if __name__ == "__main__":
    game = HigherLowerGame()
    game.configureSettings()
    game.mainLoop()

    
    
    



