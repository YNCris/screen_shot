import threading, os, time, sys
from time import sleep
import wave
from pyaudio import PyAudio,paInt16
from PIL import ImageGrab
from moviepy.editor import ImageSequenceClip

#fileName = input('FileName: ') or 'demo'

fileName = 'H:\screen_shot'

os.system('del /F /S /Q '+fileName)
os.system('del '+'H:\\01.wav')
if not os.path.isdir(fileName):
    os.mkdir(fileName)
recording, imageList, recordTime, pic_count,my_buf = True, [], 0, 0, []


NUM_SAMPLES=2000
framerate=8000
channels=1
sampwidth=2
TIME=2

pa=PyAudio()
stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)

string_audio_data = stream.read(NUM_SAMPLES)

#record audio
def my_record():
    global my_buf, recording, string_audio_data
    
    count=0
    while recording:
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count+=1
        #print('.')
    
    #save_wave_file('H:\\' + '01.wav',my_buf)
    #stream.close()

def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

#record screen
def get_pictures():
    global recordTime, pic_count
    t = time.time()
    while recording:
        image = ImageGrab.grab()
        #image = image.resize((800,600))
        #imageName = os.path.join(fileName, '%s.jpg' % int(time.time() * 1e3))
        imageName = os.path.join(fileName, '%s.jpg' % long(pic_count))
        image.save(imageName)
        imageList.append(imageName)
        recordTime = time.time() - t
        pic_count = pic_count + 1


t = threading.Thread(target=get_pictures)
t.setDaemon(True)
t.start()

t_a = threading.Thread(target=my_record)
t_a.setDaemon(True)
t_a.start()

#print('Recording screen to %s.mp4, press Ctrl-C to stop' % fileName)

stopshot = 'N'

print('Recording screen to %s.mp4, stop or not? S/N' % fileName)
try:    
    while stopshot != 'S':
        stopshot = raw_input()
except:
    recording = False

p_fps = int(len(imageList) / recordTime)

clip = ImageSequenceClip(imageList[1:len(imageList)-1],
    fps=int(len(imageList) / recordTime))

print('length:%d' % len(imageList))
print('recordTime: %d' % recordTime)
print('fps:%d' % p_fps)

print('please waiting...')
clip.write_videofile('%s.mp4' % fileName)

print('save video successful!')
print('waiting save audio...')
save_wave_file('H:\\' + '01.wav',my_buf)
#stream.close()

print('save audio successful!')

print('delete screen shot picture? Y/N')
chose = raw_input('your chose:')
judge = 'Y'
if chose == judge:
    os.system('del /F /S /Q '+fileName)
