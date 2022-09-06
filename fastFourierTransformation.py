# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from  matplotlib.widgets import Button
from   PIL import Image
from scipy.misc import toimage
import Tkinter, tkFileDialog
import numpy as np
import numpy.ma as ma
import sys
import scipy.misc
import tkinter as tk


root = Tkinter.Tk()
root.geometry("200x200")


def mentes():

    # kép betöltése
    root = Tkinter.Tk()
    root.withdraw() #elrejti a gyökérablakot
    imgFile = tkFileDialog.askopenfilename()

    #numpy tömbbe beolvassa a képet
    imgPil = Image.open(imgFile).convert('LA')
    imgNp = np.array(imgPil.convert('L'))/255.

    # Fourier Transformáció
    fourImg  = np.fft.fft2(imgNp)
    fourShft = np.fft.fftshift(fourImg)
    fourLog  = np.log(np.abs(fourShft))
    plt.pause(.001)

    #toimage(fourLog).show()
    scipy.misc.imsave('FFT.jpg', fourLog)


def program():
    
    root = Tkinter.Tk()
    root.withdraw() #elrejti a gyökérablakot

    #első kép
    imgFile = tkFileDialog.askopenfilename()
    
    #második kép
    fftimg = tkFileDialog.askopenfilename()

    #ablak megnyitása
    winXSize = 18
    winYSize = 8
    winAspect = winXSize/winYSize
    fig = plt.figure(figsize=(winXSize, winYSize))
    fig.canvas.set_window_title('Fourier Transzformáció')

    #numpy tömbbe beolvassa a képet EREDETIT
    imgPil = Image.open(imgFile).convert('LA')
    imgNp = np.array(imgPil.convert('L'))/255.
    ySize, xSize = imgNp.shape   

    #numpy tömbbe beolvassa a képet FFT-T
    imgPilfft = Image.open(fftimg).convert('LA')
    imgNpfft = np.array(imgPilfft.convert('L'))/255.
    ySize, xSize = imgNpfft.shape

    #eredeti kép x,y tengely
    axOrig = fig.add_axes([.05, .2, .7/winAspect, .6])
    axOrig.set_title('Eredeti')
    imgplot = plt.imshow(imgPil, cmap='gray')

    #fft kép x,y tengely
    axfft = fig.add_axes([.30, .2, .8/winAspect, .6])
    axfft.set_title('FFT')
    imgplotfft = plt.imshow(imgPilfft, cmap='gray')

    # inverse fourier kép x,y tengely
    axFourInv = fig.add_axes([.60, .2, .75/winAspect, .6])
    axFourInv.set_title('Inverse Fourier')

    # Fourier Transformáció
    fourImg  = np.fft.fft2(imgNp)
    fourShft = np.fft.fftshift(fourImg)
    fourLog  = np.log(np.abs(fourShft))
    plt.pause(.001)

    imgasd = 0

    imgasd = np.where(imgNpfft != 0, 1, imgasd)

    #Szerkesztés
    editImg = (fourShft * imgasd) 
  
    # Inverse Fourier Transformáció
    fourIshft = np.fft.ifftshift(editImg)
    fourInv   = np.fft.ifft2(fourIshft)
    fourReal  = np.real(fourInv)
    invPlot = plt.imshow(fourReal, cmap='gray')


    def ment(valami):
        scipy.misc.imsave('IFFT.jpg', fourReal)

    def magment(valami):
        scipy.misc.imsave('EredetiFFT.jpg', fourLog)

    axnext2 = plt.axes([0.65, 0.05, 0.237, 0.04])
    bnext2 = Button(axnext2, 'Inverz mentes')
    bnext2.on_clicked(ment)

    axnext3 = plt.axes([0.65, 0.1, 0.237, 0.04])
    bnext3 = Button(axnext3, 'FFT mentes')
    bnext3.on_clicked(magment)

    # kép megjelenités
    plt.show()



A = Tkinter.Button(root, text ="FFT mentes", command = mentes)
A.pack()

B = Tkinter.Button(root, text ="FFT beolvasás", command = program)
B.pack()

C = Tkinter.Button(root, text ="Bezar", command = root.destroy)
C.pack()


root.mainloop()

