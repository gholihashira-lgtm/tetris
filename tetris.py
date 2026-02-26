import pygame
import random

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 128, 0),
    (128, 0, 255),
    (0, 255, 128),
    (255, 0, 128),
    (128, 255, 0),
    (0, 128, 255),
    (255, 128, 128),
    (128, 255, 128),
    (128, 128, 255),
    (255, 200, 0),
    (200, 0, 255),
    (0, 255, 200),
    (255, 100, 100),
    (100, 255, 100),
]

shapes = [
    [[1, 1, 1, 1]],  
    [[1, 1, 1], [0, 1, 0]],  
    [[1, 1, 1], [1, 0, 0]],  
    [[1, 1, 1], [0, 0, 1]],  
    [[0, 1, 1], [1, 1, 0]],  
    [[1, 1], [1, 1]],  
    [[1, 1, 0], [0, 1, 1]],  
    [[1]],  
    [[1, 1, 1, 1, 1]],  
    [[1, 1, 1], [1, 0, 1]],  
    [[1, 1], [1, 0], [1, 0]],  
    [[1, 1, 1, 1], [0, 0, 0, 1]],  
    [[1, 1, 1], [0, 1, 0], [0, 1, 0]],  
    [[1, 1, 0, 0], [0, 1, 1, 1]],  
    [[1, 0, 0], [1, 1, 1], [0, 0, 1]],  
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],  
    [[1, 1, 1, 1], [0, 1, 0, 0]],  
    [[1, 1, 1], [1, 0, 1], [1, 0, 1]],  
    [[1, 1, 1, 1, 1, 1]],  
    [[1, 1], [1, 1], [1, 1]],  
    [[1, 0, 1], [1, 1, 1], [1, 0, 1]],  
    [[1, 1, 1, 1], [1, 0, 0, 0]],  
    [[1, 1, 0], [0, 1, 1], [0, 0, 1]],  
    [[0, 0, 1], [0, 1, 1], [1, 1, 0]],  
    [[1, 1, 1, 0], [0, 0, 1, 1]],  
]

class Tetris:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "start"
        self.field = []
        self.width = 12
        self.height = 22
        self.x = 150
        self.y = 80
        self.zoom = 28
        self.shape = None
        self.field = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.next_shape = None
        
    def new_shape(self):
        if self.next_shape is None:
            self.next_shape = Shape(0, 0)
        
        self.shape = self.next_shape
        self.shape.x = self.width // 2 - len(self.shape.get_matrix()[0]) // 2
        self.shape.y = 0
        self.next_shape = Shape(0, 0)
        
    def intersects(self):
        if not self.shape:
            return True
            
        shape_matrix = self.shape.get_matrix()
        for i in range(len(shape_matrix)):
            row = shape_matrix[i]
            for j in range(len(row)):
                if row[j]:
                    new_x = j + self.shape.x
                    new_y = i + self.shape.y
                    
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return True
                    if new_y >= 0 and self.field[new_y][new_x]:
                        return True
        return False
    
    def break_lines(self):
        lines_cleared = 0
        for i in range(self.height - 1, -1, -1):
            if all(self.field[i][j] for j in range(self.width)):
                lines_cleared += 1
                for k in range(i, 0, -1):
                    for j in range(self.width):
                        self.field[k][j] = self.field[k - 1][j]
                for j in range(self.width):
                    self.field[0][j] = 0
        
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared >= 4:
            self.score += 800
        
        self.level = 1 + self.score // 1000
    
    def go_space(self):
        while not self.intersects():
            self.shape.y += 1
        self.shape.y -= 1
        self.freeze()
    
    def go_down(self):
        self.shape.y += 1
        if self.intersects():
            self.shape.y -= 1
            self.freeze()
    
    def freeze(self):
        shape_matrix = self.shape.get_matrix()
        for i in range(len(shape_matrix)):
            row = shape_matrix[i]
            for j in range(len(row)):
                if row[j]:
                    if self.shape.y + i >= 0:
                        self.field[self.shape.y + i][self.shape.x + j] = self.shape.color
        
        self.break_lines()
        self.new_shape()
        if self.intersects():
            self.state = "gameover"
    
    def go_side(self, dx):
        old_x = self.shape.x
        self.shape.x += dx
        if self.intersects():
            self.shape.x = old_x
    
    def rotate(self):
        if self.shape:
            old_rotation = self.shape.rotation
            self.shape.rotation = (self.shape.rotation + 1) % 4
            if self.intersects():
                self.shape.rotation = old_rotation

class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(shapes) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0
    
    def get_matrix(self):
        shape = shapes[self.type]
        rows = len(shape)
        cols = len(shape[0]) if rows > 0 else 0
        
        size = max(rows, cols)
        matrix = [[0 for _ in range(size)] for _ in range(size)]
        
        for i in range(rows):
            for j in range(cols):
                if shape[i][j]:
                    matrix[i][j] = 1
        
        for _ in range(self.rotation % 4):
            rotated = [[0 for _ in range(size)] for _ in range(size)]
            for i in range(size):
                for j in range(size):
                    rotated[j][size - 1 - i] = matrix[i][j]
            matrix = rotated
        
        while all(cell == 0 for cell in matrix[0]):
            matrix = matrix[1:]
            matrix.append([0 for _ in range(size)])
        
        while all(row[-1] == 0 for row in matrix):
            for row in matrix:
                row.pop()
            for row in matrix:
                row.insert(0, 0)
        
        return matrix

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)

