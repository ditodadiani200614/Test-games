# shoot them up
import os

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
width = 480
height = 600
fps = 60
POWERUP_TIME = 5000
# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("shoot them up")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    m = mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (40, 60))
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image,red, self.rect.center,self.radius)
        self.rect.centerx = width / 2
        self.rect.centery = height - 35
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()


    def update(self):
        #tmeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power=1
        # unhide if hidden

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = width / 2
            self.rect.bottom = height - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
    def powerup(self):
        self.power+=1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.top)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                all_sprites.add(bullet1,bullet2)
                bullets.add(bullet1,bullet2)
                shoot_sound.play()

    def hide(self):
        # hide the player temporarly
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (width / 2, height + 200)


class mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image_orig.get_rect()
        self.radius = int(self.rect.width / 2)
        # pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 5)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 150:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = new_image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.y > height + 10 or self.rect.left < -25 or self.rect.right > width + 25:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(bullet_img, 90)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top
        if self.rect.bottom < 0:
            self.kill()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top
        if self.rect.top > height:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.fram_rate = 10

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.fram_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    draw_text(screen,"SHMUPBYDITO",64,width/2,height/4)
    draw_text(screen, "Arrow keys move,Space to fire", 22, width / 2, height / 2)
    draw_text(screen,'Press a key to begin',18,width / 2, height *3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False




# load all game graphics
background = pygame.image.load(path.join(img_dir, 'nightskycolor.png')).convert()
background = pygame.transform.scale(background, (width, height))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'shmupdragon.png')).convert()
player_img.set_colorkey(black)
meteor_list = ['meteorGrey_big4.png', 'meteorGrey_tiny2.png', 'meteorGrey_med2.png', 'meteorGrey_big3.png',
               'meteorGrey_med1.png', 'meteorGrey_small2.png']
meteor_images = []
bullet_img = pygame.image.load(path.join(img_dir, 'image14.png')).convert()
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
all_sprites = pygame.sprite.Group()
explosion_anim = {'lg': [], 'sm': [], 'pl': []}
for i in range(31):
    filename = 'expl_09_{:04}.png'.format(i)
    img1 = pygame.image.load(path.join(img_dir, filename)).convert()
    img1.set_colorkey(black)
    img_pl = pygame.transform.scale(img1, (125, 125))
    explosion_anim['pl'].append(img_pl)

for i in range(24):
    filename = 'expl_02_{:04}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (125, 125))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (70, 70))
    explosion_anim['sm'].append(img_sm)
powerup_images = {'shield': pygame.image.load(path.join(img_dir, 'powerupYellow_shield.png')).convert(),
                  'gun': pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()}

# load all the game sounds

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Shoot1.wav'))
explosion_sound = pygame.mixer.Sound(path.join(snd_dir, 'Boom1.wav'))
die_sound = pygame.mixer.Sound(path.join(snd_dir, 'Boom11.wav'))

pygame.mixer.music.load(path.join(snd_dir, 'frozenjam-seamlessloop.ogg'))
pygame.mixer.music.set_volume(0.4)
# game loop
game_over = True


pygame.mixer.music.play(loops=-1
                        )
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        for i in range(8):
            newmob()
            score = 0


    clock.tick(fps)
    # process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # update
    all_sprites.update()
    # check to see if a bullet hit  a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:

        score += (50 - hit.radius)
        explosion_sound.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.95:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # check to see if mob hit the the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        explosion_sound.play()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            die_sound.play()
            death_explosion = Explosion(player.rect.center, 'pl')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100


    # check to see if playeer hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += 20
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()


# if the player died and the explosion has finished playing
    if player.lives == 0 and not death_explosion.alive():
        game_over = True







    # draw/render
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, width / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, width - 100, 5, player.lives, player_img)
    # *after * drawing everything , fli the display
    pygame.display.flip()

pygame.quit()
