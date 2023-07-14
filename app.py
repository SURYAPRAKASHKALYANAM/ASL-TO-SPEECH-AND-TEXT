from flask import Flask, render_template, Response,send_file, send_from_directory
import cv2 as cv
from tensorflow import keras
from statistics import mode
import pyttsx3
import uuid
# load model 
model=keras.models.load_model(r"VGG16_FINAL_MODEL2.h5")  # VGG16_FINAL_MODEL2 MODEL IS LOADED
LABELS_DICT={
    0:"A",
    1:"B",
    2:"C",
    3:"D",
    4:"E",
    5:"F",
    6:"G",
    7:"H",
    8:"I",
    9:"J",
    10:"K",
    11:"L",
    12:"M",
    13:"N",
    14:"O",
    15:"P",
    16:"Q",
    17:"R",
    18:"S",
    19:"T",
    20:"U",
    21:"V",
    22:"W",
    23:"X",
    24:"Y",
    25:"Z",
    26:"del",
    27:"nothing",
    28:"space"    
}


cap = None
# video_capture = cv.VideoCapture(0) # Replace 0 with the appropriate camera index if using a webcam
breakflag = False  # Global variable to break the while loops
speech=""
app = Flask(__name__)
audio_path=""

#disable caching of static files, ensuring that the updated files are served after refreshing:
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
 
@app.route('/')
def index():
    return render_template('index.html')


def generate_frames():
    global cap, breakflag,speech,audio_path
    speaker=pyttsx3.init()
    speaker.setProperty('rate',150)
    speaker.setProperty('volume',1)
    speech=""
    final=""
    cap = cv.VideoCapture(0)  # Initialize the camera
    if not cap.isOpened():
        # Handle camera initialization failure
        return "Camera not opened"
    while True:
        if breakflag:
            break
        Isframe,frame=cap.read()
        if not Isframe:
            continue
        l=[]
        frame=cv.flip(frame,1) # flips the image L->R around y-axis
        top_left = (335, 35)
        bottom_right = (635, 335)
        img=cv.rectangle(frame,top_left,bottom_right,(248, 6, 204),thickness=2)  # A rectanle area of region to read hand input from whole image frame
        input_image=img[35:335,335:635]
        input_image=cv.flip(input_image,1) # flips the image L->R around y-axis
        final_image=img[35:335,335:635]
        final_image=cv.flip(final_image,1)
        input_image=cv.resize(input_image,(64,64))
        input_image=input_image/255.0
        input_image=input_image.reshape(1,64,64,3)
        result=model.predict(input_image,batch_size=1)
        result=list(result[0])
        key=result.index(max(result))
        while len(l)==0 or LABELS_DICT[key]!='nothing':
            Isframe,frame=cap.read()
            if not Isframe:
                breakflag=True
                break
            frame=cv.flip(frame,1) # flips the image L->R around y-axis
            top_left = (335, 35)
            bottom_right = (635, 335)
            img=cv.rectangle(frame,top_left,bottom_right,(248, 6, 204),thickness=2)  # A rectanle area of region to read hand input from whole image frame
            input_image=img[35:335,335:635]
            input_image=cv.flip(input_image,1) # flips the image L->R around y-axis
            final_image=img[35:335,335:635]
            final_image=cv.flip(final_image,1)
            input_image=cv.resize(input_image,(64,64))
            input_image=input_image/255.0
            input_image=input_image.reshape(1,64,64,3)
            result=model.predict(input_image,batch_size=1)
            result=list(result[0])
            key=result.index(max(result))
            l.append(LABELS_DICT[key])
            img=cv.putText(img,mode(l),(335,33),cv.FONT_HERSHEY_SIMPLEX,1,color=(56, 229, 77),thickness=2)
            # text=np.zeros((500,500,3),dtype='uint8')
            img=cv.putText(img,speech,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,color=(248, 6, 204),thickness=2)
            # cv.imshow("TEXT",text)
            # cv.imshow("INPUT",frame)
            # cv.imshow("HAND",final_image)
            # Convert the frame to JPEG format
            ret, buffer = cv.imencode('.jpg', img)
            if not ret:
                continue
            # Convert the frame to bytes
            frame_bytes = buffer.tobytes()
            # Yield the BYTES as a response
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            if cv.waitKey(1)==ord('q'):   # ord('q') means it waits for input q(lower case)
                breakflag=True
                break
        if len(l)!=0:
            final=mode(l)    
            if final!='nothing':
                if final=='del':
                    if len(speech)!=0:
                        speech=speech[:-1]
                elif final=='space':
                    speech+=" "
                else:
                    speech+=final            
            # img=cv.putText(img,LABELS_DICT[key],(335,33),cv.FONT_HERSHEY_SIMPLEX,1,color=(56, 229, 77),thickness=1)
            # text=np.zeros((500,500,3),dtype='uint8')
            # img=cv.putText(img,speech,(0,0),cv.FONT_HERSHEY_SIMPLEX,1,color=(0,255,0),thickness=2)
            # cv.imshow("TEXT",text)
            # cv.imshow("INPUT",frame)
            # cv.imshow("HAND",final_image)
        l=[]  #empty prediction list    
        if cv.waitKey(1)==ord('q') or breakflag:   # ord('q') means it waits for input q(lower case)
            break   
    # cv.destroyAllWindows()
    # speaker.say(s)
    audio_path=f'static\\audio_{uuid.uuid4()}.mp3'
    # audio_path = r'static/audio_' + str(uuid.uuid4()) + '.mp3'
    #audio_path = f'static/audio_{uuid.uuid4()}.mp3'
    speaker.save_to_file(speech,audio_path)
    # speaker.save_to_file(speech,'static\\audio.mp3')
    speaker.runAndWait()
 


@app.route('/start_image')
def start_image():
    global breakflag
    breakflag = False
    return  "STARTED"

@app.route('/video_feed')
def video_feed():
    # print("video_feed is called==>>")
    # global cap
    # cap = video_capture
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_audio')
def get_audio():
    global audio_path
    # print(audio_path)
    #return  audio_path
    return send_file(audio_path, mimetype='audio/mpeg')
    #return send_from_directory(directory='static', path=audio_path, mimetype='audio/mpeg')


@app.route('/stop_image')
def stop_image():
    global cap, breakflag, speech
    breakflag = True
    cap.release()  # Release the video capture object
    # speaker = pyttsx3.init()
    # speaker.setProperty('rate', 150)
    # speaker.setProperty('volume', 1)
    # speaker.save_to_file(speech, 'static/audio.mp3')
    # speaker.runAndWait()
    
    return speech



if __name__ == '__main__':
    app.run(debug=True)