"""

Movement determined by a speed and a heading

LIMITATIONS: sketchy sprite collisions, glitching together

"""



import random
import pygame
import math


class Person:
    def __init__(self, position, size):
        self.x, self.y = position
        self.size = size
        self.colour = (190, 190, 190)

        self.speed = 1.5
        self.angle = math.pi

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def collide(self, person):
        dx = self.x - person.x
        dy = self.y - person.y

        distance = math.hypot(dx, dy)
        if distance <= 2 * self.size:
            # calculate angle of tangent between two people
            tangent = math.atan2(dy, dx)
            angle = tangent + (math.pi / 2)

            self.angle = 2 * tangent - self.angle
            person.angle = 2 * tangent - person.angle

            self.speed, person.speed = person.speed, self.speed

            # overlap = 0.5 * (self.size + person.size - distance + 1)
            self.x += math.sin(angle) 
            self.y -= math.cos(angle) 
            person.x += math.sin(angle)  
            person.y -= math.cos(angle) 


class Environment:
    def __init__(self, dimensions):
        self.width, self.height = dimensions
        self.population = []

        self.bg_colour = (255, 255, 255)

    def create_population(self, n, size):
        for i in range(n):
            x = random.uniform(size, self.width - size)
            y = random.uniform(size, self.height - size)

            p = Person((x, y), size)
            p.angle = random.uniform(0, 2 * math.pi)

            self.population.append(p)

            for p2 in self.population[:-1]:
                dx = p.x - p2.x
                dy = p.y - p2.y
                distance = math.hypot(dx, dy)

                if distance < 2 * p.size:
                    diff = (2 * p.size) - distance
                    p.x += math.sin(p.angle) * diff
                    p.y -= math.cos(p.angle) * diff

    def bounce(self, person):
        """ Reflects off boundaries """
        if person.x > self.width - person.size:
            person.x = self.width - person.size
            person.angle *= -1
        elif person.x < person.size:
            person.x = person.size
            person.angle *= -1

        if person.y > self.height - person.size:
            person.y = self.height - person.size
            person.angle = math.pi - person.angle
        elif person.y < person.size:
            person.y = person.size
            person.angle = math.pi - person.angle

    def update(self):
        for i, person in enumerate(self.population):
            person.move()
            self.bounce(person)

            for person2 in self.population[i + 1:]:
                if person2 != person:
                    person.collide(person2)


def main():
    pygame.init()
    width, height = 1200, 500
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Viral Spread Simulation')

    environment = Environment((width, height))

    environment.create_population(100, 15)
    


    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        environment.update()

        window.fill(environment.bg_colour)

        for p in environment.population:
            x, y = int(p.x), int(p.y)
            pygame.draw.circle(window, p.colour, (x, y), p.size, 0)


        pygame.display.update()
        clock.tick(60)  



if __name__ == "__main__":
    main()
        

        