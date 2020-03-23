import random
import pygame
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style



class Person:
    def __init__(self, position, size):
        self.x, self.y = position
        self.size = size
        self.colour = (190, 190, 190)
        self.infected_colour = (255, 90, 25)

        self.infected = False

        self.xvel = (random.uniform(0.8, 1.5)) * ((-1) ** random.randint(1, 2))
        self.yvel = (random.uniform(0.8, 1.5)) * ((-1) ** random.randint(1, 2))

    def move(self):
        self.x += self.xvel
        self.y += self.yvel

    def collide(self, person, environment):
        # vector speed
        speed = math.hypot(self.xvel, self.yvel)
        
        # distance between two people
        dx = -(self.x - person.x)
        dy = -(self.y - person.y)

        if dx > 0:
            angle = math.atan(dy / dx)
            xvel = -speed * math.cos(angle)
            yvel = -speed * math.sin(angle)
        elif dx < 0:
            if dy > 0:
                angle = math.pi + math.atan(dy / dx)
                xvel = -speed * math.cos(angle)
                yvel = -speed * math.sin(angle)
            elif dy < 0:
                angle = -math.pi + math.atan(dy / dx)
                xvel = -speed * math.cos(angle)
                yvel = -speed * math.sin(angle)
        else:
            if dy > 0:
                angle = -(math.pi / 2)
            else:
                angle = math.pi / 2
            xvel = speed * math.cos(angle)
            yvel = speed * math.sin(angle)
        if dx < 0 and dy == 0:
            if dx < 0:
                angle = 0
            else:
                angle = math.pi
            xvel = speed * math.cos(angle)
            yvel = speed * math.sin(angle)

        self.xvel = xvel
        self.yvel = yvel

        if self.infected and not person.infected: 
            person.infected = True
            environment.infected_count += 1
        elif person.infected and not self.infected:
            self.infected = True
            environment.infected_count += 1


class Environment:
    def __init__(self, dimensions):
        self.width, self.height = dimensions
        self.population = []

        self.infected_count = 1

        self.bg_colour = (255, 255, 255)

    def create_population(self, n, size):
        for i in range(n):
            x = random.uniform(size, self.width - size)
            y = random.uniform(size, self.height - size)

            p = Person((x, y), size)

            self.population.append(p)

    def bounce(self, person):
        # reflect off boundaries

        if person.x > self.width - person.size:
            person.x = self.width - person.size
            person.xvel *= -1
        elif person.x < person.size:
            person.x = person.size
            person.xvel *= -1

        if person.y > self.height - person.size:
            person.y = self.height - person.size
            person.yvel *= -1
        elif person.y < person.size:
            person.y = person.size
            person.yvel *= -1

    def update(self):
        # call functions to update a frame
        for p1 in self.population:
            self.bounce(p1)
            p1.move()
            for p2 in self.population:
                if p1 != p2:
                    dx = p1.x - p2.x
                    dy = p1.y - p2.y
                    if math.hypot(dx, dy) <= (p1.size + p2.size):
                        p1.collide(p2, self)

    def draw(self, window):
        for p in self.population:
            x, y = int(p.x), int(p.y)
            if p.infected:
                colour = p.infected_colour
            else:
                colour = p.colour
            pygame.draw.circle(window, colour, (x, y), p.size)

    


def main():
    pygame.init()
    width, height = 1000, 500
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Viral Spread Simulation')


    environment = Environment((width, height))
    environment.create_population(100, 8)
    # infect 1 person
    environment.population[random.randint(0, len(environment.population))].infected = True
    
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        environment.update()
        window.fill(environment.bg_colour)
        environment.draw(window)

        infected = environment.infected_count
        total = len(environment.population)
        print("Total infected: {}/{}".format(infected, total))



        pygame.display.flip()
        clock.tick(60)  



if __name__ == "__main__":
    main()
        

        