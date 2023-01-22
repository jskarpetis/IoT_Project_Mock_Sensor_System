import cv2
from PIL import Image
import sys
import asyncio
import os
from model import CSRNet
from predictor import make_prediction
import requests
import base64
import numpy


import numpy
import json

# Contains Camera Id - With maximum number of people in the area
camera_base_set = {'camera-id-101392U': 100}


async def image_handler(model, image_name):

    # All of this is for one camera
    data_dictionary = {}
    model_prediction = make_prediction(model, image_to_predict=str(image_name))
    maximum_people_count = camera_base_set['camera-id-101392U']

    data = {
        "camera_id": 'camera-id-101392U',
        "image_bytes": 'None',
        "density": numpy.round(float(model_prediction / maximum_people_count * 100), 1)
    }

    data_dictionary['camera-id-101392U'] = data

    await make_request(data_dictionary, 'camera-id-101392U')

# Input is a dictionary with a specific key to upload


async def make_request(generated_dictionary_data, key):
    endpoint_url = "https://hffi70fkl9.execute-api.eu-north-1.amazonaws.com/dev/upload-data-to-s3"

    generated_dictionary_data = json.dumps(generated_dictionary_data[key])
    response = requests.post(endpoint_url, data=generated_dictionary_data)
    print({
        "message": response.json(),
        "status_code": response.status_code
    })


# Main Runner Task
async def async_task_handler(model, task_seconds):

    image_name_list = list_images()
    image_counter = 0
    try:
        while (True):
            await image_handler(model, image_name_list[image_counter])
            image_counter = image_counter + 1
            print('\n', "Cycle Complete", '\n')
            await asyncio.sleep(task_seconds)
    except KeyboardInterrupt:
        pass
    return 'Task has been completed'


def list_images():
    image_name_list = {}
    folder_dir = 'C:/Users/johns/Desktop/University/IoT/IoT_Project_Mock_Sensor_System/data/'
    for image in os.listdir(folder_dir):
        image_number_identifier = ''
        for character in str(image):
            if character.isdigit():
                image_number_identifier += character
        image_name_list[image] = int(image_number_identifier)

    sorted_dictionary = {key: val for key, val in sorted(
        image_name_list.items(), key=lambda element: element[1])}

    return list(sorted_dictionary.keys())


if __name__ == "__main__":
    model = CSRNet()
    # Setting Event Loop
    event = asyncio.get_event_loop()
    try:
        print('Camera Task Started')
        task_object_loop = event.create_task(
            async_task_handler(model, task_seconds=10))
        event.run_until_complete(task_object_loop)
    finally:
        event.close()
    print("Task status: {}".format(task_object_loop.result()))

    # print(list_images())
