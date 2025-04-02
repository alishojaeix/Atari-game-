import pygame
import random
import requests
from io import BytesIO

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pixel Space Adventure")
clock = pygame.time.Clock()

# Load online pixel art assets
def load_online_image(url, size):
    try:
        response = requests.get(url)
        img = pygame.image.load(BytesIO(response.content))
        return pygame.transform.scale(img, size)
    except:
        # Fallback pixel art
        surf = pygame.Surface(size)
        surf.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        return surf

# Pixel art assets from online sources (replace with actual pixel art URLs)
PLAYER_IMG = load_online_image("https://www.pixilart.com/images/art/123abc.png", (50, 50))
ENEMY_IMG = load_online_image("https://www.pixilart.com/images/art/456def.png", (40, 40))
BULLET_IMG = load_online_image("https://www.pixilart.com/images/art/789ghi.png", (10, 20))
BACKGROUND = load_online_image("https://www.pixilart.com/images/art/000jkl.png", (800, 600))

# Game classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (100, 300)
        self.speed = 5
        self.health = 100
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 600:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed
            
    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = random.randint(50, 550)
        self.speed = random.randint(1, 4)
        
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = 800
            self.rect.y = random.randint(50, 550)
            self.speed = random.randint(1, 4)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = BULLET_IMG
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speed = 10
        
    def update(self):
        self.rect.x += self.speed
        if self.rect.left > 800:
            self.kill()

# Game setup
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

score = 0
font = pygame.font.SysFont('pixelfont', 30)

# Game loop
running = True
while running:
    clock.tick(60)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # Update
    all_sprites.update()
    
    # Collisions
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        player.health -= 1
        if player.health <= 0:
            running = False
    
    # Render
    screen.blit(BACKGROUND, (0, 0))
    all_sprites.draw(screen)
    
    # UI
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    health_text = font.render(f"Health: {player.health}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))
    
    pygame.display.flip()

pygame.quit()
