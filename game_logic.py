import pygame
import random
import math
from reinforcement_learning import QLearning

class GameLogic:
    def __init__(self):
        # Game Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.FPS = 60
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (150, 150, 150)

        # Game States
        self.STATE_MENU = 0
        self.STATE_PLAYER_SETUP = 1
        self.STATE_PLAYER_SHOOTING = 2
        self.STATE_AI_SHOOTING = 3
        self.STATE_GAME_OVER = 4

        # Game Variables
        self.game_state = self.STATE_MENU
        self.player_pos = [self.WIDTH // 2, self.HEIGHT - 100]
        self.player_score = 0
        self.ai_score = 0
        self.game_over_message = ""

        # Grid setup for placing enemies and bombs
        self.GRID_COLS = 5
        self.GRID_ROWS = 3
        self.GRID_CELL_WIDTH = self.WIDTH // self.GRID_COLS
        self.GRID_CELL_HEIGHT = 100
        self.GRID_TOP_MARGIN = 100

        # Game objects
        self.enemies = []
        self.bombs = []
        self.shots = []
        self.explosions = []

        # Player setup variables
        self.setup_objects = []
        self.setup_selected_type = 0
        self.remaining_enemies = 10
        self.remaining_bombs = 5

        # AI variables
        self.ai_turn_timer = 0
        self.ai_shots = []
        self.ai_turn_delay = 500

        # Initialize Q-learning
        self.q_learning = QLearning()

        # Initialize Pygame
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Stickman Shootout with Adaptive AI")
        self.load_images()

    def load_images(self):
        # Load images for the game
        self.stickman_img = pygame.Surface((60, 100), pygame.SRCALPHA)
        pygame.draw.circle(self.stickman_img, self.BLUE, (30, 15), 15)
        pygame.draw.line(self.stickman_img, self.BLUE, (30, 30), (30, 70), 4)
        pygame.draw.line(self.stickman_img, self.BLUE, (30, 40), (10, 70), 4)
        pygame.draw.line(self.stickman_img, self.BLUE, (30, 40), (50, 70), 4)
        pygame.draw.line(self.stickman_img, self.BLUE, (30, 70), (10, 90), 4)
        pygame.draw.line(self.stickman_img, self.BLUE, (30, 70), (50, 90), 4)

        self.enemy_img = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.enemy_img, self.RED, (15, 15), 15)

        self.bomb_img = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.bomb_img, self.BLACK, (15, 15), 15)
        pygame.draw.circle(self.bomb_img, self.WHITE, (10, 10), 5)
        pygame.draw.rect(self.bomb_img, self.BLACK, (13, 0, 4, 5))

        self.explosion_img = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(self.explosion_img, self.RED, (30, 30), 30)
        pygame.draw.circle(self.explosion_img, (255, 165, 0), (30, 30), 20)
        pygame.draw.circle(self.explosion_img, (255, 255, 0), (30, 30), 10)

    def handle_events(self, event):
        if self.game_state == self.STATE_MENU:
            self.handle_menu_events(event)
        elif self.game_state == self.STATE_PLAYER_SETUP:
            self.handle_setup_events(event)
        elif self.game_state in [self.STATE_PLAYER_SHOOTING, self.STATE_AI_SHOOTING]:
            self.handle_game_events(event)
        elif self.game_state == self.STATE_GAME_OVER:
            self.handle_game_over_events(event)

    def handle_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.game_state = self.STATE_PLAYER_SETUP
            self.init_setup()

    def init_setup(self):
        self.setup_objects = []
        self.setup_selected_type = 0
        self.remaining_enemies = 10
        self.remaining_bombs = 5

    def handle_setup_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            enemy_button = pygame.Rect(self.WIDTH - 200, 60, 80, 30)
            bomb_button = pygame.Rect(self.WIDTH - 100, 60, 80, 30)

            if enemy_button.collidepoint(mouse_pos):
                self.setup_selected_type = 0
                return
            elif bomb_button.collidepoint(mouse_pos):
                self.setup_selected_type = 1
                return

            if self.remaining_enemies == 0 and self.remaining_bombs == 0:
                self.start_game()
                return

            if (0 <= mouse_pos[0] < self.WIDTH and 
                self.GRID_TOP_MARGIN <= mouse_pos[1] < self.GRID_TOP_MARGIN + self.GRID_ROWS * self.GRID_CELL_HEIGHT):
                
                for obj in self.setup_objects:
                    obj_x, obj_y, _ = obj
                    distance = math.sqrt((obj_x - mouse_pos[0])**2 + (obj_y - mouse_pos[1])**2)
                    if distance < 20:
                        return
                
                if self.setup_selected_type == 0 and self.remaining_enemies > 0:
                    self.setup_objects.append([mouse_pos[0], mouse_pos[1], 0])
                    self.remaining_enemies -= 1
                elif self.setup_selected_type == 1 and self.remaining_bombs > 0:
                    self.setup_objects.append([mouse_pos[0], mouse_pos[1], 1])
                    self.remaining_bombs -= 1

    def start_game(self):
        self.enemies = []
        self.bombs = []
        
        for obj in self.setup_objects:
            x, y, obj_type = obj
            if obj_type == 0:
                self.enemies.append([x, y, False])
            else:
                self.bombs.append([x, y, False])
        
        self.game_state = self.STATE_PLAYER_SHOOTING

    def handle_game_events(self, event):
        if self.game_state == self.STATE_PLAYER_SHOOTING:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                dx = mouse_pos[0] - self.player_pos[0]
                dy = mouse_pos[1] - self.player_pos[1]
                length = math.sqrt(dx * dx + dy * dy)
                if length > 0:
                    dx /= length
                    dy /= length
                shot_speed = 10
                self.shots.append([self.player_pos[0], self.player_pos[1], dx * shot_speed, dy * shot_speed])

    def update(self):
        if self.game_state == self.STATE_AI_SHOOTING:
            self.handle_ai_turn()
        
        if self.game_state in [self.STATE_PLAYER_SHOOTING, self.STATE_AI_SHOOTING]:
            self.update_shots()

    def update_shots(self):
        # Update player shots
        i = 0
        while i < len(self.shots):
            shot = self.shots[i]
            shot[0] += shot[2]
            shot[1] += shot[3]
            
            if shot[0] < 0 or shot[0] > self.WIDTH or shot[1] < 0 or shot[1] > self.HEIGHT:
                self.shots.pop(i)
                continue
            
            hit = False
            for j, enemy in enumerate(self.enemies):
                enemy_x, enemy_y, visible = enemy
                distance = math.sqrt((enemy_x - shot[0])**2 + (enemy_y - shot[1])**2)
                if distance < 15:
                    self.enemies[j][2] = True
                    self.explosions.append([enemy_x, enemy_y, 20])
                    self.shots.pop(i)
                    hit = True
                    self.player_score += 1
                    
                    if all(enemy[2] for enemy in self.enemies):
                        self.game_state = self.STATE_GAME_OVER
                        self.game_over_message = "Player Wins!"
                    else:
                        self.game_state = self.STATE_AI_SHOOTING
                        self.ai_turn_timer = pygame.time.get_ticks()
                    break
            
            if not hit:
                for j, bomb in enumerate(self.bombs):
                    bomb_x, bomb_y, visible = bomb
                    distance = math.sqrt((bomb_x - shot[0])**2 + (bomb_y - shot[1])**2)
                    if distance < 15:
                        self.bombs[j][2] = True
                        self.explosions.append([bomb_x, bomb_y, 20])
                        self.shots.pop(i)
                        self.game_state = self.STATE_GAME_OVER
                        self.game_over_message = "You hit a bomb! AI Wins!"
                        self.q_learning.record_state_action(self.get_game_state(), (bomb_x, bomb_y), -1)
                        hit = True
                        break
            
            if not hit:
                i += 1

    def handle_ai_turn(self):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.ai_turn_timer > self.ai_turn_delay:
            self.take_ai_shot()
            self.ai_turn_timer = current_time

    def take_ai_shot(self):
        state = self.get_game_state()
        target_x, target_y = self.q_learning.choose_action(state)
        
        ai_pos = [self.WIDTH // 2, self.HEIGHT - 100]
        dx = target_x - ai_pos[0]
        dy = target_y - ai_pos[1]
        
        length = math.sqrt(dx * dx + dy * dy)
        if length > 0:
            dx /= length
            dy /= length
        
        shot_speed = 10
        self.ai_shots.append([ai_pos[0], ai_pos[1], dx * shot_speed, dy * shot_speed])
        
        reward = 1 if target_x in [e[0] for e in self.enemies if e[2]] else -1
        self.q_learning.record_state_action(state, (target_x, target_y), reward)

    def get_game_state(self):
        state = []
        for enemy in self.enemies:
            x, y, visible = enemy
            if visible:
                col = int(x // self.GRID_CELL_WIDTH)
                row = int((y - self.GRID_TOP_MARGIN) // self.GRID_CELL_HEIGHT)
                state.append(('enemy', col, row))
        
        for bomb in self.bombs:
            x, y, visible = bomb
            if visible:
                col = int(x // self.GRID_CELL_WIDTH)
                row = int((y - self.GRID_TOP_MARGIN) // self.GRID_CELL_HEIGHT)
                state.append(('bomb', col, row))
        
        return tuple(sorted(state))

    def handle_game_over_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.game_state = self.STATE_MENU
            self.player_score = 0
            self.ai_score = 0

    def save_q_table(self):
        self.q_learning.save_q_table()
