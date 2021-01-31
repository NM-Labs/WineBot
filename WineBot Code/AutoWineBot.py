# Funciones
import PySimpleGUI as sg
import io
from PIL import Image, ImageTk
import speech_recognition as SRG
import time
import random
import numpy as np
import pandas as pd
import webbrowser
import string
import unicodedata
from pyswip import Prolog
prolog=Prolog()
prolog.consult("WineBot.pl")


st = SRG.Recognizer()

#-----------------------------------------------------------------------------------------------------------------#
def lista_unica_string(tipos,D='Y'):
    lista = []
    a = str()
    for i in tipos:
        lista.append(i[D].replace('_',' ').capitalize())
        tipos = np.array(lista)
        tipos = np.unique(tipos)
    for i in tipos:
        a += '\t - ' + i +'\n'

    return a

def lista_unica(tipos,D='Y', sep = False):
    if sep:
        disueltas = []
        for i in tipos:
            s = preparar_texto(i)
            for j in s:
                disueltas.append(j)
        disueltas = np.array(disueltas)
        disueltas = np.unique(disueltas)
        com = disueltas.tolist()
    else:
        lista2 = []
        for i in tipos:
            lista2.append(i[D].replace('_',' '))
        tipos = np.array(lista2)
        tipos = np.unique(tipos)
        com = tipos.tolist()
    return com

def lista(tipos,D='Y'):
    lista2 = []
    for i in tipos:
        lista2.append(i[D].replace('_',' '))
    return lista2

def input_to_prolog(x):
    if x == 'no':
        x = x.capitalize()
    else:
        x = x.lower()
        x = x.replace(' ','_')

    return x

def analizar_respuestas(respuestas):
    cont = -1
    for i in respuestas:
        cont += 1
        if i == 'No':
            respuestas[cont] += str(cont)
        else:
            respuestas[cont] = respuestas[cont]
    return respuestas


#---------------------------------------------------------------------#

tipos_vino =lista_unica(list(prolog.query('tipo(X,Y)')),'X')
tipos_uva = lista_unica(list(prolog.query('tipo(X,Y)')),'Y')
tipos_comida = lista_unica(list(prolog.query('maridaje(X,Y)')),'Y')
tipos_aroma = lista_unica(list(prolog.query('aroma(X,Y)')),'Y')
tipos_sabor = lista_unica(list(prolog.query('sabor(X,Y)')),'Y')
tipos_ocasion = lista_unica(list(prolog.query('ocasion(X,Y)')),'Y')
tipos_tipos = [tipos_vino, tipos_uva,tipos_comida,tipos_aroma,tipos_sabor,tipos_ocasion]

#-----------------------------------------------------------------------------------------------------------------#
def Recomendar():
    ranv = random.choices(Vinos, k=3)
    col1 = [[sg.Text(ranv[0].capitalize(), font=('Elephant', 25))],
                    [sg.Text(texti, auto_size_text=True, size=(35, 10), font=('Calibri', 14)),
                     sg.Image(data=get_img_data(ranv[0] + '.png', maxsize=(500, 500), first=True))]]
    col2 = [[sg.Text(ranv[1].capitalize(), font=('Bauhaus 93', 25))],
            [sg.Text(texti, auto_size_text=True, size=(35, 10), font=('Calibri', 14)),
             sg.Image(data=get_img_data(ranv[1] + '.png', maxsize=(500, 500), first=True))]]
    col3 = [[sg.Text(ranv[2].capitalize(), font=('Impact', 25))],
            [sg.Text(texti, auto_size_text=True, size=(35, 10), font=('Calibri', 14)),
             sg.Image(data=get_img_data(ranv[2] + '.png', maxsize=(500, 500), first=True))]]
    sg.theme('DarkTeal9')
    layout = [[sg.Column(col1, element_justification='center'), sg.Column(col2, element_justification='center'),
               sg.Column(col3, element_justification='center')],
              [sg.Button('', key='Exit', image_data=get_img_data('ImgV/exit1.png', maxsize=(80, 80), first=True),
                         button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                         pad=(0, 0))]] #[sg.Button('Exit')]]
    window2 = sg.Window('Mi recomendación de vinos es:', layout)
    event2, values2 = window2.read()
    # print(event2, values2)
    if event2 in (None, 'Exit'):
        window2.close()


