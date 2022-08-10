import pickle
import streamlit as st
from sklearn import svm
import pandas as pd
import numpy as np
from sklearn.exceptions import NotFittedError
from sklearn.utils.validation import check_is_fitted
import json
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import requests
import time

#เรียกใช้ model
with open('svm_model','rb') as file:
    clf = pickle.load(file)
    model = clf

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_url_hello = "https://assets10.lottiefiles.com/packages/lf20_ic37y4kv.json"
lottie_hello = load_lottieurl(lottie_url_hello)

def main():
    col1, col2 = st.columns([4, 2])
    with col1:
        #ชื่อแบบสอบถาม
        st.title('แบบรายงานคุณลักษณะการกำกับการเรียนรู้')
    with col2:
        st_lottie(lottie_hello, key="hello")

    #คำอธิบาย
    st.caption('คำชี้แจง\n ')
    st.caption('1.ให้ผู้เรียนตอบแบบสอบถามให้ถูกต้องตามตามความเป็นจริง')
    st.caption('2.ผลการตอบของท่านจะไม่มีผลต่อผลการเรียนของท่านไม่ว่าในกรณีใดๆ\n')
    
    #ส่วนของผลการเรียน
    st.subheader('ตอนที่ 1 ข้อมูลพื้นฐาน')

    #โรงเรียน
    school_name = st.selectbox(
        'โรงเรียน',
        ('บ้านเขาพลวง', 'บ้านหนองบัวทอง', 'บ้าราหุล'))

    #ระดับชั้น
    class_room = st.selectbox(
        'ระดับชั้น',
        ('มัธยมศึกษาปีที่ 1', 'มัธยมศึกษาปีที่ 2', 'มัธยมศึกษาปีที่ 3'))

    stu_id = st.text_input('รหัสนักเรียน')

    #กำหนดค่าเพศที่ต้องการเก็บกับค่าเพศที่ต้องการถาม
    sex_options = {
        1: "ชาย",
        2: "หญิง"}
    
    #แปลงเป็นค่าที่ต้องการเก็บ
    sex = st.radio( 
        label="เพศ : ",
        options= (1, 2,),
        format_func=lambda x: sex_options.get(x),)

    #ส่วนของผลการเรียน   
    st.subheader('ตอนที่ 2 ผลการเรียน')
    col1, col2 = st.columns(2)
    with col1:
        math = st.number_input('วิชาคณิตศาสตร์',min_value=0.00,max_value=4.00,value=0.00)
        sci = st.number_input('วิชาวิทยาศาสตร์',min_value=0.00,max_value=4.00,value=0.00)
        comsci = st.number_input('วิชาวิทยาการคำนวณ',min_value=0.00,max_value=4.00,value=0.00)
    with col2:
        thai = st.number_input('วิชาภาษาไทย',min_value=0.00,max_value=4.00,value=0.00)
        eng = st.number_input('วิชาภาษาอังกฤษ',min_value=0.00,max_value=4.00,value=0.00)

    st.subheader('ตอนที่ 3 กลวิธีการสร้างแรงจูงใจสำหรับการเรียนรู้')
    st.caption('คำชี้แจง 1.ให้ผู้เรียนเลือกข้อที่ตรงกับตัวท่านมากที่สุด โดยไล่ลำดับจากไม่ใช่ไปใช่มากที่สุด เช่น หมายเลข 1 คือไม่ใช่ตัวตนของผู้เรียน หรือผู้เรียนมิได้มีความคิดเช่นนั้น หมายเลข 5 อาจจะใช่ความคิดหรือตัวตนของผู้เรียนในระดับปานกลางโน้มเอียงไปทางมาก และหมายเลข 7 คือ สิ่งที่ผู้เรียนคิดและเป็นจริงอย่างนั้นจริงๆ 2.ผลการตอบของท่านจะไม่มีผลต่อผลการเรียนของท่านไม่ว่าในกรณีใดๆ')
    convert_options = {
        1.00: "1❌",
        2.00: "2",
        3.00: "3",
        4.00: "4🤔",
        5.00: "5",
        6.00: "6",
        7.00: "7✅"}
    rating_option = (1.00,2.00,3.00,4.00,5.00,6.00,7.00)

    reh1 = st.select_slider(label='1.เมื่อฉันเรียน ฉันมักบ่นกับตัวเองเกี่ยวกับอุปกรณ์สื่อการเรียนการสอนอยู่เสมอ', 
            options= rating_option,format_func=lambda x: convert_options.get(x))
    st.write(reh1)
    reh2 = st.select_slider(label='2.ในขณะเรียนในชั้นเรียน ฉันจะอ่านเอกสารประกอบการเรียนการสอนซ้ำแล้วซ้ำเล่า', 
            options= rating_option,format_func=lambda x: convert_options.get(x))
    reh3 = st.select_slider(label='3.ฉันพยายามใช้คำสำคัญเพื่อที่ช่วยในการจดจำแนวคิดสำคัญและกรอบแนวคิดรายงวิชาในขณะเรียน', 
            options= rating_option,format_func=lambda x: convert_options.get(x))
    reh4 = st.select_slider(label='4.ฉันจะจัดทำรายละเอียดเป็นลำดับของความหมายที่สำคัญและใช้ลำดับนั้นช่วยในการจำ', 
            options= rating_option,format_func=lambda x: convert_options.get(x))
    
    
    peer =3.21
    reh = 3.23
    eff = 3.45
    help = 3.45
    igo = 6.55
    ctrl = 6.45
    ego = 6.32
    org = 5.89
    cri = 6.00
    test = 6.00
    ela = 6.00
    task = 5.00
    time = 5.89
    sef = 5.00
    meta = 6.00
    
    


    if st.button('พยากรณ์'):
        input_data = (sex,math,sci,comsci,thai,eng,reh,ela,org,cri,meta,igo,ego,task,ctrl,sef,test,time,eff,peer,help)

        # changing the input_data to numpy array
        input_data_as_numpy_array = np.asarray(input_data)

        # reshape the array as we are predicting for one instance
        input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

        prediction = clf.predict(input_data_reshaped)
        st.write(prediction)
        


if __name__=='__main__':
    main()