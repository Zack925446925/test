# -*- encoding:utf-8 -*-
import sys
from google.cloud import vision
import io
import os

from google.cloud.vision import types
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "E:\01复硕正态\08项目\12google文字识别\My Project 44653-04ffef0e0ed6.json"
client = vision.ImageAnnotatorClient()

with io.open(r'E:\A_judge_pic\1.jpg', 'rb') as image_file:
    content = image_file.read()
image = types.Image(content=content)
response = client.text_detection(image=image)
labels = response.label_annotations
print(response)
print('***********************************')
print(labels)