#-----------------------------------------------------------------------------------------------------------------#

def Pregunta(pr1, pr2, a, p, modo):
    window['-OUTPUT-'].update('Pregunta ' + p + '\n Respuestas:\n' + a + '\t - No')
    window['-IN-'].update('')
    event = None
    while event != 'Submit':          # lee la respuesta
        event, values = window.read()

    x = values['-IN-'].lower()  #guarda respuesta
    tipos = list(prolog.query(f"{pr1}(X,Y)"))
    com = lista_unica(tipos)  # lista de todas las ocasiones para comparar con la respuesta
    if x == 'no':
        event = None
        tipos = list(prolog.query(f"{pr2}(X,Y)"))
        a = lista_unica_string(tipos) # String de todos los maridajes
        respuestas.append(input_to_prolog(x))
    elif x in com: # Respuesta pregunta 3
        x = input_to_prolog(x)
        event = None
        if modo == 'MA':
            filtrado = list(prolog.query(f"filtradoMA({respuestas[0]},{x},Y)"))
        else:
            filtrado = list(prolog.query(f"filtradoAS({respuestas[0]},{respuestas[1]},{x},Y)"))
        a = lista_unica_string(filtrado)
        respuestas.append(input_to_prolog(x))
#         print(a)
    else:
        # print('No tengo esa categoría, intenta de nuevo')
        values['-IN-'] = None
        window['-OUTPUT-'].update('No tengo esa categoría, intenta de nuevo')
        window['-IN-'].update('')
        a = Pregunta(pr1, pr2, a, p, modo)

    return a

#-----------------------------------------------------------------------------------------------------------------#
def Pregunta1():
#     if values['-IN-'] == 'No':
    event = None
    # Imprime las ocasiones existentes
    tipos = list(prolog.query(f"ocasion(X,Y)")) # Tipos de ocasiones para imprimir al usuario en la pregunta 1
    a = lista_unica_string(tipos)
    window['-OUTPUT-'].update('Pregunta 1\n ¿Lo quieres para alguna ocasión en especial? Puedo sugerirte vino que te acompañan bien en este tipo de ocaciones\n Respuestas: \n' + a + '\t - No')
    window['-IN-'].update('')

    while event != 'Submit':          # lee la respuesta
        event, values = window.read()

    x = values['-IN-'].lower()  #guarda respuesta
    tipos = list(prolog.query(f"ocasion(X,Y)"))
    com = lista_unica(tipos)  # lista de todas las ocasiones para comparar con la respuesta
    if x == 'no':
        event = None
        tipos = list(prolog.query(f"maridaje(X,Y)"))
        a = lista_unica_string(tipos) # String de todos los maridajes
        respuestas.append(input_to_prolog(x))
#         window['-OUTPUT-'].update(a)
    elif x in com: # Respuesta pregunta 3
        x = input_to_prolog(x)
        event = None
        filtrado_OM = list(prolog.query(f"filtradoOM({x},Y)"))
        a = lista_unica_string(filtrado_OM)
        respuestas.append(input_to_prolog(x))
#         window['-OUTPUT-'].update(a)
    else:
        tipos, a = None, None
        # print('No tengo esa categoría, intenta de nuevo')
        values['-IN-'] = None
        window['-OUTPUT-'].update('No tengo esa categoría, intenta de nuevo')
        window['-IN-'].update('')
        a = Pregunta1()
    return a

#-----------------------------------------------------------------------------------------------------------------#

