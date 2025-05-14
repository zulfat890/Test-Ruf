from pygame import *

display.set_caption('Лабиринт')
window = display.set_mode((700, 500))
BLACK = (0,0,0)
GREEN = (0,250,0)

class GameSprite(sprite.Sprite):
    def __init__(self,picture,w,h,x,y):
        super().__init__()
        self.image=transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
w1 = GameSprite('wall.jpg',120,400,300,100)
w2 = GameSprite('wall.jpg',370,100,50,400)


class Player(GameSprite):
    def __init__(self,picture,w,h,x,y):
        super().__init__(picture,w,h,x,y)
        self.x_speed = 0.5
        self.y_speed = 0.5
    def update(self):
        self.rect.x += self.x_speed
        platform_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platform_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platform_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.rect.y += self.y_speed
        platform_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platform_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platform_touched:
                    self.rect.top = max(self.rect.top, p.rect.bottom)       
player = Player('player.jpg',50,100,500,100)

final_sprite = GameSprite('monster.jpg',85,100,80,80)



class Enemy(GameSprite):
    def __init__(self,picture,w,h,x,y,speed):
        super().__init__(picture,w,h,x,y)
        self.speed = 1
    def update(self):
     if self.rect.x <= 420: #w1.wall_x + w1.wall_width
         self.side = "right"
     if self.rect.x >= - 85:
         self.side = "left"
     if self.side == "left":
         self.rect.x -= self.speed
     else:
         self.rect.x += self.speed
monster = Enemy('monster.jpg',100,200,450,200,1)


barriers = sprite.Group()


#создаем группу для пуль
bullets = sprite.Group()


#создаем группу для монстров
monsters = sprite.Group()
barriers.add(w1)

monster1 = Enemy('monster.jpg',80, 150, 80, 80, 5)


monsters.add(monster1)



font.init()
font = font.SysFont('Arial', 40)
win = font.render('YOU WIN!', True, BLACK)
los = font.render("YOU LOSE!", True, BLACK)
run = True
finish = False
while run:
    window.fill(GREEN)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                player.x_speed = -5
            elif e.key == K_RIGHT:
                player.x_speed = 5
            elif e.key == K_UP:
                player.y_speed = -5
            elif e.key == K_DOWN:
                player.y_speed = 5
            elif e.type == KEYUP:
                if e.key == K_LEFT:
                    player.x_speed = 0
            elif e.key == K_RIGHT:
                player.x_speed = 0
            elif e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_DOWN:
                player.y_speed = 0
    if not finish:
        player.update()
        bullets.update()
        player.reset()
        w1.reset()
        w2.reset()
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()
        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)
    if sprite.collide_rect(player, final_sprite):
        finish = True
        window.blit(win,(250,250))
    if sprite.collide_rect(player, monster1):
        finish = True
        window.blit(los,(250,250))
    time.delay(50)
    display.update()
