import pygame
import os
import sys
import random
import sqlite3

pygame.init()
size = width, height = 1100, 600
screen = pygame.display.set_mode(size)
enemies = pygame.sprite.Group()
fps = 60
clock = pygame.time.Clock()
con = sqlite3.connect("Game.db")
cur = con.cursor()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Scp049(pygame.sprite.Sprite):
    image = pygame.transform.flip(pygame.transform.scale(load_image("scp_049.png", -1), (260, 200)), True, False)

    def __init__(self):
        super().__init__(enemies)
        self.image = Scp049.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(700, 900)
        self.rect.y = random.randrange(250, 400)
        self.x = self.rect.x  # истиное положение
        self.money = 6
        self.hp = 200
        self.speed = 43  # пикселей в секунду

    def update(self, effect):
        global money
        if self.hp <= 0:
            money += self.money
            enemies.remove(self)
            return
        if effect != 0:
            self.x -= self.speed * effect / fps
        else:
            self.x -= self.speed / fps  # self.x - не целое
        self.rect.x = int(self.x)


class Scp049Two(Scp049):
    image = pygame.transform.flip(pygame.transform.scale(load_image("scp_049-2.png", -1), (170, 225)), True, False)

    def __init__(self):
        super().__init__()
        self.image = Scp049Two.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(700, 900)
        self.rect.y = random.randrange(250, 400)
        self.x = self.rect.x  # Истиное положение по x
        self.money = 1
        self.hp = 100
        self.speed = 58  # пикселей в секунду


class Scp106(Scp049):
    image = pygame.transform.flip(pygame.transform.scale(load_image("scp_106.png"), (90, 225)), True, False)

    def __init__(self):
        super().__init__()
        self.image = Scp106.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(700, 900)
        self.rect.y = random.randrange(250, 400)
        self.x = self.rect.x
        self.money = 20
        self.hp = 300
        self.speed = 43  # пикселей в секунду


class Scp173(Scp049):
    image = pygame.transform.flip(pygame.transform.scale(load_image("scp_173.png"), (90, 270)), True, False)

    def __init__(self):
        super().__init__()
        self.image = Scp173.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(700, 900)
        self.rect.y = random.randrange(250, 400)
        self.x = self.rect.x
        self.money = 5
        self.hp = 70
        self.speed = 116  # пикселей в секунду


class Scp178One(Scp049):
    image = pygame.transform.flip(pygame.transform.scale(load_image("scp_178-1.png", -1), (400, 225)), True, False)

    def __init__(self):
        super().__init__()
        self.image = Scp178One.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(700, 900)
        self.rect.y = random.randrange(250, 400)
        self.x = self.rect.x
        self.money = 6
        self.hp = 100
        self.speed = 34  # пикселей в секунду


class Scp682(Scp049):
    image = pygame.transform.scale(load_image("scp_682.png"), (350, 200))

    def __init__(self):
        super().__init__()
        self.image = Scp682.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(700, 900)
        self.rect.y = random.randrange(250, 400)
        self.x = self.rect.x
        self.money = 40
        self.hp = 700
        self.speed = 26  # пикселей в секунду


def terminate():
    pygame.quit()
    sys.exit()


def generate_enemies(level):
    for _ in range(1):
        Scp049Two()
    for _ in range(1):
        Scp173()
    for _ in range(level):
        Scp682()
    for _ in range(level):
        Scp178One()
    for _ in range(level):
        Scp049()
    for _ in range(level):
        Scp106()
    sorted_enemies = sorted(enemies.sprites(), key=lambda scp: scp.rect.y + scp.rect.height)  # сортирует по низу
    enemies.empty()
    for i in sorted_enemies:
        enemies.add(i)


def save(level, money):
    cur.execute("""UPDATE save
                    SET level = ?,
                        money = ?,
                        hero_1 = ?,
                        hero_2 = ?,
                        hero_3 = ?,
                        hero_4 = ?,
                        hero_5 = ?,
                        hero_6 = ?""", (level, money))  # дозаполнить
    con.commit()