def encuentra_vino(a, respuestas):
    event = None
    analizar_respuestas(respuestas)
    A, B, C = respuestas
    window['-OUTPUT-'].update('Pregunta 4\n ¿Tiene algún sabor en mente para su vino?\n Respuestas:\n' + a + '\t - No')
    window['-IN-'].update('')

    while event != 'Submit':          # lee la respuesta
        event, values = window.read()

    x = values['-IN-'].lower()  #guarda respuesta
    tipos = list(prolog.query(f"sabor(X,Y)"))
    com = lista_unica(tipos)  # lista de todas las ocasiones para comparar con la respuesta
    if x == 'no':
        event = None
        filtrado = list(prolog.query(f"filtrado({A},{B},{C},{x.capitalize()},Y)"))
        a = lista_unica_string(filtrado) # String de todos los maridajes
        window['-OUTPUT-'].update('El vino que queda mejor con las elecciones hechas es: \n' + a )
        window['-IN-'].update('')
        respuestas.append(input_to_prolog(x))
        vino = lista_unica(filtrado)
#         print(a)
    elif x in com: # Respuesta pregunta 3
        x = input_to_prolog(x)
        event = None
        filtrado = list(prolog.query(f"filtrado({A},{B},{C},{x},Y)"))
        a = lista_unica_string(filtrado)
        window['-OUTPUT-'].update('El vino que queda mejor con las elecciones hechas es: \n' + a )
        window['-IN-'].update('')
        respuestas.append(input_to_prolog(x))
        vino = lista_unica(filtrado)
#         print(a)
    else:
        # print('No tengo esa categoría, intenta de nuevo')
        values['-IN-'] = None
        window['-OUTPUT-'].update('No tengo esa categoría, intenta de nuevo')
        window['-IN-'].update('')
        a, vino = encuentra_vino(a, respuestas)

    return a, vino

#-----------------------------------------------------------------------------------------------------------------#

def definir_vinos_info(vinos):
    # print(vinos)
    vino = random.sample(vinos, 1)
    # print(vino)
    uvas = list(prolog.query(f"tipo({input_to_prolog(vino[0])},Y)"))
    uva = lista_unica(uvas)
    uva = random.sample(uva, 3)
    link_uva1 = list(prolog.query(f"link({input_to_prolog(uva[0])},X,Y)"))
    links_uva1, categorias_uva1 = lista(link_uva1), lista(link_uva1,'X')
    link_uva2 = list(prolog.query(f"link({input_to_prolog(uva[1])},X,Y)"))
    links_uva2, categorias_uva2 = lista(link_uva2), lista(link_uva2,'X')
    link_uva3 = list(prolog.query(f"link({input_to_prolog(uva[2])},X,Y)"))
    links_uva3, categorias_uva3 = lista(link_uva3), lista(link_uva3,'X')
    descripcion1 = lista(list(prolog.query(f"descripcion({input_to_prolog(uva[0])},Y)")))
    descripcion2 = lista(list(prolog.query(f"descripcion({input_to_prolog(uva[1])},Y)")))
    descripcion3 = lista(list(prolog.query(f"descripcion({input_to_prolog(uva[2])},Y)")))
    return uva, links_uva1, categorias_uva1, links_uva2, categorias_uva2, links_uva3, categorias_uva3, descripcion1, descripcion2, descripcion3

