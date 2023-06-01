#references:
#   https://github.com/google/mediapipe/blob/master/mediapipe/python/solutions/face_mesh.py
#   https://github.com/carlosfab/especializacao-visao-computacional/blob/main/projeto-02/main.py
#   https://www.youtube.com/watch?v=V9bzew8A1tc&t=1237s
#   https://www.youtube.com/watch?v=DNKAvDeqH_Y

# Importando os pacotes necessários
import sys, os
from imutils.video import VideoStream
import imutils
import cv2
import time
from threading import Thread
import playsound
import argparse
import utils
import numpy as np
from detector import BlinkDetector, QTD_CONSEC_FRAMES
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def confirmExit(self=None):
    if messagebox.askokcancel('Quit', 'Are you sure you want to exit?'):
        sys.exit()

# Função para tocar um alarme
def tocar_alarme(path):
    # Toca um som de alarme
    playsound.playsound(path)


class App:
    def __init__(self, cam_nr, alarme):
        self.cam_nr = cam_nr
        self.alarme = alarme
        self.main_window = tk.Tk()
        self.main_window.wm_title("Blink detector")
        self.main_window.geometry("1280x520")
        self.pTime = 0

        # Desenha a figura para que as animações funcionem
        self.y = [None] * 100
        self.x = np.arange(0,100)
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.li, = self.ax.plot(self.x, self.y)
        self.ax.set_xlabel("time [s]")
        self.ax.set_ylabel("f(t)")
        self.ax.set_xlim(0,100)
        self.ax.set_ylim(0.18,0.40)        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_window)  
        self.canvas.draw()

        # Inicializa o contador de quadros e uma variável booleana para
        # indicar se o alarme está tocando
        self.contador = 0
        self.alarme_on = False

        # Inicializa o preditor de marcos faciais
        self.detector = BlinkDetector(maxFaces=1)

        self.webcam_label = utils.get_img_label(self.main_window)
        self.webcam_label.place(x=30, y=30, width=640, height=420)
        self.add_webcam(self.webcam_label)
        self.canvas.get_tk_widget().place(x=720, y=130, width=520, height=320)

        # Este o metodo deveria fazer parte da classe
        self.main_window.bind('<Escape>', confirmExit)
        # Este não
        self.main_window.protocol('WM_DELETE_WINDOW', confirmExit)

    def start(self):
        self.main_window.mainloop()

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = VideoStream(self.cam_nr).start()

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        frame = self.cap.read()
        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

        img_ = self.process_img(img_)
        self.calc_fps()
        img_=utils.textWithBackground(img_, f'FPS: {round(self.fps,1)}', (50, 80), cv2.FONT_HERSHEY_PLAIN, 1.0, bgOpacity=0.9, textThickness=2)

        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil, master=self.main_window)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)

    def calc_fps(self):
        self.cTime = time.time()
        self.fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime        
    
    def process_img(self, frame):
        frame = imutils.resize(frame, width=700)

        # Determina os marcos faciais para a região do rosto, depois
        # converte os marcos faciais (coordenadas x, y) para um lista
        frame, faces = self.detector.findFaceMesh(frame)

        for face in faces:
            # Utiliza as coordenadas do olho para calcular o EAR para ambos os olhos
            is_blinking, ear = self.detector.is_blinking(face)

            # remove o primeiro elemento e adiciona o ear calculado
            self.y.pop(0)
            self.y.append(ear)

            # Atualiza o canvas imediatamente
#            plt.xlim([0, 100])
#            plt.ylim([0.15, 0.45])
            self.ax.relim()
            self.ax.autoscale_view(True, True, True)
            # define os novos dados
            self.li.set_ydata(self.y)
            self.fig.canvas.draw()
            time.sleep(0.01)

            # Verifica se está piscando,
            # e se estiver, incrementa o contador de quadros de piscar
            if is_blinking:
                self.contador += 1

                # se os olhos estavam fechados por um número suficiente de
                # quadros, então soa o alarme
                if self.contador >= QTD_CONSEC_FRAMES:
                    # se o alarme não está ligado, ligue-o
                    if not self.alarme_on:
                        self.alarme_on = True

                        # verifica se um arquivo de alarme foi fornecido,
                        # e se sim, inicia uma thread para ter o som do alarme
                        # tocado em segundo plano
                        if self.alarme !=0:
                            t = Thread(target=tocar_alarme, args=(os.path.abspath(os.path.join(os.getcwd(), "..\\arquivos\\alarm.wav")),))
                            t.deamon = True
                            t.start()

                    # desenha um alarme no quadro
                    frame=utils.textWithBackground(frame,"[ALERTA] SONOLENCIA!", (300, 95), cv2.FONT_HERSHEY_PLAIN, 1.0, textColor=(255,0,0), bgOpacity=0.9, textThickness=2)


            # caso contrário, o EAR não está abaixo do limiar de piscar,
            # então reseta o contador e o alarme
            else:
                self.contador  = 0
                self.alarme_on = False

            # desenha o EAR calculado no quadro para ajudar
            # com a depuração e ajuste dos limiares de EAR corretos
            # e contadores de quadros
            frame=utils.textWithBackground(frame,"EAR: {:.2f}".format(ear), (50, 110), cv2.FONT_HERSHEY_PLAIN, 1.0, bgOpacity=0.9, textThickness=2)
        
        return frame


def main():
    # Constroi o parser dos argumentos
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--alarme", type=int, default="1",
                help="Usar alarme sonoro?")
    ap.add_argument("-w", "--webcam", type=int, default=0,
                help="índice da webcam no sistema")
    args = vars(ap.parse_args()) 

    # Inicia a aplicacao
    app = App(args["webcam"], args["alarme"])
    app.start()    

    
if __name__ == '__main__':
    main()