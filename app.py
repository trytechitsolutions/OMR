from flask import Flask, request, jsonify
from utils1 import find_paper, read_id, get_ans
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/data', methods=['POST'])
def data():
    file = request.files['image']
    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    file_bytes = np.frombuffer(file.read(), np.uint8)
    org_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    # Process the image to find the paper
    OMR = find_paper(org_image)
    # student id image
    s_id = OMR[55:245, 10:260]
    # test id image
    t_id=OMR[55:250,281:365]
    
    # Read the student ID
    student_id = read_id(s_id, 10)
    
    # Read the test ID
    test_id=read_id(t_id,3)
    
    # question papers read
    q1=OMR[300:1287,54:184]
    q2=OMR[300:1287,256:386]
    q3=OMR[300:1287,456:586]
    q4=OMR[300:1287,658:788]
    q5=OMR[300:1287,859:989]
    
    # read answers
    q1_ans=get_ans(q1)
    q2_ans=get_ans(q2)
    q3_ans=get_ans(q3)
    q4_ans=get_ans(q4)
    q5_ans=get_ans(q5)
    # combine all answers
    final_ans=q1_ans+q2_ans+q3_ans+q4_ans+q5_ans
    final_ans=list(map(str,final_ans))
    return jsonify({"student_id": student_id,"test_id":test_id,"Ans":final_ans})

if __name__ == '__main__':
    app.run(debug=True)