import pygame


class MusicHandler:
    def __init__(self, music_file=None, volume=0.5):
        pygame.mixer.init()
        self.music_file = music_file
        self.volume = volume
        if music_file:
            self.load(music_file)
        self.sounds = {}  # For sound effects

    def load(self, music_file):
        self.music_file = music_file
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(self.volume)

    def play(self, loops=-1):
        if self.music_file:
            pygame.mixer.music.play(loops)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(volume)

    def load_sound(self, name, file_path):
        self.sounds[name] = pygame.mixer.Sound(file_path)

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()
