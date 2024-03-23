import pygame
import sys
import os
from pygame import *
from random import randint

def resourse_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    elif hasattr(sys, "_MEIPASS2"):
        return os.path.join(sys._MEIPASS2, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)

image_folder = resourse_path(".")

init()
mixer.init()
font.init()
font_big = font.Font(None, 50)
font_small = font.Font(None, 30)
W = 700
H = 500
FPS = 60
SCORE = 0
LOST = 0
RED = 118, 15, 15
YELLOW = 213, 219, 47
speed = 5
diffi = 1
background = os.path.join(image_folder, "galaxy.jpg")
img_hero = os.path.join(image_folder, "rocket.png")
img_bullet = os.path.join(image_folder, "bullet.png")
img_ufo = os.path.join(image_folder, "ufo.png")
img_ast = os.path.join(image_folder, "asteroid.png")
snd_back = os.path.join(image_folder, "space.ogg")
snd_fire = os.path.join(image_folder, "fire.ogg")
snd_dam = os.path.join(image_folder, "damage.ogg")
RELOAD_EVENT = pygame.USEREVENT + 1
bullet_image = pygame.image.load(img_bullet)
bullet_image = pygame.transform.scale(bullet_image, (20, 20))
bullet_counter_font = pygame.font.Font(None, 50)



back = mixer.Sound(snd_back)
back.set_volume(0.3)
back.play()
fire = mixer.Sound(snd_fire)
damage = mixer.Sound(snd_dam)
damage.set_volume(0.1)

font_text = font.Font(None, 36)
font_reload = pygame.font.Font(None, 50)
reload_text = font_reload.render('Перезарядка', True, RED)

window = display.set_mode((W , H))
display.set_caption('Shooter2DEngine')
clock = time.Clock()
background = transform.scale(image.load(background), (W,H))

def final():
    game = False

def game_restart_up():
    global game, SCORE, LOST, player, monsters, bullets, diffi
    if(diffi == 10):
        final()
    else:
        diffi += 1
    game = True
    back.stop()
    back.play()
    SCORE = 0
    LOST = 0
    monsters.empty()
    bullets.empty()
    asteroids.empty()
    player = Player(img_hero, 5, H -100, 100, 100, 10)  # создаем нового игрока
    player.ammo = 10  # сбрасываем счетчик патронов
    for i in range(diffi):
        monster = Enemy(img_ufo, randint(80, W - 80), -40, 50, 100, randint(1, 5))
        monsters.add(monster)
        asteroid = Asteroid(img_ast, randint(80, W - 80), -40, 70, 70, randint(1, 5))
        asteroids.add(asteroid)

def game_restart():
    global game, SCORE, LOST, player, monsters, bullets, diffi
    diffi = 1
    game = True
    back.stop()
    back.play()
    SCORE = 0
    LOST = 0
    monsters.empty()
    bullets.empty()
    asteroids.empty()
    player = Player(img_hero, 5, H -100, 100, 100, 10)  # создаем нового игрока
    player.ammo = 10  # сбрасываем счетчик патронов
    # создаем нового игрока
    for i in range(diffi):
        monster = Enemy(img_ufo, randint(80, W - 80), -40, 50, 100, randint(1, 5))
        monsters.add(monster)
        asteroid = Asteroid(img_ast, randint(80, W - 80), -40, 70, 70, randint(1, 5))
        asteroids.add(asteroid)

def game_restart_r():
    global game, SCORE, LOST, player, monsters, bullets, diffi
    game = True
    back.stop()
    back.play()
    SCORE = 0
    LOST = 0
    monsters.empty()
    bullets.empty()
    asteroids.empty()
    player = Player(img_hero, 5, H -100, 100, 100, 10)  # создаем нового игрока
    player.ammo = 10  # сбрасываем счетчик патронов
    # создаем нового игрока
    for i in range(diffi):
        monster = Enemy(img_ufo, randint(80, W - 80), -40, 50, 100, randint(1, 5))
        monsters.add(monster)
        asteroid = Asteroid(img_ast, randint(80, W - 80), -40, 70, 70, randint(1, 5))
        asteroids.add(asteroid)


class GameSprite(sprite.Sprite):
    def __init__(self, p_image: str, x: int, y: int, h: int, w: int, speed: int):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x , self.rect.y))

class Player(GameSprite):
    def __init__(self, p_image: str, x: int, y: int, h: int, w: int, speed: int):
        super().__init__(p_image, x, y, h, w, speed)
        self.ammo = 10  # количество патронов в обойме
        self.reloading = False  # состояние перезарядки

    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < W - 80:
            self.rect.x += self.speed

    def fire(self):
        if not self.reloading and self.ammo > 0:
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 5)
            bullets.add(bullet)
            fire.play()
            self.ammo -= 1
        elif self.ammo == 0 and not self.reloading:
            self.reloading = True
            pygame.time.set_timer(RELOAD_EVENT, 1000)  # начинаем перезарядку на 3 секунды

    def reload(self):
        self.ammo = 10  # восстанавливаем обойму
        self.reloading = False  # заканчиваем перезарядку

