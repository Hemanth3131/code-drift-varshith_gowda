# snake.py
import pygame

class Snake:
    def __init__(self, block_size, screen_width, screen_height):
        self.block_size = block_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.direction = "RIGHT"
        self.body = [(screen_width // 2, screen_height // 2)]
        self.color = (0, 255, 0)
        self.change_to = self.direction
        self.grow_pending = False
        self.speed = 1

    def set_direction(self, direction):
        """Avoid reversing direction"""
        opposites = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }
        if direction != opposites.get(self.direction):
            self.change_to = direction

    def move(self):
        """Move the snake based on direction"""
        self.direction = self.change_to
        head_x, head_y = self.body[0]

        if self.direction == "UP":
            head_y -= self.block_size
        elif self.direction == "DOWN":
            head_y += self.block_size
        elif self.direction == "LEFT":
            head_x -= self.block_size
        elif self.direction == "RIGHT":
            head_x += self.block_size

        new_head = (head_x, head_y)
        self.body.insert(0, new_head)

        if self.grow_pending:
            self.grow_pending = False
        else:
            self.body.pop()

    def grow(self):
        self.grow_pending = True

    def draw(self, screen):
        for i, segment in enumerate(self.body):
            color = (0, 200, 0) if i == 0 else self.color
            pygame.draw.rect(screen, color, pygame.Rect(segment[0], segment[1], self.block_size, self.block_size))

    def reset(self):
        self.body = [(self.screen_width // 2, self.screen_height // 2)]
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.grow_pending = False

    def get_head_position(self):
        return self.body[0]

        def get_body(self):
        return self.body

    def length(self):
        return len(self.body)

    def increase_speed(self, factor=0.2):
        self.speed += factor

    def get_speed(self):
        return self.speed

    def hit_wall(self):
        head_x, head_y = self.body[0]
        return (
            head_x < 0 or head_x >= self.screen_width or
            head_y < 0 or head_y >= self.screen_height
        )

    def hit_self(self):
        return self.body[0] in self.body[1:]
# scoreboard.py
import pygame
import os

class Scoreboard:
    def __init__(self, font_name="arial", font_size=28, file_path="highscore.txt"):
        self.score = 0
        self.level = 1
        self.high_score = 0
        self.score_per_food = 10
        self.file_path = file_path
        self.font = pygame.font.SysFont(font_name, font_size)
        self.load_high_score()

    def load_high_score(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    self.high_score = int(file.read().strip())
                except ValueError:
                    self.high_score = 0
        else:
            self.high_score = 0

    def save_high_score(self):
        with open(self.file_path, "w") as file:
            file.write(str(self.high_score))

    def increase_score(self, food_type="normal"):
        if food_type == "normal":
            self.score += self.score_per_food
        elif food_type == "special":
            self.score += self.score_per_food * 2

        self.update_level()

        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def update_level(self):
        """Optional: Increase level every 50 points"""
        self.level = self.score // 50 + 1

    def draw(self, screen, x=10, y=10):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 0))
        level_text = self.font.render(f"Level: {self.level}", True, (0, 255, 255))

        screen.blit(score_text, (x, y))
        screen.blit(high_score_text, (x, y + 30))
        screen.blit(level_text, (x, y + 60))

    def reset(self):
        self.score = 0
        self.level = 1

    def get_score(self):
        return self.score

    def get_high_score(self):
        return self.high_score

    def get_level(self):
        return self.level

    def increase_score_by_value(self, amount):
        self.score += amount
        self.update_level()
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

# Example usage
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    clock = pygame.time.Clock()
    scoreboard = Scoreboard()

    running = True
    while running:
        screen.fill((0, 0, 0))
        scoreboard.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
