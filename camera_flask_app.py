from flask import Flask, render_template, Response, request
import autoRoaster
from autoRoaster import utils
from autoRoaster.utils import finalRoast as finalRoast
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
import time
import urllib.parse


global capture,rec_frame, grey, switch, neg, face, rec, out, roast, roast_str, impath, roast_switch
send_to_loading = 0
impath = ""
roast_switch=0
roast_str = "Waiting for roast..."
roast = 0
capture=0
grey=0
neg=0
face=0
switch=1
rec=0

#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#Load pretrained face detection model    
net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')


camera = cv2.VideoCapture(0)

def output():
    global roast_str, impath, roast, roast_switch
    if (roast == 1) and (roast_switch == 1):
        print("Generating Roast...")
        print("Image Path: " + impath)
        roast_str = finalRoast(impath)
        roast = 0
    
    return roast_str
    


def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)

@app.route("/target_endpoint")
def target():
    global roast_str
	# This is where the loading screen will be.
	# ( You don't have to pass data if you want, but if you do, make sure you have a matching variable in the html i.e {{my_data}} )
    return render_template('loading.html', my_data = roast_str)

@app.route("/processing")
def processing():
    global impath
    data = finalRoast(impath)
    
    return render_template('success.html', passed_data = data)



def detect_face(frame):
    global net
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))   
    net.setInput(blob)
    detections = net.forward()
    confidence = detections[0, 0, 0, 2]

    if confidence < 0.5:            
            return frame           

    box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
    (startX, startY, endX, endY) = box.astype("int")
    try:
        frame=frame[startY:endY, startX:endX]
        (h, w) = frame.shape[:2]
        r = 480 / float(h)
        dim = ( int(w * r), 480)
        frame=cv2.resize(frame,dim)
    except Exception as e:
        pass
    return frame
 

def gen_frames():  # generate frame by frame from camera
    global out, capture, rec_frame, roast, roast_switch, impath, send_to_loading
    while True:
        success, frame = camera.read() 
        if success:
            if(roast):
                if (roast_switch == 0):
                    print("ROASTED >:)")
                    now = datetime.datetime.now()
                    p = os.path.sep.join(['autoRoaster/photos', "shot_{}.png".format(str(now).replace(":",''))])
                    impath = p
                    if not cv2.imwrite(p, frame):
                        raise Exception("Could not write image")
                    cv2.imwrite(p, frame)
                    roast_switch = 1
                    send_to_loading = 1
            if(face):                
                frame= detect_face(frame)  
            
            
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass


@app.route('/')
def index():
    return render_template('index.html')


@app.get("/update")
def update():
    return output()

def convert(input):
    # Converts unicode to string
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, str):
        return input.encode('utf-8')
    else:
        return input
    
    
    
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
        elif request.form.get('roast') == 'Roast':
            global roast
            roast=1
        elif  request.form.get('grey') == 'Grey':
            global grey
            grey=not grey
        elif  request.form.get('neg') == 'Negative':
            global neg
            neg=not neg
        elif  request.form.get('face') == 'Face Only':
            global face
            face=not face 
            if(face):
                time.sleep(4)   
        elif  request.form.get('stop') == 'Stop/Start':
            
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()
                
            else:
                camera = cv2.VideoCapture(0)
                switch=1
        elif  request.form.get('rec') == 'Start/Stop Recording':
            global rec, out
            rec= not rec
            if(rec):
                now=datetime.datetime.now() 
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter('vid_{}.avi'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
                #Start new thread for recording the video
                thread = Thread(target = record, args=[out,])
                thread.start()
            elif(rec==False):
                out.release()
                          
                 
    elif request.method=='GET':
        return render_template('index.html')
    if (roast == 1 and roast_switch == 1):
        return render_template('loading.html')
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
    
camera.release()
cv2.destroyAllWindows()     