import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_run_1 = pygame.image.load("graphics/player/player_run_1.png").convert_alpha()
        player_run_2 = pygame.image.load("graphics/player/player_run_2.png").convert_alpha()
        player_run_3 = pygame.image.load("graphics/player/player_run_3.png").convert_alpha()
        player_run_4 = pygame.image.load("graphics/player/player_run_4.png").convert_alpha()
        player_run_5 = pygame.image.load("graphics/player/player_run_5.png").convert_alpha()
        player_run_6 = pygame.image.load("graphics/player/player_run_6.png").convert_alpha()
        player_run_7 = pygame.image.load("graphics/player/player_run_7.png").convert_alpha()
        player_run_8 = pygame.image.load("graphics/player/player_run_8.png").convert_alpha()
        player_run_9 = pygame.image.load("graphics/player/player_run_9.png").convert_alpha()
        self.player_walk = [player_run_1,player_run_2,player_run_3,player_run_4,player_run_5,player_run_6,player_run_7,player_run_8,player_run_9]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/player_run_9.png').convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (300,350))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 350:
            self.gravity = -20
            #self.jump_sound.play()
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 350:
            self.rect.bottom = 350
    
    def animation_state(self):
        if self.rect.bottom < 350:
            self.image = self.player_jump
        else:
            self.player_index += 0.2
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 260
        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 350
            
        self.animation_index = 0            
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
            
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000)- start_time#gives us game time in milliseconds
    score_surf = test_font.render(f'Score: {current_time}',False,'Yellow')
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

pygame.init()
width = 800
screen = pygame.display.set_mode((800, 400))#creates a display serfice (width, height)in pixles
pygame.display.set_caption("runner")
clock = pygame.time.Clock()#adds clock object used to contrl frame rate
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)#specifying (font type, font size) if you type None for type it goes to defalt for pygame
game_active = False
start_time = 0
score = 0
#bg_music = pygame.mixer.Sound('audio/music.wav')
#bg_music.play(loops = -1)

#groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()
#background Images
sky_surface = pygame.image.load("graphics/NightCitySky.png").convert()
ground_surface = pygame.image.load("graphics/GroundRoad.png").convert()

UFO_image = pygame.image.load("graphics/UFO.png")
UFO_image = pygame.transform.scale2x(UFO_image)

i = 0#for moving background


#intro screen
player_stand = pygame.image.load('graphics/player/player_run_1.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name =test_font.render('Pixel Runner', False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render ('press space to run',False, (111, 196, 169))
game_message_rect = game_message.get_rect(center =(400,340))

#timer
obstacle_timer= pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)#event to triger, how often to trigger in miliseconds



while (True):#game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()            
                
        if game_active:    
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))
                
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
            
           
             
       
        
    if game_active:     
              #order matters here for blit. if it comes second and is overlaping it will cover what came first. like layering in aseprite. bottom is on top  
        screen.blit(sky_surface, (0, 0))#(surface, position) in pygame the 0,0 point is at the top left of the graph. not the bottem left like normal.
        screen.blit(ground_surface, (0, 300))
        


        #moving background, doesnt quite work. 
        screen.blit(sky_surface, (i, 0))
        screen.blit(sky_surface,(width+1,0))
        if (i==-width):
            screen.blit(sky_surface,(width+i,0))
            i=0
        i-=1
        
        
        screen.blit(ground_surface, (i, 300))
        screen.blit(ground_surface,(width+i,300))
        if (i==-width):
            screen.blit(ground_surface,(width+i,300))
            i=0
        i-=1


            
        screen.blit(UFO_image, (10,150))
# =============================================================================
#         pygame.draw.rect(screen, 'Red',score_rect)#draw a pygame.draw.shapename(display surface, color, location, width(optional),border radius (optional, it rounds the edges of the shape))
#         pygame.draw.rect(screen, 'Red',score_rect,10)#when using width the center is not colored, this one colors it
#         #pygame.draw.ellipse(screen, 'Brown',pygame.Rect(50,200,100,100))#draw a circle. specify Rect for circle to be in. pygame.draw.ellipse(drawing surface, color, pygame.rect(left,top,width,height))
#         #pygame.draw.line(screen, 'Gold',(0,0),(800,400),10)#how to draw lines: pygame.draw.line(drawing surface, color, start point, end point, width)
#         screen.blit(score_surf,(score_rect))
# =============================================================================
        score = display_score()
        
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        game_active = collision_sprite()
        
    else:
        screen.fill('Green')
        screen.blit(player_stand,player_stand_rect)
        
        score_message = test_font.render(f'Your score: {score}',False,(111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name,game_name_rect)
        
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
    

    pygame.display.update()#continuesly updates window.
    pygame.display.flip()
    clock.tick(60)#tells pygame that the loop shouldnt run faster than 60 times per second
    