# в главном цикле игры добавьте обработку события USEREVENT
for e in event.get():
    if e.type == QUIT:
        game = False
    elif e.type == MOUSEBUTTONDOWN:
        if e.button == 1:  # 1 обозначает левую кнопку мыши
            player.fire()
    elif e.type == KEYDOWN:
        if e.key == K_y:
            game = False
        if e.key == K_r:
            game = False
            game_restart_r()
    elif e.type == [K_f]:
        player.reload()
    elif e.type == pygame.USEREVENT:  # событие перезарядки
        player.reload()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global LOST
        if self.rect.y >= H:
            self.rect.x = randint(5, 600)
            self.rect.y = 0
            LOST += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= H:
            self.rect.x = randint(5, 600)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

monsters = sprite.Group()

asteroids = sprite.Group()

for i in range(diffi):
    monster = Enemy(img_ufo, randint(80, W - 80), -40, 50, 100, randint(1, 5))
    monsters.add(monster)
    asteroid = Asteroid(img_ast, randint(80, W - 80), -40, 70, 70, randint(1, 5))
    asteroids.add(asteroid)

player = Player(img_hero, 5, H -100, 100, 100, 10)
game = True

while game:
    window.blit(background,(0, 0))
    player.reset()
    player.update()
    monsters.draw(window)
    monsters.update()
    bullets.draw(window)
    bullets.update()
    asteroids.draw(window)
    asteroids.update()

    # Обнаружение столкновений
    hits = sprite.groupcollide(monsters, bullets, True, True)
    hita = sprite.groupcollide(asteroids, bullets, True, True)
    for hit in hits:
        SCORE += 1
        monster = Enemy(img_ufo, randint(80, W - 80), -40, 50, 100, randint(1, 5))
        monsters.add(monster)
    for hit in hita:
        SCORE += 1


    if sprite.spritecollide(player, monsters, False):
        back.stop()
        damage.play()
        text = font_big.render('YOU LOSE', True, RED)
        window.blit(text, (W // 2 - text.get_width() // 2, H // 2 - text.get_height() // 2))
        display.update()
        time.wait(2000)
        game_restart()

    if sprite.spritecollide(player, asteroids, False):
        back.stop()
        damage.play()
        text = font_big.render('YOU LOSE', True, RED)
        window.blit(text, (W // 2 - text.get_width() // 2, H // 2 - text.get_height() // 2))
        display.update()
        time.wait(2000)
        game_restart()

    if LOST == 3:
        back.stop()
        text = font_big.render('YOU LOSE', True, RED)
        window.blit(text, (W // 2 - text.get_width() // 2, H // 2 - text.get_height() // 2))
        display.update()
        time.wait(2000)
        game_restart()

    if SCORE == 10:
        back.stop()
        text = font_big.render('YOU WON!', True, YELLOW)
        window.blit(text, (W // 2 - text.get_width() // 2, H // 2 - text.get_height() // 2))
        display.update()
        time.wait(2000)
        game_restart_up()
    if player.reloading:
        window.blit(reload_text, (W // 2 - reload_text.get_width() // 2, H - reload_text.get_height()))
    
    score_text = font_text.render("Сбили: " + str(SCORE), True, (255, 255, 255))
    lost_text = font_text.render("Упустили: " + str(LOST), True, (255, 255, 255))
    level_text = font_text.render("Уровень: " + str(diffi), True, (255, 255, 255))
    ammo_text = bullet_counter_font.render(str(player.ammo), True, (255, 255, 255))
    window.blit(ammo_text, (W - ammo_text.get_width() - 20, H - ammo_text.get_height() - 20))
    window.blit(bullet_image, (W - ammo_text.get_width() - bullet_image.get_width() - 30, H - bullet_image.get_height() - 20))
    window.blit(score_text, (10, 20))
    window.blit(lost_text, (10, 50))
    window.blit(level_text, (10, 80))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:  # 1 обозначает левую кнопку мыши
                player.fire()
        elif e.type == KEYDOWN:
            if e.key == K_y:
                game = False
            if e.key == K_r:
                game = False
                game_restart_r()
            if e.key == K_f:
                player.reload()
        elif e.type == RELOAD_EVENT:  # событие перезарядки
            player.reload()
            pygame.time.set_timer(RELOAD_EVENT, 0)  # отключаем таймер перезарядки

    display.update()
    clock.tick(FPS)