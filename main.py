import pygame
import random
import os

pygame.init()
pygame.mixer.init()

pygame.display.set_caption("PangPang: Far From Homework")

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 540
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MEDIUM_PURPLE = (147, 112, 219)
RED = (255, 0, 0)

ICON = pygame.image.load(os.path.join("Assets", "Icon.png")).convert()
ICON.set_colorkey(BLACK)
pygame.display.set_icon(ICON)

PANGPANG_IMAGE = pygame.image.load(os.path.join("Assets", "PangPang.png")).convert()
PAPER_BOOK_IMAGES = [pygame.image.load(os.path.join("Assets", "Paper.png")).convert(),
                    pygame.image.load(os.path.join("Assets", "Book.png")).convert()]
POO_IMAGE = pygame.image.load(os.path.join("Assets", "Poo.png")).convert()
EXPLODE_IMAGES = {}
EXPLODE_IMAGES["Homework"] = []
EXPLODE_IMAGES["PangPang"] = []
EXPLODE_IMAGES["Lose"] = []
for i in range(9):
     Explode_Image_Homework = pygame.image.load(os.path.join("Assets", f"Explode{i}.png")).convert()
     Explode_Image_Homework.set_colorkey(BLACK)
     EXPLODE_IMAGES["Homework"].append(pygame.transform.scale(Explode_Image_Homework, (60, 60)))
     Explode_Image_PangPang = pygame.image.load(os.path.join("Assets", f"Explode{i}.png")).convert()
     Explode_Image_PangPang.set_colorkey(BLACK)
     EXPLODE_IMAGES["PangPang"].append(pygame.transform.scale(Explode_Image_PangPang, (39, 39)))
     Explode_Images_Lose = pygame.image.load(os.path.join("Assets", f"Player_Explode{i}.png")).convert()
     Explode_Images_Lose.set_colorkey(BLACK)
     EXPLODE_IMAGES["Lose"].append(pygame.transform.scale(Explode_Images_Lose, (90, 90)))
PANGPANG_LIFE_IMAGE = pygame.transform.scale(PANGPANG_IMAGE, (35, 49))
PANGPANG_LIFE_IMAGE.set_colorkey(BLACK)
UPGRADE_IMAGES = {}
UPGRADE_IMAGES["Poo"] = pygame.image.load(os.path.join("Assets", "Poo_Upgrade.png")).convert()
UPGRADE_IMAGES["Health"] = pygame.image.load(os.path.join("Assets", "Recover_Health.png")).convert()

FONT = pygame.font.match_font("Comic Sans MS")
def Show_Text(Scene, Content, Size, X, Y):
     Font = pygame.font.Font(FONT, Size)
     Text = Font.render(Content, True, WHITE)
     Text_Rect = Text.get_rect()
     Text_Rect.centerx = X
     Text_Rect.top = Y
     Scene.blit(Text, Text_Rect)

pygame.mixer.music.load(os.path.join("Sound Effects", "Peppa Pig.mp3"))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
GIWAWA_SOUND = pygame.mixer.Sound(os.path.join("Sound Effects", "Giwawa.wav"))
GIWAWA_SOUND.set_volume(0.1)
POO_SOUND = pygame.mixer.Sound(os.path.join("Sound Effects", "Poo.wav"))
POO_SOUND.set_volume(0.3)
EXPLODE_SOUNDS = []
for i in range(2):
     Explode_Sounds = pygame.mixer.Sound(os.path.join("Sound Effects", f"Explode{i}.wav"))
     Explode_Sounds.set_volume(0.1)
     EXPLODE_SOUNDS.append(Explode_Sounds)
LOSE_SOUND = pygame.mixer.Sound(os.path.join("Sound Effects", "Lose.wav"))
LOSE_SOUND.set_volume(0.7)
RECOVER_HEALTH_SOUND = pygame.mixer.Sound(os.path.join("Sound Effects", "Upgrade0.wav"))
RECOVER_HEALTH_SOUND.set_volume(0.3)
POO_UPGRADE_SOUND = pygame.mixer.Sound(os.path.join("Sound Effects", "Upgrade1.wav"))
POO_UPGRADE_SOUND.set_volume(0.3)

def Show_Health(Scene, Health, X, Y):
     if Health < 0:
          Health = 0
     BAR_WIDTH = 130
     BAR_HEIGHT = 15
     Current_Health = Health / 20 * BAR_WIDTH
     OUTLINE_RECT = pygame.Rect(X, Y, BAR_WIDTH + 2, BAR_HEIGHT + 2)
     FILL_RECT = pygame.Rect(X, Y, Current_Health, BAR_HEIGHT)
     pygame.draw.rect(Scene, RED, FILL_RECT)
     pygame.draw.rect(Scene, BLACK, OUTLINE_RECT, 2)

def Show_Life(Scene, Life, Image, X, Y):
     for i in range(Life):
          Image_rect = Image.get_rect()
          Image_rect.x = X + 50 * i
          Image_rect.y = Y
          Scene.blit(Image, Image_rect)

