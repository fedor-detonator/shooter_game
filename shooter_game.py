#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

window = display.set_mode((700, 500))
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)
display.set_caption('shooter game')

background = transform.scale(image.load('galaxy.jpg'), (700, 500))


LOSE = font2.render('YOU LOSE', 1, (255, 0, 0))
WIN = font2.render('YOU WIN', 1, (0, 255, 0))
ONE = font2.render('1', 1, (255, 9, 0))
TWO = font2.render('2', 1, (251, 255, 0))
THREE = font2.render('3', 1, (0, 255, 0))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

lost = 0
score = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 5, self.rect.top, -15, 15, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height, is_asteroid = False):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)
        self.is_asteroid = is_asteroid

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y == 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            if not self.is_asteroid:
                lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 6):
   monster = Enemy("ufo.png", randint(80, 620), -40, randint(1, 5), 80, 50)
   monsters.add(monster)

for i in range(1, 3):
    asteroid = Enemy("asteroid.png", randint(80, 620), -40, randint(1, 5), 80, 50, True)
    asteroids.add(asteroid)
player = Player("rocket.png", 350, 400, 10, 80, 100)
clock = time.Clock()

num_fire = 0
rel_time = False
lifes = 3
FPS = 40
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run  = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0))
        player.reset()
        player.update()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        bullets.update()
        monsters.update()
        asteroids.update()
        if lifes == 3:
            window.blit(THREE, (630, 30))
        
        if lifes == 2:
            window.blit(TWO, (630, 30))

        if lifes == 1:
            window.blit(ONE, (630, 30))

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                wait_reload = font2.render('Wait reload...', 1, (255, 0 ,0))
                window.blit(wait_reload, (150, 400))
                
            else:
                rel_time = False
                num_fire = 0


        collides = sprite.groupcollide(monsters, bullets, True, True)
        collides2 = sprite.groupcollide(asteroids, bullets, False, True)
        for c in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80, 620), -40, randint(1, 5), 80, 50)
            monsters.add(monster)
        
        if sprite.spritecollide(player, asteroids, True):
            lifes -= 1
            asteroid = Enemy("asteroid.png", randint(80, 620), -40, randint(1, 5), 80, 50, True)
            asteroids.add(asteroid)

        if lifes <= 0:
            finish = True
            window.blit(LOSE, (200, 200))

        if sprite.spritecollide(player, monsters, True):
            monster = Enemy("ufo.png", randint(80, 620), -40, randint(1, 5), 80, 50)
            monsters.add(monster)

        if score == 10:
            finish = True
            window.blit(WIN, (200, 200))
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        text_score = font1.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text_lose, (5, 5))
        window.blit(text_score, (5, 35))
    clock.tick(FPS)
    display.update()
