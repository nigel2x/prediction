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
# -*- coding: utf-8 -*-
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("key_sheet.json", scope)
client = gspread.authorize(creds)
sheet = client.open("stu_info").sheet1
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
    stu_name = title = st.text_input('ชื่อ-นามสกุลนักเรียน', 'ชื่อ-นามสกุล')
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
    st.caption('คำชี้แจง')
    st.caption('1.ให้ผู้เรียนเลือกข้อที่ตรงกับตัวท่านมากที่สุด โดยไล่ลำดับจากไม่ใช่ไปใช่มากที่สุด เช่น หมายเลข 1 คือไม่ใช่ตัวตนของผู้เรียนและหมายเลข 7 คือ สิ่งที่ผู้เรียนคิดและเป็นจริงอย่างนั้นจริงๆ')
    st.caption('2.ผลการตอบของท่านจะไม่มีผลต่อผลการเรียนของท่านไม่ว่าในกรณีใดๆ')
    convert_options = {
        1.00: "1",
        2.00: "2",
        3.00: "3",
        4.00: "4",
        5.00: "5",
        6.00: "6",
        7.00: "7"}
    rating_option = (1.00,2.00,3.00,4.00,5.00,6.00,7.00)
    
    
    reh1 = st.select_slider(label='เมื่อฉันเรียน ฉันมักบ่นกับตัวเองเกี่ยวกับอุปกรณ์สื่อการเรียนการสอนอยู่เสมอ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    reh2 = st.select_slider(label='ในขณะเรียนในชั้นเรียน ฉันจะอ่านเอกสารประกอบการเรียนการสอนซ้ำแล้วซ้ำเล่า', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    reh3 = st.select_slider(label='ฉันพยายามใช้คำสำคัญเพื่อที่ช่วยในการจดจำแนวคิดสำคัญและกรอบแนวคิดรายงวิชาในขณะเรียน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    reh4 = st.select_slider(label='ฉันจะจัดทำรายละเอียดเป็นลำดับของความหมายที่สำคัญและใช้ลำดับนั้นช่วยในการจำ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)

    ela1 = st.select_slider(label='ในขณะเรียนในชั้นเรียน ฉันจะเอาเอกสารประกอบการสอน หนังสือ สมุดจดบันทึกมาวางกองรวมกันบนโต๊ะ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    ela2 = st.select_slider(label='ฉันพยายามที่จะสร้างความสัมพันธ์ในหัวข้อที่ศึกษากับรายวิชาอื่นๆ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    ela3 = st.select_slider(label='ในการอ่านเอกสารประกอบการเรียนการสอน ฉันพยายามถ่ายโยงกับความรู้เดิมที่มีอยู่', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    ela4 = st.select_slider(label='ในขณะเรียน ฉันจะจดใจความสำคัญและสรุปความคิดหลักจากเอกสารประกอบการอ่านและใจความสำคัญจากการเรียนการสอน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    ela5 = st.select_slider(label='ฉันพยายามทำความเข้าใจกับสื่อการเรียนการสอนในชั้นเรียน โดยการสร้างความเชื่อมโยงระหว่างเอกสารประกอบการอ่านและใจความสำคัญจากการเรียนการสอน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    ela6 = st.select_slider(label='ฉันพยายามประยุกต์แนวความคิดจากเอกสารประกอบการอ่านในกิจกรรมของชั้นเรียนอื่นๆยกตัวอย่างเช่น จากการเรียนการสอนแบะการอภิปราย', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    
    org1 = st.select_slider(label='เมื่อฉันอ่านเอกสารประกอบการอ่านในชั้นเรียนนี้แล้ว ฉันจะสร้างกรอบความคิดว่าสื่อการเรียนการสอนนี้จะช่วยฉันบริหารจัดการความคิดได้อย่างไร', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    org2 = st.select_slider(label='ฉันพยายามที่จะหาใจความสำคัญและแนวคิดหลักการสำคัญจากเอกสารประกอบการอ่านและสมุดจดบันทึก', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    org3 = st.select_slider(label='ฉันพยายามสร้างแผนผัง แผนภูมิ หรือตารางเพื่อช่วยในการจดจำ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    org4 = st.select_slider(label='ฉันจะอ่านสมุดจดบันทึกการเรียนการสอนและจดจำจุดสำคัญเพื่อเป็นแนวทางในการสร้างความรู้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)    

    cri1 = st.select_slider(label='ฉันจะตั้งคำถามกับสิ่งต่างๆที่ฉันได้ยิน ได้อ่าน ในการเรียนการสอนในชั้นเรียนเพื่อนำไปเป็นแนวทางตัดสินใจ ถ้าฉันเชื่อมั่นกับความรู้ที่ได้จากการได้ยิน ได้อ่านนั้น', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    cri2 = st.select_slider(label='เมื่อมีการสอนโดนใช้หลักการ ทฤษฎี การถอดความ หรือบทสรุปสำคัญในชั้นเรียน และจากการอ่าน ฉันพยายามที่จะตัดสินใจยอมรับถ้าหากว่าสิ่งเหล่านั้นมีหลักฐานสนับสนุนที่ดี', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    cri3 = st.select_slider(label='ฉันพัฒนาแนวคิดในแบบฉบับของตนเองเกี่ยวกับเนื้อหาที่ได้เรียนโดยใช้เอกสารประกอบการเรียนการสอนเป็นจุดเริ่มต้นที่สำคัญ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    cri4 = st.select_slider(label='ฉันพยายามทบทวนแนวคิดดั้งเดิมของตัวเองกับแนวคิดหลักการใหม่ที่ได้เรียนในชั้นเรียน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    cri5 = st.select_slider(label='เมื่อไรก็ตามที่ฉันได้อ่านหรือได้ยินการยืนยัน การกล่าวอ้าง หรือการสรุปผลในชั้นเรียน ฉันคิดว่าเป็นทางเลือกที่เป็นบวกเสมอ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)          
    
    meta1 = st.select_slider(label='ในระหว่างเรียนในชั้นเรียน ฉันจะพลาดจุดสำคัญเป็นประจำเพราะฉันมัวแต่คิดเรื่องอื่น', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    meta2 = st.select_slider(label='เมื่อฉันอ่านเอกสารประกอบการเรียน ฉันจะสร้างคำถามเพื่อช่วยให้ฉันสามารถมองเห็นจุดสำคัญของเรื่องที่อ่านได้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    meta3 = st.select_slider(label='เมื่อฉันสับสนกับสิ่งใดสิ่งหนึ่งในขณะอ่าน ฉันจะย้อนกลับไปทบทวน อ่านซ้ำ และพยายามทำความเข้าใจอีกครั้ง', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    meta4 = st.select_slider(label='ถ้าเอกสารประกอบการเรียนการสอนหรือสื่อการเรียนการสอนยากต่อความเข้าใจ ฉันจะเปลี่ยนแนวทางในการอ่านเอกสารประกอบการสอนและสื่อการเรียนการสอนในแนวทางใหม่', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    meta5 = st.select_slider(label='ฉันมักจะอ่านเอกสารประกอบการเรียนการสอนแบบผ่านๆ เพื่อดูว่ามีโครงสร้างอย่างไรก่อนจะเรียน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    meta6 = st.select_slider(label='ฉันตั้งคำถามกับตัวเองเพื่อให้มั่นใจว่า ฉันเข้าใจในเอกสารประกอบการเรียนการสอนในขณะเรียน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    meta7 = st.select_slider(label='ฉันพยายามเปลี่ยน ปรับปรุง แนวทางและรูปแบบให้เหมาะสมกับวิธีการสอนของอาจารย์และให้เป็นไปตามเป้าประสงค์ของการเรียน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    meta8 = st.select_slider(label='ฉันรู้สึกว่า ฉันไม่เข้าใจกับเรื่องที่เรียนเลย ถึงแม้ว่าจะเรียนมาแล้วหลายคาบ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    meta9 = st.select_slider(label='ฉันพยายามคิดและทำความเข้าใจเกี่ยวกับหัวข้อที่เรียนและตัดสินใจว่าฉันจะเรียนรู้มันอย่างจริงจังมากกว่าอ่านผ่านๆ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    meta10 = st.select_slider(label='ฉันสามารถบอกได้ว่า ฉันไม่เข้าใจในเรื่องใดเรื่องหนึ่งขณะเรียน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    meta11 = st.select_slider(label='ฉันมีความมุ่งมั่นในการเรียน โดยการตั้งคำถามและกำหนดเป้าหมายในการเรียนด้วยตัวเอง', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    meta12 = st.select_slider(label='ถ้าฉันไม่เข้าใจในการจดบันทึกการเรียนการสอน ฉันจะกลับมาทำความเข้าใจกับมันใหม่ด้วยการแยกแยะและการจำแนกใหม่', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)

    igo1 = st.select_slider(label='ฉันชอบเอกสารประกอบการเรียนการสอนและสื่อการสอนที่ท้าทายดังนั้นฉันจึงสามารถเรียนรู้สิ่งใหม่ๆได้ดี', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    igo2 = st.select_slider(label='ฉันชอบเอกสารประกอบการเรียนการสอนและสื่อการสอน  ที่กระตุ้นความอยากรู้อยากเห็น ถึงแม้จะยากต่อการเรียนรู้ก็ตาม', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    igo3 = st.select_slider(label='สิ่งที่สร้างความพึงพอใจสูงสุดของฉันคือ การพยายามทำความเข้าใจในปริบทอย่างทั่วถึงและถ่องแท้ ถ้าเป็นไปได้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    igo4 = st.select_slider(label='เมื่อฉันได้มีโอกาส ฉันจะเลือกทำรายงานที่ไม่รับประกันว่าจะได้เกรดที่ดีหรือไม่ แต่ฉันจะศึกษาและลงมือทำด้วยความรู้สึกท้าทาย', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)    

    ego1 = st.select_slider(label='การได้เกรดที่ดีคือสิ่งที่สำคัญที่สุดในการเรียนของฉัน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    ego2 = st.select_slider(label='สิ่งสำคัญที่สุดในขณะนี้คือพยายามให้ได้เกรดที่ดี นั้นจึงเป็นสาเหตุที่ฉันตั้งใจเรียน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    ego3 = st.select_slider(label='ถ้าฉันสามารถทำได้ ฉันขอให้ได้เกรดที่ดีกว่าเพื่อนร่วมชั้นเรียน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    ego4 = st.select_slider(label='ฉันจะตั้งใจเรียนเพื่อให้ได้เกรดที่ดี เพื่อที่จะเป็นจุดสนใจของคนอื่นและโอกาสให้ได้งานที่ดี', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)    


    task1 = st.select_slider(label='ฉันคิดว่าความรู้ที่ได้เรียนสามารถนำไปประยุกต์ใช้ในการเรียนอีกวิชาหนึ่งได้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    task2 = st.select_slider(label='มีความจำเป็น และสำคัญกับฉันมากที่จะเรียนโดยมีสื่อการเรียนการสอนในชั้นเรียน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    task3 = st.select_slider(label='ฉันมีความสนใจอย่างมากในการเรียนวิชานี้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    task4 = st.select_slider(label='ฉันคิดว่าสื่อการเรียนการสอนมีความจำเป็นอย่างมากในวิชานี้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    task5 = st.select_slider(label='ฉันชอบเนื้อหาที่จะศึกษาในรายวิชานี้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    task6 = st.select_slider(label='การทำความเข้าใจเนื้อหาระหว่างที่เรียนเป็นสิ่งสำคัญอย่างมากต่อตัวฉัน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    
    ctrl1 = st.select_slider(label='ถ้าฉันศึกษาด้วยวิธีที่เหมาะสม ฉันคิดว่าฉันสามารถที่จะเรียนรู้อะไรได้มากมายจากเอกสารประกอบการเรียนการสอนและสื่อการเรียนการสอนในรายวิชานี้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    ctrl2 = st.select_slider(label='มันเป็นความผิดพลาดของฉันเองที่ไม่สามารถเรียนรู้ได้จากสื่อการเรียนการสอน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    ctrl3 = st.select_slider(label='ถ้าฉันมีความพยายามที่เพียงพอ ฉันจะสามารถเรียนรู้และทำความเข้าใจกับสื่อการเรียนการสอนรายวิชานี้ได้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    ctrl4 = st.select_slider(label='เป็นเพราะฉันไม่มีความพยายามที่มากพอ จึงเป็นเหตุให้ฉันไม่สามารถทำความเข้าใจเนื้อหาในสื่อการเรียนการสอน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)    

    sef1 = st.select_slider(label='ฉันเชื่อว่าฉันสามารถที่จะได้เกรดที่ดีจากรายวิชานี้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    sef2 = st.select_slider(label='ฉันสามารถยืนยันได้ว่า ฉันสามารถเข้าใจไม่ว่ามันจะยากแค่ไหนก็ตามจากสื่อการเรียนการสอนในรายวิชานี้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    sef3 = st.select_slider(label='ฉันมีความเชื่อมั่นว่า ฉันสามารถทำความเข้าใจความคิดพื้นฐานเกี่ยวกับรายวิชานี้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    sef4 = st.select_slider(label='ฉันเชื่อมั่นว่า ฉันสามารถเข้าใจเนื้อหา ใจความสำคัญ ที่นำเสนอด้วยสื่อการเรียนการสอนนี้ได้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    sef5 = st.select_slider(label='ฉันเชื่อมั่นว่าฉันจะตั้งใจทำอย่างสุดความสามารถในงานที่ได้รับมอบหมายจากการเรียนในรายวิชานี้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    sef6 = st.select_slider(label='ฉันคาดหวังว่าฉันจะตั้งใจเรียนให้มากที่สุดในรายวิชานี้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    sef7 = st.select_slider(label='ฉันยืนยันว่า ฉันสามารถมีทักษะในการถ่ายทอดความรู้ที่ได้เรียนจากรายวิชานี้ได้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    sef8 = st.select_slider(label='ฉันคิดว่าจะประสบความสำเร็จในการเรียนรายวิชานี้ถึงแม้จะยากด้วยการมีอาจารย์ที่ดีและเก่ง บวกด้วยทักษะ และความสามารถของฉัน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)    

    test1 = st.select_slider(label='เมื่อฉันต้องเข้าทำการทดสอบ ฉันคิดว่าคงทำได้ไม่ดีเท่าเพื่อนคนอื่นๆ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    test2 = st.select_slider(label='เมื่อฉันต้องเข้าทำการทดสอบ ฉันคิดว่ามีหลยข้อที่ไม่สามารถทำได้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    test3 = st.select_slider(label='-เมื่อฉันต้องเข้าทำการทดสอบ ฉันคิดว่าฉันจะตก', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    test4 = st.select_slider(label='ฉันรู้สึกไม่สบายใจ กังวลในขณะสอบ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    test5 = st.select_slider(label='ฉันรู้สึกหัวใจเต้นแรง ตื่นเต้นในการเข้าสอบทุกครั้ง', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
 
    time1 = st.select_slider(label='ฉันมักหาสถานที่ที่เหมาะสมในการศึกษาทบทวนเนื้อหาที่ได้เรียนไป', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    time2 = st.select_slider(label='ฉันแบ่งเวลาระหว่างการเรียนกับเรื่องอื่นได้อย่างพอดีลงตัว', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    time3 = st.select_slider(label='ฉันคิดว่าเป็นการยากถ้าจะมีการกำหนดตารางเวลาในการเรียน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    time4 = st.select_slider(label='ฉันมีที่ส่วนตัวและใช้เป็นที่ทบทวนความรู้นอกห้องเรียนเป็นประจำดี', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    time5 = st.select_slider(label='ฉันพยายามที่จะอ่านทบทวนหนังสือและทำรายงานทุกสัปดาห์เมื่อได้รับมอบหมาย', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    time6 = st.select_slider(label='ฉันเข้าเรียนบ่อยๆและเป็นประจำ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    time7 = st.select_slider(label='ฉันรู้สึกว่าฉันไม่ค่อยตั้งใจเรียนเนื่องจากเอาเวลาไปทำกิจกรรมอื่นๆมากกว่า', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    time8 = st.select_slider(label='ฉันจะกำหนดและหาเวลาในการทบทวน ศึกษา อ่านหนังสือก่อนสอบ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)    

    eff1 = st.select_slider(label='ฉันรู้สึกขี้เกียจและเบื่อเป็นประจำทุกครั้ง และจะเลิกก่อนเป็นประจำในการวางแผนทบทวนบทเรียน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    eff2 = st.select_slider(label='ฉันจะตั้งใจและจะทำอย่างเต็มที่ถึงแม้ว่าฉันจะไม่ชอบก็ตาม', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    eff3 = st.select_slider(label='เมื่อใดก็ตามที่ฉันรู้สึกว่าเรื่องที่เรียนมันยาก ฉันจะเลิกสนใจมัน แต่ฉันจะมองในมุมกลับกันว่ามันง่ายต่อความเข้าใจ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    eff4 = st.select_slider(label='เมื่อใดก็ตามที่สื่อการเรียนการสอนมันยากต่อการทำความเข้าใจ ฉันก็จะตั้งใจดูและศึกษาจากสื่อการเรียนการสอนนั้นๆถึงแม้ว่าจะไม่เข้าใจก็ตาม', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)    

    peer1 = st.select_slider(label='ฉันพยายามที่จะบรรยายและอธิบายให้เพื่อนฟังเสมอๆเกี่ยวกับสื่อการเรียนการสอน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    peer2 = st.select_slider(label='ฉันพยายามทำงานและเรียนร่วมกันกับเพื่อนในการทำรายงานและศึกษาเรียนรู้', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    peer3 = st.select_slider(label='ฉันมักจะหาเวลาในการพูดคุย สรุป อภิปรายกับเพื่อนเกี่ยวกับเรื่องที่เรียนจากอาจารย์และรายละเอียดจากสื่อการเรียนการสอน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)

    help1 = st.select_slider(label='ฉันพยายามแก้ปัญหาด้วยตนเองก่อนเป็นอันดับแรก ถึงแม้ว่าการเรียนการสอนในชั้นเรียนจากอาจารย์หรือสื่อการเรียนการสอนจะยากต่อความเข้าใจ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    help2 = st.select_slider(label='ฉันจะถามอาจารย์ผู้สอนทุกครั้งเพื่อความเข้าใจในเรื่องที่ฉันยังสับสนและยังไม่เข้าใจ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    help3 = st.select_slider(label='เมื่อฉันไม่เข้าใจเกี่ยวกับเนื้อหาหรือความรู้จากเอกสารประกอบการสอนหรือสื่อการเรียนการสอน ฉันมักจะถามเพื่อน', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)
    help4 = st.select_slider(label='ฉันพยายามที่จะค้นหาและแยกแยะเพื่อนร่วมชั้นเรียนที่สามารถช่วยฉันในการเรียนและเป็นประโยชน์กับตัวฉัน ', 
        options= rating_option,format_func=lambda x: convert_options.get(x),value=4)    

    reh = (reh1+reh2+reh3+reh4)/4
    ela = (ela1+ela2+ela3+ela4+ela5+ela6)/6
    org = (org1+org2+org3+org4)/4
    cri = (cri1+cri2+cri3+cri4+cri5)/5
    meta = (meta1+meta2+meta3+meta4+meta5+meta6+meta7+meta8+meta9+meta10+meta11+meta12)/12
    igo = (igo1+igo2+igo3+igo4)/4
    ego = (ego1+ego2+ego3+ego4)/4
    task = (task1+task2+task3+task4+task5+task6)/6
    ctrl = (ctrl1+ctrl2+ctrl3+ctrl4)/4
    sef = (sef1+sef2+sef3+sef4+sef5+sef6+sef7+sef8)/8
    test = (test1+test2+test3+test4+test5)/5
    time = (time1+time2+time3+time4+time5+time6+time7+time8)/8
    eff = (eff1+eff2+eff3+eff4)/4
    peer =(peer1+peer2+peer3)/3
    help = (help1+help2+help3+help4)/4
    
    
    
    if st.button('พยากรณ์'):
        st.balloons()
        input_data = (sex,math,sci,comsci,thai,eng,reh,ela,org,cri,meta,igo,ego,task,ctrl,sef,test,time,eff,peer,help)

        # changing the input_data to numpy array
        input_data_as_numpy_array = np.asarray(input_data)

        # reshape the array as we are predicting for one instance
        input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

        prediction = clf.predict(input_data_reshaped)
        print(prediction)
        if prediction==[4] :
            predic=4
        elif prediction==[3] :
            predic=3
        elif prediction==[2] :
            predic=2
        elif prediction==[1] :
            predic=1
        else :
            predic=0
        input_sheet = (school_name,class_room,stu_name,stu_id,sex,math,sci,comsci,thai,eng,reh,ela,org,cri,meta,igo,ego,task,ctrl,sef,test,time,eff,peer,help,predic)
        sheet.insert_row(input_sheet,2)
        
        if prediction==[4] :
            st.success('บันทึกผลการพยากรณ์สำเร็จ : ผลการพยากรณ์พบว่า ผลการเรียนของคุณอาจอยู่ในระดับดีมาก')
        elif prediction==[3] :
            st.success('บันทึกผลการพยากรณ์สำเร็จ : ผลการพยากรณ์พบว่า ผลการเรียนของคุณอาจอยู่ในระดับดี')
        elif prediction==[2] :
            st.success('บันทึกผลการพยากรณ์สำเร็จ : ผลการพยากรณ์พบว่า ผลการเรียนของคุณอาจอยู่ในระดับปานกลาง')
        elif prediction==[1] :
            st.success('บันทึกผลการพยากรณ์สำเร็จ : ผลการพยากรณ์พบว่า ผลการเรียนของคุณอาจอยู่ในระดับต่ำ')
        else :
            st.success('บันทึกผลการพยากรณ์สำเร็จ : ผลการพยากรณ์พบว่า ผลการเรียนของคุณอาจอยู่ในระดับที่ตำมาก')


if __name__=='__main__':
    main()
