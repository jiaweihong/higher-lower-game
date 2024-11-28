<p align="center"><img alt="logo" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS671ygHQI-Podn72Qg7pLtY5BHTUzN28tdDA&s" width="120px" /></p>
<h1 align="center">Higher Lower Game - Chicago Bulls Edition</h1>

<p align="center">
  <a href="#"><img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"></a>
  <a href="#"><img alt="CTKinter" src="https://img.shields.io/badge/CTKinter-029cff?style=for-the-badge&logoColor=38B2AC"></a>
  <a href="#"><img alt="Pillow" src="https://img.shields.io/badge/Pillow-343c3c?style=for-the-badge&logoColor=343C3"></a>
</p>

<p align="center">A higher lower card game with the option to enable a special Bulls edition mode which inserts special Micheal Jordan and Dennis Rodman cards into the deck.</p>

## Getting Started:

### Prerequisites:

- Python
- Poetry

Using `brew` package manager as an example:

```shell
# Install system dependencies
brew install python
# Install poetry
pipx ensurepath
pipx install poetry

# Install project dependencies
poetry install
```

### Usage:

Activate the Python virtual environment:

```shell
poetry shell
```

Start the application:

```shell
python3 main.py
```

## Design Explanation:

1. The option to include jokers was expanded upon with the option to enable the Bulls edition of the game. I chose the Bulls as Micheal Jordan is **the GOAT** and that their jerseys are also Red or Black.
2. Assuming Bulls edition is enabled, this will insert **2 MJ cards** into the 5th and 20th position, and also randomly inserts **4 Dennis Rodman cards**.
3. Drawing an MJ card, activates a special round whereby the player must complete the next 8 rounds in the following manner: **(W, W, W, L, L, W, W, W)**. This sequence reflects the Bulls double 3-peat in the NBA finals from 1991-1998.
   - 'W' means the player must guess correctly if the next card is higher/lower.
   - 'L' means the player must purposely guess wrongly.
   - Drawing a rodman card during this sequence does not contribute towards the round.
   - Doing so correctly will give 10 bonus points.
4. Drawing a Rodman card will give players a **2nd chance** on the next card they get wrong, and doubles the point of the next card if guessed correctly. This ability was chosen as Rodman was known for his rebounding (essentially providing players with a 2nd shot).
5. I added a **'True Sight'** option which shows you what the next card will be. This allows the player to test and make sure that all the features are working as intended without wasting time.
6. If a special card is drawn, the **previous normal card** will be kept as the current card.
7. If 2 cards are the same rank, then the game will compare it by suit in the order of weakest to strongest: diamonds, clubs, hearts, spades.

## Implementation Explanation:

1. Inside the HigherLowerGame class, I initialise a normalCardsDrawned attribute which we need to keep count of,since the game ends when either the player incorrectly guesses or all the **normal cards** have been drawn, and the deck contains both special and normal cards so just checking when the length of deck == 0 would not work.
2. The MJ cards are inserted as specified positions (instead of being random) since they require atleast 8 remaining normal cards to play so if they were initialised towards the end, there may not be sufficient cards. It also prevents the MJ cards from being within 8 cards of each other.
3. The top card is always guranteed to be a normal card because I think it would be weird if you immediately got a special card as the 1st card.

## Improvements:

1. I think the higher lower handling logic of the game (HigherLowerGame.playRound) is a bit messy. There are a bit too many nested if else statements that make it a little bit hard to understand, so I would refine the logic.
2. Since the CLI implementation was developed first, then only the GUI application. The final game was not designed with the MVC design pattern in mind and therefore not adhered to very well. The view (GUI) layer often directly interacts and changes the data of the Model (Game). I would develop the interface with the Model with the MVC model in mind next time.
3. I would also change the deck's data structure from a stack to a queue (deque). Since we don't actually need the LIFO principle of a stack as cards are not being readded to the pile. Using a queue would make indexing simpler. Currently in the code, when I'm trying to get the ith card (from the top), I always need to do cardsStack[(length of cards - ith card)], whereas a queue would allow me to use 'i' directly like cardsQueue[i].
4. I would make the game a bit prettier, its currently looking a bit rough :p
