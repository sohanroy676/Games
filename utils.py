import pygame

def draw_grid_lines(surf: pygame.Surface, rows: int, cols: int, size: int, color: tuple[int], update=False, width=1) -> None:
    for i in range(rows+1):
        pygame.draw.line(surf, color, (0, i*size), (cols*size, i*size), width)
    for i in range(cols+1):
        pygame.draw.line(surf, color, (i*size, 0), (i*size, rows*size), width)
    if update: pygame.display.update()

class Label:
    saved = {}
    default = {"typeface": "freesansbold.ttf", "size": 50, "foreground": (0,0,0), "background": (255, 255, 255), "anchor": "center", "width":0, "borderRadius": -1, "save": False, "saveID":None}
    def __init__(self, text, pos, **kwargs):
        self.text = text
        self.settings = self.default | kwargs

        if self.settings["save"]:
            if self.settings["saveID"] is None: Label.saved[self.text] = self
            else: Label.saved[self.settings["saveID"]] = self
        
        self.font = pygame.font.Font(self.settings["typeface"], self.settings["size"])
        self.renderedText = self.font.render(f" {self.text} ", True, self.settings["foreground"])
        
        self.rect = self.renderedText.get_rect()
        exec(f"self.rect.{self.settings['anchor']} = pos")
    
    def draw(self, surf):
        pygame.draw.rect(surf, self.settings["background"], self.rect, self.settings["width"], self.settings["borderRadius"])
        surf.blit(self.renderedText, self.rect)

    def changeText(self, text):
        self.__init__(text, eval(f"self.rect.{self.settings['anchor']}"), **self.settings)
    
    def setDefault(**kwargs):
        Label.default |= kwargs
    
    def __repr__(self):
        return self.text

class Button(Label):
    def __init__(self, text, pos, onClick, **kwargs):
        self.onClick = onClick
        super().__init__(text, pos, **kwargs)
        if "hover" not in self.settings: self.settings["hover"] = (200, 200, 200)
        if "funcArgs" not in self.settings: self.settings["funcArgs"] = set()
        self.settings["isHovering"] = False
        self.bg = self.settings["background"]
    
    def checkHover(self, mousePos):
        self.settings["isHovering"] = self.rect.collidepoint(mousePos)
    
    def checkPress(self):
        if self.settings["isHovering"]:
            self.onClick(*self.settings["funcArgs"])
        return self.settings["isHovering"]

    def draw(self, surf):
        self.settings["background"] = self.settings["hover"] if self.settings["isHovering"] else self.bg
        super().draw(surf)