def Recomendar(vinos):
    uva, luva1, cuva1, luva2, cuva2, luva3, cuva3, des1, des2, des3 = definir_vinos_info(vinos)
    col1 = [[sg.Text(uva[0].capitalize(), font=('Elephant', 25))],
                    [sg.Text(des1[0], auto_size_text=True, size=(35, 10), font=('Calibri', 14))],
                    [sg.Button(cuva1[0].capitalize(), enable_events=True, key='-LINK11-')],
                    [sg.Button(cuva1[1].capitalize(), enable_events=True, key='-LINK12-')],
                    [sg.Button(cuva1[2].capitalize(), enable_events=True, key='-LINK13-')]]
    col11 = [[sg.Image(data=get_img_data('ImgV/' + uva[0] + '.png', maxsize=(500, 500), first=True))]]
    col2 = [[sg.Text(uva[1].capitalize(), font=('Bauhaus 93', 25))],
                    [sg.Text(des2[0], auto_size_text=True, size=(35, 10), font=('Calibri', 14))],
                    [sg.Button(cuva2[0].capitalize(), enable_events=True, key='-LINK21-')],
                    [sg.Button(cuva2[1].capitalize(), enable_events=True, key='-LINK22-')],
                    [sg.Button(cuva2[2].capitalize(), enable_events=True, key='-LINK23-')]]
    col21 = [[sg.Image(data=get_img_data('ImgV/' + uva[1] + '.png', maxsize=(500, 500), first=True))]]
    col3 = [[sg.Text(uva[2].capitalize(), font=('Impact', 25))],
                    [sg.Text(des3[0], auto_size_text=True, size=(35, 10), font=('Calibri', 14))],
                    [sg.Button(cuva3[0].capitalize(), enable_events=True, key='-LINK31-')],
                    [sg.Button(cuva3[1].capitalize(), enable_events=True, key='-LINK32-')],
                    [sg.Button(cuva3[2].capitalize(), enable_events=True, key='-LINK33-')]]
    col31 = [[sg.Image(data=get_img_data('ImgV/' + uva[2] + '.png', maxsize=(500, 500), first=True))]]
    sg.theme('DarkTeal9')
    layout = [[sg.Column(col1, element_justification='center'), sg.Column(col11, element_justification='center'),
               sg.Column(col2, element_justification='center'), sg.Column(col21, element_justification='center'),
               sg.Column(col3, element_justification='center'), sg.Column(col31, element_justification='center')],
              [sg.Button('', key='Exit', image_data=get_img_data('ImgV/exit1.png', maxsize=(80, 80), first=True),
                         button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                         pad=(0, 0))]] #[sg.Button('Exit')]]
    window2 = sg.Window('Mi recomendación de vinos es:', layout, no_titlebar=True, grab_anywhere = True)
    while True:
        event2, values2 = window2.read()
        print(event2, values2)
        checar_botones(event2, luva1, luva2, luva3)

        if event2 in (None, 'Exit'):
            break
        event2,values2 = None, None

    window2.close()

def checar_botones(event2, luva1, luva2, luva3):
    print('checando')
    if event2 == '-LINK11-':
        webbrowser.open(luva1[0])
    if event2 == '-LINK12-':
        webbrowser.open(luva1[1])
    if event2 == '-LINK13-':
        webbrowser.open(luva1[2])
    if event2 == '-LINK21-':
        webbrowser.open(luva2[0])
    if event2 == '-LINK22-':
        webbrowser.open(luva2[1])
    if event2 == '-LINK23-':
        webbrowser.open(luva2[2])
    if event2 == '-LINK31-':
        webbrowser.open(luva3[0])
    if event2 == '-LINK32-':
        webbrowser.open(luva3[1])
    if event2 == '-LINK33-':
        webbrowser.open(luva3[2])


#-----------------------------------------------------------------------------------------------------------------#

