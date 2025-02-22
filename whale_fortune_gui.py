import pygame
import math
import random
import time
import sys

class WhaleFortuneGUI:
    def __init__(self):
        pygame.init()
        # Make window smaller (from 1024x768 to 800x600)
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Whale Wheel")
        
        # Make fonts even smaller
        self.font = pygame.font.Font(None, 24)      # Changed from 36
        self.large_font = pygame.font.Font(None, 32) # Changed from 48
        
        # Colors - make them more vibrant
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        
        # Adjust pointer size for smaller text
        self.pointer_size = 15  # New variable for pointer size
        
        # Make wheel smaller
        self.wheel_center = (self.width//2, self.height//2)
        self.wheel_radius = 200  # Changed from 300
        self.angle = 0
        self.spinning = False
        self.spin_speed = 0
        
        # Wheel sections with solid colors
        self.sections = [
            ("$500", (255, 140, 0)),         # Orange
            ("$1000", (255, 0, 255)),        # Magenta
            ("LOSE TURN", (139, 0, 0)),      # Dark Red
            ("BANKRUPT", (255, 0, 0)),       # Bright Red
            ("$100", (255, 255, 0)),         # Yellow
            ("$200", (0, 255, 0)),           # Green
            ("$300", (0, 255, 255)),         # Cyan
        ]
        self.num_sections = len(self.sections)
        
        # Add score tracking
        self.score = 0

    def draw_wheel(self):
        section_angle = 360 / self.num_sections
        for i in range(self.num_sections):
            start_angle = math.radians(i * section_angle + self.angle)
            end_angle = math.radians((i + 1) * section_angle + self.angle)
            
            # Draw solid color pie sections
            points = [self.wheel_center]  # Start from center
            # Add points along the arc
            for angle in range(int(math.degrees(start_angle)), int(math.degrees(end_angle)) + 1):
                rad = math.radians(angle)
                x = self.wheel_center[0] + math.cos(rad) * self.wheel_radius
                y = self.wheel_center[1] + math.sin(rad) * self.wheel_radius
                points.append((x, y))
            
            # Draw filled polygon for each section
            pygame.draw.polygon(self.screen, self.sections[i][1], points)
            
            # Draw text
            mid_angle = (start_angle + end_angle) / 2
            text_x = self.wheel_center[0] + math.cos(mid_angle) * (self.wheel_radius * 0.7)
            text_y = self.wheel_center[1] + math.sin(mid_angle) * (self.wheel_radius * 0.7)
            
            # Draw text with black outline
            text = self.large_font.render(self.sections[i][0], True, self.BLACK)
            outline_positions = [(2,2), (-2,-2), (2,-2), (-2,2)]
            for dx, dy in outline_positions:
                text_rect = text.get_rect(center=(text_x + dx, text_y + dy))
                self.screen.blit(text, text_rect)
            
            # Draw main text in white
            text = self.large_font.render(self.sections[i][0], True, self.WHITE)
            text_rect = text.get_rect(center=(text_x, text_y))
            self.screen.blit(text, text_rect)
        
        # Draw smaller center circles
        pygame.draw.circle(self.screen, self.BLACK, self.wheel_center, 15)  # Changed from 20
        pygame.draw.circle(self.screen, self.WHITE, self.wheel_center, 10)  # Changed from 15
        
        # Draw right triangle pointer outside the wheel
        pointer_points = [
            (self.wheel_center[0] - self.pointer_size, self.wheel_center[1] - self.wheel_radius - 30),  # Left point
            (self.wheel_center[0] + self.pointer_size, self.wheel_center[1] - self.wheel_radius - 30),  # Right point
            (self.wheel_center[0], self.wheel_center[1] - self.wheel_radius)  # Bottom point at wheel
        ]
        pygame.draw.polygon(self.screen, (255, 0, 0), pointer_points)

    def draw_scoreboard(self):
        # Draw scoreboard background (white rectangle with black border)
        scoreboard_rect = pygame.Rect(20, 20, 150, 80)
        pygame.draw.rect(self.screen, self.WHITE, scoreboard_rect)
        pygame.draw.rect(self.screen, self.BLACK, scoreboard_rect, 2)
        
        # Draw "SCORE" text
        score_text = self.font.render("SCORE:", True, self.BLACK)
        self.screen.blit(score_text, (30, 30))
        
        # Draw score value
        score_value = self.font.render(f"${self.score}", True, self.BLACK)
        self.screen.blit(score_value, (30, 60))

    def spin(self):
        self.spinning = True
        self.spin_speed = random.uniform(10, 20)

    def update(self):
        if self.spinning:
            self.angle += self.spin_speed
            self.spin_speed *= 0.99
            
            if self.spin_speed < 0.01:
                self.spinning = False
                self.spin_speed = 0
                section_angle = 360 / self.num_sections
                adjusted_angle = (-self.angle - 90) % 360
                current_section = int(adjusted_angle / section_angle)
                result = self.sections[current_section]
                
                # Update score to accumulate values
                if result[0] == "BANKRUPT":
                    self.score = 0  # Reset score on BANKRUPT
                elif result[0] != "LOSE TURN":
                    value = int(result[0].replace("$", ""))
                    self.score += value  # Add new value to existing score
                    
                return result[0]
        return None

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.spinning:
                        self.spin()
                
            self.screen.fill(self.WHITE)
            self.draw_wheel()
            self.draw_scoreboard()  # Add scoreboard drawing
            result = self.update()
            
            if not self.spinning:
                instructions = self.font.render("Click to spin the wheel!", True, self.BLACK)
                instructions_rect = instructions.get_rect(center=(self.width//2, 50))
                self.screen.blit(instructions, instructions_rect)
            
            if result:
                text = self.large_font.render(f"Landed on: {result}!", True, self.BLACK)
                text_rect = text.get_rect(center=(self.width//2, 50))
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = WhaleFortuneGUI()
    game.run() 