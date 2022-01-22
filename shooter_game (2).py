from pygame import*
from random import randint
 
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
#шрифты и надписи
font.init()
font1 = font.SysFont('Arial', 65)
font2 = font.SysFont('Arial', 30)

win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))


#нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг
img_bullet = "bullet.png" # пуля

max_lost = 3
goal = 11




score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
 
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
#конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
#Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
 
#каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
#каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
#метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
#метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
#метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        
        #if keys[SPACE] and len(bullets) < 5:
        bullets.add(bullet)       
#класс спрайта-врага  
class Enemy(GameSprite):
#движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
#исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

#класс пули
class Bullet(GameSprite):
#движение пули
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < -10:
            self.kill()
 
#Создаём окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
#создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = sprite.Group()
for i in range(1, 7):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()
 
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
#событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            run = False

            
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if len(bullets) < 5:
                    fire_sound.play()
                    ship.fire()
 
    if not finish:
#обновляем фон
        window.blit(background,(0,0))
 
       #пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))



        if score == 10:
            text = font2.render("YOU WIN!", 1, (255, 255, 255))
            window.blit(text(300, 300))
            text_lose = font2.render("Пропущено: " + str(lost, 1, (255, 255, 255)))
            window.blit(text_lose, (300, 330))
            finish = True
        
        if lost == 3 or sprite.collide_rect(ship, monsters):
            text = font2.render("YOU LOSE!", 1, (255, 255, 255))
            window.blit(text(300, 300))
            text_lose = font2.render("Счёт: " + str(score, 1, (255, 255, 255)))
            window.blit(text_lose, (300, 330))







    
 


        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides:
            score +=1
            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            window.blit(lose, (200,200))
            finish = True

        if score == goal:
            window.blit(win, (200, 200))
            #score = 10

            finish = True
        
               #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
       #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        display.update()

        display.update()
   #цикл срабатывает каждую 0.05 секунд
    time.delay(50)