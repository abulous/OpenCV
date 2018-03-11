import cv2, numpy as np, argparse, time, glob, os, sys, subprocess, pandas, random, Update_Model, math, ctypes

#Define variables and load classifier
camnumber = 0
video_capture = cv2.VideoCapture()
facecascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
fishface = cv2.face.FisherFaceRecognizer_create()
fishface.read("trained_emoclassifier.xml")
#try:
#fishface.load("trained_emoclassifier.xml")
#except:
#    print("no trained xml file found, please run program with --update flag first")

parser = argparse.ArgumentParser(description="Options for the emotion-based music player")
parser.add_argument("--update", help="Call to grab new images and update the model accordingly", action="store_true")
parser.add_argument("--retrain", help="Call to re-train the the model based on all images in training folders", action="store_true") #Add --update argument
parser.add_argument("--wallpaper", help="Call to run the program in wallpaper change mode. Input should be followed by integer for how long each change cycle should last (in seconds)", type=int) #Add --update argument
args = parser.parse_args()
facedict = {}
actions = {}
emotions = ["angry", "happy", "sad", "neutral"]
df = pandas.read_excel("EmotionLinks.xlsx") #open Excel file
actions["angry"] = [x for x in df.angry.dropna()] #We need de dropna() when columns are uneven in length, which creates NaN values at missing places. The OS won't know what to do with these if we try to open them.
actions["happy"] = [x for x in df.happy.dropna()]
actions["sad"] = [x for x in df.sad.dropna()]
actions["neutral"] = [x for x in df.neutral.dropna()]

def open_stuff(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def crop_face(clahe_image, face):
    for (x, y, w, h) in face:
        faceslice = clahe_image[y:y+h, x:x+w]
        faceslice = cv2.resize(faceslice, (350, 350))
    facedict["face%s" %(len(facedict)+1)] = faceslice
    return faceslice

def update_model(emotions):
    print("Model update mode active")
    check_folders(emotions)
    for i in range(0, len(emotions)):
        save_face(emotions[i])
    print("collected images, looking good! Now updating model...")
    Update_Model.update(emotions)
    print("Done!")

def check_folders(emotions):
    for x in emotions:
        if os.path.exists("dataset/%s" %x):
            pass
        else:
            os.makedirs("dataset/%s" %x)

def save_face(emotion):
    print("\n\nplease look " + emotion + ". Press enter when you're ready to have your pictures taken")
    #raw_input() #Wait until enter is pressed with the raw_input() method
    video_capture.open(camnumber)
    while len(facedict.keys()) < 16:
        detect_face()
    video_capture.release()
    for x in facedict.keys():
        cv2.imwrite("dataset/%s/%s.jpg" %(emotion, len(glob.glob("dataset/%s/*" %emotion))), facedict[x])
    facedict.clear()

def recognize_emotion():
    predictions = []
    confidence = []
    for x in facedict.keys():
        pred, conf = fishface.predict(facedict[x])
        cv2.imwrite("images/%s.jpg" %x, facedict[x])
        predictions.append(pred)
        confidence.append(conf)
    recognized_emotion = emotions[max(set(predictions), key=predictions.count)]
    print("I think you're %s" %recognized_emotion)
    return recognized_emotion

def grab_webcamframe():
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clahe_image = clahe.apply(gray)
    return clahe_image

def detect_face():
    clahe_image = grab_webcamframe()
    face = facecascade.detectMultiScale(clahe_image, scaleFactor=1.1, minNeighbors=15, minSize=(10, 10), flags=cv2.CASCADE_SCALE_IMAGE)
    if len(face) == 1:
        faceslice = crop_face(clahe_image, face)
        return faceslice
    else:
        print("no/multiple faces detected, passing over frame")

def run_detection():
    while len(facedict) != 10:
        detect_face()
    recognized_emotion = recognize_emotion()
    return recognized_emotion

def wallpaper_timer(seconds):
    video_capture.release()
    time.sleep(int(seconds))
    video_capture.open(camnumber)
    facedict.clear()

def change_wallpaper(emotion):
    files = glob.glob("wallpapers/%s/*.bmp" %emotion)
    current_dir = os.getcwd()
    random.shuffle(files)
    file = "%s\%s" %(current_dir, files[0])
    setWallpaperWithCtypes(file)

def setWallpaperWithCtypes(path): #Taken from http://www.blog.pythonlibrary.org/2014/10/22/pywin32-how-to-set-desktop-background/
    cs = ctypes.c_buffer(path)
    ok = ctypes.windll.user32.SystemParametersInfoA(win32con.SPI_SETDESKWALLPAPER, 0, cs, 0)

if args.update:
    update_model(emotions)
elif args.retrain:
    Update_Model.update(emotions)
elif args.wallpaper:
    cycle_time = args.wallpaper
    while True:
        wallpaper_timer(cycle_time)
        recognized_emotion = run_detection()
        change_wallpaper(recognized_emotion)
else:
    video_capture.open(camnumber)
    recognized_emotion = run_detection()
    actionlist = [x for x in actions[recognized_emotion]] #get list of actions/files for detected emotion
    random.shuffle(actionlist) #Randomly shuffle the list
    open_stuff(actionlist[0])
