import bpy
import numpy as np
import math
import mathutils


SCENE_NAME = "Scene"
TOTAL_FRAMES = 100
FRAME_NUM = 10
ORIGIN_COORDS = np.array([5.0,5.0,15.0])
LABEL_MODIFIER = "near/training_"

Z_AXIS_RANGE = ORIGIN_COORDS[2]*2
Z_AXIS_STEP = Z_AXIS_RANGE/(TOTAL_FRAMES/FRAME_NUM)

cameraOrigin = np.copy(ORIGIN_COORDS)

camera = bpy.data.objects['Camera']
theta = 2 * math.pi/FRAME_NUM

bpy.data.scenes[SCENE_NAME].render.resolution_x = 800
bpy.data.scenes[SCENE_NAME].render.resolution_y = 600
bpy.data.scenes[SCENE_NAME].render.image_settings.file_format='JPEG'

print("Starting Camera Location:")
print(cameraOrigin)

def rotateCamera(scene):

    if scene.frame_current % TOTAL_FRAMES == 0:
        print("adjusting origin")
        print(ORIGIN_COORDS)
        cameraOrigin[2] = np.array(ORIGIN_COORDS[2])

    newTheta = theta * scene.frame_current
    rotationMatrix = np.array([[math.cos(newTheta), -math.sin(newTheta), 0],
            [math.sin(newTheta), math.cos(newTheta), 0],
            [0, 0, 1]])

    if scene.frame_current % FRAME_NUM == 0 and scene.frame_current != 0:
        print(scene.frame_current)
        print("Current Z Value:")
        print(cameraOrigin[2] - Z_AXIS_STEP)
        cameraOrigin[2] = np.array(cameraOrigin[2] - Z_AXIS_STEP)

    camera.location = np.dot(cameraOrigin, rotationMatrix)

    path = f"C:/Users/Spencer/blender-output/{LABEL_MODIFIER}{scene.frame_current}.jpg"
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)

for frame in range(0, TOTAL_FRAMES):
    scene = bpy.data.scenes[SCENE_NAME]
    scene.frame_set(frame)
    rotateCamera(scene)
