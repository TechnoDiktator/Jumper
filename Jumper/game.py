import pygame
from sys import exit
from random import randint , choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gravity = 0
        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.player_walk = [player_walk1 , player_walk2]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.1)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom>=300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1 
        self.rect.y += self.gravity
        if self.rect.bottom>=300:
            self.rect.bottom = 300
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index+=0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
            
class Obstacle(pygame.sprite.Sprite):
    def __init__(self , type):
        super().__init__()
        if type == 'fly':
            fly_1  = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            fly_2  = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            self.frames = [fly_1 , fly_2]
            y_pos = randint(100 ,220 )
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1 , snail_2]
            y_pos = 300
            
        #creating the rectangles
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900 , 1100) , y_pos ))

    def animation_state(self):
        self.animation_index +=0.1
        if self.animation_index >= len(self.frames):self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -=5
        self.destroy()
        
    def destroy(self):
        if self.rect.x <=-100:
            self.kill()
        
        

#this essentially starts pygame
pygame.init()

#SETTING UP THE WINDOWS
#this is how we set the width and height of our game
screen = pygame.display.set_mode((800 , 400))
pygame.display.set_caption('dino-run-clone')
test_font = pygame.font.Font('font/Pixeltype.ttf' , 50)  #setting font
#trying to set the frame rate
clock = pygame.time.Clock()
game_active = True
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops= -1)




#CREATING SINGLE TYPE SPRITE GROUP
player = pygame.sprite.GroupSingle()
player.add(Player())


#CREATING MULTI SPRITE GROUP
obstacle_group = pygame.sprite.Group()



def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x-=5
            
            if(obstacle_rect.bottom ==300):
                screen.blit(snail_surface , obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        #here we are running a loop to check which obstacles are out of view ....and simply removing them from the pbstacle list    
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []
    
def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
#                                    text                       anti-aliasing    #color
    score_surface = test_font.render( 'Score : ' + str(current_time) , False , (255,255,255))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface , score_rect)
    return current_time
   
def collisions(player , obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True      

def collision_sprite():      #player sprite    enemy sprite group
    if pygame.sprite.spritecollide(player.sprite , obstacle_group ,False ):
        obstacle_group.empty() #clearing obstacle sprite group
        return False
    return True

def player_animation():
    #play walking animation of the player in on floor 
    #jumping naimation if the player is jumping
    global player_surface , player_index
    
    if(player_rect.bottom < 300):
        #jump animation
        player_surface = player_jump
    else:
        #walk animation
        player_index += 0.1  #this will make the walk animation slow ...so that human eye can see it ...as our FPS is 60(too fast)
        if(player_index >= len(player_walk)):
            player_index =0
            
        player_surface = player_walk[int(player_index)]
        

#SURFACES
#creating a regular surface
#test_surface = pygame.Surface((100,200)) 
#creating an image based surface
sky_surface = pygame.image.load('graphics/sky8.jpg').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_walk = [player_walk1 , player_walk2]
player_index = 0 #this will help us choose which surface to render to show the walking animation
player_gravity = 0
player_surface = player_walk[0]


#OBSTACLES
snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
fly_frame1  = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frame2  = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
obstacle_rect_list = []        #  graphics\Fly\Fly2.png
snail_frames = [snail_frame1 , snail_frame2]
fly_frames = [fly_frame1 , fly_frame2]
snail_frame_index = 0
fly_frame_index = 0
snail_surface = snail_frames[snail_frame_index]
fly_surface = fly_frames[fly_frame_index]




#Intro Screen
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand , 270 , 2) #increasingthe size
player_stand_rect = player_stand.get_rect(center = (400 , 200))
game_name = test_font.render('Jump Forrest Jump !!!' , False , (222,196,169))
game_name_rect = game_name.get_rect(center = (400,80))
game_message = test_font.render('Press SPACE to Restart' , False , (222,196 , 169))
game_message_rect = game_message.get_rect(center = (400,330))


#TIMER
obstacle_timer = pygame.USEREVENT + 1  #this is how you create a custom user event
pygame.time.set_timer(obstacle_timer , 1300) #that is we will trigger this event after every 900ms


#we will make timers to run obstacle animations and alternate between the obstacle surfaces using these timers 
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer , 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer , 200)



#RECTANGLES
#Rectangles ---- > help in position of surfaces with precision ...that is they 
player_rect = player_surface.get_rect(midbottom = (80,300))  #this will from a rectangle around the player


#Origin   ----- >  in pygame the windows/displays top left corner is the origin
'''
(0 , 0)   --------------> +x
  |  # # # # # # # # # # # # # #
  |  #
  |  #
  +y #
     #
     #
     #
     #
'''

#we run an infinite loop
while True:
    #draw all our elements 
    #update the frame of the game on command
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 

            exit()
        if game_active:
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:   #that is player bottom is at the ground
                    player_gravity = -21
            
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE  and player_rect.bottom >= 300:
                    player_gravity = -21
        else:
            if event.type == pygame.KEYDOWN  and event.key == pygame.K_SPACE:   #that is game is over ...and we are restarting the game
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)
                
        if game_active:
            if(event.type == obstacle_timer):
                obstacle_group.add(Obstacle(choice(['fly'  , 'snail' ,'snail','snail']))) #will randomly pick between the choices but since 
                
            

            if(event.type == snail_animation_timer):
                if snail_frame_index == 0:snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surface  = snail_frames[snail_frame_index]
                                                                                    
            if(event.type == fly_animation_timer):
                if fly_frame_index == 0:fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surface  = fly_frames[fly_frame_index]
                                                                                    
            

    if game_active:
                    
        #display surface  -  the game window ....is always shown...and always visible
        #regular surface - only displayed when we put it on the display surface        
        # 0 0 is the place where we want the surface to be displayed
        screen.blit(sky_surface , (0 , 0))      #we are updating/blitting all these surfaces 60FPS
        screen.blit(ground_surface , (0 , 300))        
        score  = display_score()
         

        #PLAYER AND OBSTACLES
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        #COLLISION DETECTION
        game_active = collision_sprite()
        
    else:
        screen.fill((84 , 129 , 170))
        screen.blit(player_stand , player_stand_rect)
        score_message = test_font.render(   f'Your Score :  {score} ..... Press SPACE to restart ' ,False , (222,196,169) ) 
        score_message_rect = score_message.get_rect(center = (400 , 330))
        screen.blit(game_name , game_name_rect)
        if(score == 0):
            screen.blit(game_message , game_message_rect)
        else:
            screen.blit(score_message , score_message_rect)
        obstacle_rect_list.clear() #emptying the obstacle rect list
        player_rect.midbottom = (80 , 300) #resetting player position
        player_gravity = 0
    
    #whatever we draw we haev to update on the display
    pygame.display.update()
    clock.tick(60)          #60FPS

    
    
      
    
    
    


















































