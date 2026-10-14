import random
import time
import pygame
import sys



class InterfaceGraficzny:
    def __init__(self):
        pygame.init()

        self.okno = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()


    def ustaw_wymiary_planszy(self, szerokosc, wysokosc):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.rozmiar_okna = (szerokosc * 100, wysokosc * 100)
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


    def uruchom_okno(self):
        pygame.display.set_caption("Kółko i Krzyżyk")
        self.okno.fill((255, 255, 255))
        plansza = ['X', 'O', ' ', 'O', 'X', ' ', ' ', ' ', 'X']
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
                    #indeks = (wiersz-1) * self.szerokosc + (kolumna-1)

                    print(f"Kliknięto na pole: ({wiersz}, {kolumna})")
            self.okno.fill((255, 255, 255))
            self.rysuj_plansze()
            self.rysuj_znaki(plansza)
            pygame.display.flip()
            self.clock.tick(10)

    def odswiez_ekran(self, plansza):
        self.okno.fill((255, 255, 255))
        self.rysuj_plansze()
        self.rysuj_znaki(plansza)
        pygame.display.flip()
        self.clock.tick(60)


    def rysuj_plansze(self):
        for i in range(1, self.szerokosc):
            x = i * 100
            pygame.draw.line(self.okno, (0, 0, 0), (x, 0), (x, self.rozmiar_okna[1]), 3)

        for i in range(1, self.wysokosc):
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

    def rysuj_znaki(self, plansza):
        for y in range(self.wysokosc):
            for x in range(self.szerokosc):
                znak = plansza.pola[y * self.szerokosc + x]
                if znak == 'O':
                    self.rysuj_o(y, x)
                elif znak == 'X':
                    self.rysuj_x(y, x)



class Przycisk:
    def __init__(self, x, y, szerokosc, wysokosc, tekst, kolor):
        self.x = x
        self.y = y
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.tekst = tekst
        self.kolor = kolor

        self.font = pygame.font.Font(None, 36)

        self.prostokąt = pygame.Rect(x, y, szerokosc, wysokosc)

    def czy_kliknięty(self, pozycja_myszy):
        return self.prostokąt.collidepoint(pozycja_myszy)

    def rysuj(self, okno):
        pygame.draw.rect(okno, self.kolor, self.prostokąt)
        tekst_surface = self.font.render(self.tekst, True, (255, 255, 255))
        tekst_rect = tekst_surface.get_rect(center=self.prostokąt.center)
        okno.blit(tekst_surface, tekst_rect)



class Plansza:
    def __init__(self, szerokosc, wysokosc, wygrana):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.wygrana = wygrana
        self.pola = [' ']* (self.wysokosc * self.szerokosc)
        self.wygrane = self.generowanie_wygranych()

    def generowanie_wygranych(self):
        szerokosc = self.szerokosc
        wysokosc = self.wysokosc
        wygrana = self.wygrana

        poziome = [tuple(szerokosc * y + x + k for k in range(wygrana)) 
                for y in range(wysokosc) for x in range(szerokosc - wygrana + 1)]

        pionowe = [tuple(szerokosc * (y + k) + x for k in range(wygrana)) 
                for y in range(wysokosc - wygrana + 1) for x in range(szerokosc)]

        przekatna_1 = [tuple(szerokosc * (y + k) + (x + k) for k in range(wygrana)) 
                    for y in range(wysokosc - wygrana + 1) for x in range(szerokosc - wygrana + 1)]

        przekatna_2 = [tuple(szerokosc * (y - k) + (x + k) for k in range(wygrana)) 
                    for y in range(wygrana - 1, wysokosc) for x in range(szerokosc - wygrana + 1)]

        return poziome + pionowe + przekatna_1 + przekatna_2

    def wyswietl_plansze(self):
        linia_oddzielajaca = '-' * (4 * self.szerokosc +1) + '\n'
        
        pola = linia_oddzielajaca
        for y in range(self.wysokosc):
            wiersz = '|'
            for x in range(self.szerokosc):
                wiersz += f' {self.pola[x + (y * self.szerokosc)]} |'
            pola += wiersz + '\n' + linia_oddzielajaca
            
        print(pola, end='')

    def mozliwe_ruchy(self):
        return [x for x in range(self.wysokosc*self.szerokosc) if self.pola[x] == ' ']

    def sedzia(self):
        for kombinacja in self.wygrane:
            pierwszy_znak = self.pola[kombinacja[0]]
            if pierwszy_znak != ' ':
                if all(self.pola[indeks] == pierwszy_znak for indeks in kombinacja):
                    return pierwszy_znak
                
        if len(self.mozliwe_ruchy()) == 0:
            return 'remis'
            
        return None

    def zamien_znak(self, index, gracz):
        self.pola[index] = gracz

    def kopiuj(self):
        nowa_plansza = Plansza(self.szerokosc, self.wysokosc, self.wygrana)
        nowa_plansza.pola = self.pola.copy()
        return nowa_plansza
         


