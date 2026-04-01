import pytest
from game import SpaceShooter


@pytest.fixture
def game(qtbot):
    g = SpaceShooter()
    qtbot.addWidget(g)
    g.timer.stop()
    return g


def test_player_initial_position(game):
    assert game.player.width() == 40
    assert game.player.height() == 40
    assert game.player.y() > 0


def test_shoot_creates_bullet(game):
    initial_bullets = len(game.bullets)
    game.shoot()
    assert len(game.bullets) == initial_bullets + 1


def test_bullet_moves_up(game):
    game.shoot()
    bullet = game.bullets[0]
    initial_y = bullet.y()

    game.game_loop()

    assert bullet.y() < initial_y


def test_spawn_enemy(game):
    initial_enemies = len(game.enemies)
    game.spawn_enemy()
    assert len(game.enemies) == initial_enemies + 1


def test_bullet_hits_enemy(game):
    game.shoot()
    bullet = game.bullets[0]

    enemy = bullet
    game.enemies.append(enemy)

    game.game_loop()

    assert game.score == 10
    assert len(game.enemies) == 0


def test_enemy_hits_player(game):
    enemy = game.player
    game.enemies.append(enemy)

    game.game_loop()

    assert game.game_over is True


def test_reset_game(game):
    game.score = 100
    game.enemies.append(game.player)
    game.game_over = True

    game.reset_game()

    assert game.score == 0
    assert game.game_over is False
    assert len(game.enemies) == 0
