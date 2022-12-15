import cv2
from PIL import Image
import sys
import asyncio
import os
import requests
import base64
import numpy
import json


def dummy_data_generator():

    camera_list = ['camera-id-101392U',
                   'camera-id-438593U', 'camera-id-472395U']
    density_list = [x for x in range(0, 100, 5)]

    data_dictionary = {}

    for camera in camera_list:
        generated_data = {
            "camera_id": camera,
            "image_bytes": 'testing_bytes',
            "density": str(numpy.random.choice(density_list))
        }
        data_dictionary[camera] = generated_data

    return data_dictionary


async def POST_image():

    # data = open(os.getcwd() + '/images/current_image.jpg', 'rb').read()
    generated_dictionary_data = dummy_data_generator()

    # data = {
    #     # "image_bytes": base64.b64encode(data).decode('utf8')
    #     "image_bytes": "testing_bytes"
    # }

    for key in generated_dictionary_data.keys():
        await make_request(generated_dictionary_data, key)


async def make_request(generated_dictionary_data, key):
    endpoint_url = "https://hffi70fkl9.execute-api.eu-north-1.amazonaws.com/dev/upload-data-to-s3"

    generated_dictionary_data = json.dumps(generated_dictionary_data[key])
    response = requests.post(endpoint_url, data=generated_dictionary_data)
    print({
        "message": response.json(),
        "status_code": response.status_code
    })


async def async_task(task_seconds):

    try:
        while (True):
            # image = Image.fromarray(frame.astype('uint8')).convert('RGB')
            # image.save(images_path + '/current_image.jpg')

            # Sending Image To The Server
            await POST_image()
            print('\n', "Cycle Complete", '\n')
            await asyncio.sleep(task_seconds)

    except KeyboardInterrupt:
        pass
    return 'Task has been completed'

if __name__ == "__main__":

    # Setting Event Loop
    event = asyncio.get_event_loop()
    try:
        print('Camera Task Started')
        task_object_loop = event.create_task(
            async_task(task_seconds=10))
        event.run_until_complete(task_object_loop)
    finally:
        event.close()
    print("Task status: {}".format(task_object_loop.result()))