class BotMinimax_3x3:
    def __init__(self, bot_znak):
        self.bot = bot_znak
        self.przeciwnik = 'X' if bot_znak == 'O' else "O"


        
    def _minmax(self, plansza_obiekt, aktualny_gracz):
        wynik = plansza_obiekt.sedzia()
        if wynik == 'remis':
            return 0
        elif wynik == self.bot:
            return 1
        elif wynik is not None and wynik != self.bot:
            return -1

        ruchy = plansza_obiekt.mozliwe_ruchy()
        wyniki = []
        for ruch in ruchy:
            plansza_obiekt.zamien_znak(ruch, aktualny_gracz)
            kolejny_gracz = "X" if aktualny_gracz == "O" else "O"
            wynik = self._minmax(plansza_obiekt, kolejny_gracz)
            wyniki.append(wynik)
            plansza_obiekt.zamien_znak(ruch, " ")

        if aktualny_gracz == self.bot:
            return max(wyniki)
        else:
            return min(wyniki)



    def znajdz_najlepszy_ruch(self, plansza_obiekt):
        najlepszy_wynik = -100
        najlepszy_ruch = None

        for ruch in plansza_obiekt.mozliwe_ruchy():
            plansza_obiekt.zamien_znak(ruch, self.bot)  
            wynik = self._minmax(plansza_obiekt, self.przeciwnik) 
            plansza_obiekt.zamien_znak(ruch, " ")  

            if wynik > najlepszy_wynik:
                najlepszy_wynik = wynik
                najlepszy_ruch = ruch

        return najlepszy_ruch




class BotMonteCarlo:
    def __init__(self, bot_znak, czas_na_ruch):
        self.bot = bot_znak
        self.czas_na_ruch = czas_na_ruch
        self.przeciwnik = 'X' if bot_znak == 'O' else 'O'



    def _symuluj_gre(self, plansza_kopia, aktualny_gracz):
        while True:
            losowy_ruch = random.choice(plansza_kopia.mozliwe_ruchy())
            plansza_kopia.zamien_znak(losowy_ruch, aktualny_gracz)
            wynik = plansza_kopia.sedzia()
            if wynik == 'remis':
                return 0
            elif wynik == self.bot:
                return 1
            elif wynik is not None and wynik != self.bot:
                return -1
            aktualny_gracz = 'X' if aktualny_gracz == 'O' else 'O'



    def znajdz_najlepszy_ruch(self, plansza_obiekt):
        najlepszy_ruch = None
        najlepszy_wynik = -999999
        mozliwe_ruchy = plansza_obiekt.mozliwe_ruchy()
        czas_na_ruch = self.czas_na_ruch / len(mozliwe_ruchy)
        for ruch in mozliwe_ruchy:
            suma_punktow = 0
            czas_start = time.time()
            while time.time() - czas_start < czas_na_ruch:
                kopia_planszy = plansza_obiekt.kopiuj()
                kopia_planszy.zamien_znak(ruch, self.bot)
                suma_punktow += self._symuluj_gre(kopia_planszy, self.przeciwnik)
            if suma_punktow > najlepszy_wynik:
                najlepszy_wynik = suma_punktow
                najlepszy_ruch = ruch

        return najlepszy_ruch




