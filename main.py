import pygame
from sys import exit
import math
from random import randint


class Health(pygame.sprite.Sprite):
    def __init__(self,x,y,immortal):
        super().__init__()
        if immortal == 0:
            self.image = pygame.image.load('Assets/Graphics/heart.png').convert_alpha()
        else:
            self.image = pygame.image.load('Assets/Graphics/absorption.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect(topleft=(x,y))


class Player(pygame.sprite.Sprite):
    def __init__(self, wall_list, bullet_list, enemy_list, x, y):
        super().__init__()
        self.original_image = pygame.Surface((40,40), pygame.SRCALPHA)
        self.original_image.fill((0,0,0))
        self.image = pygame.image.load('Assets/Graphics/player_sprite.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.angle = -90
        self.speed = 3

        self.change_x = 0
        self.change_y = 0
        self.wall_list = wall_list

        self.bullet_list = bullet_list
        self.bullet_speed = 5
        self.bullet_size = 10
        self.reload_speed = 300
        self.can_fire = True
        self.fire_time = 0

        self.enemy_list = enemy_list
        self.health = 3

        self.immortal = 0

    def display_health(self):
        health.empty()
        for i in range(self.health):
            health.add(Health(5+i*40,5,self.immortal))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.change_y = -self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            self.change_y = self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.change_x = -self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.change_x = self.speed

        # if keys[pygame.K_x] and self.immortal == 0:
        #     self.health -= 1
        #     self.immortal = 120
        #
        # if self.immortal != 0:
        #     self.immortal -= 1


        if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and self.can_fire:
            self.bullet_list.add(Player_Bullet(self.bullet_size,self.bullet_speed,self.rect))
            self.can_fire = False
            self.fire_time = pygame.time.get_ticks()
        if self.can_fire == False:
            if self.fire_time + self.reload_speed <= pygame.time.get_ticks():
                self.can_fire = True


    def wall_collision(self):
        wall_hit = pygame.sprite.spritecollide(self, self.wall_list, False)
        if wall_hit:
            self.rect.x -= self.change_x
            self.rect.y -= self.change_y
            self.change_x = 0
            self.change_y = 0

    def enemy_collision(self):
        global game_active
        enemy_hit = pygame.sprite.spritecollide(self, self.enemy_list, False)
        if enemy_hit and self.immortal == 0:
            self.health -= 1
            self.immortal = 120
            if self.health == 0:
                game_active = False
        if self.immortal != 0:
            self.immortal -= 1

        # if keys[pygame.K_w]:
        #     offset = 3
        #     radians = math.radians(self.angle)
        #     x = math.cos(radians) * -offset
        #     y = math.sin(radians) * offset
        #     self.rect.x += x
        #     self.rect.y += y
        # elif keys[pygame.K_s]:
        #     offset = -3
        #     radians = self.angle * math.pi / 180
        #     x = math.cos(radians) * -offset
        #     y = math.sin(radians) * offset
        #     self.rect.x += x
        #     self.rect.y += y
        # elif keys[pygame.K_a]:
        #     old_center = self.rect.center
        #     self.angle += 2.5
        #     self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        #     self.rect = self.image.get_rect(center=old_center)
        # elif keys[pygame.K_d]:
        #     old_center = self.rect.center
        #     self.angle -= 2.5
        #     self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        #     self.rect = self.image.get_rect(center=old_center)

    def update(self):
        self.player_input()
        self.wall_collision()
        self.enemy_collision()
        self.display_health()


class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        stone_bricks = pygame.image.load('Assets/Graphics/polished_blackstone_bricks.png')
        stone_bricks = pygame.transform.scale(stone_bricks,(40,40))
        self.image = stone_bricks.convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.x = x
        self.y = y


class Floor(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        stone = pygame.image.load('Assets/Graphics/stone.png')
        stone = pygame.transform.scale(stone, (40, 40))
        self.image = stone.convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))


class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self,size,speed,player_rect):
        super().__init__()
        self.size = size
        self.speed = speed
        self.image = pygame.image.load('Assets/Graphics/player_bullet.png')
        self.image = pygame.transform.scale(self.image,(self.size,self.size))
        self.rect = self.image.get_rect(center=(player_rect.center))
        x, y = pygame.mouse.get_pos()
        x_1, y_1 = self.rect.center
        v_x = x - x_1
        v_y = y - y_1
        magnitude = math.sqrt(math.pow(v_x, 2) + math.pow(v_y, 2))
        self.v_x = v_x / magnitude
        self.v_y = v_y / magnitude

    def fly(self):

        self.rect.x += self.v_x*self.speed
        self.rect.y += self.v_y*self.speed


    def update(self):
        self.fly()
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > 600:
            self.kill()
        if self.rect.left > 800:
            self.kill()
        if self.rect.right < 0:
            self.kill()


