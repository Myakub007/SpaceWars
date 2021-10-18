import os
import sys
import pygame
from pygame.constants import USEREVENT
# initialize pygame
pygame.init()
# Initialize pygame font
pygame.font.init()

# Initialize music in pygame
pygame.mixer.init()

# creating the screen
WIDTH = 900
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Data',"Shoot!")# Title of the screen.


# Adding sound 
BULLET_HIT = pygame.mixer.Sound(os.path.join('Data','hit.mp3'))
BULLET_FIRE = pygame.mixer.Sound(os.path.join('Data','shot.mp3'))

# music
pygame.mixer.music.load(os.path.join('Data','Pixel_Birds.mp3'))
pygame.mixer.music.play(-1)
Music=pygame.mixer.music.set_volume(0.1)

#COlORs
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW =(255,255,0)
RED = (255, 0, 0)
INDIGO = (80,208,255)

FPS = 60

#collision with bullets
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

# Adding health font 
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 40)


# value of movement
VEL = 5

# velocity of bullets
BULLET_VEL = 7

# scale of image on screen
Spaceship_width, Spaceship_height = 60,70

# Loading images
Yellow_Spaceship_Image = pygame.image.load(os.path.join('Data','spaceship_yellow.png'))# location of spaceship images

Yellow_Spaceship = pygame.transform.scale(Yellow_Spaceship_Image , (Spaceship_width , Spaceship_height))

Yellow_Spaceship_Rotated = pygame.transform.rotate(Yellow_Spaceship, 90) # Rotate the image (name, angle)

Red_Spaceship_Image = pygame.image.load(os.path.join('Data','spaceship_red.png'))
Red_Spaceship = pygame.transform.scale(Red_Spaceship_Image , (Spaceship_width , Spaceship_height)) #Change Size of spaceship
Red_Spaceship_Rotated = pygame.transform.rotate(Red_Spaceship, 270) # Rotate the image (name, angle)

# BORDER of single spaceship 
BORDER = pygame.Rect(WIDTH//2-5, 0 , 10 , HEIGHT)
# (limit, start point, width of border , hieght(fullscreen) )


# Loading Background
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Data','galaxyspace_background.png')),(WIDTH, HEIGHT))



def Winner(text):
   draw_text = WINNER_FONT.render( text, 1 , WHITE)
   screen.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2 , HEIGHT/2 - draw_text.get_height()/2))
   pygame.display.update()
   pygame.time.delay(5000)


def Screen(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
   #Drawing the background
    screen.blit(SPACE, (0,0))

# health of players
    red_health_text = HEALTH_FONT.render('Health: ' + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), 1, WHITE)

    # Showing the health
    screen.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10,10 ))
    screen.blit(yellow_health_text, (10,10 ))


   #  screen.fill(INDIGO) # change screen color
   #  # screen color should always be added first in code
    
    #ADDING a border
    pygame.draw.rect(screen, BLACK, BORDER)

    # DRAWING BULLETS ON SCREEN
    for bullet in red_bullets:
       pygame.draw.rect(screen, RED, bullet)
    for bullet in yellow_bullets:
       pygame.draw.rect(screen, YELLOW, bullet)


    # load the image on screen
    # Use blit to load on screen
    screen.blit(Yellow_Spaceship_Rotated ,(yellow.x,yellow.y)) 
    screen.blit(Red_Spaceship_Rotated ,(red.x, red.y)) 


    pygame.display.update() # update the display to see changes done



def yellow_Movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
           yellow.x -= VEL 
        if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # RIGHT
           yellow.x += VEL 
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
           yellow.y  -= VEL 
        if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT : # DOWN
           yellow.y += VEL 



def red_Movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT]and red.x - VEL > BORDER.x : # LEFT
           red.x -= VEL 
        if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
           red.x += VEL
        if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
           red.y -= VEL 
        if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: # DOWN
           red.y += VEL 


def handle_bullets(yellow_bullets,red_bullets, red, yellow):
   for bullets in yellow_bullets:
      bullets.x += BULLET_VEL
      if red.colliderect(bullets): # both should be pygame rectangles
         pygame.event.post(pygame.event.Event(RED_HIT))
         yellow_bullets.remove(bullets)
      elif bullets.x > WIDTH:
         yellow_bullets.remove(bullets)


   for bullets in red_bullets:
      bullets.x -= BULLET_VEL
      if yellow.colliderect(bullets):
         pygame.event.post(pygame.event.Event(YELLOW_HIT))
         red_bullets.remove(bullets)
      elif bullets.x < 0:
         red_bullets.remove(bullets)



def main():
    # framerate
    clock = pygame.time.Clock()

    # Defining Health
    red_health = 10
    yellow_health = 10

    #adding Bullets
    red_bullets = []
    yellow_bullets = []
    MAX_BULLETS = 3

    # MUsic
    Music

    # movement representation
    
    yellow = pygame.Rect(40,100 , Spaceship_width, Spaceship_height)
    red = pygame.Rect( 790, 100, Spaceship_width,   Spaceship_height)
# game loop 
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()

    # OR
    
    run = True
    while run:
        # Framerate value
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

                # shoot!
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_LCTRL and len(yellow_bullets)< MAX_BULLETS:
                  bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10 , 5)
                  BULLET_FIRE.play()
                  yellow_bullets.append(bullet)


               if event.key == pygame.K_RCTRL and len(red_bullets)< MAX_BULLETS:
                  bullet = pygame.Rect(red.x , red.y + yellow.height//2 - 2, 10 , 5)
                  BULLET_FIRE.play()
                  red_bullets.append(bullet)

            if event.type == RED_HIT:
               red_health -= 1
               BULLET_HIT.play()
            
            if event.type == YELLOW_HIT:
               yellow_health -= 1
               BULLET_HIT.play()

        winner_text = ""
      
        if red_health <= 0:
               winner_text = "Yellow Wins!"
        if yellow_health <= 0:
               winner_text = "Red Wins!"
        if winner_text != "":
         Winner(winner_text)
         break


        handle_bullets(yellow_bullets, red_bullets, red , yellow)
        keys_pressed = pygame.key.get_pressed()
        yellow_Movement(keys_pressed,yellow)
        red_Movement(keys_pressed,red)

        Screen(red , yellow , red_bullets, yellow_bullets, red_health,yellow_health)

    main()
if __name__ == '__main__': # only run game when main file is run directly
   main()

sys.exit()