def Show_Initiate():
     SCREEN.fill(BLACK)
     Show_Text(SCREEN, "PangPang: Far From Homework", 39, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 9 * 2)
     Show_Text(SCREEN, "WASD to move", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 9 * 3.5)
     Show_Text(SCREEN, "Space to shoot", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 9 * 4)
     Show_Text(SCREEN, "Press any button to start", 17, SCREEN_WIDTH / 2, SCREEN_HEIGHT /  9 * 5)
     Show_Text(SCREEN, "Highest Score: " + str(int(Highest_Score)), 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT /  9 * 6)
     pygame.display.update()
     Start = False
     while not(Start):
          CLOCK.tick(FPS)
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
               elif event.type == pygame.KEYUP:
                    Start = True
                    return False

class PangPang(pygame.sprite.Sprite):
     def __init__(self):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.transform.scale(PANGPANG_IMAGE, (70, 98))
          self.image.set_colorkey(BLACK)
          self.rect = self.image.get_rect()
          self.radius = 35
          self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.3)
          self.XSPEED = 3
          self.YSPEED = 1.7
          self.Shoot_Cooldown = 300
          self.Health = 20
          self.Hidden = False
          self.Hide_Time = 0
          self.Life = 3
          self.Poo = 1
          self.Upgrade_Time = 0

     def update(self):
          KEY_PRESSED = pygame.key.get_pressed()

          if self.Poo > 1 and pygame.time.get_ticks() - self.Upgrade_Time > 3000:
               self.Shoot_Cooldown = 300
               self.Poo = 1

          if self.Hidden and pygame.time.get_ticks() - self.Hide_Time > 1000:
               self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.3)
               self.Hidden = False

          if not(self.Hidden):
               if KEY_PRESSED[pygame.K_w]:
                    self.rect.y -= self.YSPEED
               if KEY_PRESSED[pygame.K_a]:
                    self.rect.x -= self.XSPEED
               if KEY_PRESSED[pygame.K_s]:
                    self.rect.y += self.YSPEED
               if KEY_PRESSED[pygame.K_d]:
                    self.rect.x += self.XSPEED

               if self.rect.bottom < 0:
                    self.rect.top = SCREEN_HEIGHT
               if self.rect.right < 0:
                    self.rect.left = SCREEN_WIDTH
               if self.rect.top > SCREEN_HEIGHT:
                    self.rect.bottom = 0
               if self.rect.left > SCREEN_WIDTH:
                    self.rect.right = 0

     def Shoot(self):
          if not(self.Hidden):
               if self.Poo == 1:
                    POO = Poo(self.rect.centerx, self.rect.top)
                    ALL_SPRITE.add(POO)
                    POO_COLLISION.add(POO)
                    POO_SOUND.play()
               else:
                    POOL = Poo(self.rect.left, self.rect.top)
                    POOR = Poo(self.rect.right, self.rect.top)
                    ALL_SPRITE.add(POOL)
                    ALL_SPRITE.add(POOR)
                    POO_COLLISION.add(POOL)
                    POO_COLLISION.add(POOR)
                    POO_SOUND.play()
                    

     def Hide(self):
          self.Hidden = True
          self.Hide_Time = pygame.time.get_ticks()
          self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT + 777)

     def Poo_Upgrade(self):
          self.Shoot_Cooldown = 0
          self.Poo = 2
          self.Upgrade_Time = pygame.time.get_ticks()

class Paper_Book(pygame.sprite.Sprite):
     def __init__(self):
          pygame.sprite.Sprite.__init__(self)
          self.image = random.choice(PAPER_BOOK_IMAGES)
          self.image.set_colorkey(MEDIUM_PURPLE)
          self.rect = self.image.get_rect()
          self.radius = self.rect.width / 2
          self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
          self.rect.y = random.randrange(-70, -30)
          self.XSPEED = random.randrange(-3, 3)
          self.YSPEED = random.randrange(2, 9)

     def update(self):
          self.rect.x += self.XSPEED
          self.rect.y += self.YSPEED

          if self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
               self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
               self.rect.y = random.randrange(-70, -30)
               self.XSPEED = random.randrange(-3, 3)
               self.YSPEED = random.randrange(1, 3)

class Poo(pygame.sprite.Sprite):
     def __init__(self, X, Y):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.transform.scale(POO_IMAGE, (30, 30))
          self.image.set_colorkey(WHITE)
          self.rect = self.image.get_rect()
          self.radius = 10
          self.rect.centerx = X
          self.rect.bottom = Y
          self.YSPEED = -3

     def update(self):
          self.rect.y += self.YSPEED

          if self.rect.bottom < 0:
               self.kill()

