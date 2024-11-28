
from src.game import HigherLowerGame
from src.gui import HigherLowerApp

if __name__ == "__main__":
    game = HigherLowerGame()
    app = HigherLowerApp(game)
    app.mainloop()