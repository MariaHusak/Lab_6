import sys
from game import SpaceShooter
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SpaceShooter()
    game.show()
    sys.exit(app.exec())
