from imports import * 
class Loading_menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("assets/sprites/bg.png").convert_alpha()
        self.text = pygame.image.load("assets/sprites/txt.png").convert_alpha()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                    return "QUIT"
                if event.key == pygame.K_RETURN:
                    self.running = False
        return None
    def update(self):
        pass
    def draw(self):
        self.screen.fill((30, 30, 30))
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.text, (0, 0))
        pygame.display.flip()
    def run(self):
        while self.running:
            result = self.handle_events()
            if result == "QUIT": return "QUIT"
            self.update()
            self.draw()
            self.clock.tick(60)