import pygame
import yaml
from src.splash import SplashScreen
from src.mainscreen import SoundStudioApp

# Pygameを初期化
pygame.mixer.init()

# Load configuration
with open('config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

if __name__ == "__main__":
    if config.get('splash', True):
        splash = SplashScreen()
        splash.mainloop()
    app = SoundStudioApp()
    app.mainloop()