import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jet Plane Bombing Animation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

jet_img = pygame.image.load('jet.png')
jet_img = pygame.transform.scale(jet_img, (100, 50))
bomb_img = pygame.image.load('bomb.png')
bomb_img = pygame.transform.scale(bomb_img, (30, 30))
house_img = pygame.image.load('building.png')
house_img = pygame.transform.scale(house_img, (100, 100))
explosion_img = pygame.image.load('explosion.png')
explosion_img = pygame.transform.scale(explosion_img, (100, 100))

class Jet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 5

    def move(self):
        self.x -= self.vel
        if self.x < -100: 
            self.x = WIDTH

    def draw(self, win):
        win.blit(jet_img, (self.x, self.y))

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10
        self.exploded = False  
        self.explosion_timer = 0  
        self.house_hit = None  

    def move(self):
        self.y += self.vel

    def draw(self, win):
        if not self.exploded:
            win.blit(bomb_img, (self.x, self.y))

class House:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        win.blit(house_img, (self.x, self.y))

def main():
    clock = pygame.time.Clock()
    run = True
    jet = Jet(WIDTH, 200)  
    bombs = []
    houses = [House(i * 150, HEIGHT - 150) for i in range(6)]  
    collisions = 0  

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        jet.move()

        if random.randint(0, 100) < 5:
            bomb = Bomb(jet.x + 35, jet.y + 50)
            bombs.append(bomb)

        for bomb in bombs:
            bomb.move()
            for house in houses:
                if not bomb.exploded and bomb.x > house.x and bomb.x < house.x + 100 and bomb.y > house.y and bomb.y < house.y + 100:
                    bomb.exploded = True
                    bomb.explosion_timer = 30 
                    bomb.house_hit = house  
                    collisions += 1  

        WIN.fill(WHITE)
        for house in houses:
            house.draw(WIN)  
        jet.draw(WIN)
        for bomb in bombs:
            bomb.draw(WIN)
            if bomb.exploded:
                if bomb.house_hit:
                    WIN.blit(explosion_img, (bomb.house_hit.x + 50 - 50, bomb.house_hit.y + 50 - 50))
                bomb.explosion_timer -= 1
                if bomb.explosion_timer <= 0:
                    bombs.remove(bomb)  

        font = pygame.font.Font(None, 36)
        text = font.render(f'Collisions: {collisions}', True, BLACK)
        WIN.blit(text, (10, 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
