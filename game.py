import random
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont, QRadialGradient, QBrush
from PySide6.QtCore import Qt, QTimer, QRect

WIDTH = 800
HEIGHT = 600


class SpaceShooter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Space Shooter")
        self.setFixedSize(WIDTH, HEIGHT)
        self.setFocusPolicy(Qt.StrongFocus)

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(30)

        self.reset_game()

    def reset_game(self):
        self.player = QRect(WIDTH//2 - 20, HEIGHT - 60, 40, 40)
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.game_over = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            if self.player.left() > 0:
                self.player.translate(-20, 0)

        elif event.key() == Qt.Key_D:
            if self.player.right() < WIDTH:
                self.player.translate(20, 0)


        elif event.key() == Qt.Key_Space:
            self.shoot()

        elif event.key() == Qt.Key_R and self.game_over:
            self.reset_game()

    def shoot(self):
        bullet = QRect(self.player.x() + 15, self.player.y(), 10, 20)
        self.bullets.append(bullet)

    def spawn_enemy(self):
        x = random.randint(0, WIDTH - 40)
        enemy = QRect(x, 0, 40, 40)
        self.enemies.append(enemy)

    def game_loop(self):
        if self.game_over:
            return

        enemy_speed = 3 + self.score // 100

        for b in self.bullets:
            b.translate(0, -10)

        self.bullets = [b for b in self.bullets if b.y() > 0]

        for e in self.enemies:
            e.translate(0, enemy_speed)

        if random.random() < 0.03:
            self.spawn_enemy()

        for e in self.enemies:
            if e.intersects(self.player):
                self.game_over = True

        for b in self.bullets[:]:
            for e in self.enemies[:]:
                if b.intersects(e):
                    self.score += 10
                    if e in self.enemies:
                        self.enemies.remove(e)
                    if b in self.bullets:
                        self.bullets.remove(b)

        self.update()

    def draw_player(self, painter):
        x = self.player.x()
        y = self.player.y()

        painter.setBrush(QColor(139, 69, 19))
        painter.drawRect(x, y + 20, 40, 20)

        painter.setBrush(QColor(160, 82, 45))
        painter.drawRect(x + 5, y + 10, 30, 10)

        painter.setBrush(QColor(200, 200, 200))
        painter.drawRect(x + 12, y, 16, 12)

        painter.setBrush(QColor(100, 200, 255))
        painter.drawRect(x + 14, y + 2, 4, 4)
        painter.drawRect(x + 22, y + 2, 4, 4)

        painter.setBrush(QColor(80, 40, 20))
        painter.drawRect(x + 19, y - 10, 2, 10)

        painter.setBrush(QColor(255, 0, 0))
        painter.drawRect(x + 21, y - 10, 8, 5)

    def draw_bullet(self, painter, b):
        gradient = QRadialGradient(b.center(), 10)
        gradient.setColorAt(0, QColor(255, 0, 0))
        gradient.setColorAt(1, QColor(255, 165, 0))

        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(b)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(135, 206, 235))

        self.draw_player(painter)

        for b in self.bullets:
            self.draw_bullet(painter, b)

        painter.setBrush(QColor(255, 0, 0))
        for e in self.enemies:
            painter.drawEllipse(e)

        painter.setPen(QColor(0, 0, 0))
        painter.setFont(QFont("Arial", 14))
        painter.drawText(10, 20, f"Score: {self.score}")

        if self.game_over:
            painter.setFont(QFont("Arial", 24))
            painter.drawText(self.rect(), Qt.AlignCenter, "GAME OVER\nPress R")

