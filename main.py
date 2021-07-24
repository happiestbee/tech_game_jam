import pygame
from sys import exit
import math
from random import randint, choice


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
    def __init__(self, wall_list, bullet_list, enemy_bullets,enemy1_list,enemy2_list,item_list,goal_list,portal, x, y, player_info):
        super().__init__()
        self.original_image = pygame.Surface((40,40), pygame.SRCALPHA)
        self.original_image.fill((0,0,0))
        self.image = pygame.image.load('Assets/Graphics/player_sprite.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.angle = -90
        self.speed = player_info[4]

        self.prev_x = self.rect.x
        self.prev_y = self.rect.y
        self.wall_list = wall_list

        self.bullet_list = bullet_list
        self.bullet_speed = player_info[0]
        self.bullet_size = player_info[1]
        self.reload_speed = player_info[2]
        self.damage = player_info[5]
        self.can_fire = True
        self.fire_time = 0

        self.enemy1_list = enemy1_list
        self.enemy_2list = enemy2_list
        self.health = player_info[3]
        self.enemy_bullets = enemy_bullets

        self.goal_list = goal_list
        self.goal_timer = 90

        self.portal = portal

        self.item_list = item_list
        self.pick_up = False

        self.kills = player_info[6]
        self.coins = 0

        self.immortal = 0
    def display_health(self):
        health.empty()
        for i in range(self.health):
            health.add(Health(5+i*40,5,self.immortal))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.prev_y = self.rect.y
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.prev_y = self.rect.y
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.prev_x = self.rect.x
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.prev_x = self.rect.x
            self.rect.x += self.speed

        # if keys[pygame.K_x] and self.immortal == 0:
        #     self.health -= 1
        #     self.immortal = 120
        #
        # if self.immortal != 0:
        #     self.immortal -= 1


        if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and self.can_fire:
            shoot.play()
            self.bullet_list.add(Player_Bullet(self.bullet_size,self.bullet_speed,self.rect,self.wall_list))
            self.can_fire = False
            self.fire_time = pygame.time.get_ticks()
        if self.can_fire == False:
            if self.fire_time + self.reload_speed <= pygame.time.get_ticks():
                self.can_fire = True


    def wall_collision(self):
        wall_hit = pygame.sprite.spritecollide(self, self.wall_list, False)
        if wall_hit:
            self.rect.x = self.prev_x
            self.rect.y = self.prev_y
            self.prev_x = self.rect.x
            self.prev_y = self.rect.y

    def enemy_collision(self):
        global game_active, player_stats
        enemy_hit = pygame.sprite.spritecollide(self, self.enemy1_list, False)
        bullet_hit = pygame.sprite.spritecollide(self, self.enemy_bullets, False)
        if enemy_hit and self.immortal == 0:
            hit.play()
            self.health -= enemy1_stats[1]
            self.immortal = 120
        if bullet_hit and self.immortal == 0:
            hit.play()
            self.health -= enemy2_stats[1]
            self.immortal = 120
        if self.health <= 0:
            player_stats = [self.bullet_speed, self.bullet_size, self.reload_speed, self.health, self.speed,
                            self.damage, self.kills]
            pygame.mixer.stop()
            end.play(loops=-1)
            game_active = False
        if self.immortal != 0:
            self.immortal -= 1

    def portal_collision(self):
        global player_stats
        global next_level
        global portal_placed
        enter_portal = pygame.sprite.spritecollide(self,self.portal,False)
        if enter_portal:
            level_sound.play()
            next_level = True
            player_stats = [self.bullet_speed,self.bullet_size,self.reload_speed,self.health,self.speed,self.damage,self.kills]



    def item_pickup(self):
        global item_effect
        if item_effect:
            pickup.play()
            self.health += item_effect[0]
            self.bullet_speed *= item_effect[1]
            self.bullet_size += item_effect[2]
            self.speed *= item_effect[3]
            self.reload_speed *= item_effect[4]
            self.damage += item_effect[5]
            player_stats = [self.bullet_speed, self.bullet_size, self.reload_speed, self.health, self.speed,self.damage,self.kills]
            item_effect = []

    def check_goals(self):
        global dead, goals_list
        if dead:
            self.kills += 1
            dead = False
        if self.kills == 1 and not(goals_list[0]):
            goal.play()
            self.goal_list.add(Goal1(self.goal_timer),Goal2(0,self.goal_timer),Goal3(0,self.goal_timer))
        if self.kills == 10 and not(goals_list[1]):
            goal.play()
            self.goal_list.add(Goal1(self.goal_timer),Goal2(1,self.goal_timer),Goal3(1,self.goal_timer))
        if self.kills == 50 and not(goals_list[2]):
            goal.play()
            self.goal_list.add(Goal1(self.goal_timer),Goal2(2,self.goal_timer),Goal3(2,self.goal_timer))


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
        global portal_placed
        self.player_input()
        self.wall_collision()
        self.enemy_collision()
        self.display_health()
        self.item_pickup()
        self.check_goals()
        self.portal_collision()
        if enemy_count == 0:
            portal.add(Portal(40,40))


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
    def __init__(self,size,speed,player_rect,walls):
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
        if magnitude == 0:
            magnitude = 1
            self.v_x = 1
            self.v_y = 0
        else:
            self.v_x = v_x / magnitude
            self.v_y = v_y / magnitude
        self.walls = walls

    def fly(self):

        self.rect.x += self.v_x*self.speed
        self.rect.y += self.v_y*self.speed

    def wall_collisions(self):
        wall_hit = pygame.sprite.spritecollide(self, self.walls, False)
        if wall_hit:
            self.kill()

    def update(self):
        self.fly()
        self.wall_collisions()
        # if self.rect.bottom < 0:
        #     self.kill()
        # if self.rect.top > 600:
        #     self.kill()
        # if self.rect.left > 800:
        #     self.kill()
        # if self.rect.right < 0:
        #     self.kill()


class enemy_bullet(pygame.sprite.Sprite):
    def __init__(self,size,speed,enemy_rect,player_center,walls):
        super().__init__()
        self.size = size
        self.speed = speed
        self.image = pygame.image.load('Assets/Graphics/enemy_bullet.png')
        self.image = pygame.transform.scale(self.image,(self.size,self.size))
        self.rect = self.image.get_rect(center=(enemy_rect.center))
        x, y = player_center
        x_1, y_1 = self.rect.center
        v_x = x - x_1
        v_y = y - y_1
        magnitude = math.sqrt(math.pow(v_x, 2) + math.pow(v_y, 2))
        if magnitude == 0:
            magnitude = 1
            self.v_x = 1
            self.v_y = 0
        else:
            self.v_x = v_x / magnitude
            self.v_y = v_y / magnitude
        self.walls = walls

    def fly(self):

        self.rect.x += self.v_x*self.speed
        self.rect.y += self.v_y*self.speed

    def wall_collisions(self):
        wall_hit = pygame.sprite.spritecollide(self, self.walls, False)
        if wall_hit:
            self.kill()

    def update(self):
        self.fly()
        self.wall_collisions()

class Test_Enemy(pygame.sprite.Sprite):
    def __init__(self,type,x,y,wall_list,player_bullets,enemy_bullets,item_list,player):
        super().__init__()
        if type == 1:
            self.image = pygame.image.load('Assets/Graphics/enemy1.png').convert_alpha()
        elif type == 2:
            self.image = pygame.image.load('Assets/Graphics/enemy2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect(topleft=(x,y))

        self.move_x = 0
        self.move_y = 0
        self.move_time = 0

        self.old_x = 0
        self.old_y = 0

        self.speed = 0

        self.type = type
        if self.type == 1:
            self.health = enemy1_stats[0]
        elif self.type == 2:
            self.health = enemy2_stats[0]
            self.bullet_speed = enemy2_stats[2]
            self.reload_speed = enemy2_stats[3]
            self.bullet_timer = 0

        self.player_bullets = player_bullets
        self.enemy_bullets = enemy_bullets
        self.immortal = 0

        self.wall_list = wall_list
        self.item_list = item_list

        self.player = player
    def movement(self):
        if self.type == 1:
            self.move_x = randint(-60,60)
            self.move_y = randint(-60,60)
            self.move_time = randint(50,100)
            self.speed = randint(5,6)
        elif self.type == 2:
            self.move_x = randint(-20, 20)
            self.move_y = randint(-20, 20)
            self.move_time = randint(50, 100)
            self.speed = randint(1, 3)

        magnitude = math.sqrt(math.pow(self.move_x,2)+math.pow(self.move_y,2))
        if magnitude == 0:
            self.move_x = 1
            self.move_y = 0
        else:
            self.move_x /= magnitude
            self.move_y /= magnitude

    def wall_collision(self):
        wall_hit = pygame.sprite.spritecollide(self, self.wall_list, False)
        if wall_hit:
            self.rect.x = self.old_x
            self.rect.y = self.old_y
            self.movement()

    def shoot_bullet(self):
        if self.bullet_timer == 0:
            self.enemy_bullets.add(enemy_bullet(10,8,self.rect,self.player.sprite.rect.center,self.wall_list))
            self.bullet_timer = self.reload_speed
        else:
            self.bullet_timer -= 1


    def player_bullet_collision(self):
        global enemy_count
        global dead
        bullet_hit = pygame.sprite.spritecollide(self, self.player_bullets, False)
        if bullet_hit and self.immortal == 0:
            self.health -= player_stats[5]
            self.immortal = 30
            if self.health <= 0:
                enemy_count -= 1
                if enemy_count == 0:
                    clear.play()
                dead = True
                self.drop_item()
                self.kill()
        if self.immortal != 0:
            self.immortal -= 1

    def drop_item(self):
        if randint(1,10) < 7:
            self.item_list.add(Item(randint(0,3),self.rect.center[0],self.rect.center[1],self.player))

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
        if self.type == 2:
            self.shoot_bullet()




class Item(pygame.sprite.Sprite):
    def __init__(self,item_number,x,y,player):
        global item_effect
        super().__init__()
        self.item_image = [pygame.image.load('Assets/Graphics/milk_bucket.png').convert_alpha(),
                           pygame.image.load('Assets/Graphics/bullet_speed.png').convert_alpha(),
                           pygame.image.load('Assets/Graphics/egg.png').convert_alpha(),
                           pygame.image.load('Assets/Graphics/iron_sword.png').convert_alpha(),
                           pygame.image.load('Assets/Graphics/glint.png').convert_alpha()]
        self.item_effect = [[1,1,5,1,1,0],
                            [0,1.1,0,1,1,0],
                            [0,1,0,1,0.85,0],
                            [0,1,0,1,1,1],
                            [0,1,0,1.1,1,0]]

        self.image = self.item_image[item_number]
        self.image = pygame.transform.scale(self.image,(30,30))
        self.rect = self.image.get_rect(center=(x,y))

        self.player = player
        self.effect = self.item_effect[item_number]

    def item_drop(self):
        global item_effect
        item_hit = pygame.sprite.spritecollide(self,self.player,False)
        if item_hit:
            item_effect = self.effect
            self.kill()

    def update(self):
        self.item_drop()


class Goal1(pygame.sprite.Sprite):
    def __init__(self,timer):
        super().__init__()
        self.image = pygame.image.load('Assets/Graphics/text_box.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(200,75))
        self.rect = self.image.get_rect(center=(400,50))
        self.timer = timer

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.kill()


class Goal2(pygame.sprite.Sprite):
    def __init__(self,goal_number,timer):
        global goals_list
        super().__init__()
        self.goal_title = ['Monster Slayer I','Monster Slayer II', 'Monster Slayer III']
        self.image = goal_font_1.render(self.goal_title[goal_number], True, (200, 200, 200))
        self.rect = self.image.get_rect(center=(400,43))
        self.timer = timer
        goals_list[goal_number] = 1

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.kill()


class Goal3(pygame.sprite.Sprite):
    def __init__(self,goal_number,timer):
        super().__init__()
        self.goal_descriptions = ['Kill 1 Monster','Kill 10 Monsters','Kill 50 Monsters']
        self.image = goal_font_2.render(self.goal_descriptions[goal_number], True, (200, 200, 200))
        self.rect = self.image.get_rect(center=(400,60))
        self.timer = timer

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.kill()


class Portal(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('Assets/Graphics/portal.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect(topleft=(x,y))

def load_level(level_array,player_group,wall_group,enemy1_group,enemy2_group,item_list,player_bullets,enemy_bullets,goals,portal):
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
                player_group.add(Player(wall_group,player_bullets,enemy_bullets,enemy1_group,enemy2_group,item_list,goals,portal,i*40,j*40,player_stats))
            if level_array[j][i] == '1':
                enemy_count += 1
                enemy1_group.add(Test_Enemy(1,i*40,j*40,wall_group,player_bullets,enemy_bullets,item_list,player_group))
            if level_array[j][i] == '2':
                enemy_count += 1
                enemy2_group.add(Test_Enemy(2,i*40,j*40,wall_group,player_bullets,enemy_bullets,item_list,player_group))


pygame.init()
pygame.font.init()
pygame.mixer.init()

shoot = pygame.mixer.Sound('Assets/Audio/shoot.wav')
hit = pygame.mixer.Sound('Assets/Audio/hit.wav')
pickup = pygame.mixer.Sound('Assets/Audio/pickup.wav')
clear = pygame.mixer.Sound('Assets/Audio/clear.wav')
level_sound = pygame.mixer.Sound('Assets/Audio/next_level.wav')
goal = pygame.mixer.Sound('Assets/Audio/goal.wav')
game_over = pygame.mixer.Sound('Assets/Audio/game_over.wav')
menu = pygame.mixer.Sound('Assets/Audio/menu.wav')
active = pygame.mixer.Sound('Assets/Audio/active.wav')
end = pygame.mixer.Sound('Assets/Audio/end.wav')

test_level = [["WWWWWWWWWWWWWWWWWWWW",
              'WXXXXXXXXXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WXXXXXX2XXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WXX2XXXXXXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXPXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WXX1XXXXXXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WXXXXX1XXXXXXXXXXXXW',
              'WXXXXXXXXXXXXXXXXXXW',
              'WWWWWWWWWWWWWWWWWWWW'],
              ["WWWWWWWWWWWWWWWWWWWW",
               'W2XXXXXXXXXXXXXXXXXW',
               'WXXXXXXXXXXXXXXXXXXW',
               'WXXWWWWWWXXWWWWWWXXW',
               'WXXW1XXXXXXXXXX1WXXW',
               'WXXWXXXXXXXXXXXXWXXW',
               'WXXXXXXXXXXXXXXXXXXW',
               'WXXXXXXXXXXXXXXXXXXW',
               'WXXWXXXXXXXXXXXXWXXW',
               'WXXWXXXXXXXXXXXXWXXW',
               'WXXW1XXXXXXXXXX1WXXW',
               'WXXWWWWWWXXWWWWWWXXW',
               'WXXXXXXXXXXXXXXXXXXW',
               'W2XXXXXXXXXXXXXXXXPW',
               'WWWWWWWWWWWWWWWWWWWW'],
              ["WWWWWWWWWWWWWWWWWWWW",
               'WXXXXXXXWXXWXXXXXXXW',
               'WXXXXXXXWXXWXXXXXXXW',
               'WXX1XXXXWXXWXXXX1XXW',
               'WXXXXXXXXXXXXXXXXXXW',
               'WWWWWWWXXXXXXWWWWWWW',
               'WXXXXXXXXXXXXXXXXXXW',
               'W2XXXXXXXXXXXXXXXX2W',
               'WXXXXXXXXXXXXXXXXXXW',
               'WWWWWWWXXXXXXWWWWWWW',
               'WXXXXXXXXXXXXXXXXXXW',
               'WXXXXXXXWXXWXXXXXXXW',
               'WXX1XXXXWXXWXXXXXXXW',
               'WXXXXXXXWXXWXXXXXXPW',
               'WWWWWWWWWWWWWWWWWWWW'],
             ["WWWWWWWWWWWWWWWWWWWW",
              'WXXXW2XXXXXXW1XXXX1W',
              'WXXXWXXXXXXXWXXXXXXW',
              'WXXXWXXXXXXXWXXXXXXW',
              'WXXXWXXXXXXXWXXXXXXW',
              'WXXXWXXXXXXXWXXXXXXW',
              'WXXXWXXXWXXXWXXXWXXW',
              'WXXXWXXXWXXXWXXXWXXW',
              'WXXXWXXXWXXXWXXXWXXW',
              'WXXXXXXXWXXXXXXXWXXW',
              'WXXXXXXXWXXXXXXXWXXW',
              'WXXXXXXXWXXXXXXXWXXW',
              'WXXXXXXXWXXXXXXXWXXW',
              'W2XXXXXXW1XXXXX2WXPW',
              'WWWWWWWWWWWWWWWWWWWW']
              ]

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Prototype")
clock = pygame.time.Clock()

test_font = pygame.font.Font(None, 60)

goal_font_1 = pygame.font.Font(None, 30)
goal_font_2 = pygame.font.Font(None, 20)


item_effect = []

dead = False
goals_list = [0,0,0]

walls = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

player = pygame.sprite.GroupSingle()
portal = pygame.sprite.GroupSingle()
portal_placed = False

enemies1 = pygame.sprite.Group()
enemies2 = pygame.sprite.Group()

floor = pygame.sprite.Group()

items = pygame.sprite.Group()

goals = pygame.sprite.Group()

health = pygame.sprite.Group()
game_active = False
screen_num = 0
enemy_count = 0
level = 0
next_level = True
player_stats = [7,10,500,5,4,1,0]
enemy1_stats = [2,1]
enemy2_stats = [2,1,5,100]


#main menu images
cool_font = pygame.font.Font('Assets/Font/8-BIT WONDER.TTF',50)
normal_font = pygame.font.Font('Assets/Font/8-BIT WONDER.TTF',20)
bg = pygame.image.load('Assets/Graphics/bg.png')
bg = pygame.transform.scale(bg,(int(288*15/4),600))

title_text = cool_font.render('Hellish Grind',True,(255, 30, 30))
title_rect = title_text.get_rect(center=(400,100))

start_text = normal_font.render('press SPACE to start', True, (255,70,70))
start_rect = start_text.get_rect(center=(400,340))

help_text = normal_font.render('press [ H ] for help', True, (255,70,70))
help_rect = help_text.get_rect(center=(400,400))

#help screen

stone_wall = pygame.image.load('Assets/Graphics/stone_wall.jpeg')
stone_wall = pygame.transform.scale(stone_wall,(int(1024*25/24),600))

control_text = cool_font.render('Controls',True,(255, 50, 50))
control_rect = control_text.get_rect(center=(400,160))

#pause screen
pause_text = cool_font.render('Paused',True,(255, 30, 30))
pause_rect = pause_text.get_rect(center=(400,100))

pause_text_1 = normal_font.render('press SPACE to resume', True, (255,70,70))
pause_rect_1 = pause_text_1.get_rect(center=(400,340))

#game over screen
dead_text = cool_font.render('Game Over',True,(255, 30, 30))
dead_rect = dead_text.get_rect(center=(400,200))

kill_text = normal_font.render(f'Monsters Killed: {player_stats[6]}', False, (255,30,30))
levels_text = normal_font.render(f'Rooms Cleared: {level-1}', False, (255,30,30))


controls = ['    - Use WASD to move',
            '    - Use SPACE to shoot',
            '    - Use MOUSE to aim',
            '    - Use ESC to pause',
            '    - Enemies drop helpful items',
            '    - Survive as long as you can',
            '    - [ W ] to go back']



#test = pygame.image.load('graphics/player/jump.png')
# test = pygame.Surface((100,100)).convert_alpha()
# test.fill((255,0,0))
# test_rect = test.get_rect(center=(400,300))
# angle = 0


menu.play(loops=-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if not(game_active) and screen_num == 0:
        screen.blit(bg,(0,0))
        pygame.draw.rect(screen, '#f5a442', title_rect)
        pygame.draw.rect(screen, '#f5a442', title_rect,10)
        screen.blit(title_text,title_rect)
        pygame.draw.rect(screen, '#f5a442', start_rect)
        pygame.draw.rect(screen, '#f5a442', start_rect, 10)
        screen.blit(start_text, start_rect)
        pygame.draw.rect(screen, '#f5a442', help_rect)
        pygame.draw.rect(screen, '#f5a442', help_rect, 10)
        screen.blit(help_text, help_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            pygame.mixer.stop()
            active.play(loops=-1)
            screen_num = 1
            game_active = True
        elif keys[pygame.K_h]:
            screen_num = 2

    if not(game_active) and screen_num == 2:
        screen.blit(stone_wall,(0,0))
        pygame.draw.rect(screen, '#f5a442', control_rect)
        pygame.draw.rect(screen, '#f5a442', control_rect, 10)
        screen.blit(control_text, control_rect)
        for i in range(len(controls)):
            controls_text = normal_font.render(controls[i],False,(255,40,40))
            controls_rect = controls_text.get_rect(center=(400, 280+i*40))
            pygame.draw.rect(screen, '#f5a442', controls_rect)
            pygame.draw.rect(screen, '#f5a442', controls_rect, 10)
            screen.blit(controls_text,controls_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            screen_num = 0

    if game_active and not(next_level):
        floor.draw(screen)
        walls.draw(screen)
        player.update()
        player.draw(screen)
        player_bullets.draw(screen)
        player_bullets.update()
        enemy_bullets.draw(screen)
        enemy_bullets.update()
        enemies1.draw(screen)
        enemies1.update()
        enemies2.draw(screen)
        enemies2.update()
        items.draw(screen)
        items.update()
        health.draw(screen)
        goals.draw(screen)
        goals.update()
        portal.draw(screen)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.mixer.pause()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    pygame.mixer.unpause()
                    break

                pygame.draw.rect(screen, '#f5a442', pause_rect)
                pygame.draw.rect(screen, '#f5a442', pause_rect, 10)
                screen.blit(pause_text, pause_rect)
                pygame.draw.rect(screen, '#f5a442', pause_rect_1)
                pygame.draw.rect(screen, '#f5a442', pause_rect_1, 10)
                screen.blit(pause_text_1, pause_rect_1)

                pygame.display.update()
                clock.tick(60)



    else:
        if next_level:
            player.empty()
            portal.empty()
            walls.empty()
            player_bullets.empty()
            enemy_bullets.empty()
            items.empty()
            level += 1
            if level%3 == 0:
                enemy1_stats[0] += 1
                enemy1_stats[1] += 1
                enemy2_stats[0] += 1
                enemy2_stats[1] += 1
                enemy2_stats[2] *= 1.1
                enemy2_stats[3] *= 0.9


            load_level(test_level[randint(0,3)], player, walls, enemies1, enemies2, items, player_bullets, enemy_bullets, goals, portal)
            next_level = False


        if screen_num == 1:
            screen.fill((40,40,40))
            pygame.draw.rect(screen, '#f5a442', dead_rect)
            pygame.draw.rect(screen, '#f5a442', dead_rect, 10)
            kill_text = normal_font.render(f'Monsters Killed [ {player_stats[6]} ]', False, (255, 30, 30))
            kill_rect = kill_text.get_rect(center=(400,350))
            levels_text = normal_font.render(f'Rooms Cleared [ {level - 1} ]', False, (255, 30, 30))
            levels_rect = levels_text.get_rect(center=(400,390))
            screen.blit(dead_text,dead_rect)
            screen.blit(kill_text,kill_rect)
            screen.blit(levels_text,levels_rect)
    # angle += 1
    # test_rotated = pygame.transform.rotozoom(test,angle,1)
    # test_rect = test_rotated.get_rect(center=(400,300))
    # screen.blit(test_rotated,test_rect)
    pygame.display.update()

    clock.tick(60)