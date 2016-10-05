import pygame
import pyaudio
import wave
import sys
import time
import glob
import contextlib
import lyric

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
width = 1300
height = 700
red = (255, 0, 0)
blue = (50, 205, 50)

def message_display(text,width,height,fontsize,colour = black):
    largeText = pygame.font.Font('freesansbold.ttf',fontsize)
    TextSurf, TextRect = text_objects(text, largeText, colour)
    TextRect = height,width 
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

    #time.sleep(2)

y1_start = 200
y1_end  = 260
y2_start = 270
y2_end = 320
x_start_play = 90
x_end_play = 145
x_start_pause = 90
x_end_pause = 145
x_start_stop = 20
x_end_stop = 85
x_start_record = 150
x_end_record = 210

songs = {}
allsongs = {}
def displaylist(songs):
    fileOfsongs = glob.glob("*.wav")
    fileOfkaraokes = glob.glob("*_karaoke.wav")
    fileOfsongs = sorted(set(fileOfsongs))
    i = 0
    j = 0
    k = 330
    for song in fileOfsongs :
       allsongs[j + 1] = song
       j += 1
       if song not in fileOfkaraokes:
           songs[i + 1] = song
           print ("%s %s"%(i+1,song));
           #message_display("%s" %(i+1),k,3,15)
	   #message_display("\t",k,3)
           #message_display("      %s" %song,k,6,15)
           i += 1
           k += 15

displaylist(songs)
FILE_NAME = int(input("enter song to play"))
file_name =  "recorded_" + songs[FILE_NAME].replace(".mp3",".wav")


def songlength(fname = songs[FILE_NAME].replace(".mp3",".wav")):
    with contextlib.closing(wave.open(fname,'r')) as f:
         frames = f.getnframes()
         rate = f.getframerate()
         duration = frames / float(rate)

    return duration

def showlyrics(file_name):

     fileOflyrics = glob.glob("*.txt")
     file_name = file_name.replace(".wav",".txt")
     i = 15
     j =  15
     if( file_name in fileOflyrics) :
         file = open(file_name)	
         for line in file :
             line = line.replace('\n','')
             if( i > 680):
                message_display(line, j, 815, 18)
                j += 18 
             else :
                message_display(line, i, 250, 18)
         #message_display("\n",i)
             i += 18

     else :
         lyrics(file_name.replace(".txt",""))

	



def Play_button(x, y,song):
    if x in range(x_start_play, x_end_play) and y in range(y1_start, y1_end):
        #showlyrics(songs[FILE_NAME])
        message_display("%s"%song,10,10,15)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()


def Pause_button(x, y):
     if x in range(x_start_pause, x_end_pause) and y in range(y2_start, y2_end):
         pygame.mixer.music.pause()

def Stop_button(x, y):
    if x in (x_start_stop, x_end_stop) and y in range(y2_start, y2_end):
       pygame.mixer.music.stop()

def Record_button(x, y):
    if x in range(x_start_record, x_end_record) and y in range(y2_start, y2_end):
        karaoke = songs[FILE_NAME].replace(".wav","_karaoke.wav")
        pygame.mixer.music.stop()
        pygame.mixer.music.load(karaoke)
        pygame.mixer.music.play()
        if len(sys.argv) == 2:
            frames = recording(RECORD_SECONDS = int(sys.argv[1]))
        else :
            frames = recording()
        pygame.mixer.music.stop()
        save_recorded(frames,FILE_NAME)
        Play_button(x, y,file_name)


def recording(CHUNK = 1024, RATE = 44100, CHANNELS = 2 , FORMAT = pyaudio.paInt16, RECORD_SECONDS = songlength()):
    audio = pyaudio.PyAudio()
    stream = audio.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
    message_display("Recording..", 100, 15, 30, red)
#       time.sleep(2)
    pygame.display.update()
    clock.tick(15)
        #millisec = clock.get_time()
    if pygame.mouse.get_pos() :
       frames = [stream.read(CHUNK) for data in range(2, int(RATE / CHUNK * RECORD_SECONDS)) ]
       stream.stop_stream()
       stream.close()
       audio.terminate()
       return frames

def save_recorded(frames, FILE_NAME,CHUNK = 1024, RATE = 44100, CHANNELS = 2 , FORMAT = pyaudio.paInt16):
        audio = pyaudio.PyAudio()
        print(FILE_NAME)
        name =  "recorded_" + songs[FILE_NAME].replace(".mp3",".wav")
        if name in songs :
           file_name = name + '-1'
        else :
           file_name = name
        waveFile = wave.open(file_name, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        message_display("                    Done", 100, 15, 30, red)
                                                         
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Karaoke")
clock = pygame.time.Clock()
img = pygame.image.load('buttons.png')
image = pygame.image.load('music1.png')
screen.fill(white)
background = pygame.image.load('back1.png')
screen.blit(background,(0,200))
screen.blit(image,(30,20))
screen.blit(img, (5,190))
pygame.display.update()

def karaoke_player(FILE_NAME):
    exit = False
    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                x, y = pygame.mouse.get_pos()
                Play_button(x, y,songs[FILE_NAME])
                showlyrics(songs[FILE_NAME])
                Pause_button(x, y)
                Record_button(x, y)
                Stop_button(x, y)

karaoke_player(FILE_NAME)



