import pygame
from random import randint,choice

# Definicion de colores que se van usar en al interfaz
RED=(210,44,44)
GREEN =(0,153,0)
BLUE =(0,102,204)
BACKGROUND_GREEN=(204, 255, 204)
FONT_COLOR=(0,0,0)
BOTON_COLOR=(160,160,160)

# Definicion de los tamaños para el juego
screen_size=[500,500]
hero_size = [25,25]
badguy_size=[25,25]
bullet_size=[10,10]

# Definicion de la posicion inicial para el personaje
hero_position= [screen_size[0]/2,3*screen_size[1]/4]

# Definicion de los diccionarios donde se guardaran las caracteristicas de los personajes
badguys_dict={}
bullets_dict={}

#lista para dar color a los enemigos al azar
color_list=(BLUE,GREEN,RED)

#Informacion de los niveles
level_dict = {'level_1':(17,BLUE),'level_2':(31,GREEN),'level_3':(97,RED)}
#level_dict = {'level_1':(2,BLUE),'level_2':(2,GREEN),'level_3':(2,RED)}

# definicion de valores que daran las carateriticas del juego 
loops = 0
minion_spon_counter = 0
minion_kill_counter = 0
boss_level_alive=False

# definicion de valores para acceder a los menus
game_pause=False
color_menu=False
shape_menu=False

# valores iniciales en caso de que el usuarion no aceda a los menus antes de iniciar
hero_color = BOTON_COLOR
hero_sides = 4
hero_lives = 3

# funcion que crea al heroe
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

# funcion que crea los enemigos
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

# funcion que actualiza la posicion del heroe
def hero_movement(x,y,screen_size, hero_size,movement_key):
    right_limit=screen_size[0]-hero_size[0]
    if(x in range(0,right_limit+1)):
        if movement_key[pygame.K_LEFT]==True:
            x-=1
        elif movement_key[pygame.K_RIGHT]==True:
            x+=1
    elif x<1:
        x=0
    elif x>right_limit:
        x=right_limit

    bottom_limit=screen_size[1]-hero_size[1]
    if(y in range(0,bottom_limit+1)):
        if movement_key[pygame.K_UP]==True:
            y-=1
        elif movement_key[pygame.K_DOWN ]==True:
            y+=1
    elif y<1:
        y=0
    elif y>bottom_limit:
        y=bottom_limit
    return(x,y)

# funcion que actualiza la posicion de los enemigos. Funciona como un generador
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

# Funcion para escoger el nivel. Funciona como un generador
def levels(levels):
    for level_name,level in levels.items():
        current_level=level_name
        minion_number = level[0]
        boss_color = level[1]
        yield (current_level,minion_number,boss_color)
    while True:
        yield ("THE END",0,None)

# Funcion para determinar la poscion de las balas. Funciona como un generador
def bullet_movement(location):
    y_start=location[1]
    x=location[0]
    while y_start>=0:
        yield (x,y_start)
        y_start-=1
    y_start=-50
    x=-50
    while True:
        yield(x,y_start)

# Esctructura del diccionario {'nombre':surface,generator_function,(posicion_x,posicion_y)}
# Funcion para revisar que el heroe colisiono con un enemigo. Retorna el nombre de la llave para el enemigo colisionado
def hero_hit(enemy_dict,hero_position):
   
    global hero_lives

    hero_space = pygame.Rect(*hero_position,25,25)
    enemy_spaces=[]
    
    for enemy in enemy_dict.values():
        enemy_spaces.append(pygame.Rect(*enemy[2],enemy[0].get_width(),enemy[0].get_height()))
    colision = hero_space.collidelist(enemy_spaces)
    if colision == -1:
        return None
    else:
        hero_lives-=1
        return(list(enemy_dict.keys())[colision])

# Funcion que genera disparos del heroe
def hero_shoot(x_start,y_strat,color):
    bullet=pygame.Surface(bullet_size)
    bullet.set_colorkey((0,0,0))
    pygame.draw.polygon(bullet,color, ((0,10),(10,10),(5,5)))
    return(bullet,(x_start,y_strat))