screen_width = 900
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Tetris - 25 Shapes")

done = False
clock = pygame.time.Clock()
fps = 60
game = Tetris()
game.new_shape()

counter = 0
last_move_time = 0
move_delay = 100

font = pygame.font.SysFont('arial', 28, True, False)
font_big = pygame.font.SysFont('arial', 65, True, False)
game_over_text = font_big.render("GAME OVER", True, (255, 50, 50))
game_over_rect = game_over_text.get_rect(center=(screen_width//2, screen_height//2 - 50))

def draw_grid():
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, DARK_GRAY, 
                           [game.x + game.zoom * j, 
                            game.y + game.zoom * i, 
                            game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                               [game.x + game.zoom * j + 1, 
                                game.y + game.zoom * i + 1, 
                                game.zoom - 2, game.zoom - 2])

def draw_current_shape():
    if game.shape:
        shape_matrix = game.shape.get_matrix()
        for i in range(len(shape_matrix)):
            row = shape_matrix[i]
            for j in range(len(row)):
                if row[j]:
                    pygame.draw.rect(screen, colors[game.shape.color],
                                   [game.x + game.zoom * (j + game.shape.x) + 1,
                                    game.y + game.zoom * (i + game.shape.y) + 1,
                                    game.zoom - 2, game.zoom - 2])

def draw_next_shape():
    if game.next_shape:
        next_x = game.x + game.zoom * game.width + 60
        next_y = game.y + 120
        
        pygame.draw.rect(screen, DARK_GRAY, 
                        [next_x - 15, next_y - 15, 
                         game.zoom * 6 + 30, game.zoom * 6 + 30], 0)
        
        next_text = font.render("Next Shape:", True, WHITE)
        screen.blit(next_text, [next_x - 10, next_y - 50])
        
        shape_matrix = game.next_shape.get_matrix()
        shape_color = game.next_shape.color
        
        offset_x = (6 - len(shape_matrix[0])) * game.zoom // 2
        offset_y = (6 - len(shape_matrix)) * game.zoom // 2
        
        for i in range(len(shape_matrix)):
            row = shape_matrix[i]
            for j in range(len(row)):
                if row[j]:
                    pygame.draw.rect(screen, colors[shape_color],
                                   [next_x + offset_x + game.zoom * j,
                                    next_y + offset_y + game.zoom * i,
                                    game.zoom - 2, game.zoom - 2])

def draw_game_area():
    pygame.draw.rect(screen, GRAY, 
                    [game.x - 15, game.y - 15, 
                     game.zoom * game.width + 30, 
                     game.zoom * game.height + 30], 0)
    draw_grid()
    draw_current_shape()

pressing_down = False
pressing_left = False
pressing_right = False

while not done:
    current_time = pygame.time.get_ticks()
    
    counter += 1
    if counter > 100000:
        counter = 0
    
    if counter % (fps // (game.level * 2)) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                pressing_left = True
            if event.key == pygame.K_RIGHT:
                pressing_right = True
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game = Tetris()
                game.new_shape()
            if event.key == pygame.K_r:
                game = Tetris()
                game.new_shape()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
            if event.key == pygame.K_LEFT:
                pressing_left = False
            if event.key == pygame.K_RIGHT:
                pressing_right = False
    
    if pressing_left and current_time - last_move_time > move_delay:
        game.go_side(-1)
        last_move_time = current_time
    
    if pressing_right and current_time - last_move_time > move_delay:
        game.go_side(1)
        last_move_time = current_time
    
    screen.fill((15, 15, 35))
    
    draw_game_area()
    draw_next_shape()
    
    score_text = font.render(f"Score: {game.score}", True, WHITE)
    level_text = font.render(f"Level: {game.level}", True, WHITE)
    shapes_text = font.render(f"Shapes: {len(shapes)}", True, WHITE)
    
    screen.blit(score_text, [50, 40])
    screen.blit(level_text, [50, 80])
    screen.blit(shapes_text, [50, 120])
    
    controls = [
        "CONTROLS:",
        "UP: Rotate",
        "LEFT/RIGHT: Move",
        "DOWN: Fast Drop",
        "SPACE: Instant Drop",
        "R: Restart",
        "ESC: New Game"
    ]
    
    for i, text in enumerate(controls):
        control_text = font.render(text, True, WHITE)
        screen.blit(control_text, [game.x + game.zoom * game.width + 60, 220 + i * 40])
    
    if game.state == "gameover":
        screen.blit(game_over_text, game_over_rect)
        restart_text = font.render("Press R to restart", True, WHITE)
        screen.blit(restart_text, [screen_width//2 - 120, screen_height//2 + 30])
    
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()