import cv2
from PIL import Image
import sys
import asyncio
import os
import requests
import base64
import json



def POST_image():
    
    # print(sys.getsizeof(frame.tolist()))
    
    endpoint_url = "https://hffi70fkl9.execute-api.eu-north-1.amazonaws.com/dev/upload-data-to-s3"

    data = open(os.getcwd() + '/images/current_image.jpg', 'rb').read()
    data = {
        "camera_id": "camera-id-101392U",
        "image_bytes": base64.b64encode(data).decode('utf8')
        }
    
    data_json = json.dumps(data)
    response = requests.post(endpoint_url, data=data_json)
    print({
            "message": response.json(),
            "status_code": response.status_code
        })



async def capture_photo(task_seconds, capture):
    images_path = os.getcwd() + '/images'
    
    try:
        while (True):
            frame = capture.read()
            print('Camera Picture Size in Bytes -> {}'.format(sys.getsizeof(frame)))
            # print(frame)
            image = Image.fromarray(frame.astype('uint8')).convert('RGB')
            image.save(images_path + '/current_image.jpg')
            
            # Sending Image To The Server
            POST_image()
            break
            await asyncio.sleep(task_seconds)
            
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        capture.release()   
    return 'Task has been completed'

if __name__ == "__main__":

    
    camera_port = 0
    # Open the device at the ID 0 
    capture = cv2.VideoCapture(camera_port)

     #Check whether user selected camera is opened successfully.

    if not (capture.isOpened()):
        print("Could not open video device")
    
    else:
        #To set the resolution 
        capture.set(3, 640)
        capture.set(4, 480)

        # Setting Event Loop
        event = asyncio.get_event_loop()
        try:
            print('Camera Task Started')
            task_object_loop = event.create_task(capture_photo(task_seconds=5, capture=capture))
            event.run_until_complete(task_object_loop)
        finally:
            event.close()
        print("Task status: {}".format(task_object_loop.result()))
        

    
    
   
    
    
    
    
    
    
    
    # # if __name__ == '__main__':
    #     sample_event = asyncio.get_event_loop()
    #     try:
    #         print('Creation of tasks started')
    #         task_object_loop = sample_event.create_task(sample_task(task_seconds=3))
    #         sample_event.run_until_complete(task_object_loop)
    #     finally:
    #         sample_event.close()
    #     print("Task status: {}".format(task_object_loop.result()))