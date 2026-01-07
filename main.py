# -----------------------------------------------------------
# Plafó de comunicació de l'Esther v1.0
#
# Mostra un plafó amb 10 imatges que es poden seleccionar en
# un cicle rotatiu. Un cop seleccionada es reprodueix una audio
# d'aquesta mateixa imatge amb un reproductor incorporat.
#
# Aquest programa serveix per facilitar la comunicació entre dos 
# persones amb problemes de comunicació.
#
# (C) 2022 Isaac Ochoa, Girona.
# email: isaacohoagarriga@gmail.com
# -----------------------------------------------------------

import pygame, time, sys, os

# Inicialitzacions de pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Inicialitzacions de fonts
font_titol = pygame.font.SysFont('system', 50)
font_text = pygame.font.SysFont('system', 25)

# Agafant les dimensions de la pantalla
X, Y = pygame.display.Info().current_w - 30, pygame.display.Info().current_h - 30

# Inicialitzant la superficie de la pantalla + títol del header
pantalla1 = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
pygame.display.set_caption("Plafó de comunicació de l'Esther")

# Consts dels marges de la pantalla i dimensions dels botons
MARGES = (int(X/20), int(Y/10))
BUT_DIMS = (int(X/9), int(Y/5))

# Temps per botó
T_BUT = 2

# Colors de la pantalla
COLOR_FONS = (130, 220, 240)
COLOR_PREDETERMINAT = (0, 0, 0)
COLOR_SELECCIONAT = (0, 255, 0)
COLOR_BARRA1 = (150, 150, 150)
COLOR_BARRA2 = (0, 0, 0)

# Adreça i format en que es guarden les fotos.
ADRECA_FOTOS = "fotos\\"
FORMAT_FOTOS = ".jpg"

# Adreça i format en que es guarden els audios.
ADRECA_AUDIOS = "audios\\"
FORMAT_AUDIOS = ".wav"

# Un diccionari que assigna u nombre i unes coordenades  
# a cada un dels 10 botons que surten a la pantalla.
DICT_POS = {"1":(MARGES[0], MARGES[1]),
            "2":(int(X/4-BUT_DIMS[0]/2+MARGES[0]), MARGES[1]),
            "3":(int(X/2-BUT_DIMS[0]/2), MARGES[1]),
            "4":(int(3*X/4-BUT_DIMS[0]/2-MARGES[0]), MARGES[1]),
            "5":(X-BUT_DIMS[0]-MARGES[0], MARGES[1]),
            "6":(MARGES[0], Y/2 - MARGES[1]),
            "7":(int(X/4-BUT_DIMS[0]/2+MARGES[0]), Y/2 - MARGES[1]),
            "8":(int(X/2-BUT_DIMS[0]/2), Y/2 - MARGES[1]),
            "9":(int(3*X/4-BUT_DIMS[0]/2-MARGES[0]), Y/2 - MARGES[1]),
            "10":(X-BUT_DIMS[0]-MARGES[0], Y/2 - MARGES[1])}



def llegir_index():
    """
    Llegeix el fitxer index.txt amb tots els noms de les fotos/audios i trasforma
    aquests noms a noms amb els que el programa pot operar.
    """
    f = open("index.txt", mode="r", encoding="utf-8")
    aux = f.readlines()
    f.close()
    n_but = [i[0:-1] for i in aux]
    dict_noms = {}

    for i in range(2):
        for j in range(1, 11):
            dict_noms["".join([str(i), str(j)])] = n_but[len(dict_noms)]
            
    return dict_noms


# Diccionari que fa servir el programa per els noms de les imatges/audios.
DICT_NOMS = llegir_index()


def selec_but(but_compt, t_inici):
    """
    Segons el botó actual(but_compt), augmenta but_compt(següent botó)
    T_BUT segons després de t_inici.
    """
    # Si fa més de T_BUT segons que s'ha canviat botó es reinicia el temps
    # desde l'últim botó.
    if time.time() >= t_inici + T_BUT:
        t_inici = time.time()
        
        # Si s'arriba a l'últim botó es torna a començar sinó al següent.
        if but_compt < 10: but_compt += 1
        else: but_compt = 0
        
        
    return but_compt, t_inici


def pos_boto(audio_wav):
    """
    Reb el nom de l'audio.wav i retorna les coordenades del botó
    corresponent a aquest audio accedint a DICT_POS per les seves coords.
    """
    # Extrec el nom de l'audio
    nom = audio_wav.split(".")[0]
    
    # Busco la key nom al diccionari i retorno les coords segons DICT_POS
    return DICT_POS[list(DICT_NOMS.keys())[list(DICT_NOMS.values()).index(nom)][1:]]


def nom_but(n_but, pag):
    """
    Reb el número del botó i la pàgina, i retorna un string amb el nom
    de l'audio/imatge que li corresponen, on pag correspon al primer dígit
    i n_but al segon.
    """
    return DICT_NOMS["".join([str(int(pag)), str(n_but)])]

    