def tableize(df):
    if not isinstance(df, pd.DataFrame):
        return
    df_columns = df.columns.tolist()
    max_len_in_lst = lambda lst: len(sorted(lst, reverse=True, key=len)[0])
    align_center = lambda st, sz: "{0}{1}{0}".format(" "*(1+(sz-len(st))//2), st)[:sz] if len(st) < sz else st
    align_right = lambda st, sz: "{0}{1} ".format(" "*(sz-len(st)-1), st) if len(st) < sz else st
    align_left = lambda st, sz: "{1}{0} ".format(" "*(sz-len(st)-1), st) if len(st) < sz else st
    max_col_len = max_len_in_lst(df_columns)
    max_val_len_for_col = dict([(col, max_len_in_lst(df.iloc[:,idx].astype('str'))) for idx, col in enumerate(df_columns)])
    col_sizes = dict([(col, 2 + max(max_val_len_for_col.get(col, 0), max_col_len)) for col in df_columns])
    build_hline = lambda row: ' '.join(['*' * col_sizes[col] for col in row]).join([' ', ' '])
    build_data = lambda row, align: " ".join([align(str(val), col_sizes[df_columns[idx]]) for idx, val in enumerate(row)]).join([' ', ' '])
    hline = build_hline(df_columns)
    out = [hline, build_data(df_columns, align_center), hline]
    for _, row in df.iterrows():
        out.append(build_data(row.tolist(), align_left))
    out.append(hline)
    return "\n".join(out)

def pad_dict_list(dict_list, padel):
    lmax = 0
    for lname in dict_list.keys():
        lmax = max(lmax, len(dict_list[lname]))
    for lname in dict_list.keys():
        ll = len(dict_list[lname])
        if  ll < lmax:
            dict_list[lname] += [padel] * (lmax - ll)
    return dict_list

#-----------------------------------------------------------------------------------------------------------------------#

def checar_frases(lista_frases,string):
    string = quitar_acentos(remover_puntuacion(string.lower()))
    vinos,uvas,comida,aromas,sabores,ocasiones = [],[],[],[],[],[]
    for frase in lista_frases[0]:
        if frase in string:
            vinos.append(frase)
    for frase in lista_frases[1]:
        if frase in string:
            uvas.append(frase)
    for frase in lista_frases[2]:
        if frase in string:
            comida.append(frase)
    for frase in lista_frases[3]:
        if frase in string:
            aromas.append(frase)
    for frase in lista_frases[4]:
        if frase in string:
            sabores.append(frase)
    for frase in lista_frases[5]:
        if frase in string:
            ocasiones.append(frase)
    encontradas = [vinos,uvas,comida,aromas,sabores,ocasiones]
    return encontradas

#---------------------------------------------------------------------------------------#
def selec_aleatorio(lista):
    try:
        uva = input_to_prolog(random.sample(lista[1],3)[0])
    except:
        uva = 'Uva'
    try:
        comida = input_to_prolog(random.sample(lista[2],1)[0])
    except:
        comida = 'Comida'
    try:
        aroma = input_to_prolog(random.sample(lista[3],1)[0])
    except:
        aroma = 'Aroma'
    try:
        sabor = input_to_prolog(random.sample(lista[4],1)[0])
    except:
        sabor = 'Sabor'
    try:
        ocasion = input_to_prolog(random.sample(lista[5],1)[0])
    except:
        ocasion = 'Ocasion'
    # print(uva,comida,aroma, sabor,ocasion)
    if lista[0]:
        decision = input_to_prolog(random.sample(lista[0],1)[0])
    else:
        decision = lista_unica(list(prolog.query(f'filtrado({ocasion},{comida},{aroma},{sabor}, Y)')))

    if not decision:
        decision = lista_unica(list(prolog.query(f'filtrado(A,{comida},B,C, Y)')))
        window['-OUTPUT-'].update('Las características solicitadas no parecen estar coincidiendo del todo bien con algun vino en mi lista, basados en sus gustos culinarios yo le recomendaría el siguiente vino:\n')

    return decision

#-------------------------------------------------------------------------------------------------------------#

def quitar_acentos(string):
    acentos = set(map(unicodedata.lookup, ('COMBINING ACUTE ACCENT', 'COMBINING GRAVE ACCENT', 'COMBINING TILDE')))
    chars = [c for c in unicodedata.normalize('NFD', string) if c not in acentos]
    return unicodedata.normalize('NFC', ''.join(chars))
def remover_puntuacion(entrada):
    out_string = ""
    for i in entrada:
        if i not in string.punctuation:
            out_string += i
    return out_string
def preparar_texto(entrada):
    temp_string = entrada.lower()
    temp_string = remover_puntuacion(temp_string)
    temp_string = quitar_acentos(temp_string)
    lista_salida = temp_string.split()
    return lista_salida

def encontrar_en_lista(lista_uno, lista_dos):
    encontradas = []
    for elemento in lista_uno:
        if elemento in lista_dos:
            encontradas.append(elemento)
    return encontradas

def escuchar_mensaje(w=False):
    texto_salida_audio = None
    mensaje = None
    with SRG.Microphone() as s:
        window['Micro'].update(image_data=get_img_data('ImgV/microgreen.png', maxsize=(100, 100), first=True))
        # print(chr(27)+"[1;31m"+'Estoy escuchando...')
        entrada_audio = st.record(s, duration=8)
        # sys.stdout.write("\033[F")
        try:
            # print(chr(27)+"[1;31m"+"Procesando...")
            texto_salida_audio = st.recognize_google(entrada_audio,language="es")
            # print(texto_salida_audio)
            # print(chr(27)+"[1;31m"+"Reconocido.")
            window['Micro'].update(image_data=get_img_data('ImgV/microfonored.png', maxsize=(100, 100), first=True))
            window['-OUTPUT-'].update("Para empezar escribe: inicio\n O da clic DOS veces al microfono.")
            if w:
                mensaje = texto_salida_audio
            else:
                mensaje = preparar_texto(texto_salida_audio)
        except:
            print(chr(27)+"[1;31m"+"No he podido escucharte, intenta de nuevo")
            # window['-OUTPUT-'].update("No he podido escucharte, intenta de nuevo u otra opc")
            window['Micro'].update(image_data=get_img_data('ImgV/microfonored.png', maxsize=(100, 100), first=True))
            mensaje = escuchar_mensaje(True)
    return mensaje

#-------------------------------------------------------------------------------------------------------------#

def get_img_data(f, maxsize=(1200, 850), first=False):
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)
#-------------------------------------------------------------------------------------------------------------#


filename = "ImgV/microfonored.png"
sg.theme('DarkTeal9')

layout = [
    [sg.Text('WineBot', size=(25, 1), justification='center', font=("Elephant", 30), text_color='IndianRed3')],
    [sg.Button('', key='Micro', image_data=get_img_data(filename, maxsize=(100, 100), first=True),
               button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0, pad=(310, 10))],
    [sg.Input('', key='-IN-', enable_events=True, size=(60, 1), pad=(40, 1),font=("Monaco", 12))],
    [sg.Text('Para empezar escribe: inicio\n O da clic DOS veces al microfono.',size=(70, 20), key='-OUTPUT-',font=("Monaco", 12))],
    [sg.Submit(), sg.Cancel()],
    [sg.Button('', key='Exit', image_data=get_img_data('ImgV/exit1.png', maxsize=(50, 50), first=True),
               button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
               pad=(0, 0))]]  # [sg.Button('Exit')]]

window = sg.Window('WineBot', layout, no_titlebar=True, alpha_channel=.95, grab_anywhere=True)
activate = False

p2 = '2\n ¿Acompañara su vino con algún tipo de alimento en especial?'
p3 = '3\n ¿Tiene algún aroma en mente para su vino?'
p4 = '4\n ¿Tiene algún sabor en mente para su vino?'


while True:
    event, values = window.read()

    # print(event, values)

    if event in (None, 'Exit'):
        break

    if activate == True:
        st = SRG.Recognizer()
        escuchado=escuchar_mensaje(True)
        window['Micro'].update(image_data=get_img_data('ImgV/microfonored.png', maxsize=(100, 100), first=True))
        chec_vinos = checar_frases(tipos_tipos,escuchado)
        checar = selec_aleatorio(chec_vinos)
        if type(checar) == str:
            checar = [checar]
        Recomendar(checar)
        # print(escuchado,'\n', chec_vinos,'\n',checar)
        activate = False
        event = None


    # Empezar el experto guiado
    if values['-IN-'] in ['Inicio', 'inicio']:
        event = None
        window['-IN-'].update('')
        respuestas = []
        # Imprime los tipos de vinos haciendo la pregunta cero ¿conoces?
        tipos = list(prolog.query(f"tipo(X,Y)"))
        a = lista_unica_string(tipos,'X')
        window['-OUTPUT-'].update('Pregunta 0\n ¿De la siguiente lista conoces algún tipo de vino?\n Lista:\n' + a +'Respuestas:\n - Si \n - No \n ' )

        while event != 'Submit':
            event, values = window.read()

        # En el caso de que no conozca ninguno de la lista
        if values['-IN-'] in ['No', 'no']:
            event = None
            a = Pregunta1()
            # print(respuestas)
            b = Pregunta('maridaje', 'aroma', a, p2, 'MA')
            # print(respuestas)
            c = Pregunta('aroma', 'sabor', b, p3, 'AS')
            # print(respuestas)
            d, vinos = encuentra_vino(c, respuestas)
            # print(respuestas)
            # print(vinos)
            Recomendar(vinos)
            window['-OUTPUT-'].update('Para volver a empezar escribe: inicio')
        elif values['-IN-'] in ['Si', 'si']:
            window['-IN-'].update('')
            event = None
            tipos = list(prolog.query(f"tipo(X,Y)"))
            a = lista_unica_string(tipos,'X')
            window['-OUTPUT-'].update('Indicame el vino que apeteces.\n Respuestas:\n' + a)
            com = lista_unica(tipos,'X')

            while event != 'Submit':
                event, values = window.read()

            if values['-IN-'] in com:
                event = None
                window['-IN-'].update('')
                Y = input_to_prolog(values['-IN-'])
                # print(Y)
                filtrado = list(prolog.query(f"filtrado(A,B,C,D,{Y})"))
                a = lista_unica(filtrado, 'A')
                b = lista_unica(filtrado, 'B')
                c = lista_unica(filtrado, 'C')
                d = lista_unica(filtrado, 'D')
                Data = {'Ocasión':a,
                        'Maridaje':b,
                        'Aroma':c,
                        'Sabor':d}

                Data = pad_dict_list(Data, ' ')
                Data = pd.DataFrame(Data)
                # print(Data)
                window['-OUTPUT-'].update('Este tipo de vino que elegiste se acompaña bien en los siguientes escenarios.\n'
                                          + tableize(Data) +
                                            '\n ¿Te agrada? ¿Quieres que te recomiende tipos de uva de esta categoría?\nRespuestas: \n - Si \n - No')

                while event != 'Submit':
                    event, values = window.read()

                if values['-IN-'] in ['Si', 'si']:
                    event = None
                    window['-IN-'].update('')
                    Recomendar([Y])
                    window['-OUTPUT-'].update('Para volver a empezar escribe: inicio')
                elif values['-IN-'] in ['No', 'no']:
                    event = None
                    a = Pregunta1()
                    # print(respuestas)
                    b = Pregunta('maridaje', 'aroma', a, p2, 'MA')
                    # print(respuestas)
                    c = Pregunta('aroma', 'sabor', b, p3, 'AS')
                    # print(respuestas)
                    d, vinos = encuentra_vino(c, respuestas)
                    # print(respuestas)
                    Recomendar(vinos)
                    window['-OUTPUT-'].update('Para volver a empezar escribe: inicio')
                else:
                    window['-IN-'].update('inicio ')
                    window['-OUTPUT-'].update('')

            else:
                    window['-IN-'].update('inicio ')
                    window['-OUTPUT-'].update('')

        else:
            window['-IN-'].update('inicio ')
            window['-OUTPUT-'].update('')


    if event == 'Micro':
        window['Micro'].update(image_data=get_img_data('ImgV/microgreen.png', maxsize=(100, 100), first=True))
        activate = True
    else:
        print('No Event Micro')
        # window['Micro'].update(image_data=get_img_data('microfonored.png', maxsize=(100, 100), first=True))
# Close
window.close()