class Test_Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,wall_list,player_bullets):
        super().__init__()
        self.image = pygame.image.load('Assets/Graphics/enemy1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect(topleft=(x,y))

        self.move_x = 0
        self.move_y = 0
        self.move_time = 0

        self.old_x = 0
        self.old_y = 0

        self.speed = 0

        self.health = 2
        self.player_bullets = player_bullets
        self.immortal = 0

        self.wall_list = wall_list

    def movement(self):
        self.move_x = randint(-60,60)
        self.move_y = randint(-60,60)
        self.move_time = randint(50,100)
        self.speed = randint(5,6)

        magnitude = math.sqrt(math.pow(self.move_x,2)+math.pow(self.move_y,2))
        self.move_x /= magnitude
        self.move_y /= magnitude

    def wall_collision(self):
        wall_hit = pygame.sprite.spritecollide(self, self.wall_list, False)
        if wall_hit:
            self.rect.x = self.old_x
            self.rect.y = self.old_y
            self.movement()

    def player_bullet_collision(self):
        global enemy_count
        bullet_hit = pygame.sprite.spritecollide(self, self.player_bullets, False)
        if bullet_hit and self.immortal == 0:
            self.health -= 1
            self.immortal = 80
            if self.health == 0:
                enemy_count -= 1
                self.kill()
        if self.immortal != 0:
            self.immortal -= 1

    def update(self):
        if self.move_time == 0:
            self.movement()
            pass
        else:
            self.old_x = self.rect.x
            self.old_y = self.rect.y
            self.rect.x += self.move_x * self.speed
            self.rect.y += self.move_y * self.speed
            self.move_time -= 1
        self.wall_collision()
        self.player_bullet_collision()


def load_level(level_array,player_group,wall_group,enemy_group,player_bullets):
    global enemy_count
    for i in range(20):
        for j in range(15):
            floor.add(Floor(i * 40, j * 40))
            if level_array[j][i] == 'W':
                # wall = pygame.Surface((40,40))
                # wall.fill((255,0,0))
                # screen.blit(wall, (i*40,j*40))
                wall_group.add(Wall(i*40,j*40))
            if level_array[j][i] == 'P':
                player_group.add(Player(wall_group,player_bullets,enemies,i*40,j*40))
            if level_array[j][i] == '1':
                enemy_count += 1
                enemy_group.add(Test_Enemy(i*40,j*40,wall_group,player_bullets))

pygame.init()
pygame.font.init()

test_level = ["WWWWWWWWWWWWWWWWWWWW",
              'WXXXXXXXXXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WXXXXXX1XXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WXX1XXXXXXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXPXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WXX1XXXXXXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WXXXXX1XXXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WWWWWWWWWWWWWWWWWWWW']

walls = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()

player = pygame.sprite.GroupSingle()

enemies = pygame.sprite.Group()

floor = pygame.sprite.Group()

health = pygame.sprite.Group()
game_active = True
enemy_count = 0

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Prototype")
clock = pygame.time.Clock()

#test = pygame.image.load('graphics/player/jump.png')
# test = pygame.Surface((100,100)).convert_alpha()
# test.fill((255,0,0))
# test_rect = test.get_rect(center=(400,300))
# angle = 0

test_font = pygame.font.Font(None, 60)

dead_text = test_font.render('Game Over!', True, (160,160,160))
dead_text_rect = dead_text.get_rect(center=(400,300))

win_text = test_font.render('Nice Job!', True, (160,160,160))
win_text_rect = win_text.get_rect(center=(400,300))

load_level(test_level, player, walls, enemies, player_bullets)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_active and enemy_count != 0:
        floor.draw(screen)
        walls.draw(screen)
        player.update()
        player.draw(screen)
        player_bullets.draw(screen)
        player_bullets.update()
        enemies.draw(screen)
        enemies.update()
        health.draw(screen)
    else:
        if enemy_count == 0:
            screen.fill((40, 40, 40))
            screen.blit(win_text, win_text_rect)
        else:
            screen.fill((40,40,40))
            screen.blit(dead_text,dead_text_rect)
    # angle += 1
    # test_rotated = pygame.transform.rotozoom(test,angle,1)
    # test_rect = test_rotated.get_rect(center=(400,300))
    # screen.blit(test_rotated,test_rect)
    pygame.display.update()

    clock.tick(60)