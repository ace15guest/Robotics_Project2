from jetbot import Robot
import traitlets
from IPython.display import display
from jetbot import Camera, bgr8_to_jpeg
import ipywidgets.widgets as widgets
import ipywidgets as widgets
from ipywidgets import *
from IPython.display import display, HTML
from uuid import uuid4
import time
import uuid
from IPython.display import Image
import subprocess
import os, os.path
from uuid import uuid1

controller = widgets.Controller(index=0)
jetbot = Robot()
camera = Camera.instance(width=224, height=224)
image = widgets.Image(format='jpeg', width=224, height=224)
left_link = traitlets.dlink((controller.axes[1], 'value'), (jetbot.left_motor, 'value'), transform=lambda x: -.3*x)
right_link = traitlets.dlink((controller.axes[0], 'value'), (jetbot.right_motor, 'value'), transform=lambda x: -.3*x)
camera_link = traitlets.dlink((camera, 'value'), (image, 'value'), transform=bgr8_to_jpeg)
# jetbot.left_motor.value = 0.1
# jetbot.right_motor.value = 0.1
display(controller)

snapshot_image = widgets.Image(format='jpeg', width=300, height=300)
subprocess.call(['mkdir', '-p', 'freesnapshots'])
subprocess.call(['mkdir', '-p', 'dataset/blocked'])

def save_freesnapshot(change):
    # save snapshot when button is pressed down
    if change['new']:
        file_path = 'freesnapshots/' + str(uuid.uuid1()) + '.jpg'

        # write snapshot to file (we use image value instead of camera because it's already in JPEG format)
        with open(file_path, 'wb') as f:
            f.write(image.value)

        # display snapshot that was saved
        snapshot_image.value = image.value


def save_blockedsnapshot(change):
    # save snapshot when button is pressed down
    if change['new']:
        file_path = 'dataset/blocked/' + str(uuid.uuid1()) + '.jpg'

        # write snapshot to file (we use image value instead of camera because it's already in JPEG format)
        with open(file_path, 'wb') as f:
            f.write(image.value)

        # display snapshot that was saved
        snapshot_image.value = image.value
#Controller for the game pad
controller.buttons[6].observe(save_freesnapshot, names='value')
controller.buttons[7].observe(save_blockedsnapshot, names='value')
