import cv2, requests, operator, os, pygame, random
from datetime import datetime, timedelta

# Player set up
pygame.init()
pygame.mixer.init()
player = pygame.mixer.music

# Cooldown settings
delta = 5 # in seconds
last_check = datetime.now() - timedelta(seconds = delta)

# Camea set up
cap = cv2.VideoCapture(-1)
#cap.set(3, 1920)
#cap.set(4, 1080)
#cap.set(5, 60)


# Face detection set up
#face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

# Face API set up
subscription_key = 'e34696f9d2e94670a5867cbf51f5b782'
uri_base = 'https://westcentralus.api.cognitive.microsoft.com'

headers = {
     'Content-Type': 'application/octet-stream',
     'Ocp-Apim-Subscription-Key': subscription_key,
}

params = {
    'returnFaceId': 'false',
    'returnFaceAttributes': 'emotion',
}

path_to_face_api = '/face/v1.0/detect'

# File paths
path = '/home/pi/Desktop/EMI/'
img_file = path + 'data/img.jpg'
history_file = path + 'data/history.txt' 

print ("loaded")
while(True):
    # Search for face
    ret, frame = cap.read()
    #print (ret)
    #print frame.shape
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    '''
    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Eye thingy
        #roi_gray = gray[y:y+h, x:x+w]
        #roi_color = frame[y:y+h, x:x+w]
        #eyes = eye_cascade.detectMultiScale(roi_gray)
        #for (ex,ey,ew,eh) in eyes:
        #   cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        '''
    # Face detected
    if  (datetime.now() - last_check).seconds >= delta and not player.get_busy():
        last_check = datetime.now()
        cv2.imwrite(img_file, frame)

        with open(img_file, 'rb') as f:
            img_data = f.read()

        try:
            # Call API
            response =  requests.post (
                uri_base + path_to_face_api,
                data = img_data, 
                headers = headers,
                params = params,
            )

            #response = (1, 2, 3)
            # Log data
            #os.remove(img_file)
            #print "test"
            response = response.json()
            #print response
            if len(response) > 0:
                emotions = response[0]['faceAttributes']['emotion']
                #with open(history_file, 'a') as myfile:
                #    myfile.write(str(last_check) + ' ' + str(emotions) + '\n')
            
                # Process data
                emotions = sorted(emotions.items(), key = operator.itemgetter(1), reverse = True)
                predominant = 0 if emotions[0][0] != 'neutral' or emotions[1][1] == 0 else 1
                emotions = emotions[predominant]

                # Play response
                player.load(path + 'sounds/' + emotions[0] + '.wav')
                player.play(loops = random.randint(0, 1))
                print (emotions[0] + ' ' + str(emotions[1]))

       
        except Exception as e:
            print('Error:')
            print(e)

    #cv2.imshow('EMI', frame)

    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #break

try:
    os.remove(img_file)
except:
    pass

cap.release()
cv2.destroyAllWindows()
