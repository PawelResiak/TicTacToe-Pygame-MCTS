import random
import time
import pygame
import sys



class GraphicalInterface:
    def __init__(self):
        pygame.init()

        self.okno = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()


    def set_board_size(self, width, height):
        self.width = width
        self.height = height
        self.rozmiar_okna = (width * 100, height * 100)
        self.okno = pygame.display.set_mode(self.rozmiar_okna)


    def pobierz_kliknięcie(self):
        for zdarzenie in pygame.event.get():
            if zdarzenie.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif zdarzenie.type == pygame.MOUSEBUTTONDOWN:
                x, y = zdarzenie.pos
                kolumna = x // 100
                wiersz = y // 100
                return (wiersz, kolumna)
        return None


    def umoveom_okno(self):
        pygame.display.set_caption("Kółko i Krzyżyk")
        self.okno.fill((255, 255, 255))
        board = ['X', 'O', ' ', 'O', 'X', ' ', ' ', ' ', 'X']
        running = True
        while running:
            for zdarzenie in pygame.event.get():
                if zdarzenie.type == pygame.QUIT:
                    #running = False
                    pygame.quit()
                    sys.exit()
                elif zdarzenie.type == pygame.MOUSEBUTTONDOWN:
                    x, y = zdarzenie.pos
                    kolumna = x // 100
                    wiersz = y // 100
                    #index = (wiersz-1) * self.width + (kolumna-1)

                    print(f"Kliknięto na pole: ({wiersz}, {kolumna})")
            self.okno.fill((255, 255, 255))
            self.rysuj_plansze()
            self.rysuj_znaki(board)
            pygame.display.flip()
            self.clock.tick(10)

    def odswiez_ekran(self, board):
        self.okno.fill((255, 255, 255))
        self.rysuj_plansze()
        self.rysuj_znaki(board)
        pygame.display.flip()
        self.clock.tick(60)


    def rysuj_plansze(self):
        for i in range(1, self.width):
            x = i * 100
            pygame.draw.line(self.okno, (0, 0, 0), (x, 0), (x, self.rozmiar_okna[1]), 3)

        for i in range(1, self.height):
            y = i * 100
            pygame.draw.line(self.okno, (0, 0, 0), (0, y), (self.rozmiar_okna[0], y), 3)

    def rysuj_o(self, wiersz, kolumna):
        srodek_x = kolumna * 100 + 50
        srodek_y = wiersz * 100 + 50
        pygame.draw.circle(self.okno, (0, 0, 255), (srodek_x, srodek_y), 35, 5)

    def rysuj_x(self, wiersz, kolumna):
        srodek_x = kolumna * 100 + 50
        srodek_y = wiersz * 100 + 50
        pygame.draw.line(self.okno, (255, 0, 0), (srodek_x - 35, srodek_y - 35), (srodek_x + 35, srodek_y + 35), 5)
        pygame.draw.line(self.okno, (255, 0, 0), (srodek_x + 35, srodek_y - 35), (srodek_x - 35, srodek_y + 35), 5)

    def rysuj_znaki(self, board):
        for y in range(self.height):
            for x in range(self.width):
                znak = board.grid[y * self.width + x]
                if znak == 'O':
                    self.rysuj_o(y, x)
                elif znak == 'X':
                    self.rysuj_x(y, x)



