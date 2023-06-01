import cv2 
import tkinter as tk
from tkinter import messagebox

def textWithBackground(img, text, textPos, font, fontScale, textColor=(0,255,0), textThickness=1, bgColor=(0,0,0), pad_x=3, pad_y=3, bgOpacity=0.5):
    """
    Draws text with background, with  control transparency
    @param img:(mat) which you want to draw text
    @param text: (string) text you want draw
    @param textPos: tuple(x,y) position where you want to draw text
    @param font: fonts face, like FONT_HERSHEY_COMPLEX, FONT_HERSHEY_PLAIN etc.
    @param fontScale: (double) the size of text
    @param textColor: tuple(BGR) the color of text
    @param textThickness:(int) fonts weight
    @param bgColor: tuple(BGR), the color of background
    @param pad_x: int(pixels)  padding of in x direction
    @param pad_y: int(pixels) controls transparency of text background 
    @return: img(mat) with draw with background
    """
    (t_w, t_h), _= cv2.getTextSize(text, font, fontScale, textThickness)
    x, y = textPos
    overlay = img.copy()
    cv2.rectangle(overlay, (x-pad_x, y+ pad_y), (x+t_w+pad_x, y-t_h-pad_y), bgColor,-1)
    new_img = cv2.addWeighted(overlay, bgOpacity, img, 1 - bgOpacity, 0)
    cv2.putText(new_img,text, textPos,font, fontScale, textColor,textThickness )
    img = new_img

    return img

def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=2,
                        width=20,
                        font=('Helvetica bold', 20)
                    )

    return button

def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label

def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label

def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=2,
                       width=15, font=("Arial", 32))
    return inputtxt

def msg_box(title, description):
    messagebox.showinfo(title, description)
