import pygame
import time
import random
import json
import math
from enum import Enum
from datetime import datetime

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20
PLAYER_SPEED = 0.05  # Reduced for better control
ROTATION_SPEED = 0.03  # Reduced for smoother rotation
EPSILON = 1e-10
TEXTURE_SIZE = 64
FOV = math.pi / 3 # 60 - degree field of view

# Game settings for different difficulties
DIFFICULTY_SETTINGS = {
    'Easy': {
        'maze_size': 11,
        'initial_view_time': 8,
        'top_view_allowed': 2,
        'score_multiplier': 1
    },
    'Medium': {
        'maze_size': 15,
        'initial_view_time': 6,
        'top_view_allowed': 2,
        'score_multiplier': 2
    },
    'Hard': {
        'maze_size': 21,
        'initial_view_time': 4,
        'top_view_allowed': 2,
        'score_multiplier': 3
    }
}

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    INSTRUCTIONS = 4

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("MemoMaze")
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.assets = self.load_assets()
        self.init_textures()
        self.difficulty = None
        self.top_view_counts = 0
        self.show_minimap = False
        self.score = 0
        self.start_time = None
        self.load_high_scores()

    def load_assets(self):
        """Load and prepare game assets"""
        assets = {}
        try:
            assets['font'] = pygame.font.Font('mario_font.ttf', 60)
            assets['medium_font'] = pygame.font.Font('mario_font.ttf', 45)
            assets['small_font'] = pygame.font.Font('mario_font.ttf', 20)

            # Load sky texture
            try:
                sky = pygame.image.load('sky.jpg')
                assets['sky'] = pygame.transform.scale(sky, (SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            except:
                assets['sky'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT // 2))
                assets['sky'].fill((135, 206, 235))

            # Load background
            try:
                bg = pygame.image.load('maze_bg.png')
                assets['background'] = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except:
                assets['background'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                assets['background'].fill((135, 206, 235))

            # Load exit texture
            # In load_assets method, after loading exit texture:
            try:
                exit_tex = pygame.image.load('maze_exit.jpeg')
                assets['exit_wall'] = pygame.transform.scale(exit_tex, (TEXTURE_SIZE, TEXTURE_SIZE))
            except Exception as e:
                assets['exit_wall'] = pygame.Surface((TEXTURE_SIZE, TEXTURE_SIZE))
                assets['exit_wall'].fill((0, 0, 0))

        except:
            assets['font'] = pygame.font.Font(None, 74)
            assets['medium_font'] = pygame.font.Font(None, 55)
            assets['small_font'] = pygame.font.Font(None, 36)
            assets['background'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            assets['background'].fill((135, 206, 235))
            assets['sky'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            assets['sky'].fill((135, 206, 235))
            assets['exit_wall'] = pygame.Surface((TEXTURE_SIZE, TEXTURE_SIZE))
            assets['exit_wall'].fill((255, 0, 0))

        # Create wall texture
        wall_surface = pygame.Surface((TEXTURE_SIZE, TEXTURE_SIZE))
        wall_surface.fill((139, 69, 19))
        pygame.draw.rect(wall_surface, (101, 67, 33), (0, 0, TEXTURE_SIZE, TEXTURE_SIZE // 8))

        assets['wall'] = wall_surface
        assets['ground'] = pygame.Surface((TEXTURE_SIZE, TEXTURE_SIZE))
        assets['ground'].fill((173, 208, 179))

        return assets

    def init_textures(self):
        """Initialize and prepare textures for rendering"""
        self.wall_texture = self.assets['wall']
        self.ground_pattern = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        ground_tex = self.assets['ground']

        # Create repeating ground pattern
        for y in range(0, SCREEN_HEIGHT // 2, TEXTURE_SIZE):
            for x in range(0, SCREEN_WIDTH, TEXTURE_SIZE):
                self.ground_pattern.blit(ground_tex, (x, y))

    def draw_menu(self):
        """Draw main menu"""
        # Draw background
        self.screen.blit(self.assets['background'], (0, 0))

        # Draw title
        self.draw_text("MemoMaze", 'large', SCREEN_WIDTH // 2, 100, (0, 0, 0))

        # Draw difficulty options
        y_pos = 250
        for diff in ['1. Easy', '2. Medium', '3. Hard']:
            self.draw_text(f"{diff}", 'medium', SCREEN_WIDTH // 2, y_pos, (0, 0, 0))
            y_pos += 70

        # Draw instructions option
        self.draw_text("Press 'I' for Instructions", 'small', SCREEN_WIDTH // 2, y_pos + 30, (0, 0, 0))

        pygame.display.flip()

    def draw_instructions(self):
        """Draw instructions screen"""
        # Draw background
        self.screen.blit(self.assets['background'], (0, 0))

        instructions = [
            "MemoMaze - Instructions",
            "",
            "Find your way out of the maze!",
            "Use arrow keys to move and turn.",
            f"Press M to view map 2 times.",
            "After using both map views,",
            "press M once more for permanent minimap.",
            "",
            "Press SPACE to return to menu."
        ]

        y_pos = 100
        for line in instructions:
            self.draw_text(line, 'small', SCREEN_WIDTH // 2, y_pos, (0, 0, 0))
            y_pos += 50

        pygame.display.flip()

    def handle_menu_input(self):
        """Handle menu input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_e:
                    self.difficulty = 'Easy'
                    self.start_game()
                elif event.key == pygame.K_2 or event.key == pygame.K_m:
                    self.difficulty = 'Medium'
                    self.start_game()
                elif event.key == pygame.K_3 or event.key == pygame.K_h:
                    self.difficulty = 'Hard'
                    self.start_game()
                elif event.key == pygame.K_i:
                    self.state = GameState.INSTRUCTIONS
                elif event.key == pygame.K_SPACE and self.state == GameState.INSTRUCTIONS:
                    self.state = GameState.MENU
        return True

    def start_game(self):
        """Initialize and start the game"""
        self.state = GameState.PLAYING
        self.top_view_counts = 0
        self.show_minimap = False
        self.start_time = time.time()

        settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.maze = self.generate_maze(settings['maze_size'], settings['maze_size'])
        # Initial view with starting position and angle
        self.display_top_view(self.maze, settings['initial_view_time'], [1.5, 1.5], 0)

    def display_game_over(self, elapsed_time):
        """Display game over screen with simplified score display"""
        # Draw background
        self.screen.blit(self.assets['background'], (0, 0))

        # Draw completion message
        self.draw_text("Game Complete!", 'medium', SCREEN_WIDTH // 2, 80, (0, 0, 0))

        # Display stats without calculations
        y_pos = 160
        stats = [
            f"Time: {elapsed_time:.2f} seconds",
            f"Map Views: {self.top_view_counts}",
            f"Minimap Used: {'Yes' if self.show_minimap else 'No'}"
        ]

        for stat in stats:
            self.draw_text(stat, 'small', SCREEN_WIDTH // 2, y_pos, (0, 0, 0))
            y_pos += 50

        # Draw final scores
        y_pos += 20
        final_score = self.calculate_score()
        high_score = self.high_scores.get(self.difficulty, 0)

        self.draw_text(f"Final Score: {final_score}", 'small', SCREEN_WIDTH // 2, y_pos, (0, 0, 0))
        y_pos += 50
        self.draw_text(f"High Score: {high_score}", 'small', SCREEN_WIDTH // 2, y_pos, (0, 0, 0))

        # Draw return instruction
        self.draw_text("Press SPACE to return to menu", 'small', SCREEN_WIDTH // 2, y_pos + 70, (0, 0, 0))

        # Current timestamp
        timestamp = f"Completed on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
        timestamp_surface = pygame.font.Font(None, 24).render(timestamp, True, (100, 100, 100))
        timestamp_rect = timestamp_surface.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
        self.screen.blit(timestamp_surface, timestamp_rect)

        pygame.display.flip()

    def generate_maze(self, width, height):
        """Generate a random maze using depth-first search"""
        maze = [[1] * width for _ in range(height)]

        def carve(x, y):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                    maze[ny][nx] = 0
                    maze[y + dy][x + dx] = 0
                    carve(nx, ny)

        # Start from the center
        start_x, start_y = 1, 1
        maze[start_y][start_x] = 0
        carve(start_x, start_y)

        # Create exit
        maze[height - 2][width - 2] = 0
        return maze

    def display_top_view(self, maze, view_time, player_pos=None, player_angle=None):
        """Display top-down view of the maze"""
        width, height = len(maze[0]), len(maze)
        cell_size = min(SCREEN_WIDTH // width, SCREEN_HEIGHT // height)
        start_time = time.time()

        surface = pygame.Surface((width * cell_size, height * cell_size))
        while time.time() - start_time < view_time:
            surface.fill((0, 0, 0))

            # Draw maze
            for y, row in enumerate(maze):
                for x, cell in enumerate(row):
                    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                    if cell == 0:
                        if (x, y) == (width - 2, height - 2):
                            pygame.draw.rect(surface, (255, 0, 0), rect)  # Red exit
                        else:
                            pygame.draw.rect(surface, (255, 255, 255), rect)  # White path
                    else:
                        pygame.draw.rect(surface, (139, 69, 19), rect)  # Brown walls

            # Center the maze on screen
            self.screen.fill((0, 0, 0))
            maze_rect = surface.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(surface, maze_rect)

            # Draw player position if available
            if player_pos is not None:
                player_screen_x = maze_rect.left + player_pos[0] * cell_size
                player_screen_y = maze_rect.top + player_pos[1] * cell_size
                pygame.draw.circle(self.screen, (0, 255, 0),
                                   (int(player_screen_x), int(player_screen_y)),
                                   cell_size // 3)

                # Draw player direction if angle is available
                if player_angle is not None:
                    direction_end = (
                        int(player_screen_x + math.cos(player_angle) * cell_size),
                        int(player_screen_y + math.sin(player_angle) * cell_size)
                    )
                    pygame.draw.line(self.screen, (0, 255, 0),
                                     (int(player_screen_x), int(player_screen_y)),
                                     direction_end, 2)

            # Draw countdown
            remaining = int(view_time - (time.time() - start_time)) + 1
            countdown_text = str(remaining)
            text_surface = self.assets['font'].render(countdown_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

    def render_frame(self, player_pos, player_angle, maze):
        """Render a single frame of the 3D view"""
        self.screen.fill((0, 0, 0))

        # Draw sky texture
        self.screen.blit(self.assets['sky'], (0, 0))

        # Draw floor with new color #985f2a
        pygame.draw.rect(self.screen, (173, 208, 179),
                         (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))

        # Ray casting
        for x in range(SCREEN_WIDTH):
            ray_angle = (player_angle - FOV / 2) + (x / SCREEN_WIDTH) * FOV
            self.cast_ray(x, ray_angle, player_pos, maze)

    def cast_ray(self, x, ray_angle, player_pos, maze):
        """Cast a single ray and render the corresponding wall strip"""
        ray_dir = (math.cos(ray_angle), math.sin(ray_angle))
        map_pos = [int(player_pos[0]), int(player_pos[1])]

        delta_dist = [
            abs(1 / (ray_dir[0] + EPSILON)),
            abs(1 / (ray_dir[1] + EPSILON))
        ]

        step = [-1 if ray_dir[0] < 0 else 1, -1 if ray_dir[1] < 0 else 1]
        side_dist = [
            (player_pos[0] - map_pos[0]) * delta_dist[0] if ray_dir[0] < 0
            else (map_pos[0] + 1.0 - player_pos[0]) * delta_dist[0],
            (player_pos[1] - map_pos[1]) * delta_dist[1] if ray_dir[1] < 0
            else (map_pos[1] + 1.0 - player_pos[1]) * delta_dist[1]
        ]

        hit = False
        side = 0
        while not hit:
            if side_dist[0] < side_dist[1]:
                side_dist[0] += delta_dist[0]
                map_pos[0] += step[0]
                side = 0
            else:
                side_dist[1] += delta_dist[1]
                map_pos[1] += step[1]
                side = 1

            # Check if we hit a wall
            if map_pos[1] < 0 or map_pos[1] >= len(maze) or \
                    map_pos[0] < 0 or map_pos[0] >= len(maze[0]):
                hit = True
            elif maze[map_pos[1]][map_pos[0]] == 1:
                hit = True

        # Calculate wall distance
        if side == 0:
            wall_dist = side_dist[0] - delta_dist[0]
        else:
            wall_dist = side_dist[1] - delta_dist[1]

        # Calculate wall height
        line_height = int(SCREEN_HEIGHT / (wall_dist + EPSILON))

        # Calculate drawing boundaries
        draw_start = max(0, -line_height // 2 + SCREEN_HEIGHT // 2)
        draw_end = min(SCREEN_HEIGHT - 1, line_height // 2 + SCREEN_HEIGHT // 2)

        # Check if this is the exit wall
        exit_x, exit_y = len(maze[0]) - 2, len(maze) - 2
        is_exit = False

        # We only want to show the exit texture on the wall that leads to the exit
        # Check if we hit a wall and if it's adjacent to the exit cell
        if hit and maze[map_pos[1]][map_pos[0]] == 1:  # We hit a wall
            # Check if this wall is directly adjacent to the exit cell
            # and if it's the wall we need to pass through to reach the exit
            if ((map_pos[0] == exit_x + 1 and map_pos[1] == exit_y) or  # Right wall
                    (map_pos[0] == exit_x - 1 and map_pos[1] == exit_y) or  # Left wall
                    (map_pos[0] == exit_x and map_pos[1] == exit_y + 1) or  # Bottom wall
                    (map_pos[0] == exit_x and map_pos[1] == exit_y - 1)):  # Top wall

                # Additional check to ensure it's the wall facing the exit
                if ((map_pos[0] == exit_x + 1 and side == 0) or  # Right wall
                        (map_pos[0] == exit_x - 1 and side == 0) or  # Left wall
                        (map_pos[0] == exit_x and map_pos[1] == exit_y + 1 and side == 1) or  # Bottom wall
                        (map_pos[0] == exit_x and map_pos[1] == exit_y - 1 and side == 1)):  # Top wall
                    is_exit = True

        if is_exit:
            # Use exit wall texture
            texture = self.assets['exit_wall']

            # Calculate texture coordinates
            if side == 0:
                wall_x = player_pos[1] + wall_dist * ray_dir[1]
            else:
                wall_x = player_pos[0] + wall_dist * ray_dir[0]
            wall_x -= math.floor(wall_x)

            tex_x = int(wall_x * TEXTURE_SIZE)
            if (side == 0 and ray_dir[0] > 0) or (side == 1 and ray_dir[1] < 0):
                tex_x = TEXTURE_SIZE - tex_x - 1

            # Draw textured strip
            h = draw_end - draw_start
            if h > 0:  # Prevent division by zero
                step = TEXTURE_SIZE / h
                tex_pos = 0

                for y in range(draw_start, draw_end):
                    tex_y = int(tex_pos) & (TEXTURE_SIZE - 1)
                    tex_pos += step
                    try:
                        color = texture.get_at((tex_x, tex_y))
                        if side == 1:  # Darken one side
                            color = (int(color[0] * 0.7), int(color[1] * 0.7), int(color[2] * 0.7))
                        self.screen.set_at((x, y), color)
                    except IndexError:
                        # Fallback if texture sampling fails
                        color = (255, 0, 0)  # Bright red for debugging
                        pygame.draw.line(self.screen, color, (x, draw_start), (x, draw_end), 1)
        else:
            # Draw regular wall
            color = (139, 69, 19)  # Brown color for walls
            if side == 1:  # Darker for one side to create depth
                color = (color[0] * 0.7, color[1] * 0.7, color[2] * 0.7)
            pygame.draw.line(self.screen, color, (x, draw_start), (x, draw_end), 1)

    def draw_minimap(self, maze, player_pos, player_angle):
        """Draw minimap in the corner"""
        minimap_size = 100
        cell_size = minimap_size // len(maze)

        minimap = pygame.Surface((minimap_size, minimap_size))
        minimap.set_alpha(128)
        minimap.fill((0, 0, 0))

        # Draw maze walls
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 1:
                    pygame.draw.rect(minimap, (255, 255, 255),
                                     (x * cell_size, y * cell_size,
                                      cell_size, cell_size))
                # Draw exit
                elif x == len(maze[0]) - 2 and y == len(maze) - 2:
                    pygame.draw.rect(minimap, (255, 0, 0),
                                     (x * cell_size, y * cell_size,
                                      cell_size, cell_size))

        # Draw player
        player_x = int(player_pos[0] * cell_size)
        player_y = int(player_pos[1] * cell_size)
        pygame.draw.circle(minimap, (0, 255, 0), (player_x, player_y), 2)

        # Draw player direction
        end_pos = (int(player_x + math.cos(player_angle) * 8),
                   int(player_y + math.sin(player_angle) * 8))
        pygame.draw.line(minimap, (0, 255, 0),
                         (player_x, player_y), end_pos, 1)

        self.screen.blit(minimap, (10, 10))

    def display_first_person_view(self, maze):
        """Display first-person view of the maze"""
        player_pos = [1.5, 1.5]
        player_angle = 0
        keys = {'left': False, 'right': False, 'up': False, 'down': False}
        map_press_count = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.MENU
                        self.show_minimap = False
                        self.top_view_counts = 0
                        return 0
                    elif event.key == pygame.K_LEFT:
                        keys['left'] = True
                    elif event.key == pygame.K_RIGHT:
                        keys['right'] = True
                    elif event.key == pygame.K_UP:
                        keys['up'] = True
                    elif event.key == pygame.K_DOWN:
                        keys['down'] = True
                    elif event.key == pygame.K_m:
                        map_press_count += 1
                        if self.top_view_counts < DIFFICULTY_SETTINGS[self.difficulty]['top_view_allowed']:
                            self.display_top_view(maze, 2, player_pos, player_angle)
                            self.top_view_counts += 1
                        if map_press_count > DIFFICULTY_SETTINGS[self.difficulty]['top_view_allowed']:
                            # Enable minimap on the third press (after using both map views)
                            self.show_minimap = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        keys['left'] = False
                    elif event.key == pygame.K_RIGHT:
                        keys['right'] = False
                    elif event.key == pygame.K_UP:
                        keys['up'] = False
                    elif event.key == pygame.K_DOWN:
                        keys['down'] = False

            # Update player position and angle
            if keys['left']: player_angle -= ROTATION_SPEED
            if keys['right']: player_angle += ROTATION_SPEED

            new_pos = list(player_pos)
            if keys['up']:
                new_pos[0] += math.cos(player_angle) * PLAYER_SPEED
                new_pos[1] += math.sin(player_angle) * PLAYER_SPEED
            if keys['down']:
                new_pos[0] -= math.cos(player_angle) * PLAYER_SPEED
                new_pos[1] -= math.sin(player_angle) * PLAYER_SPEED

            # Collision detection
            if (len(maze) > int(new_pos[1]) >= 0 == maze[int(new_pos[1])][int(new_pos[0])] and
                    0 <= int(new_pos[0]) < len(maze[0])):
                player_pos = new_pos

            # Render frame
            self.render_frame(player_pos, player_angle, maze)

            # Draw minimap if enabled
            if self.show_minimap:
                self.draw_minimap(maze, player_pos, player_angle)

            pygame.display.flip()
            self.clock.tick(60)

            # Check if player reached the exit
            if (int(player_pos[0]) == len(maze[0]) - 2 and
                    int(player_pos[1]) == len(maze) - 2):
                elapsed_time = time.time() - self.start_time
                self.save_high_score()
                return elapsed_time

    def load_high_scores(self):
        """Load high scores from file"""
        try:
            with open('high_scores.json', 'r') as f:
                self.high_scores = json.load(f)
        except:
            self.high_scores = {'Easy': float('inf'), 'Medium': float('inf'), 'Hard': float('inf')}

    def save_high_score(self):
        """Save high score if it's better than previous"""
        score = self.calculate_score()
        if score < self.high_scores.get(self.difficulty, float('inf')):
            self.high_scores[self.difficulty] = score
            with open('high_scores.json', 'w') as f:
                json.dump(self.high_scores, f)

    def calculate_score(self):
        """
        Calculate score based on:
        - Base score: 1000 points (reduced from 10000)
        - Time penalty: Points decrease as time increases
        - Map view penalty: Each map view reduces score
        - Minimap penalty: Using permanent minimap reduces score
        - Difficulty multiplier: Higher difficulties give better scores
        """
        # Base score
        base_score = 1000

        # Time penalty
        elapsed_time = time.time() - self.start_time
        time_penalty = elapsed_time * 2  # Lose 2 points per second

        # Map view penalty
        map_penalty = self.top_view_counts * 100  # Lose 100 points per map view

        # Minimap penalty
        minimap_penalty = 200 if self.show_minimap else 0  # Flat penalty for using permanent minimap

        # Calculate raw score
        raw_score = base_score - time_penalty - map_penalty - minimap_penalty

        # Apply difficulty multiplier
        difficulty_multiplier = DIFFICULTY_SETTINGS[self.difficulty]['score_multiplier']
        final_score = max(0, raw_score) * difficulty_multiplier

        return round(final_score, 2)

    def draw_text(self, text, size, x, y, color=(255, 255, 255)):
        """Draw text on screen"""
        if size == 'large':
            font = self.assets['font']
        elif size == 'medium':
            font = self.assets['medium_font']
        else:  # small
            font = self.assets['small_font']

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

def main():
    game = Game()
    running = True

    while running:
        if game.state == GameState.MENU:
            game.draw_menu()
            running = game.handle_menu_input()
        elif game.state == GameState.INSTRUCTIONS:
            game.draw_instructions()
            running = game.handle_menu_input()
        elif game.state == GameState.PLAYING:
            elapsed_time = game.display_first_person_view(game.maze)
            if elapsed_time is None:
                running = False
            else:
                game.display_game_over(elapsed_time)
                game.state = GameState.GAME_OVER
        elif game.state == GameState.GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game.state = GameState.MENU

    pygame.quit()


if __name__ == "__main__":
    main()