class Gra:
    def __init__(self):
        self.interface = InterfaceGraficzny()
        self.historia = []

        # 1. Wybór trybu gry
        opcje_trybu = [
            ("Człowiek vs Człowiek", 1),
            ("Człowiek vs Bot", 2)
        ]
        self.rodzaj_gry = self.menu_wyboru(opcje_trybu)

        # 2. Jeśli gra z botem, pytamy o szczegóły
        if self.rodzaj_gry == 2:
            opcje_znaku = [("Gram jako Kółko (O)", "O"), ("Gram jako Krzyżyk (X)", "X")]
            self.znak_czlowieka = self.menu_wyboru(opcje_znaku)
            self.znak_bota = "X" if self.znak_czlowieka == "O" else "O"

            opcje_trudnosci = [("Poziom Łatwy", 1), ("Poziom Średni", 2), ("Poziom Trudny", 3)]
            self.poziom_trudnosci = self.menu_wyboru(opcje_trudnosci)

        # 3. Wybór rozmiaru planszy (Gotowe pakiety wymiarów i warunków wygranej)
        opcje_planszy = [
            ("Klasyczna 3x3 (Wygrana: 3)", (3, 3, 3)),
            ("Rozszerzona 5x5 (Wygrana: 4)", (5, 5, 4)),
            ("Ogromna 10x10 (Wygrana: 5)", (10, 10, 5))
        ]
        wybrana_plansza = self.menu_wyboru(opcje_planszy)
        self.szerokosc = wybrana_plansza[0]
        self.wysokosc = wybrana_plansza[1]
        self.wygrana = wybrana_plansza[2]

        # 4. Inicjalizacja gry po zebraniu danych
        self.interface.ustaw_wymiary_planszy(self.szerokosc, self.wysokosc)
        self.plansza = Plansza(self.szerokosc, self.wysokosc, self.wygrana)
        self.aktualny_gracz = 'X'
    
    
    
    def menu_wyboru(self, opcje):
        # opcje to lista krotek, np. [("Tekst na przycisku", zwracana_wartosc), ...]
        przyciski = []
        start_y = 100 # Wysokość, od której zaczynamy rysować pierwszy przycisk
        
        # Generator: przechodzi przez listę opcji i automatycznie buduje z nich przyciski
        for tekst, wartosc in opcje:
            nowy_przycisk = Przycisk(200, start_y, 400, 60, tekst, (100, 100, 200))
            przyciski.append((nowy_przycisk, wartosc))
            start_y += 80 # Każdy kolejny przycisk będzie o 80 pikseli niżej
            
        while True:
            for zdarzenie in pygame.event.get():
                if zdarzenie.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Sprawdzanie, czy kliknięto w którykolwiek przycisk
                if zdarzenie.type == pygame.MOUSEBUTTONDOWN:
                    for przycisk, wartosc in przyciski:
                        if przycisk.czy_kliknięty(zdarzenie.pos):
                            return wartosc

            self.interface.okno.fill((255, 255, 255))
            for przycisk, _ in przyciski:
                przycisk.rysuj(self.interface.okno)
            pygame.display.flip()
            self.interface.clock.tick(60)
    
    
    
    def ekran_koncowy(self, wynik):
        if wynik == 'remis':
            komunikat = "Remis!"
        elif self.rodzaj_gry == 1:
            komunikat = f"Wygrał gracz {wynik}!"
        elif self.rodzaj_gry == 2:
            if wynik == self.znak_czlowieka:
                komunikat = "Wygrałeś!"
            else:
                komunikat = "Przegrałeś!"
        else:
            komunikat = f"Bot {wynik} wygrał!"

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
                        return True # Gracz zdecydował się na restart

            # Tło: Rysujemy normalną planszę
            self.interface.okno.fill((255, 255, 255))
            self.interface.rysuj_plansze()
            self.interface.rysuj_znaki(self.plansza)
            
            # Wierzch: Od razu nakładamy napis i przycisk
            self.interface.okno.blit(napis, napis_rect)
            przycisk_restart.rysuj(self.interface.okno)
            
            pygame.display.flip()
            self.interface.clock.tick(15)


    
    def start(self):
        running = True
        while running:
            self.interface.odswiez_ekran(self.plansza)


            # Sędziowanie
            wynik = self.plansza.sedzia()

            if wynik is not None:
                chce_zagrac_ponownie = self.ekran_koncowy(wynik)
                return chce_zagrac_ponownie # True jeśli gracz chce zagrać ponownie, False jeśli nie

            # 3. ROZDZIELENIE TUR: Gra z botem i jego tura
            if self.rodzaj_gry == 2 and self.aktualny_gracz == self.znak_bota:
                # Bot odpala silnik
                indeks = self._ruch_bota(self.znak_bota)
                
                # Wykonanie ruchu na planszy
                self.plansza.zamien_znak(indeks, self.aktualny_gracz)
                self.historia.append(indeks)
                self.aktualny_gracz = "O" if self.aktualny_gracz == "X" else "X"
                continue # Bot zagrał, wracamy na początek pętli

            klik = self.interface.pobierz_kliknięcie()
            if klik is not None:
                wiersz, kolumna = klik
                indeks = wiersz * self.szerokosc + kolumna

                if self.plansza.pola[indeks] == ' ':
                    self.plansza.zamien_znak(indeks, self.aktualny_gracz)
                    self.historia.append(indeks)
                    self.aktualny_gracz = "O" if self.aktualny_gracz == "X" else "X"
                else:
                    print("To pole jest już zajęte. Wybierz inne pole.")



    def _sedzia(self, wynik):
        if wynik == 'remis':
            print('Remis!')
            return # Twarde wyjście, żeby nie drukowało przegranej niżej

        if self.rodzaj_gry == 1:
            if wynik == 'X':
                print("Wygrał gracz X!")
            else:
                print("Wygrał gracz O!")
        elif self.rodzaj_gry == 2:
            if wynik == self.znak_czlowieka:
                print("Wygrałeś!")
            else:
                print("Przegrałeś!")
        else:
            if wynik == 'X':
                print("Bot X wygrał!")
            else:
                print("Bot O wygrał!")

    
    
    def _ruch_bota(self, znak_bota):
        
        # 1. Ustalenie, jaki poziom trudności dotyczy tego konkretnego bota
        if self.rodzaj_gry == 2:
            poziom = self.poziom_trudnosci
        else: # Tryb 3 (Bot vs Bot)
            poziom = self.poziom_trudnosci_x if znak_bota == 'X' else self.poziom_trudnosci_o
            
        #
        ilosc_opcji = len(self.plansza.mozliwe_ruchy())
        konfiguracja_czasu = {1: (0.2, 0.03), 2: (0.5, 0.05), 3: (2.0, 0.15)}
        baza, mnoznik = konfiguracja_czasu[poziom]
        czas_na_ruch = baza + (mnoznik * ilosc_opcji)
        
        # 3. Powołanie "świeżego" bota z precyzyjnymi wytycznymi na tę jedną turę
        aktywny_bot = BotMonteCarlo(znak_bota, czas_na_ruch)
        
        # 4. Odpytanie obiektu o najlepszy ruch
        return aktywny_bot.znajdz_najlepszy_ruch(self.plansza)



if __name__ == '__main__':
    gra_trwa = True
    while gra_trwa:
        nowa_gra = Gra()
        gra_trwa = nowa_gra.start()
