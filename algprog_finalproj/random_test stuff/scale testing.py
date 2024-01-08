import pygame

class objecttt(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bigger-block.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

pygame.init()

therun = True
scx = 500
scy = 500
dis = pygame.display.set_mode((scx, scy))
objects = pygame.sprite.Group()

world_data = [
    [1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1,1  ,1  ,1  ,1  ,1,0  ,0  ,0  ,1  ],
    [1  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1,0  ,0  ,0  ,1  ,1,0  ,0  ,0  ,1  ],
    [1  ,0  ,1  ,1  ,1  ,1  ,1  ,1  ,0  ,1,0  ,0  ,0  ,1  ,1,0  ,0  ,0  ,1  ],
    [1  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1,0  ,0  ,0  ,1  ,1,0  ,0  ,0  ,1  ],
    [1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1,0  ,0  ,0  ,1  ,1,0  ,0  ,0  ,1  ],
    [1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1,0  ,0  ,0  ,1  ,1,0  ,0  ,0  ,1  ],
    [1  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1,0  ,0  ,0  ,1  ,1,0  ,0  ,0  ,1  ],
    [1  ,0  ,1  ,1  ,1  ,1  ,1  ,1  ,0  ,1,0  ,0  ,0  ,1 ,1,0  ,0  ,0  ,1  ],
    [1  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1,0  ,0  ,0  ,1  ,1,0  ,0  ,0  ,1  ],
    [1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1,0  ,0  ,0  ,1  ,1,0  ,0  ,0  ,1  ],
    [1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1,0  ,0  ,0  ,1  ,1,0  ,0  ,0  ,1  ],
    [1  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1,0  ,0  ,0  ,1  ,1,0  ,0  ,0  ,1  ],
    [1  ,0  ,1  ,1  ,1  ,1  ,1  ,1  ,0  ,1,0  ,0  ,0  ,1  ,1,0  ,0  ,0  ,1  ],
    [1  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1,0  ,0  ,0  ,1  ,1,0  ,0  ,0  ,1  ],
    [1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1  ,1,1  ,1  ,1  ,1  ,1]

]
tilelis = []
cell_size = 32  # Adjust the cell size as needed

for y in range(len(world_data)):
    for x in range(len(world_data[y])):
        if world_data[y][x] == 1:
            tile = objecttt(x * cell_size, y * cell_size)
            objects.add(tile)

while therun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            therun = False

    k = pygame.key.get_pressed()

    objects.update()
    dis.fill((255, 255, 255))
    objects.draw(dis)
    pygame.display.update()