# Funcion que examina si los disparos colisionaron con algun enemigo
def enemy_hit(enemy_dict,bullet_dict,enemy_index=0):
    bullet_spaces = []
    enemy_spaces=[]
    hits=[]
    
    for enemy in enemy_dict.values():
        enemy_spaces.append(pygame.Rect(*enemy[2],enemy[0].get_width(),enemy[0].get_height()))
    
    for bullet in bullet_dict.values():
        bullet_spaces.append(pygame.Rect(*bullet[2],bullet[0].get_width(),bullet[0].get_height()))
    
    
    for enemy_space in enemy_spaces:
        colision = enemy_space.collidelist(bullet_spaces)
        if colision == -1:
            pass
        else:
            hits.append((list(enemy_dict.keys())[enemy_index],list(bullets_dict.keys())[colision]))
            enemy_index+=1
        
    return(hits)

# Funcio para cerra la ventana del juego 
def quit_game():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.init()

screen = pygame.display.set_mode(screen_size)
clock =pygame.time.Clock()

menu_font = pygame.font.Font(None, size=30)
text_font = pygame.font.Font(None, size=50)

running = True
while running:
    screen.fill(BACKGROUND_GREEN)

    quit_game()

    if loops==0:
            currente_level=levels(level_dict)
            specs=next(currente_level)
            game_pause=True
    elif loops==-1:
            specs=next(currente_level)
            loops=1
            game_pause=True

    if hero_lives < 0:
        game_over_text= text_font.render("GAME OVER",True,FONT_COLOR)
        screen.blit(game_over_text,(screen_size[0]*5/32,screen_size[1]/3))
    
    #falta hacer los sub menus
    elif game_pause==True:
        main_menu_text = text_font.render("Main Menu",True,FONT_COLOR)
        screen.blit(main_menu_text,(screen_size[0]*5/32,screen_size[1]/4))
        main_menu_1 = menu_font.render("Change character sides: press \"N\"",True,BOTON_COLOR)
        screen.blit(main_menu_1,(screen_size[0]*5/32,screen_size[1]*3/8))
        main_menu_2 = menu_font.render("Change character colors: press \"C\"",True,BOTON_COLOR)
        screen.blit(main_menu_2,(screen_size[0]*5/32,screen_size[1]*4/8))
        main_menu_3 = menu_font.render("CONTINUE PLAYING: press \"P\"",True,(200,0,0))
        screen.blit(main_menu_3,(screen_size[0]*5/32,screen_size[1]*5/8))
        
        instructions = menu_font.render("* Use keyboard arrows to move and \"S\" to shoot",True,(0,0,0))
        screen.blit(instructions,(screen_size[0]*1/32,screen_size[1]*7/8))

        pressed_key_menu = pygame.key.get_pressed()
        if pressed_key_menu[pygame.K_p] == True:
            game_pause = False
        elif pressed_key_menu[pygame.K_c] == True:
            color_menu = True
            game_pause=False
        elif pressed_key_menu[pygame.K_n] == True:
            shape_menu = True
            game_pause=False
   
    elif color_menu==True:
        color_menu_text = text_font.render("Color menu",True,FONT_COLOR)
        screen.blit(color_menu_text,(screen_size[0]*5/32,screen_size[1]/4))
        red_text = menu_font.render("For RED press \"R\"",True,RED)
        screen.blit(red_text,(screen_size[0]*5/32,screen_size[1]*3/8))
        green_text = menu_font.render("For GREEN press \"G\"",True,GREEN)
        screen.blit(green_text,(screen_size[0]*5/32,screen_size[1]*4/8))
        blue_text = menu_font.render("For BLUE press \"B\"",True,BLUE)
        screen.blit(blue_text,(screen_size[0]*5/32,screen_size[1]*5/8))

        pressed_key_menu = pygame.key.get_pressed()
        if pressed_key_menu[pygame.K_r] == True:
            hero_color = RED
            game_pause = True
            color_menu=False
        elif pressed_key_menu[pygame.K_g] == True:
            hero_color = GREEN
            game_pause = True
            color_menu=False
        elif pressed_key_menu[pygame.K_b] == True:
            hero_color = BLUE
            game_pause=True
            color_menu=False

    elif shape_menu == True:
        shape_menu_text = text_font.render("Shape Menu",True,FONT_COLOR)
        screen.blit(shape_menu_text,(screen_size[0]*5/32,screen_size[1]/4))    
        four_text = menu_font.render("Press 4 for a square",True,BOTON_COLOR)
        screen.blit(four_text,(screen_size[0]*5/32,screen_size[1]*3/8))
        five_text = menu_font.render("Press 5 for a pentagon",True,BOTON_COLOR)
        screen.blit(five_text,(screen_size[0]*5/32,screen_size[1]*4/8))
        six_text = menu_font.render("Press 6 for an Hexagon",True,BOTON_COLOR)
        screen.blit(six_text,(screen_size[0]*5/32,screen_size[1]*5/8))
        seven_text = menu_font.render("Press 7 for an Heptagon",True,BOTON_COLOR)
        screen.blit(seven_text,(screen_size[0]*5/32,screen_size[1]*6/8))
         

        pressed_key_menu = pygame.key.get_pressed()
        if pressed_key_menu[pygame.K_4] == True:
            hero_sides = 4
            game_pause = True
            shape_menu=False
        elif pressed_key_menu[pygame.K_5] == True:
            hero_sides = 5
            game_pause = True
            shape_menu=False
        elif pressed_key_menu[pygame.K_6] == True:
            hero_sides = 6
            game_pause = True
            shape_menu=False
        elif pressed_key_menu[pygame.K_7] == True:
            hero_sides = 7
            game_pause = True
            shape_menu=False

    else:
        hero=create_hero(hero_sides,hero_color)    

    #crea los jefes
        if minion_kill_counter == specs[1] and boss_level_alive==False:
            boss=create_badguy(specs[2],True)
            boss_pos=badguy_movement(boss)
            badguys_dict[f'boss_{specs[0]}']=(boss,boss_pos,(0,0),50)
            boss_level_alive=True

    #crea nuevos malos
        if loops%101==0 and minion_spon_counter < specs[1]:
            minion_color=choice(color_list)
            bad_guy=create_badguy(minion_color,False)
            bad_pos=badguy_movement(bad_guy)
            badguys_dict[f'badguy_counter_{loops}']=(bad_guy,bad_pos,(0,0),5)
            minion_spon_counter+=1
    
        # actualiza la posicion de los malos
        for enemy_name, enemy in badguys_dict.items():
            if loops%2==0:
                bad_coordinate=next(enemy[1])
                badguys_dict[enemy_name]=(enemy[0],enemy[1],bad_coordinate,enemy[3])
            screen.blit(enemy[0],enemy[2])
        
        # borrar malos que se lasen de la pantalla, si no los mata se sube el numero de minions que deben salir
        for enemy_name in list(badguys_dict.keys()):
            if badguys_dict[enemy_name][2]==(-50,-50):
                if badguys_dict[enemy_name][0].get_width() == 25:
                    minion_spon_counter-=1
                else:
                    boss_level_alive=False
                del badguys_dict[enemy_name]
            elif badguys_dict[enemy_name][3]<=0:
                if badguys_dict[enemy_name][0].get_width() == 25:
                    minion_kill_counter+=1
                else:
                    boss_level_alive=False
                    minion_kill_counter=0
                    minion_spon_counter=0
                    loops=-2
                del badguys_dict[enemy_name]
            
        

        badguy_name = hero_hit(badguys_dict,hero_position)
        
        if badguy_name is not None:
            del badguys_dict[badguy_name]
            
            minion_kill_counter+=1

        if minion_kill_counter > specs[1]:
            loops =-2
            minion_kill_counter=0
            minion_spon_counter=0
            boss_level_alive = False
            
        
        bullseye = enemy_hit(badguys_dict,bullets_dict)

        if bullseye is not None:
            for bullets_hit in bullseye:
                del bullets_dict[bullets_hit[1]]
                badguys_dict[bullets_hit[0]]=(badguys_dict[bullets_hit[0]][0],badguys_dict[bullets_hit[0]][1],badguys_dict[bullets_hit[0]][2],badguys_dict[bullets_hit[0]][3]-1)

        pressed_key = pygame.key.get_pressed()
        hero_position=hero_movement(*hero_position,screen_size,hero_size,pressed_key)

        if pressed_key[pygame.K_s]==True:
            if loops%11==0:
                bullet_basics = hero_shoot(round(hero_position[0]+hero_size[0]/2),round(hero_position[1]),hero_color)
                bullet_pos = bullet_movement(bullet_basics[1])
                bullets_dict[f"bullet_{loops}"]=(bullet_basics[0],bullet_pos,bullet_basics[1])
            
        for bullet_name in list(bullets_dict.keys()):
            if bullets_dict[bullet_name][2]==(-50,-50):
                del bullets_dict[bullet_name]

        for bullet_name, bullet in bullets_dict.items():
            bullet_coordinate=next(bullet[1])
            bullets_dict[bullet_name]=(bullet[0],bullet[1],bullet_coordinate)
            screen.blit(bullet[0],bullet[2])   
        
        screen.blit(hero,hero_position)

    pygame.display.flip()

    clock.tick(60)
    loops+=1
pygame.quit()
