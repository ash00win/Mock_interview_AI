from flask import *
from database import *
from voice import *



users=Blueprint('user',__name__)


@users.route("/userhome",methods=['post','get'])
def userhome():
   
    return render_template("user.html")


@users.route("/manage_profile",methods=['post','get'])
def manage_profile():
    
    z="select * from user where user_id='%s'"%(session['uid'])
    a=select(z)
    print(a,"//")
    
    if 'update' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        place=request.form['place']
        phone=request.form['phone']
        email=request.form['email']
        
        c="update user set fname='%s',lname='%s',place='%s',phone='%s',email='%s' where user_id='%s'"%(fname,lname,place,phone,email,session['uid'])
        update(c)
        return '''<script>alert("Updated Successfully");window.location="/manage_profile"</script>'''
        
        
        
        
        
   
    return render_template("manage_profile.html",a=a)




@users.route("/view_role",methods=['post','get'])
def view_role():
    q="select * from roles"
    r=select(q)
    return render_template("view_role.html",r=r)



@users.route("/view_notification",methods=['post','get'])
def view_notification():
    q="select * from notification"
    r=select(q)
    return render_template("view_notification.html",r=r)


@users.route("/send_complaint",methods=['post','get'])
def send_complaint():
    q="select * from complaint where login_id='%s'"%(session['log'])
    r=select(q)
    
    if 'submit' in request.form:
        com=request.form['com']
        
        a="insert into complaint values(null,'%s','%s',curdate(),'pending')"%(session['log'],com)
        insert(a)
        return '''<script>alert("Submitted Successfully");window.location="/send_complaint"</script>'''
        
    return render_template("send_complaint.html",r=r)



@users.route('/role_selection')
def role_selection():
    a="select * from roles"
    r=select(a)
    return render_template('role_selection.html',r=r)

def create_and_store_questions(role):
    cursor.execute("SELECT role_id FROM roles WHERE role_name = %s", (role,))
    role_id = cursor.fetchone()
    if role_id:
        role_id = role_id[0]
        questions_and_answers = []
        for _ in range(10):
            question_prompt = f"Generate a unique and non-repetitive theoretical interview question for a {role} position, specifically tailored for recent graduates. Ensure the question is concise (no more than 2 lines) and focuses on different fundamental knowledge areas related to the role. Avoid repeating any concepts or questions already generated."
            question_text = generate_gemini_response(question_prompt)
            if question_text:
                answer_prompt = f"Provide a simple one line answer for the following question: {question_text}"
                answer_text = generate_gemini_response(answer_prompt)
                if answer_text:
                    questions_and_answers.append((question_text, answer_text))
                else:
                    print("Failed to generate an answer for the question.")
            else:
                print("Failed to generate a question.")
        for question_text, answer_text in questions_and_answers:
            cursor.execute("INSERT INTO questions (question_text, role_id,user_id,date) VALUES (%s, %s,%s,curdate())", (question_text, role_id,session['uid']))
            question_id = cursor.lastrowid
            cursor.execute("INSERT INTO answers (question_id, correct_answer) VALUES (%s, %s)", (question_id, answer_text))
        db.commit()
    else:
        print("Role not found in the database.")
        
from face_recognize import *  

    
@users.route('/face_recog', methods=['POST','GET'])
def face_recog():
    a=camclick()
    return a


# from face_time import *

# @users.route('/start_interview', methods=['POST'])
# def start_interview():
    
   
    
#     role = request.form.get('role')
#     print(role,"/")

#     z="select * from questions inner join roles using(role_id) where user_id='%s' and date=curdate()"%(session['uid'])
#     ed=select(z)



#     if not ed:
      
#         create_and_store_questions(role)
#         question = fetch_next_question(role)
#         if question:
#             question_id, question_text = question
#             return render_template('question_page.html', role=role, question=question_text, question_id=question_id)
#         else:
#             return "No questions available for this role. Please try again."
#     else:
#         return '''<script>alert('You have already tooked assesment for this role today.Try next day');window.location='/role_selection'</script>'''
        

   
        



    

# @users.route('/submit_answer', methods=['POST'])
# def submit_answer():

#     question_id = request.form.get('question_id')
#     role = request.form.get('role')
#     user_answer = request.form.get('user_answer')  # This will be the converted speech to text
    
    
#     # Retrieve correct answer from the database
#     cursor.execute("SELECT correct_answer FROM answers WHERE question_id = %s", (question_id,))
#     correct_answer = cursor.fetchone()[0]
    
#     # Check similarity between the user's answer and the correct answer
#     similarity_score = similarity(user_answer, correct_answer)
    
#     if similarity_score > 0.8:  # Adjust the threshold as needed
#         # Correct answer, increment score
#         cursor.execute("UPDATE answers SET score =1  WHERE question_id = %s", (question_id,))
#         db.commit()
#         message = "Correct! Your answer is similar to the correct answer."
#     else:
#         cursor.execute("UPDATE answers SET score =0  WHERE question_id = %s", (question_id,))
#         db.commit()
#         message = "Incorrect. Your answer does not match the correct answer."
    
#     # Update the user_answer in the database
#     cursor.execute("UPDATE answers SET user_answer = %s WHERE question_id = %s", (user_answer, question_id))
#     db.commit()
    
