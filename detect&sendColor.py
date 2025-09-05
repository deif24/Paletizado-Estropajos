import cv2
import numpy as np
import keyboard
import mss
import threading
import socket
import time

# Definir los rangos de colores en HSV
color_ranges = {
    "Rojo": [(0, 120, 70), (10, 255, 255)],  # Rojo (primer rango)
    "Rojo2": [(170, 120, 70), (180, 255, 255)],  # Rojo (segundo rango)
    "Verde": [(40, 40, 40), (80, 255, 255)],  # Verde
    "Azul": [(90, 50, 50), (130, 255, 255)],  # Azul
    "Amarillo": [(20, 100, 100), (30, 255, 255)],  # Amarillo
    "Naranja": [(10, 100, 100), (20, 255, 255)]  # Naranja
}

# Variables globales para capturar imagen de pantalla
captura_img = None
dominant_color = None
captura_lock = threading.Lock()
stop_event = threading.Event()

def capturar_pantalla(fps=30):
    global captura_img

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    roi = cv2.selectROI("Selecciona región", screenshot, fromCenter=False, showCrosshair=True)
    cv2.destroyAllWindows()

    left, top, width, height = roi
    monitor_roi = {"top": int(top), "left": int(left), "width": int(width), "height": int(height)}

    frame_delay = 1.0 / fps

    with mss.mss() as sct:
        while not stop_event.is_set():
            start_time = time.time()

            img = np.array(sct.grab(monitor_roi))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            with captura_lock:
                captura_img = img

            elapsed = time.time() - start_time
            sleep_time = frame_delay - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

def detectar_color_en_pantalla():
    global captura_img
    global dominant_color
    last_color = None
    while not stop_event.is_set():
        with captura_lock:
            if captura_img is not None:
                frame = captura_img.copy()
            else:
                continue

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        color_counts = {}
        dominant_color = None
        max_pixels = 0

        for color, (lower, upper) in color_ranges.items():
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)
            mask = cv2.inRange(hsv, lower, upper)
            pixel_count = cv2.countNonZero(mask)
            color_counts[color] = pixel_count

            if color == "Rojo":
                color_counts["Rojo"] += color_counts.pop("Rojo2", 0)

            if pixel_count > max_pixels:
                max_pixels = pixel_count
                dominant_color = color

        if dominant_color and last_color != dominant_color:
            last_color = dominant_color
            print(f"Color detectado: {dominant_color}")

        time.sleep(0.1)

def connect_to_server(host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        return client_socket
    except socket.error as e:
        print(f"Error al conectar con {host}:{port} -> {e}")
        return None
    
def connect_ABB():
    global dominant_color
    server_host, server_port = '127.0.0.1', 8000

    socket = connect_to_server(server_host, server_port)

    if not socket:
        print("No se pudo conectar a uno o ambos servidores. Saliendo...")
        exit(1)

    last_color = None
    while not stop_event.is_set():
        #colocar aqui si se recibe señal que mande el color
        respuesta = socket.recv(1024).decode()
        if respuesta=="Activa vision":
        #if dominant_color and last_color != dominant_color:
            last_color = dominant_color

            # Enviar color detectado
            socket.sendall(str(dominant_color).encode())
            #respuesta = socket.recv(1024).decode()         
            time.sleep(0.5)  # Pausa opcional
        
    socket.close()

def main(show=True):
    captura_thread = threading.Thread(target=capturar_pantalla, kwargs={'fps': 30})
    deteccion_thread = threading.Thread(target=detectar_color_en_pantalla)
    conection_thread = threading.Thread(target=connect_ABB)

    captura_thread.start()
    deteccion_thread.start()
    conection_thread.start()

    try:
        while not stop_event.is_set():
            if show:
                with captura_lock:
                    if captura_img is not None:
                        cv2.imshow("Deteccion de pantalla", captura_img)

                key = cv2.waitKey(1) & 0xFF
                if key == 27 or keyboard.is_pressed('esc'):
                    stop_event.set()
                    break

                time.sleep(0.01)
            else:
                if keyboard.is_pressed('esc'):
                    stop_event.set()
                    break
                time.sleep(0.1)
    except KeyboardInterrupt:
        stop_event.set()

    captura_thread.join()
    deteccion_thread.join()
    conection_thread.join()
    cv2.destroyAllWindows()
    print("Deteccion finalizada")

if __name__ == "__main__":
    main(show=True)