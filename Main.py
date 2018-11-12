import pygame
import random
from Menu import Menu
# --- Global constants ---

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0,0,238)
RED = (255,0,0)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

size=(SCREEN_WIDTH,SCREEN_HEIGHT)
barra = pygame.image.load("barra11.png")
barra2 = pygame.image.load("barra2.png")



imagem_fundo = pygame.image.load("fundo2.png")

bola = pygame.image.load("bola2.png")

# Controla tamnaho da imagem de fundo
fundo = pygame.transform.scale(imagem_fundo, (size))

# --- Classes ---


class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """
        self.font = pygame.font.Font("kenvector_future_thin.ttf", 50)
        self.playerscore = 0
        self.player2score = 0
        self.playervsscore = 0
        self.player1score=0
        self.menu = Menu(("start", "about", "exit", "Player vs Player"), font_color=WHITE, font_size=50, ttf_font="kenvector_future.ttf")
        self.show_about_frame = False  # True: display about frame of the menu
        self.show_menu = True
        self.game_over = False
        self.som=Som()


        # Create sprite lists
       # self.block_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        # Create the player
        self.player = Player(20,90)
        self.all_sprites_list.add(self.player)



        # Create AI 2
        self.player2 = Player2(0, 0)
        self.all_sprites_list.add(self.player2)
     #   self.player2.estado = True
        #if self.player2.estado:
         #   self.all_sprites_list.remove(self.player2)


        # Criar jogador 2
        self.playervs=Playervs(0,0)
        self.all_sprites_list.add(self.playervs)


        # Create Bola
        self.bola = Bola(0,0)
        self.all_sprites_list.add(self.bola)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.show_menu and not self.show_about_frame:
                        if self.menu.state == 0:
                            self.show_menu = False
                            self.player2.estado = False
                            self.all_sprites_list.add(self.player2)
                            self.all_sprites_list.remove(self.playervs)
                            self.som.musica.play(-1)

                        elif self.menu.state == 1:
                            self.show_about_frame = True
                        elif self.menu.state == 2:
                            # User clicked exit
                            return True
                        elif self.menu.state == 3:
                            self.player2.estado=True
                            self.show_menu = False
                            self.all_sprites_list.remove(self.player2)
                            self.all_sprites_list.add(self.playervs)
                            
                            self.som.musica.play(-1)

                elif event.key == pygame.K_ESCAPE:
                    self.show_menu = True
                    self.show_about_frame = False
                    self.som.musica.stop()
                    self.player1score=0
                    self.playervsscore=0
                    self.playerscore=0
                    self.player2score=0
                    self.bola.reset()
                    self.player.reset()
                    self.playervs.reset()



                elif event.key == pygame.K_UP:
                    self.player.cima()
                elif event.key == ord('w'):#para o W ser primido
                    self.playervs.cima()#o w vai para cima
                elif event.key == pygame.K_DOWN:
                    self.player.baixo()
                elif event.key == ord('s'):
                    self.playervs.baixo()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.player.stop()
                elif event.key == ord('w') or event.key == ord('s'):
                    self.playervs.stop()

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        size=int(70)
        size1=int(70)

        if not self.show_menu and not self.player2.estado:
            # Move all the sprites
          #  self.player.rect.centery = SCREEN_HEIGHT / 2
            self.player.update(self.bola,self.som)
            self.player2.update(self.bola,self.som)
            self.bola.update(self.som)

            if self.bola.rect.x < 0:
                self.bola.reset()  # chama a funcao reset
                self.player.rect.centery = SCREEN_HEIGHT / 2
                self.player2score += 1

                if self.player2score == 1:
                    self.player.image = pygame.transform.smoothscale(barra, (20,size))
                    self.player.rect=self.player.image.get_rect()
                    self.player.rect.center = (50, SCREEN_HEIGHT / 2)

                elif self.player2score == 2:
                    self.player.image = pygame.transform.smoothscale(barra, (20, size-20))
                    self.player.rect = self.player.image.get_rect()
                    self.player.rect.center = (50, SCREEN_HEIGHT / 2)

            elif self.bola.rect.x > SCREEN_WIDTH:
                self.bola.reset()
                self.player.rect.centery = SCREEN_HEIGHT / 2
                self.playerscore += 1



        #Corre o update do playervs
        elif not self.show_menu and self.player2.estado:
            # Move all the sprites
            #  self.player.rect.centery = SCREEN_HEIGHT / 2
            self.player.update(self.bola, self.som)
            self.playervs.update(self.bola, self.som)
            self.bola.update(self.som)

            if self.bola.rect.x < 0:
                self.bola.reset()  # chama a funcao reset
                self.player.rect.centery = SCREEN_HEIGHT / 2
                self.playervsscore += 1
                if self.playervsscore == 1:
                    self.player.image = pygame.transform.smoothscale(barra, (20,size))
                    self.player.rect=self.player.image.get_rect()
                    self.player.rect.center = (50, SCREEN_HEIGHT / 2)
                elif self.playervsscore == 2:
                    self.player.image = pygame.transform.smoothscale(barra, (20, size-20))
                    self.player.rect = self.player.image.get_rect()
                    self.player.rect.center = (50, SCREEN_HEIGHT / 2)


            elif self.bola.rect.x > SCREEN_WIDTH:
                self.bola.reset()
                self.player.rect.centery = SCREEN_HEIGHT / 2
                self.player1score += 1
                if self.player1score == 1:
                    self.playervs.image=pygame.transform.smoothscale(barra2,(20, size1))
                    self.playervs.rect = self.player.image.get_rect()
                    self.playervs.rect.center=(SCREEN_WIDTH - 50,SCREEN_HEIGHT/2)
                elif self.player1score == 2:
                    self.playervs.image=pygame.transform.smoothscale(barra2,(20, size1-20))
                    self.playervs.rect = self.player.image.get_rect()
                    self.playervs.rect.center = (SCREEN_WIDTH - 50, SCREEN_HEIGHT / 2)


    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(BLACK)
        # background
        screen.blit(fundo, [0, 0])

        if not self.game_over:
            self.all_sprites_list.draw(screen) #mostra as imagens (sprites)


            time_wait = False  # True: when we have to wait at the end
            # --- Drawing code should go here
            if self.show_menu:
                if self.show_about_frame:
                    # Display the about frame
                    self.display_message(screen, "By Hugo and Vicente")
                else:
                    # Display the menu
                    self.menu.display_frame(screen)




            if self.playerscore == 3:
                self.display_message(screen, "Ganhou!", WHITE)
                time_wait = True
                self.playerscore = 0
                self.player2score = 0
                self.player.reset()
                self.show_menu = True
                self.som.win.play(0,3000)
                self.som.musica.stop()
                # Check if the enemy won the game
            elif self.player2score == 3:
                self.display_message(screen, "Perdes-te !", WHITE)
                time_wait = True
                self.playerscore = 0
                self.player2score = 0
                self.player.reset()
                self.show_menu = True
                self.som.lost.play(0,3000)
                self.som.musica.stop()

            #ve se o player 2 ganhou
            elif self.playervsscore == 3:
                self.display_message(screen, "Ganhas-te player 2!", WHITE)
                time_wait = True
                self.player1score = 0
                self.playervsscore = 0
                self.playervs.reset()
                self.player.reset()
                self.show_menu = True
                self.som.win.play(0,3000)
                self.som.musica.stop()

            elif self.player1score == 3:
                self.display_message(screen, "Ganhas-te player 1!", WHITE)
                time_wait = True
                self.player1score = 0
                self.playervsscore = 0
                self.playervs.reset()
                self.player.reset()
                self.show_menu = True
                self.som.win.play(0,3000)
                self.som.musica.stop()

            elif not self.show_menu:
            # Draw the score
                
                if not self.player2.estado:
                    player_score_label = self.font.render(str(self.playerscore), True, BLUE)  # mostrar score
                    screen.blit(player_score_label, (SCREEN_WIDTH - 551, SCREEN_HEIGHT - 590))

                    player2_score_label = self.font.render(str(self.player2score), True, RED)
                    screen.blit(player2_score_label, (SCREEN_WIDTH - 475, SCREEN_HEIGHT - 590))  #mostrar score

                elif self.player2.estado:
                    player1_score_label = self.font.render(str(self.player1score), True, BLUE)  # mostrar score
                    screen.blit(player1_score_label, (SCREEN_WIDTH - 551, SCREEN_HEIGHT - 590))

                    playervs_score_label = self.font.render(str(self.playervsscore), True, RED)
                    screen.blit(playervs_score_label , (SCREEN_WIDTH - 475, SCREEN_HEIGHT - 590))
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
        # --- This is for the game to wait a few seconds to display the message
            if time_wait:
                pygame.time.wait(3000)

    def display_message(self, screen, message, color=(255, 0, 0)):
        label = self.font.render(message, True, color)
        # Get the width and height of the label
        width = label.get_width()
        height = label.get_height()
        # Determine the position of the label
        posX = (SCREEN_WIDTH / 2) - (width / 2)
        posY = (SCREEN_HEIGHT / 2) - (height / 2)
        # Draw the label onto the screen
        screen.blit(label, (posX, posY))

class Player(pygame.sprite.Sprite):
    """ This class represents the player. """

    def __init__(self,x,y):
        super().__init__()

        self.image=pygame.transform.smoothscale(barra,(x,y)) #manipulação da barra
        #Para se desenhado
        self.rect = self.image.get_rect()
        self.vel=0
        self.rect.center = (50, SCREEN_HEIGHT / 2)



    def update(self,bola,Som):
        if self.rect.top <= 0 and self.vel < 0:
            self.vel = 0
        elif self.rect.bottom >= SCREEN_HEIGHT and self.vel > 0:
            self.vel = 0

        if self.rect.colliderect(bola.rect):
            # Change change_y to a random number between -5 and 5
            bola.vely = random.randint(-5, 5)
            bola.velx *= -1
            bola.rect.left = self.rect.right
            Som.barra.play(0)
        self.rect.y += self.vel

    def cima(self):
        self.vel = -5

    def baixo(self):
        self.vel = 5

    def stop(self):
        self.vel = 0

    def reset(self):
      #Return to initial values
        self.image = pygame.transform.smoothscale(barra, (20, 90))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT / 2


class Player2(pygame.sprite.Sprite):
    """ This class represents the player. """
    estado = True
    def __init__(self,x,y):
        super().__init__()

        self.image=pygame.transform.smoothscale(barra2,(20,90)) #manipulação da barra 20 90
        self.vely = 0
        #Para se desenhado
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH - 50, SCREEN_HEIGHT / 2)

    def update(self, bola, Som):

        if self.rect.top < 0:  # se for menor que o tamanho do ecra
            self.vely *= -1
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:  # se for maior que o tamnho do ecra
            self.vely *= -1  # multiplica a velocidade
            self.rect.bottom = SCREEN_HEIGHT

        if self.rect.centery > bola.rect.centery: #ir para cima
            dif = self.rect.centery - bola.rect.centery

            if dif <= 4:
                self.rect.centery = bola.rect.centery
            else:
                self.rect.y -= 4

        elif self.rect.centery < bola.rect.centery:
            dif = bola.rect.centery - self.rect.centery
            if dif <= 4:
               self.rect.centery = bola.rect.centery
            else:
                self.rect.y += 4
            # Check if we hit the ball
        if self.rect.colliderect(bola.rect):
            bola.velx *= -1
            bola.rect.right = self.rect.left
            Som.barra.play(0)




class Bola(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()

        self.image = pygame.transform.scale(bola, (25, 25))  # manipulação da bola

        # Para se desenhado
        self.rect = self.image.get_rect()
        self.vely = random.randint(-3, 3)
        self.velx = -5 # velocidade inical da bola
        #self.vely = 0

        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def update(self,Som):   #collider com a janela
        # Check for limits
        if self.rect.top < 0: # se for menor que o tamanho do ecra
            self.vely *= -1
            self.rect.top = 0
            Som.barra.play()
        elif self.rect.bottom > SCREEN_HEIGHT: #se for maior que o tamnho do ecra
            self.vely *= -1         #multiplica a velocidade
            self.rect.bottom = SCREEN_HEIGHT
            Som.barra.play()
        # Move left/right
        self.rect.x += self.velx
        # Move up/down
        self.rect.y += self.vely

    def reset(self):
        # Return to initial values
        self.rect.x = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT / 2
        self.vely = random.randint(-3, 3)
        self.velx = -5



class Playervs(pygame.sprite.Sprite):
    """ This class represents the player. """

    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.transform.smoothscale(barra2,(20,90)) #manipulação da barra

        #Para se desenhado
        self.rect = self.image.get_rect()
        self.vel=0
        self.rect.center = (SCREEN_WIDTH - 50, SCREEN_HEIGHT / 2)

    def update(self,bola,Som):
        if self.rect.top <= 0 and self.vel < 0:
            self.vel = 0
        elif self.rect.bottom >= SCREEN_HEIGHT and self.vel > 0:
            self.vel = 0

        if self.rect.colliderect(bola.rect):
            # Change change_y to a random number between -5 and 5
            bola.vely = random.randint(-5, 5)
            bola.velx *= -1
            bola.rect.right = self.rect.left
           # pygame.mixer.Sound("bola_hit.wav").play(0)
            Som.barra.play(0)
        self.rect.y += self.vel

    def cima(self):
        self.vel = -5

    def baixo(self):
        self.vel = 5

    def stop(self):
        self.vel = 0

    def reset(self):
      #Return to initial values
        self.image = pygame.transform.smoothscale(barra2, (20, 90))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - 50
        self.rect.y = SCREEN_HEIGHT / 2

class Som(object):
    def __init__(self):
        super().__init__()

        self.barra = pygame.mixer.Sound("bola_hit.wav")
      #  self.bola = pygame.mixer.Sound("bola_hit.wav")
        self.win = pygame.mixer.Sound("vitoria.wav")
        self.lost = pygame.mixer.Sound("derrota.wav")
        self.musica=pygame.mixer.Sound("musica.ogg")
        self.volume=pygame.mixer.Sound.set_volume(self.musica,0.3)