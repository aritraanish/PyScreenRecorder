import numpy as np
import cv2
from time import time
import d3dshot
from imutils.video import FPS
import sys


def record():
    d = d3dshot.create()
    d = d3dshot.create(capture_output="numpy")

    recording = []
    
    original_screen = d.screenshot()
    #screen = np.array(original_screen, dtype='uint8').reshape((original_screen.size[1], original_screen.size[0], 3))
    Fps = FPS().start()
    
    while True:
        original_screen = d.screenshot()
        screen = np.array(original_screen, dtype='uint8').reshape((original_screen.size[1], original_screen.size[0], 3))

        #screen = cv2.resize(screen, (835, 480))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        
        recording.append(screen)
        
        cv2.imshow('Capture', screen)
        Fps.update()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            Fps.stop()
            break

    cv2.destroyAllWindows()

    fps = Fps.fps()

    return fps, recording, original_screen

def write_file(fps, recording, original_screen):
    filename = str(time()) + '.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(filename, fourcc, fps, (original_screen.size[0], original_screen.size[1]))
    for i in range(len(recording)):
        out.write(recording[i])
    out.release()

    return filename


if __name__ == "__main__":
    fps, recording, original_screen = record()
    filename = write_file(fps, recording, original_screen)
    print(f'Your video fps is: {fps}')
    print(f'Your file has been created with the name: {filename}')

    