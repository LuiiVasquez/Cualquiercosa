 # importar las librerias
import cv2
import numpy as np
# aqui le hace falta una libreria

# crear la variable para la captura de video
video = cv2.VideoCapture(-1)

# inicializar un contador
i = 0

# capturar el video
while True:
    ret, frame = video.read()
    if ret == False:
        break

    # creacion del color y texto
    color = (0,255,0)
    texto_estado = "Todo bien, todo correcto"


    # convertir el frame a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray = cv2.cvtColor(cv2.UMat(frame), cv2.COLOR_RGB2GRAY)
    #gray = cv2.cvtColor(np.float32(frame), cv2.COLOR_RGB2GRAY)
    # la imagen 20 se toma y se resta con las demas imagenes tomadas
    if i == 20:
        bgGray = gray
    if i > 20:
        dif = cv2.absdiff(gray, bgGray)
        # escala de grises a escala binaria (blanco y negro)
        _, th = cv2.threshold(dif, 40, 255, cv2.THRESH_BINARY)
        # buscar los contornos con opencv 3.4.4
        #_, cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # buscar los contornos con opencv 4
        cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # visualizar contornos (-1 para que todos los contornos sean dibujados), luego el color y grosos de linea
        #cv2.drawContours(frame, cnts, -1, (0, 0, 255), 2)
        #cv2.imshow('dif', dif)
        
        # area en pixeles de cada contorno
        for c in cnts:
            area = cv2.contourArea(c)
            # si el area es > 9000 se encierra en un cuadro
            if area > 5000:
                # cuatro datos, x y ancho y alto
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                color = (255,0,0)
                texto_estado = "Movimiento detectado"

            # Si dos personas estan muy cerca
            if area > 15000:
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)
                color = (0,0,255)
                texto_estado = "Distanciemiento violado"

            # Mostrar ventana de grises
            cv2.imshow('th', th)
    
    
    # mostrar texto
    cv2.putText(frame, texto_estado, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Mostrar el video en tiempo real
    cv2.imshow('frame', frame)
    # aumentar en 1 el contador
    i += 1
    # resionar q para salir
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break
# cerrar la captura de video    
video.release()
