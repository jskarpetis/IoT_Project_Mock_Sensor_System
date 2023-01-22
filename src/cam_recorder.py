import cv2

import os

print('\nOpenCv Version -> ', cv2.__version__, '\n')
print('\nOpenCv File -> ', cv2.__file__, '\n')

camera = cv2.VideoCapture('../video/crowd-footage.mp4')

if (camera.isOpened() == False):
    print('Error Opening Video File')

else:
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print("Error creating directory")

    time_interval = 5
    fps = int(camera.get(cv2.CAP_PROP_FPS))
    currentframe = 0

    while (True):

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        ret, frame = camera.read()
        if ret:
            if (currentframe % (fps * time_interval) == 0):
                name = '../data/frame' + str(currentframe) + '.jpg'
                print("Creating...")
                cv2.imwrite(name, frame)
            currentframe += 1
        else:
            print('breaking')
            break
    camera.release()
    cv2.destroyAllWindows()
