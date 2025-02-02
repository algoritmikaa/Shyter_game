from pygame import *
from random import randint
from time import time as timer

/

mixer.init()
mixer.music.load('fon.mp3')
mixer.music.play()
fire_sound = mixer.Sound('win1.mp3')


font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0 , 0))
font2 = font.Font(None, 36)



img_back = 'card2.jpg'
img_hero = 'card1.png'
img_bullet = 'karta.png'
img_enemy = '+4.jpg'


score = 0
goal = 10
lost = 0
mast_lost = 3
life = 3



class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):

        sprite.Sprite.__init__(self)



        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed



        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_width - 80:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 90, 100, -15)
        bullets.add(bullet)



class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = 0
            lost = lost + 1



class Bullet(GameSprite):

    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()



win_width = 1920
win_height = 1080
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))



ship = Player(img_hero, 5, win_height - 100, 150, 140, 10)


monsters = sprite.Group()
for i in range(1, 5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 50, 80, randint(1 , 4))
    monsters.add(monster)


bullets = sprite.Group()



finish = False

run = True


rel_time = False


num_fire = 0
while run:
    
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                
                if num_fire < randint(4,9) and rel_time == False:
                    num_fire = num_fire + 1
                    ship.fire()

                if num_fire >= randint(4,9) and rel_time == False :
                    last_time = timer()
                    rel_time = True

    if not finish:

        window.blit(background, (0,0))

        ship.update()
        monsters.update()
        bullets.update()

        

        ship.reset()
        monsters.draw(window)
        bullets.draw(window) 

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Отмена вашего хода...', 1, (255, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False




        colllides = sprite.groupcollide(monsters, bullets, True, True)
        for c in colllides:

            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 50, 80, randint(1 , 4))
            monsters.add(monster)


        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
            life = life -1

        if life == 0 or lost >= mast_lost:
            finish = True
            fire_sound.play()
            window.blit(lose, (200, 200))



        if score >= goal:
                finish = True
                window.blit(win, (200, 200))



        text = font2.render('Cчет: ' + str(score), 1, (255, 255,255))
        window.blit(text, (10 , 20))


        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255,255))
        window.blit(text_lose, (10 , 50))

        display.update()

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (1500, 0, 0)
        if life == 1:
            life_color = (0, 0, 150)

    else:
            finish = False
            score = -5
            lost = 0
            num_fire = 0
            life = 3
            for b in bullets:
                b.kill()
            for m in monsters:
                m.kill()


            time.delay(3000)
            for i in range(1, 7):
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 50, 80, randint(1, 6))
                monsters.add(monster)

    time.delay(35)