#     # Fetch the next question
#     next_question = fetch_next_question(role, current_question_id=question_id)
#     if next_question:
#         question_id, question_text = next_question
#         return render_template('question_page.html', role=role, question=question_text, question_id=question_id, message=message)
#     else:
#         q="select * from roles where role_name='%s'"%(role)
#         cc=select(q)
#         roleid=cc[0]['role_id']
#         z="select count(score) as total from questions inner join answers using(question_id) where user_id='%s' and date=curdate() and role_id='%s'"%(session['uid'],roleid)
#         t=select(z)
        
        
#         x="select count(score) as mark from questions inner join answers using(question_id) where user_id='%s' and date=curdate() and score=1 and role_id='%s'"%(session['uid'],roleid)
#         m=select(x)
        
#         if t and x:
#             total=t[0]['total']
#             mark=m[0]['mark']
            
#             print(total,mark)
            
#             per = round((float(mark)/float(total))*100, 2)
            
          
#         return render_template('final.html',per=per)
import numpy as np
import cv2
from keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import winsound  # For beep sound on Windows
from flask import render_template, request, session
import threading

# Define the emotions and assign a confidence factor for each.
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Load the pre-trained emotion detection model and its weights.
classifier = load_model('model_78.h5')
classifier.load_weights('model_weights_78.h5')

# Load the face detector using OpenCV's Haar Cascade.
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Global variables to store the latest detected emotion and confidence score
latest_emotion = None
latest_confidence_score = 0
emotion_detection_running = False  # Flag to control the emotion detection thread

def emotion_detect():
    global latest_emotion, latest_confidence_score, emotion_detection_running
    face_absent_counter = 0  # Counter to track frames without a detected face

    # Start the webcam feed.
    cap = cv2.VideoCapture(0)

    while emotion_detection_running:  # Run while the flag is True
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if len(faces) == 0:
            face_absent_counter += 1
            if face_absent_counter > 30:
                winsound.Beep(1000, 500)
                face_absent_counter = 0
        else:
            face_absent_counter = 0

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                prediction = classifier.predict(roi)[0]
                maxindex = int(np.argmax(prediction))
                emotion_detected = emotion_labels[maxindex]
                confidence_score = prediction[maxindex] * 100

                # Update the latest emotion and confidence score
                latest_emotion = emotion_detected
                latest_confidence_score = confidence_score

                label_position = (x, y - 10)
                cv2.putText(frame, f'{emotion_detected}: {confidence_score:.2f}%', label_position, 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Emotion & Confidence Detector', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def emotion_detection_thread():
    global emotion_detection_running
    emotion_detection_running = True
    emotion_detect()  # Start emotion detection
    emotion_detection_running = False  # Stop the thread after the function finishes

@users.route('/start_interview', methods=['POST'])
def start_interview():
    global emotion_detection_running  # Reference the global flag

    role = request.form.get('role')

    # Check for existing assessments
    z = "SELECT * FROM questions INNER JOIN roles USING(role_id) WHERE user_id='%s' AND date=CURDATE()" % (session['uid'])
    ed = select(z)

    if not ed:
        create_and_store_questions(role)
        question = fetch_next_question(role)
        if question:
            question_id, question_text = question
            
            # Start the emotion detection in a separate thread
            threading.Thread(target=emotion_detection_thread).start()
            
            return render_template('question_page.html', role=role, question=question_text, question_id=question_id)
        else:
            return "No questions available for this role. Please try again."
    else:
        return '''<script>alert('You have already taken assessment for this role today. Try next day');window.location='/role_selection'</script>'''

@users.route('/submit_answer', methods=['POST'])
def submit_answer():
    global emotion_detection_running  # Reference the global flag

    question_id = request.form.get('question_id')
    role = request.form.get('role')
    user_answer = request.form.get('user_answer')

    cursor.execute("SELECT correct_answer FROM answers WHERE question_id = %s", (question_id,))
    correct_answer = cursor.fetchone()[0]

    similarity_score = similarity(user_answer, correct_answer)

    if similarity_score > 0.8:
        cursor.execute("UPDATE answers SET score = 1 WHERE question_id = %s", (question_id,))
        db.commit()
        message = "Correct! Your answer is similar to the correct answer."
    else:
        cursor.execute("UPDATE answers SET score = 0 WHERE question_id = %s", (question_id,))
        db.commit()
        message = "Incorrect. Your answer does not match the correct answer."

    cursor.execute("UPDATE answers SET user_answer = %s WHERE question_id = %s", (user_answer, question_id))
    db.commit()

    next_question = fetch_next_question(role, current_question_id=question_id)
    if next_question:
        question_id, question_text = next_question
        return render_template('question_page.html', role=role, question=question_text, question_id=question_id, message=message)
    else:
        # Stop the emotion detection
        emotion_detection_running = False  # Signal the thread to stop

        # Calculate scores for the final result
        roleid = select(f"SELECT role_id FROM roles WHERE role_name='{role}'")[0]['role_id']
        total = select(f"SELECT COUNT(score) AS total FROM questions INNER JOIN answers USING(question_id) WHERE user_id='{session['uid']}' AND date=CURDATE() AND role_id='{roleid}'")[0]['total']
        mark = select(f"SELECT COUNT(score) AS mark FROM questions INNER JOIN answers USING(question_id) WHERE user_id='{session['uid']}' AND date=CURDATE() AND score=1 AND role_id='{roleid}'")[0]['mark']
        
        per = round((float(mark) / float(total)) * 100, 2)

        # Render the final page with the latest detected emotion
        return render_template('final.html', per=per, emotion=latest_emotion, confidence=latest_confidence_score)
