import threading, os, time, sys
from PIL import ImageGrab
from moviepy.editor import ImageSequenceClip


fileName = 'H:\screen_shot'

recording, imageList, recordTime = True, [], 0

print('pic_min:')
pic_min = long(raw_input())
print('pic_max:')
pic_max = long(raw_input())

recordTime = pic_max - pic_min

for i in range((pic_min),(pic_max)):
    imageName = fileName + '\\' + str(i) + '.jpg'
    imageList.append(imageName)

clip = ImageSequenceClip(imageList[1:len(imageList)-1], fps=20)
clip.write_videofile('%s.mp4' % fileName)