class Przycisk:
    def __init__(self, x, y, width, height, tekst, kolor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tekst = tekst
        self.kolor = kolor

        self.font = pygame.font.Font(None, 36)

        self.prostokąt = pygame.Rect(x, y, width, height)

    def czy_kliknięty(self, pozycja_myszy):
        return self.prostokąt.collidepoint(pozycja_myszy)

    def rysuj(self, okno):
        pygame.draw.rect(okno, self.kolor, self.prostokąt)
        tekst_surface = self.font.render(self.tekst, True, (255, 255, 255))
        tekst_rect = tekst_surface.get_rect(center=self.prostokąt.center)
        okno.blit(tekst_surface, tekst_rect)



class Board:
    def __init__(self, width, height, win_streak):
        self.width = width
        self.height = height
        self.win_streak = win_streak
        self.grid = [' ']* (self.height * self.width)
        self.winning_lines = self.generowanie_wygranych()

    def generowanie_wygranych(self):
        width = self.width
        height = self.height
        win_streak = self.win_streak

        horizontal = [tuple(width * y + x + k for k in range(win_streak)) 
                for y in range(height) for x in range(width - win_streak + 1)]

        vertical = [tuple(width * (y + k) + x for k in range(win_streak)) 
                for y in range(height - win_streak + 1) for x in range(width)]

        diag_1 = [tuple(width * (y + k) + (x + k) for k in range(win_streak)) 
                    for y in range(height - win_streak + 1) for x in range(width - win_streak + 1)]

        diag_2 = [tuple(width * (y - k) + (x + k) for k in range(win_streak)) 
                    for y in range(win_streak - 1, height) for x in range(width - win_streak + 1)]

        return horizontal + vertical + diag_1 + diag_2

    def display_console(self):
        separator = '-' * (4 * self.width +1) + '\n'
        
        grid = separator
        for y in range(self.height):
            wiersz = '|'
            for x in range(self.width):
                wiersz += f' {self.grid[x + (y * self.width)]} |'
            grid += wiersz + '\n' + separator
            
        print(grid, end='')

    def get_legal_moves(self):
        return [x for x in range(self.height*self.width) if self.grid[x] == ' ']

    def check_winner(self):
        for line in self.winning_lines:
            first_mark = self.grid[line[0]]
            if first_mark != ' ':
                if all(self.grid[index] == first_mark for index in line):
                    return first_mark
                
        if len(self.get_legal_moves()) == 0:
            return 'draw'
            
        return None

    def make_move(self, index, player_mark):
        self.grid[index] = player_mark

    def clone(self):
        new_board = Board(self.width, self.height, self.win_streak)
        new_board.grid = self.grid.copy()
        return new_board
         


class BotMinimax_3x3:
    def __init__(self, bot_mark):
        self.bot = bot_mark
        self.opponent_mark = 'X' if bot_mark == 'O' else "O"


        
    def _minmax(self, board_object, current_player_mark):
        result = board_object.check_win_streakner()
        if result == 'draw':
            return 0
        elif result == self.bot:
            return 1
        elif result is not None and result != self.bot:
            return -1

        movey = board_object.get_legal_moves()
        resulti = []
        for move in movey:
            board_object.make_move(move, current_player_mark)
            kolejny_player_mark = "X" if current_player_mark == "O" else "O"
            result = self._minmax(board_object, kolejny_player_mark)
            resulti.append(result)
            board_object.make_move(move, " ")

        if current_player_mark == self.bot:
            return max(resulti)
        else:
            return min(resulti)



    def find_best_move(self, board_object):
        best_result = -100
        best_move = None

        for move in board_object.get_legal_moves():
            board_object.make_move(move, self.bot)  
            result = self._minmax(board_object, self.opponent_mark) 
            board_object.make_move(move, " ")  

            if result > best_result:
                best_result = result
                best_move = move

        return best_move




class BotMonteCarlo:
    def __init__(self, bot_mark, time_for_move):
        self.bot = bot_mark
        self.time_for_move = time_for_move
        self.opponent_mark = 'X' if bot_mark == 'O' else 'O'



    def _simulate_game(self, board_copy, current_player_mark):
        while True:
            random_move = random.choice(board_copy.get_legal_moves())
            board_copy.make_move(random_move, current_player_mark)
            result = board_copy.check_winner()
            if result == 'draw':
                return 0
            elif result == self.bot:
                return 1
            elif result is not None and result != self.bot:
                return -1
            current_player_mark = 'X' if current_player_mark == 'O' else 'O'



    def find_best_move(self, board_object):
        best_move = None
        best_result = -999999
        get_legal_moves = board_object.get_legal_moves()
        time_for_move = self.time_for_move / len(get_legal_moves)
        for move in get_legal_moves:
            sum_of_points = 0
            czas_start = time.time()
            while time.time() - czas_start < time_for_move:
                board_copy = board_object.clone()
                board_copy.make_move(move, self.bot)
                sum_of_points += self._simulate_game(board_copy, self.opponent_mark)
            if sum_of_points > best_result:
                best_result = sum_of_points
                best_move = move

        return best_move




class Gra:
    def __init__(self):
        self.interface = GraphicalInterface()
        self.history = []

        # 1. Wybór trybu gry
        mode = [
            ("player vs player", 1),
            ("player vs bot", 2)
        ]
        self.rodzaj_gry = self.choice_menu(mode)

        # 2. Jeśli gra z botem, pytamy o szczegóły
        if self.rodzaj_gry == 2:
            opcje_znaku = [("Play as a (O)", "O"), ("Play as a(X)", "X")]
            self.znak_czlowieka = self.choice_menu(opcje_znaku)
            self.znak_bota = "X" if self.znak_czlowieka == "O" else "O"

            difficulty_options = [("Poziom Łatwy", 1), ("Poziom Średni", 2), ("Poziom Trudny", 3)]
            self.difficulty_level = self.choice_menu(difficulty_options)

        # 3. Wybór rozmiaru planszy (Gotowe pakiety wymiarów i warunków winning_linesj)
        board_size = [
            ("Klasyczna 3x3 (win_streak: 3)", (3, 3, 3)),
            ("Rozszerzona 5x5 (win_streak: 4)", (5, 5, 4)),
            ("Ogromna 10x10 (win_streak: 5)", (10, 10, 5))
        ]
        wybrana_board = self.choice_menu(board_size)
        self.width = wybrana_board[0]
        self.height = wybrana_board[1]
        self.win_streak = wybrana_board[2]

        # 4. Inicjalizacja gry po zebraniu danych
        self.interface.set_board_size(self.width, self.height)
        self.board = Board(self.width, self.height, self.win_streak)
        self.current_player_mark = 'X'
    
    
    
    def choice_menu(self, opcje):
        # opcje to lista krotek, np. [("Tekst na przycisku", zwracana_wartosc), ...]
        buttons = []
        start_y = 100 # Wysokość, od której zaczynamy rysować pierwszy przycisk
        
        # Generator: przechodzi przez listę opcji i automatycznie buduje z nich buttons
        for tekst, wartosc in opcje:
            nowy_przycisk = Przycisk(200, start_y, 400, 60, tekst, (100, 100, 200))
            buttons.append((nowy_przycisk, wartosc))
            start_y += 80 # Każdy kolejny przycisk będzie o 80 pikseli niżej
            
        while True:
            for zdarzenie in pygame.event.get():
                if zdarzenie.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Sprawdzanie, czy kliknięto w którykolwiek przycisk
                if zdarzenie.type == pygame.MOUSEBUTTONDOWN:
                    for przycisk, wartosc in buttons:
                        if przycisk.czy_kliknięty(zdarzenie.pos):
                            return wartosc

            self.interface.okno.fill((255, 255, 255))
            for przycisk, _ in buttons:
                przycisk.rysuj(self.interface.okno)
            pygame.display.flip()
            self.interface.clock.tick(60)
    
    
    
    def ekran_koncowy(self, result):
        if result == 'draw':
            komunikat = "draw!"
        elif self.rodzaj_gry == 1:
            komunikat = f"Wygrał player_mark {result}!"
        elif self.rodzaj_gry == 2:
            if result == self.znak_czlowieka:
                komunikat = "Wygrałeś!"
            else:
                komunikat = "Przegrałeś!"
        else:
            komunikat = f"Bot {result} wygrał!"

        srodek_x = self.interface.rozmiar_okna[0] // 2
        srodek_y = self.interface.rozmiar_okna[1] // 2

        czcionka = pygame.font.Font(None, 72)
        napis = czcionka.render(komunikat, True, (0, 0, 0), (255, 255, 255))
        napis_rect = napis.get_rect(center=(srodek_x, srodek_y - 50))

        przycisk_restart = Przycisk(srodek_x - 150, srodek_y + 20, 300, 60, "Zagraj ponownie", (100, 200, 100))

        while True:
            for zdarzenie in pygame.event.get():
                if zdarzenie.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if zdarzenie.type == pygame.MOUSEBUTTONDOWN:
                    if przycisk_restart.czy_kliknięty(zdarzenie.pos):
                        return True # player_mark zdecydował się na restart

            # Tło: Rysujemy normalną planszę
            self.interface.okno.fill((255, 255, 255))
            self.interface.rysuj_plansze()
            self.interface.rysuj_znaki(self.board)
            
            # Wierzch: Od razu nakładamy napis i przycisk
            self.interface.okno.blit(napis, napis_rect)
            przycisk_restart.rysuj(self.interface.okno)
            
            pygame.display.flip()
            self.interface.clock.tick(15)


    
    def start(self):
        running = True
        while running:
            self.interface.odswiez_ekran(self.board)


            # Sędziowanie
            result = self.board.check_winner()

            if result is not None:
                chce_zagrac_ponownie = self.ekran_koncowy(result)
                return chce_zagrac_ponownie # True jeśli player_mark chce zagrać ponownie, False jeśli nie

            # 3. ROZDZIELENIE TUR: Gra z botem i jego tura
            if self.rodzaj_gry == 2 and self.current_player_mark == self.znak_bota:
                # Bot odpala silnik
                index = self._move_bota(self.znak_bota)
                
                # Wykonanie moveu na planszy
                self.board.make_move(index, self.current_player_mark)
                self.history.append(index)
                self.current_player_mark = "O" if self.current_player_mark == "X" else "X"
                continue # Bot zagrał, wracamy na początek pętli

            klik = self.interface.pobierz_kliknięcie()
            if klik is not None:
                wiersz, kolumna = klik
                index = wiersz * self.width + kolumna

                if self.board.grid[index] == ' ':
                    self.board.make_move(index, self.current_player_mark)
                    self.history.append(index)
                    self.current_player_mark = "O" if self.current_player_mark == "X" else "X"
                else:
                    print("To pole jest już zajęte. Wybierz inne pole.")



    def _check_win_streakner(self, result):
        if result == 'draw':
            print('draw!')
            return # Twarde wyjście, żeby nie drukowało przegranej niżej

        if self.rodzaj_gry == 1:
            if result == 'X':
                print("Wygrał player_mark X!")
            else:
                print("Wygrał player_mark O!")
        elif self.rodzaj_gry == 2:
            if result == self.znak_czlowieka:
                print("Wygrałeś!")
            else:
                print("Przegrałeś!")
        else:
            if result == 'X':
                print("Bot X wygrał!")
            else:
                print("Bot O wygrał!")

    
    
    def _move_bota(self, znak_bota):
        
        # 1. Ustalenie, jaki poziom trudności dotyczy tego konkretnego bota
        if self.rodzaj_gry == 2:
            poziom = self.difficulty_level
        else: # Tryb 3 (Bot vs Bot)
            poziom = self.difficulty_level_x if znak_bota == 'X' else self.difficulty_level_o
            
        #
        ilosc_opcji = len(self.board.get_legal_moves())
        konfiguracja_czasu = {1: (0.2, 0.03), 2: (0.5, 0.05), 3: (2.0, 0.15)}
        baza, mnoznik = konfiguracja_czasu[poziom]
        time_for_move = baza + (mnoznik * ilosc_opcji)
        
        # 3. Powołanie "świeżego" bota z precyzyjnymi wytycznymi na tę jedną turę
        aktywny_bot = BotMonteCarlo(znak_bota, time_for_move)
        
        # 4. Odpytanie objectu o best move
        return aktywny_bot.find_best_move(self.board)



if __name__ == '__main__':
    gra_trwa = True
    while gra_trwa:
        new_gra = Gra()
        gra_trwa = new_gra.start()