def play(args):
    fon_sprites = pygame.sprite.Group()
    fon_sprite = pygame.sprite.Sprite()
    fon_sprite.image = pygame.transform.scale(load_image("fon_1.png"), (1100, 600))
    fon_sprite.rect = fon_sprite.image.get_rect()
    fon_sprites.add(fon_sprite)

    barricade_sprites = pygame.sprite.Group()
    barricade_sprite = pygame.sprite.Sprite()
    barricade_sprite.image = pygame.transform.scale(load_image("barricade.png"), (150, 150))
    barricade_sprite.rect = barricade_sprite.image.get_rect()
    barricade_sprite.rect.x = 210
    barricade_sprite.rect.y = 290
    barricade_sprites.add(barricade_sprite)

    barricade_2_sprite = pygame.sprite.Sprite()
    barricade_2_sprite.image = barricade_sprite.image
    barricade_2_sprite.rect = barricade_2_sprite.image.get_rect()
    barricade_2_sprite.rect.x = 210
    barricade_2_sprite.rect.y = 380
    barricade_sprites.add(barricade_2_sprite)

    barricade_3_sprite = pygame.sprite.Sprite()
    barricade_3_sprite.image = barricade_sprite.image
    barricade_3_sprite.rect = barricade_3_sprite.image.get_rect()
    barricade_3_sprite.rect.x = 210
    barricade_3_sprite.rect.y = 470
    barricade_sprites.add(barricade_3_sprite)

    pygame.mixer.music.load('sounds_and_music/level.mp3')
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)

    level = args[1]
    money = args[2]

    attack = False
    lose = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save(level, money)
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save(level, money)
                    pygame.mixer.music.load('sounds_and_music/main_menu.mp3')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)
                    return
                if event.key == pygame.K_w and not attack:
                    attack = True
                    generate_enemies(level)
        if attack:
            if len(enemies.sprites()) == 0:  # проверка на победу
                attack = False
                level += 1
            elif len(pygame.sprite.groupcollide(enemies, barricade_sprites, False, False)) != 0:  # проверка на проигрыш
                lose = True
            scp_049 = scp_106 = scp_178 = 0
            for i in enemies.sprites():  # считается кол-во врагов, которые могут накладывать эффекты
                if isinstance(i, Scp049):
                    scp_049 += 1
                elif isinstance(i, Scp106):
                    scp_106 += 1
                elif isinstance(i, Scp178One):
                    scp_178 += 1
            enemies.update(scp_049 * 0.05 + 1)  # scp 049 увеличивает скорость на 5 %. Эффект сумируется
        fon_sprites.draw(screen)
        barricade_sprites.draw(screen)
        enemies.draw(screen)
        if lose:
            lose = False
            attack = False
            enemies.empty()
            text_lose = font.render("Вы проиграли", 1, (0, 0, 0))
            text_lose_x = width // 2 - text_lose.get_width() // 2
            text_lose_y = 100
            screen.blit(text_lose, (text_lose_x, text_lose_y))
            pygame.display.flip()
            restart = True
            while restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        save(level, money)
                        terminate()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            save(level, money)
                            pygame.mixer.music.load('sounds_and_music/main_menu.mp3')
                            pygame.mixer.music.set_volume(0.3)
                            pygame.mixer.music.play(-1)
                            return
                        if event.key == pygame.K_SPACE:
                            restart = False
        clock.tick(fps)
        pygame.display.flip()


menu_sprites = pygame.sprite.Group()
menu_sprite = pygame.sprite.Sprite()
menu_sprite.image = pygame.transform.scale(load_image("main_menu.png"), (1100, 600))
menu_sprite.rect = menu_sprite.image.get_rect()
menu_sprites.add(menu_sprite)

pygame.mixer.music.load('sounds_and_music/main_menu.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and text_y <= event.pos[1] <= text_y + text.get_height() + 20:
                if text_x <= event.pos[0] <= text_x + text.get_width() + 20:  # кнопка НОВАЯ ИГРА
                    cur.execute("""UPDATE save
                                    SET level = '1',
                                        money = '0',
                                        hero_1 = '1 1',
                                        hero_2 = hero_3 = hero_4 = hero_5 = hero_6 = ''""")
                    con.commit()
                    play(cur.execute("""SELECT * FROM save""").fetchone())
                elif text_2_x <= event.pos[0] <= text_2_x + text_2.get_width() + 20:  # кнопка ЗАГРУЗИТЬ ИГРУ
                    play(cur.execute("""SELECT * FROM save""").fetchone())
                elif text_3_x <= event.pos[0] <= text_3_x + text_3.get_width() + 20:  # кнопка ВЫХОД
                    running = False

    menu_sprites.draw(screen)

    font = pygame.font.Font(None, 50)  # кнопка ИГРАТЬ
    text = font.render("Новая игра", 1, (0, 0, 0))
    text_x = 100
    text_y = 490
    pygame.draw.rect(screen, (255, 255, 255), (text_x, text_y, text.get_width() + 20, text.get_height() + 20))
    screen.blit(text, (text_x + 10, text_y + 10))

    text_2 = font.render("Загрузить игру", 1, (0, 0, 0))  # кнопка ЗАГРУЗИТЬ ИГРУ
    text_2_x = 450
    text_2_y = 490
    pygame.draw.rect(screen, (255, 255, 255), (text_2_x, text_2_y, text_2.get_width() + 20, text_2.get_height() + 20))
    screen.blit(text_2, (text_2_x + 10, text_2_y + 10))

    text_3 = font.render("Выход", 1, (0, 0, 0))  # кнопка ВЫХОД
    text_3_x = 850
    text_3_y = 490
    pygame.draw.rect(screen, (255, 255, 255), (text_3_x, text_3_y, text_3.get_width() + 20, text_3.get_height() + 20))
    screen.blit(text_3, (text_3_x + 10, text_3_y + 10))

    pygame.display.flip()