def dibuix_imatge(color, coords, nom):
    """
    Dibuixa la imatge corresponent a nom i el seu recuadre a les
    coordenades coords i de color color.
    """
    # carregant la imatge desde el seu arxiu i reescalant-la a la pantalla.
    imatge = pygame.image.load("".join([ADRECA_FOTOS, nom, FORMAT_FOTOS]))
    imatge = pygame.transform.scale(imatge, BUT_DIMS)
    pantalla1.blit(imatge, coords)

    # dibuixant el recuadre al voltant de la imatge del color corresponent.
    pygame.draw.rect(pantalla1, color, (coords, BUT_DIMS), 6)


def dibuix_quadres(but_compt, pag_2):
    """
    Dibuixa tots els botons a la pantalla a les coords adients segons DICT_POS
    i amb el recuadre del color adient segons el botó seleccionat(but_compt).
    """
    color = COLOR_PREDETERMINAT
    compt = 1  # potser es pot treure el compt amb un enumerate
    nom = "bfletxa"

    # Per cada botó i coordenada en DICT_POS.
    for elem, coords in DICT_POS.items():

        # Si el botó està seleccionat, color = COLOR_SELECCIONAT i es dibuixa.
        if compt == but_compt: color = COLOR_SELECCIONAT
        else: color = COLOR_PREDETERMINAT
        dibuix_imatge(color, coords, nom_but(elem, pag_2))
        compt += 1

    # Si està seleccionat el botó per canviar de pag, també es canvia de color
    if but_compt == 0: color = COLOR_SELECCIONAT
    else: color = COLOR_PREDETERMINAT

    # Depenent de la pag, es dibuixa una fletxa o una altra.
    if pag_2: nom = "dfletxa"
    dibuix_imatge(color, (int(X/2)-int(BUT_DIMS[0]/2), Y-MARGES[1]-BUT_DIMS[1]), nom)


def reproductor(temps, audio, duracio):
    """
    Dibuixa el reproductor a sota del botó seleccionat i dibuixa el temps fent
    una regla de tres amb les dimensions X del botó i el temps restant de l'audio.
    """
    # Calculo la llargada de la barra total i la barra reproductor segons les DIMS[0]
    # i el temps restant d'audio amb una simple regla de tres.
    coords = pos_boto(audio)
    llargada = BUT_DIMS[0]
    temps_restant = temps - time.time()
    llargada_repr = llargada/duracio*temps_restant

    # dibuix de la línia de la llargada total de l'audio.
    pygame.draw.line(pantalla1, COLOR_BARRA1,
                     (coords[0], coords[1]+int(BUT_DIMS[1]*1.1)),
                      (coords[0]+BUT_DIMS[0], coords[1]+int(BUT_DIMS[1]*1.1)), 8)

    # dibuix de la línia de la reproducció segons el temps restant de l'audio.
    pygame.draw.line(pantalla1, COLOR_BARRA2,
                     (coords[0], coords[1]+int(BUT_DIMS[1]*1.1)),
                      (BUT_DIMS[0]+coords[0]-llargada_repr, coords[1]+int(BUT_DIMS[1]*1.1)), 6)


def reproduir_audio(but_compt, pag_2):
    """
    Reprodueix l'audio corresponent al botó (segons but_compt i pag_2) i n'extreu
    la seva duració per poder calcular més endevant 
    """
    nom = "".join([nom_but(but_compt, pag_2), FORMAT_AUDIOS])
    audio = pygame.mixer.Sound("".join([ADRECA_AUDIOS, nom]))
    duracio = audio.get_length()
    audio.play()
    return time.time() + duracio, nom, duracio



# Inicialització de les variables globals del mainloop.
but_compt = 1
t_inici = time.time()
t_selec = 0
pag_2 = False
fi_repr = 0
audio_repr = str()

            
# A aquí s'inicia el mainloop del programa.
while True:

    # Si es prem la creu per tancar el programa, es para adequadement el programa.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Tecles és una llista amb totes les tecles del teclat i els seus estats.  
    tecles = pygame.key.get_pressed()

    # Si es prem l'espai del teclat i fa menys de T_BUT que s'ha premut
    # per última vegada, es reseteiga el temps desde l'última premuda de botó. 
    if tecles[pygame.K_SPACE] and time.time() > t_selec + T_BUT:
        t_selec = time.time()

        # Si el botó és el de canviar de pàgina es canvia, si no es reprodueix
        # l'audio adient al botó.
        if but_compt == 0:
            if pag_2: pag_2 = False
            else: pag_2 = True
        else: fi_repr, audio_repr, duracio = reproduir_audio(but_compt, pag_2)

    # Quan fi_repr >= time.time() vol dir que estic reproduint un audio així que
    # el cicle rotatiu dels botons es pausa fins al final de l'audio.
    if fi_repr >= time.time(): reproductor(fi_repr, audio_repr, duracio)
    else: but_compt, t_inici = selec_but(but_compt, t_inici)  

    # Dibuix dels botons.
    dibuix_quadres(but_compt, pag_2)

    # Dibuix del títol del projecte.
    titol = font_titol.render("Plafó de comunicació de l'Esther", True, (0, 0, 0))
    pantalla1.blit(titol, titol.get_rect(center=(int(X/2),int(Y/25))))

    # Actualitzo la pantalla dibuixant-ho tot i la resta queda de color COLOR_FONS
    pygame.display.update()
    pantalla1.fill(COLOR_FONS)
