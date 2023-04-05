import replicate
import random
import string
from utils import finalRoast, finalCompliment
from cv2 import imshow, imwrite,waitKey, destroyWindow
from cv2 import VideoCapture

letters = string.ascii_lowercase
name_seed = ''.join(random.choice(letters) for i in range(10))

def output(output_type):
    cam_port = 0
    cam = VideoCapture(cam_port)

    # reading the input using the camera
    result, image = cam.read()

    # If image will detected without any error,
    # show result
    if result:

        # showing result, it take frame name and image
        # output
        imshow(name_seed, image)

        # saving image in local storage
        imwrite("demo/" + name_seed + ".png", image)

        # If keyboard interrupt occurs, destroy image
        # window
        waitKey(0)
        destroyWindow(name_seed)

    # If captured image is corrupted, moving to else part
    else:
        print("No image detected. Please! try again")
    
    if (output_type == "roast"):
        finalRoast("demo/" + name_seed + ".png")
    elif (output_type == "compliment"):
        finalCompliment("demo/" + name_seed + ".png")


if __name__ == "__main__":
    type_string = input("'roast' or 'compliment'?")
    output(type_string)
    #finalRoast("dog.jpeg")
    #finalCompliment("dog.jpeg")