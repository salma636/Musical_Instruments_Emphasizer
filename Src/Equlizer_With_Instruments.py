from typing import Any
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
import sys, os, csv
#import threading
import numpy.fft as fft
import scipy
from scipy.interpolate import make_interp_spline
from PyQt5 import QtGui
import numpy as np
import pandas as pd
from PyQt5 import QtWidgets as qtw
import pyqtgraph as pg
from scipy.io import wavfile
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
from scipy import signal
from Music_Equlizer import Ui_MainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QPixmap
import wave
from PyQt5.QtWidgets import QFileDialog , QLabel
import contextlib
import sounddevice as sd
from threading import Thread


QMediaContent = QtMultimedia.QMediaContent
QMediaPlayer = QtMultimedia.QMediaPlayer
pauseCounter = False

class MainWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.pen6 = pg.mkPen(color=(0,206,209))
        self.pen4 = pg.mkPen(color=(0, 255, 0))
        self.pen3 = pg.mkPen(color=(255,255,0))
        self.pen1 = pg.mkPen(color=(255, 0, 0))
        self.ui.Open_file.triggered.connect(lambda: self.open_file())
        self.player = QMediaPlayer(self)
        self.playTimer = QtCore.QTimer()
        self.timer = QtCore.QTimer()

        # self.ui.label_6.clicked.connect(lambda: self.volumedown())
        # self.ui.label_7.clicked.connect(lambda: self.volumeup())
        self.instro_freq1 = []
        self.ui.Slider_for_piano_2.valueChanged.connect(lambda: self.equalize())
        self.ui.Slider_for_drums_2.valueChanged.connect(lambda: self.equalize())
        self.ui.Slider_for_all_instrument_2.valueChanged.connect(lambda: self.equalize())
        self.ui.Slider_for_piano_2.setMaximum(10)
        self.ui.Slider_for_piano_2.setMinimum(0)
        self.ui.Slider_for_drums_2.setMaximum(10)
        self.ui.Slider_for_drums_2.setMinimum(0)
        self.ui.Slider_for_all_instrument_2.setMaximum(10)
        self.ui.Slider_for_all_instrument_2.setMinimum(0)

        self.ui.spectrogram_buttom.clicked.connect(lambda: self.spectro())
        self.ui.Play_buttom.clicked.connect(lambda: self.pause())
        self.ui.button_high_volum.clicked.connect(lambda: self.volumeup())
        self.ui.button_low_volum.clicked.connect(lambda: self.volumedown())
        self.sample_rate = 44100
        self.frequency_guitar=15000
        self.wavetable_sizeg = self.frequency_guitar // 55 
        self.wavetableg = (2 * np.random.randint(0, 2, self.wavetable_sizeg) - 1).astype(np.float)

        self.frequency_guitar2=9000
        self.wavetable_sizeg2 = self.frequency_guitar2 // 55 
        self.wavetableg2 = (2 * np.random.randint(0, 2, self.wavetable_sizeg2) - 1).astype(np.float)
        self.frequency_guitar3=12000
        self.wavetable_sizeg3 = self.frequency_guitar3 // 55 
        self.wavetableg3 = (2 * np.random.randint(0, 2, self.wavetable_sizeg3) - 1).astype(np.float)
        self.frequency_guitar4=5000
        self.wavetable_sizeg4 = self.frequency_guitar4 // 55 
        self.wavetableg4 = (2 * np.random.randint(0, 2, self.wavetable_sizeg4) - 1).astype(np.float)
        self.frequency_guitar5=17000
        self.wavetable_sizeg5 = self.frequency_guitar5 // 55 
        self.wavetableg5 = (2 * np.random.randint(0, 2, self.wavetable_sizeg5) - 1).astype(np.float)
        self.frequency_guitar6=19000
        self.wavetable_sizeg6 = self.frequency_guitar4 // 55 
        self.wavetableg6 = (2 * np.random.randint(0, 2, self.wavetable_sizeg6) - 1).astype(np.float)
       
        self.ui.drums_buttom.clicked.connect(lambda: self.drumssound())
        self.ui.Slider_for_change_Drums.valueChanged.connect(lambda: self.changeofsound())
        self.ui.Slider_for_change_Drums.setValue(50)
        self.ui.buttom_for_guitar1.clicked.connect(lambda: sd.play(self.karplus_strong_giutar(2*self.wavetableg4, self.frequency_guitar), samplerate=self.frequency_guitar))
        self.ui.buttom_for_guitar2.clicked.connect(lambda: sd.play(self.karplus_strong_giutar(2*self.wavetableg2, self.frequency_guitar), samplerate=self.frequency_guitar))
        self.ui.buttom_for_guitar3.clicked.connect(lambda: sd.play(self.karplus_strong_giutar(2*self.wavetableg3, self.frequency_guitar), samplerate=self.frequency_guitar))
        self.ui.buttom_for_guitar4.clicked.connect(lambda: sd.play(self.karplus_strong_giutar(2*self.wavetableg, self.frequency_guitar), samplerate=self.frequency_guitar))
        self.ui.buttom_for_guitar5.clicked.connect(lambda: sd.play(self.karplus_strong_giutar(2*self.wavetableg5, self.frequency_guitar), samplerate=self.frequency_guitar))
        self.ui.buttom_for_guitar6.clicked.connect(lambda: sd.play(self.karplus_strong_giutar(2*self.wavetableg6, self.frequency_guitar), samplerate=self.frequency_guitar))
        self.ui.Slider_for_change_in_piano.valueChanged.connect(lambda: self.changeofsound1())
        self.ui.buttom_white_piano_1.clicked.connect(lambda: self.piano('H'))
        self.ui.buttom_white_piano_2.clicked.connect(lambda: self.piano('D'))
        self.ui.buttom_white_piano_3.clicked.connect(lambda: self.piano('J'))
        self.ui.buttom_white_piano_4.clicked.connect(lambda: self.piano('G'))
        self.ui.buttom_white_piano_5.clicked.connect(lambda: self.piano('A'))
        self.ui.buttom_white_piano_6.clicked.connect(lambda: self.piano('F'))
        self.ui.buttom_white_piano_7.clicked.connect(lambda: self.piano('Z'))
        self.ui.buttom_white_piano_8.clicked.connect(lambda: self.piano('O'))
        self.ui.buttom_white_piano_9.clicked.connect(lambda: self.piano('C'))
        self.ui.buttom_white_piano_10.clicked.connect(lambda: self.piano('E'))
        self.ui.buttom_white_piano_11.clicked.connect(lambda: self.piano('B'))
        self.ui.buttom_white_piano_12.clicked.connect(lambda: self.piano('Q'))
        self.ui.buttom_white_piano_13.clicked.connect(lambda: self.piano('L'))
        self.ui.buttom_white_piano_14.clicked.connect(lambda: self.piano('M'))
        self.ui.buttom_black_piano_1.clicked.connect(lambda: self.piano('a'))
        self.ui.buttom_black_piano_2.clicked.connect(lambda: self.piano('f'))
        self.ui.buttom_black_piano_3.clicked.connect(lambda: self.piano('z'))
        self.ui.buttom_black_piano_4.clicked.connect(lambda: self.piano('o'))
        self.ui.buttom_black_piano_5.clicked.connect(lambda: self.piano('c'))
        self.ui.buttom_black_piano_6.clicked.connect(lambda: self.piano('e'))
        self.ui.buttom_black_piano_7.clicked.connect(lambda: self.piano('b'))
        self.ui.buttom_black_piano_8.clicked.connect(lambda: self.piano('q'))
        self.ui.buttom_black_piano_9.clicked.connect(lambda: self.piano('l'))
        self.ui.buttom_black_piano_10.clicked.connect(lambda: self.piano('m'))
        self.ui.buttom_black_piano_11.clicked.connect(lambda: self.piano('g'))
        self.ui.buttom_black_piano_12.clicked.connect(lambda: self.piano('d'))
        self.ui.buttom_black_piano_13.clicked.connect(lambda: self.piano('j'))






    def open_file(self):
        self.ui.View_signal.clear()
        options = QFileDialog.Options()
        self.filename, _ = QFileDialog.getOpenFileName(None, "Open File", "*.WAV", options=options)
        with contextlib.closing(wave.open(self.filename, 'r')) as f:
            self.frames = f.getnframes()
            self.rate = f.getframerate()
            duration = self.frames / float(self.rate)
        self.samplingfrequency, self.dataa = wavfile.read(self.filename)
        url= QtCore.QUrl.fromLocalFile(self.filename)
        self.time = np.arange(0, duration, 1 / self.samplingfrequency)
        self.data_line1 = self.ui.View_signal.plot(self.time, self.dataa, pen=self.pen6)
        self.ui.View_signal.plotItem.setLimits(xMin=0, xMax=10, yMin=-7000, yMax=7000)
        self.idx1 = 0
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        self.specdata = self.dataa
        self.content = QMediaContent(url)
        self.player.setMedia(self.content)
        self.player.play()
        self.threadplayAudioFile()
    

    def threadplaysignal(self):
        t1=Thread(target=self.playsignal)
        t1.start()

    def playsignal(self):
        self.idx1 = 0
        self.playTimer.setInterval(10)
        self.playTimer.timeout.connect(self.update_plot_data)
        self.playTimer.start()

    def plot(self, time1, dataa1):
        self.x_axis = time1[:self.idx1]
        self.y_axis = dataa1[:self.idx1]
        self.value = 1
        self.playTimer.setInterval(10)
        self.playTimer.timeout.connect(self.update_plot_data)
        self.playTimer.start()

    def update_plot_data(self):
        self.x_axis = self.time[:self.idx1]
        self.y_axis = self.dataa[:self.idx1]
        self.idx1 += 5
        if (pauseCounter == False):
             if self.idx1 > len(self.time):
                 self.idx1 = 0
             if self.time[self.idx1] > 0.5:
                self.ui.View_signal.setLimits(xMin=min(self.x_axis, default=0), xMax=max(self.x_axis, default=0))  # disable paning over xlimits
             self.ui.View_signal.plotItem.setXRange(max(self.x_axis, default=0) - 0.5, max(self.x_axis, default=0))
             self.data_line1.setData(self.x_axis, self.y_axis)
             self.player.play()

    def threadplayAudioFile(self):
        t1=Thread(target=self.playAudioFile)
        t1.start()
        
    def playAudioFile(self):
        self.playsignal()
        url = QUrl.fromLocalFile(self.filename)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    def threadspectro(self):
        t1=Thread(target=self.spectro)
        t1.start()
    def spectro(self):
        self.ui.view_spectrogram.clear()
        plt.specgram(self.dataa, Fs=self.samplingfrequency)
        plt.savefig('spec_img.png', dpi=300, bbox_inches='tight')
        pixmap = QPixmap('spec_img.png').scaled(550, 250)
        self.ui.view_spectrogram.setPixmap(pixmap)
        
    # def threadspectro1(self):
    #     t1=Thread(target=self.spectro1)
    #     t1.start()
    # def spectro1(self):
    #     self.ui.view_spectrogram_new.clear()
    #     plt.specgram(self.dataa11, Fs=self.samplingfrequency)
    #     plt.savefig('spec_img.png', dpi=300, bbox_inches='tight')
    #     pixmap = QPixmap('spec_img.png').scaled(550, 250)
    #     self.ui.view_spectrogram_new.setPixmap(pixmap)
       

    def pause(self):
        global pauseCounter
        if pauseCounter == True:
            pauseCounter = False
            self.player.play()
        else:
            pauseCounter = True
            self.player.pause()

    
    def threadplayAudioFile_tab2(self,play):
        t1=Thread(target=self.playAudioFile_tab2(play))
        t1.start()
    def playAudioFile_tab2(self, play):
        url = QUrl.fromLocalFile(play)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
    def thread(self):
        t1=Thread(target=self.equalize)
        t1.start()
    def equalize(self):
        self.new_file_piano = -1
        self.signal = self.dataa[:]
        self.spectrum = np.fft.rfft(self.signal)
        self.freq = np.fft.rfftfreq(len(self.signal), d=1. / self.samplingfrequency)
        self.fft_spectrum_abs = np.abs(self.spectrum)

        for i, f in enumerate(self.freq):
            #piano
            if (f >= 1000) and (f <= 4000):  # (1)
                self.spectrum[i] *= self.ui.Slider_for_piano_2.value() /50
             #viola
            if (f >= 80) and (f <= 500):  # (2)
                 self.spectrum[i] *= self.ui.Slider_for_drums_2.value() / 50
           #guitar
            if (f >= 600) and (f <= 900):  # (3)
                 self.spectrum[i] *= self.ui.Slider_for_all_instrument_2.value() / 50
        self.fft_spectrum_abs = np.abs(self.spectrum)
        self.newSound = np.fft.irfft(self.spectrum)
        self.list = ["newsound.wav", "newsound1.wav", "newsound2.wav", "newsound3.wav","newsound4wav"]
        self.new_file_piano += 1
        scipy.io.wavfile.write(self.list[self.new_file_piano], self.samplingfrequency, self.newSound.astype(np.int16))
        self.ui.View_signal.clear()
        self.playAudioFile_tab2(self.list[self.new_file_piano])
        self.dataa11 = self.newSound
        self.spectro()
        self.data_line1 = self.ui.View_signal.plot(self.time, self.dataa, pen=self.pen6)
        self.playsignal()
    def volumeup(self):
        self.currentvolume = self.player.volume()
        print(self.currentvolume)
        self.player.setVolume(self.currentvolume + 20)
    def volumedown(self):
        self.currentvolume = self.player.volume()
        print(self.currentvolume)
        self.player.setVolume(self.currentvolume - 20)    

    def karplus_strong_drum(self,wavetable,n_samples, prob):
        #fs = 8000
      
        samples = []
        current_sample = 0
        previous_value = 0
        while len(samples) < n_samples:
             r = np.random.binomial(1, prob)
             sign = float(r == 1) * 2 - 1
             wavetable[current_sample] = sign * 0.5 * (wavetable[current_sample] + previous_value)
            # print(wavetable[self.current_sample])
             samples.append(wavetable[current_sample])
             previous_value = samples[-1]
             current_sample += 1
             current_sample = current_sample % wavetable.size
        return np.array(samples)
    
    
    def drumssound (self):
        samplingfrequency=50000
        wavetable_size =   samplingfrequency // 40 
        wavetable = np.ones(wavetable_size)
        sound = self.karplus_strong_drum (wavetable, 1 * samplingfrequency, self.changeofsound())
        sd.play(sound,samplingfrequency)

    def changeofsound(self):
        changeoffrequency =.01*(self.ui.Slider_for_change_Drums.value())
        return float ( changeoffrequency)



    def changeofsound1(self):
        changeoffrequency =44100+(self.ui.Slider_for_change_in_piano.value()*500)
        return float ( changeoffrequency)


    def get_wave(self,freq, duration=0.5):
        amplitude = 4096
        self.t = np.linspace(0, duration, int(self.changeofsound1() * duration))
        self.wave = amplitude * np.sin(2 * np.pi * freq * self.t)
        return self.wave    
    def get_piano_notes(self):
        octave = ['C', 'c', 'D', 'd', 'E','e', 'F', 'f', 'G', 'g', 'A', 'a', 'B','b','H','Z','z','J','j','O','o','Q','q','L','l','M','m']
        base_freq = 261.63
        note_freqs = {octave[i]:base_freq*pow(2, (i/12)) for i in range(len(octave))}
        note_freqs[''] = 0.0
        return note_freqs
      
    def get_piano_data(self,chords):
        note_freqs = self.get_piano_notes()
        chord_data = []
        for chord in chords:
             data = sum([self.get_wave(note_freqs[note]) for note in list(chord)])
             chord_data.append(data)
        chord_data = np.concatenate(chord_data, axis = 0)
        return chord_data.astype(np.int16)

    def piano(self,button):    
        data = self.get_piano_data(button)
        data = data * (16300/np.max(data))
        data = np.resize(data, (len(data),))
        sd.play(data,self.sample_rate,blocking=True)

    def karplus_strong_giutar(self,wavetable, n_samples):
        samples = []
        current_sample = 0
        previous_value = 0
        while len(samples) < n_samples:
              wavetable[current_sample] = 0.5 * (wavetable[current_sample] + previous_value)
              samples.append(wavetable[current_sample])
              previous_value = samples[-1]
              current_sample += 1
              current_sample = current_sample % wavetable.size
        return np.array(samples)
    
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())