class Explode_Animation(pygame.sprite.Sprite):
     def __init__(self, Center, Type):
          pygame.sprite.Sprite.__init__(self)
          self.image = EXPLODE_IMAGES[Type][0]
          self.rect = self.image.get_rect()
          self.rect.center = Center
          self.type = Type
          self.frame = 0
          self.last_update = pygame.time.get_ticks()
          if Type == "Lose":
               self.frame_rate = 100
          else:
               self.frame_rate = 50

     def update(self):
          Now = pygame.time.get_ticks()
          if Now - self.last_update > self.frame_rate:
               self.last_update = Now
               self.frame += 1
               if self.frame == len(EXPLODE_IMAGES[self.type]):
                    self.kill()
               else:
                    self.image = EXPLODE_IMAGES[self.type][self.frame]
                    Center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = Center

class Upgrade(pygame.sprite.Sprite):
     def __init__(self, Center):
          pygame.sprite.Sprite.__init__(self)
          self.type = random.choice(["Poo", "Health"])
          self.image = UPGRADE_IMAGES[self.type]
          self.image.set_colorkey(BLACK)
          self.rect = self.image.get_rect()
          self.rect.center = Center
          self.YSPEED = 3

     def update(self):
          self.rect.y += self.YSPEED
          if self.rect.top > SCREEN_HEIGHT:
               self.kill()

Continue = True
Shoot_Time = 0
Initiate = True
Highest_Score = 0

while Continue:
     CLOCK.tick(FPS)
     Current_Time = pygame.time.get_ticks()

     if Initiate:
          if Show_Initiate():
               break
          Initiate = False

          Score = 0

          ALL_SPRITE = pygame.sprite.Group()
          PAPER_BOOK_COLLISIONS = pygame.sprite.Group()
          POO_COLLISION = pygame.sprite.Group()
          UPGRADE_ITEMS = pygame.sprite.Group()
          PANGPANG = PangPang()
          ALL_SPRITE.add(PANGPANG)

          for i in range(9):
               PAPER_BOOK = Paper_Book()
               ALL_SPRITE.add(PAPER_BOOK)
               PAPER_BOOK_COLLISIONS.add(PAPER_BOOK)

     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               Continue = False
          elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE:
                    if Current_Time - Shoot_Time > PANGPANG.Shoot_Cooldown:
                         Shoot_Time = Current_Time
                         PANGPANG.Shoot()

     ALL_SPRITE.update()
     Hit = pygame.sprite.groupcollide(PAPER_BOOK_COLLISIONS, POO_COLLISION, True, True, pygame.sprite.collide_circle)
     for Hit in Hit:
          PAPER_BOOK = Paper_Book()
          ALL_SPRITE.add(PAPER_BOOK)
          PAPER_BOOK_COLLISIONS.add(PAPER_BOOK)
          Score += (Current_Time / 10000 + Hit.radius / 2)
          random.choice(EXPLODE_SOUNDS).play()
          Explode = Explode_Animation(Hit.rect.center, "Homework")
          ALL_SPRITE.add(Explode)
          if random.random() > 0.87:
               UPGRADE = Upgrade(Hit.rect.center)
               ALL_SPRITE.add(UPGRADE)
               UPGRADE_ITEMS.add(UPGRADE)

     Hit = pygame.sprite.spritecollide(PANGPANG, PAPER_BOOK_COLLISIONS, True, pygame.sprite.collide_circle)
     for Hit in Hit:
          PAPER_BOOK = Paper_Book()
          ALL_SPRITE.add(PAPER_BOOK)
          PAPER_BOOK_COLLISIONS.add(PAPER_BOOK)
          Explode = Explode_Animation(Hit.rect.center, "PangPang")
          ALL_SPRITE.add(Explode)
          GIWAWA_SOUND.play()
          PANGPANG.Health -= int(Hit.radius / 7)
          if PANGPANG.Health <= 0:
               LOSE_SOUND.play()
               PANGPANG.Life -= 1
               Explode = Explode_Animation(PANGPANG.rect.center, "Lose")
               ALL_SPRITE.add(Explode)
               PANGPANG.Hide()
               if PANGPANG.Life != 0:
                    PANGPANG.Health = 20

     if PANGPANG.Life == 0 and not(Explode.alive()):
          if Highest_Score < Score:
               Highest_Score = Score

          Initiate = True

     Hit = pygame.sprite.spritecollide(PANGPANG, UPGRADE_ITEMS, True)
     for Hit in Hit:
          if Hit.type == "Health":
               RECOVER_HEALTH_SOUND.play()
               PANGPANG.Health += 1
               if PANGPANG.Health > 20:
                    PANGPANG.Health = 20
          else:
               POO_UPGRADE_SOUND.play()
               PANGPANG.Poo_Upgrade()

     SCREEN.fill(BLACK)
     ALL_SPRITE.draw(SCREEN)
     Show_Text(SCREEN, "SCORE: " + str(int(Score)), 30, SCREEN_WIDTH / 2, 5)
     Show_Health(SCREEN, PANGPANG.Health, 17, 21)
     Show_Life(SCREEN, PANGPANG.Life, PANGPANG_LIFE_IMAGE, SCREEN_WIDTH - 150, 3)
     pygame.display.update()

pygame.quit