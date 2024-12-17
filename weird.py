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

