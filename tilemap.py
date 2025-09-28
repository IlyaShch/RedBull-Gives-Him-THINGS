import math
import pygame

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FPS = 60

# Colors (retro palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
class TileMap:
    def __init__(self, layout, tile_size=48):
        self.tile_size = tile_size
        # Your current layout here...
        self.layout = layout
        self.door1=None
        self.door2=None

        self._fit_to_screen()
        self._build_walls()
        self._build_doors()

    def _fit_to_screen(self):
        req_cols = math.ceil(SCREEN_WIDTH  / self.tile_size)
        req_rows = math.ceil(SCREEN_HEIGHT / self.tile_size)

        fixed = []
        for row in self.layout:
            row = list(row)
            if len(row) < req_cols:
                row += ['.'] * (req_cols - len(row))
            row[0] = 'W'
            row[-1] = 'W'
            fixed.append(''.join(row))

        while len(fixed) < req_rows:
            empty = '.' * req_cols
            empty = 'W' + empty[1:-1] + 'W'
            fixed.append(empty)

        fixed[0]  = 'W' * req_cols
        fixed[-1] = 'W' * req_cols

        self.layout = fixed

    def _build_walls(self):
        self.walls = []
        self.dropzones = []   # <<< add this
        for r, row in enumerate(self.layout):
            for c, ch in enumerate(row):
                rect = pygame.Rect(c*self.tile_size, r*self.tile_size,
                                   self.tile_size, self.tile_size)
                if ch == 'W':
                    self.walls.append(rect)
                elif ch == 'Z':  # <<< new case for dropzones
                    self.dropzones.append(rect)
    
    def _build_doors(self):
        self.doors1=[]
        self.doors2=[]
        for r, row in enumerate(self.layout):
            for c, ch in enumerate(row):
                if ch == 'D':
                    self.doors1.append(
                        pygame.Rect(c*self.tile_size, r*self.tile_size,
                                    self.tile_size, self.tile_size)
                    )
                if ch == 'E':
                    self.doors2.append(
                        pygame.Rect(c*self.tile_size, r*self.tile_size,
                                    self.tile_size, self.tile_size)
                    )

    def draw(self, screen):
        # floor tiles
        for r, row in enumerate(self.layout):
            for c, _ in enumerate(row):
                rect = pygame.Rect(c*self.tile_size, r*self.tile_size,
                                   self.tile_size, self.tile_size)
                pygame.draw.rect(screen, (30,30,36), rect)
                pygame.draw.rect(screen, (45,45,52), rect, 1)

        # walls
        for rect in self.walls:
            pygame.draw.rect(screen, (85,85,100), rect)
            pygame.draw.rect(screen, (160,160,175), rect, 2)

        for rect in self.doors1:
            pygame.draw.rect(screen, (255, 255, 255), rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 2)

        for rect in self.doors2:
            pygame.draw.rect(screen, (255, 255, 255), rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 2)

        # dropzones (bright cyan with border)
        for rect in self.dropzones:
            pygame.draw.rect(screen, (0,200,200), rect)
            pygame.draw.rect(screen, (0,255,255), rect, 2)

    def add_target1(self, target_map):
        self.door1=target_map
    
    def add_target2(self, target_map):
        self.door2=target_map
