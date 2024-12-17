def generate_random_wave(self):
    # the more waves you do the bigger they become
    num_enemies = min(10 + self.current_wave, 50)  # Stopping point: max 50 enemies

    # Generate a random wave configuration
    wave_config = {}
    for i in range(num_enemies):
        weights = [self.enemies_data[enemy]["tier"] for enemy in self.possible_enemies]
        chosen_enemy = random.choices(self.possible_enemies, weights=weights, k=1)[0]
        wave_config[chosen_enemy] = wave_config.get(chosen_enemy, 0) + 1

    return wave_config

def end_wave(self):
    if not self.active_enemies and self.is_wave_active:
        print(f"Wave {self.current_wave} ended!")
        self.is_wave_active = False


def reward_player(self, display):
    """Rewards the player and displays the reward message on the screen."""
    # Gold reward
    gold_reward = 50
    self.player.gold += gold_reward

    # Determine if a bonus reward is granted
    bonus_reward = random.random() < 0.3  # 30% chance
    bonus_text = " and a bonus!" if bonus_reward else "!"

    # Prepare reward message
    reward_text = f"Wave {self.current_wave} completed! You earned {gold_reward} gold{bonus_text}"
    text_surface = self.font.render(reward_text, True, (255, 255, 0))  # Yellow text
    text_rect = text_surface.get_rect(center=(display.get_width() // 2, display.get_height() // 4))

    # Draw a "balloon" background
    balloon_rect = text_rect.inflate(20, 10)  # Add padding around the text
    pygame.draw.rect(display, deep_black, balloon_rect)  # Black rectangle as the balloon
    pygame.draw.rect(display, white, balloon_rect, 3)  # White border

    # Blit text onto the screen
    display.blit(text_surface, text_rect)

    pygame.time.delay(2000)

    # Apply bonus if granted
    if bonus_reward:
        self.player.give_bonus()  # todo: add this method to the player class

def display_wave_completed_message(self, display):
    message = f"Wave {self.current_wave} completed!"
    text_color = white
    font_size = 48

    # Render the text
    font = pygame.font.Font("fonts/pixel_font.ttf", font_size)
    text_surface = font.render(message, True, text_color)
    text_rect = text_surface.get_rect(center=(display.get_width() // 2, display.get_height() // 2))

    display.blit(text_surface, text_rect)

# todo: one of these must have a treasure chest
    def handle_enemy_drop(self, enemy):
        """Handles rewards dropped by a defeated enemy."""
        drop_chance = random.random()
        if drop_chance < 0.33:  # 20% chance to drop gold
            print(f"Enemy {enemy.name} dropped gold!")
            self.player.gold += 10

    def show_wave_complete_popup(self, display):
        font = pygame.font.Font("pixel_font.ttf", 36)
        text_color = white

        # Create popup message
        message = "Wave Completed! Start next wave or leave?"
        text_surface = font.render(message, True, text_color)
        text_rect = text_surface.get_rect(center=(display.get_width() // 2, display.get_height() // 2 - 50))

        # Buttons for user choice
        next_wave_button = pygame.Rect(display.get_width() // 2 - 100, display.get_height() // 2 + 50, 200, 50)
        leave_button = pygame.Rect(display.get_width() // 2 - 100, display.get_height() // 2 + 120, 200, 50)

        pygame.draw.rect(display, greenish, next_wave_button)  # Green button for Next Wave
        pygame.draw.rect(display, red, leave_button)  # Red button for Leave

        # Render buttons text
        next_wave_text = font.render("Next Wave", True, text_color)
        leave_text = font.render("Leave", True, text_color)

        display.blit(text_surface, text_rect)
        display.blit(next_wave_text, (next_wave_button.centerx - next_wave_text.get_width() // 2,
                                      next_wave_button.centery - next_wave_text.get_height() // 2))
        display.blit(leave_text, (leave_button.centerx - leave_text.get_width() // 2,
                                  leave_button.centery - leave_text.get_height() // 2))

        # Wait for player input to make a choice
        choice_made = False
        while not choice_made:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if next_wave_button.collidepoint(event.pos):
                        self.start_next_wave()  # Start the next wave
                        choice_made = True
                    elif leave_button.collidepoint(event.pos):
                        self.is_wave_active = False  # End the wave
                        choice_made = True

