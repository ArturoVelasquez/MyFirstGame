import pygame
from random import randint
pygame.init()

screen_size=[500,500]
hero_size = [25,25]
badguy_size=[25,25]
screen = pygame.display.set_mode(screen_size)
bad_guy=pygame.Surface(hero_size)
bad_guy.set_colorkey((0,0,0))
x,y=10,10
running = True

RED=(210,44,44)
GREEN =(0,153,0)
BLUE =(0,102,204)

clock =pygame.time.Clock()
loops=0
#hero = pygame.Surface(hero_size)
#hero.set_colorkey((0,0,0))

def create_hero(sides,color):
    hero =pygame.Surface(hero_size)
    hero.set_colorkey((0,0,0))
    if sides == 4:
        pygame.draw.polygon(hero,color, ((0,0),(0,25),(25,25),(25,0)))
    elif sides == 5:
        pygame.draw.polygon(hero,color, ((0,12.5),(5,25),(20,25),(25,12.5),(12.5,0)))
    elif sides ==6:
        pygame.draw.polygon(hero,color, ((0,12.5),(5,25),(20,25),(25,12.5),(20,0),(5,0)))
    elif sides ==7:    
        pygame.draw.polygon(hero,color, ((3.5,5),(0,15),(7.5,25),(17.5,25),(25,15),(21.5,5),(12.5,0)))
    
    return hero

def create_badguy(color,boss=False):
    if boss:
        badguy=pygame.Surface([2*size for size in badguy_size])
        badguy.set_colorkey((0,0,0))
        pygame.draw.polygon(badguy,color, ((0,0),(50,0),(25,50)))
    else:
        badguy=pygame.Surface(badguy_size)
        badguy.set_colorkey((0,0,0))
        pygame.draw.polygon(badguy,color, ((0,0),(25,0),(12.5,25)))
    return badguy


def hero_movement(x,y,screen_size, hero_size,movment_key):
    right_limit=screen_size[0]-hero_size[0]
    if(x in range(0,right_limit+1)):
        if movment_key[pygame.K_LEFT]==True:
            x-=1
        elif movment_key[pygame.K_RIGHT]==True:
            x+=1
    elif x<1:
        x=0
    elif x>right_limit:
        x=right_limit

    bottom_limit=screen_size[1]-hero_size[1]
    if(y in range(0,bottom_limit+1)):
        if movment_key[pygame.K_UP]==True:
            y-=1
        elif movment_key[pygame.K_DOWN ]==True:
            y+=1
    elif y<1:
        y=0
    elif y>bottom_limit:
        y=bottom_limit
    return(x,y)

def badguy_movement(badguy):
    y=0
    x_start=randint(0,screen_size[0]-badguy.get_width())
    
    while y<screen_size[1]:
        yield (x_start,y)
        y+=1
    y=-50
    x_start=-50
    while True:
        yield(x_start,y)


bad_pos=badguy_movement(bad_guy)

counter=0
badguys_list={}
hero=create_hero(5,BLUE)

while running:
    screen.fill((204, 255, 204))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    if loops%101==0 and counter < 2:
        bad_guy=create_badguy(RED,True)
        bad_pos=badguy_movement(bad_guy)
        badguys_list[f'badgui_counter_{counter}']=(bad_guy,bad_pos,(0,0))
        counter+=1
    
    for enemy_name, enemy in badguys_list.items():
        if loops%2==0:
            bad_coordinate=next(enemy[1])
            badguys_list[enemy_name]=(enemy[0],enemy[1],bad_coordinate)

        screen.blit(enemy[0],enemy[2])
    
    for enemy_name in list(badguys_list.keys()):
        if badguys_list[enemy_name][2]==(-50,-50):
            del badguys_list[enemy_name]


    screen.blit(hero,(x,y))


    pressed_key = pygame.key.get_pressed()
    x,y=hero_movement(x,y,screen_size,hero_size,pressed_key)
    

    pygame.display.flip()

    clock.tick(60)
    loops+=1
pygame.quit()

