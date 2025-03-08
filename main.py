from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import bs4
import time
import pandas as pd
import random
import os
import re
import json
from dotenv import load_dotenv
# ระบุไฟล์ .env โดยตรง
load_dotenv(dotenv_path=".env")

URL = os.getenv("URL")

def find_answer_exams():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-tensorflow')  # ปิดการใช้งาน TensorFlow
    options.add_argument('--disable-software-rasterizer')  # ปิดการประมวลผลกราฟฟิก
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=options)

    print(f"URL: {URL}, Type: {type(URL)}")

    driver.get(URL)

    time.sleep(1)
    driver.execute_script("document.body.style.zoom='70%'")



    def generate_random_answer():
        answers = [
            "ไหมไทย หัวใจสิน",
            "มนแคนต์ แก่นคูณ",
            "ลำไย ไห",
            "ติ๊ก ชีโร่"
        ]
        return random.choice(answers)


    try:
        # ดึงข้อมูลหน้าเว็บ
        data = driver.page_source
        soup = bs4.BeautifulSoup(data, "html.parser")
        list_items = soup.select(
            '#mG61Hd > div.RH5hzf.RLS9Fe > div.lrKTG > div.o3Dpx > div')

        # วนลูปผ่านแต่ละ item
        for index, item in enumerate(list_items, 1):
            # 1. ตรวจสอบและจัดการกับ Radio options (ช้อยข้อสอบ)
            radio_options = driver.find_elements(By.CSS_SELECTOR,
                                                f"#mG61Hd > div.RH5hzf.RLS9Fe > div.lrKTG > div.o3Dpx > div:nth-child({index}) div[role='radio']")

            if radio_options:
                # สุ่มเลือกตัวเลือก (ยกเว้นตัวเลือกแรกถ้าเป็น "เลือก")
                valid_options = radio_options[1:] if len(
                    radio_options) > 1 else radio_options
                if valid_options:
                    random_option = random.choice(valid_options)
                    option_text = random_option.text.strip()
                    driver.execute_script("arguments[0].scrollIntoView();", random_option)
                    driver.execute_script("arguments[0].click();", random_option)
                    print(f"เลือกช้อยข้อสอบ: {option_text}")
                    time.sleep(0.5)
                    continue

            # 2. ตรวจสอบ Text input
            text_inputs = driver.find_elements(By.CSS_SELECTOR,
                                            f"#mG61Hd > div.RH5hzf.RLS9Fe > div.lrKTG > div.o3Dpx > div:nth-child({index}) input[type='text']")
            if text_inputs:
                answer = generate_random_answer()
                text_inputs[0].send_keys(answer)
                print(f"กรอกข้อความ: {answer}")
                continue

            # 3. ตรวจสอบ Dropdown
            dropdown = driver.find_elements(By.CSS_SELECTOR, 
                ".MocG8c.HZ3kWc.mhLiyf.LMgvRb.KKjvXb.DEh1R")

            if dropdown:
                # เลื่อน dropdown เข้ามาใน viewport
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown[0])
                time.sleep(0.5)  # ให้เวลา UI โหลด

                print(f"Dropdownมี: {len(dropdown)}ตัว")

                # คลิกที่ตัวเลือกแรก (เลือก)
                driver.execute_script("arguments[0].scrollIntoView();", dropdown[0])
                driver.execute_script("arguments[0].click();", dropdown[0])
                time.sleep(1)

                # เลือกตัวเลือกอื่นใน dropdown
                options = driver.find_elements(By.CSS_SELECTOR, 
                    ".MocG8c.HZ3kWc.mhLiyf.LMgvRb.KKjvXb.DEh1R[aria-selected='false']")

                if options:
                    random_option = random.choice(options)
                    driver.execute_script("arguments[0].scrollIntoView();", random_option)
                    driver.execute_script("arguments[0].click();", random_option)
                    print(f"เลือกตัวเลือกจาก dropdown: {random_option.text.strip()}")
                    time.sleep(0.5)



            # 4. ตรวจสอบ Radio ในรูปแบบอื่น
            other_radio_options = driver.find_elements(By.CSS_SELECTOR,
                                                        f"#mG61Hd > div.RH5hzf.RLS9Fe > div.lrKTG > div.o3Dpx > div:nth-child({index}) div[role='option']")
            if other_radio_options:
                valid_options = [
                    opt for opt in other_radio_options if opt.text.strip() != "เลือก"]
                if valid_options:
                    random_option = random.choice(valid_options)
                    option_text = random_option.text.strip()
                    driver.execute_script("arguments[0].scrollIntoView();",random_option)
                    driver.execute_script("arguments[0].click();", random_option)
                    print(f"เลือกตัวเลือก radio: {option_text}")
                    time.sleep(0.5)
                continue
        
        time.sleep(1)

        # ใช้ JavaScript เพื่อคลิกปุ่ม
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Submit']")
            driver.execute_script("arguments[0].click();", submit_button)
            print("\n########### กดปุ่ม 'ส่ง' สำเร็จ ###########\n")
        except NoSuchElementException:
            print("ไม่พบปุ่มส่ง (Submit button) บนหน้าเว็บ")
            submit_button = driver.find_elements(By.CSS_SELECTOR, "div[role='button']")
            for idx, btn in enumerate(submit_button):
                print(f'ข้อความในButtonที่ {idx} role=button: {btn.text}')

                if "ถัดไป" in btn.text.strip():
                    driver.execute_script("arguments[0].click();", btn)
                    print("\n########### กดปุ่ม 'ถัดไป' สำเร็จ ###########\n")



    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {str(e)}")



    # เลือกช้อยแบบสุ่ม
    try:
        # ดึงรายการ Radio Group ทั้งหมด
        radio_groups = driver.find_elements(By.CSS_SELECTOR, 'div[role="radiogroup"]')

        for idx, group in enumerate(radio_groups):
            print(f"\n🔹 รายการที่ {idx + 1}\n{'-'*30}")

            # หา radio options ในกลุ่มนั้น
            radio_options = group.find_elements(By.CSS_SELECTOR, 'div[role="radio"]')

            # กรองตัวเลือกที่ยังไม่ได้เลือก (aria-checked="false")
            unchecked_options = [opt for opt in radio_options if opt.get_attribute("aria-checked") == "false"]

            if unchecked_options:
                # สุ่มเลือก 1 ตัวจากตัวเลือกที่ยังไม่ถูกเลือก
                random_choice = random.choice(unchecked_options)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", random_choice)
                time.sleep(0.5)  # หน่วงเวลาให้ UI โหลด

                # คลิกเลือกตัวเลือก
                driver.execute_script("arguments[0].scrollIntoView();", random_choice)
                driver.execute_script("arguments[0].click();", random_choice)
                print(f"✅ เลือก: {random_choice.get_attribute('aria-label')}")

            else:
                print("⚠️ ไม่มีตัวเลือกที่ยังไม่ได้เลือก")

            time.sleep(1)  # พักก่อนเลือกกลุ่มถัดไป

    except Exception as e:
        print(f"EXCEPT: {e}")

    submit_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Submit']")
    driver.execute_script("arguments[0].click();", submit_button)
    print("\n########### กดปุ่ม 'ส่ง' สำเร็จ ###########\n")

    # รอให้ปุ่ม 'ดูคะแนน' โหลด
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='presentation']")))

    # ค้นหาปุ่ม 'ดูคะแนน'
    view_score = driver.find_elements(By.CSS_SELECTOR, "div[role='presentation']")

    for idx, btn in enumerate(view_score):
        text = btn.text.strip()
        print(f'ข้อความใน Button ที่ {idx}: {repr(text)}')

        if "ดูคะแนน" in text:
            print(f"\n🎯 พบปุ่มที่ตรงกับ 'ดูคะแนน' กำลังกด...\n")

            # เลื่อนให้ปุ่มอยู่ตรงกลางก่อนกด
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)

            # รอให้ปุ่มสามารถคลิกได้
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(btn))

            try:
                btn.click()  # กดปุ่ม
                print("\n✅ กดปุ่ม 'ดูคะแนน' สำเร็จ (click)\n")
            except Exception as e:
                print(f"❌ เกิดข้อผิดพลาดในการคลิกปุ่ม: {e}")
                driver.execute_script("arguments[0].click();", btn)  # คลิกด้วย JS
                print("\n✅ กดปุ่ม 'ดูคะแนน' สำเร็จ (JS click)\n")

    # สลับแท็บไปแท็บใหม่
    time.sleep(2)
    # ดึงรายการ window handles ทั้งหมด
    tabs = driver.window_handles

    # สลับไปยังแท็บใหม่ (แท็บล่าสุด)
    driver.switch_to.window(tabs[-1])

    print("✅ เปลี่ยนไปที่แท็บใหม่สำเร็จ!")

    # รอให้ element โหลดเสร็จ ก่อนที่จะทำการดึงข้อมูล
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "label.docssharedWizToggleLabeledContainer.LygNqb.N2RpBe.O4MBef.RDPZE")))

    driver.execute_script("document.body.style.zoom='70%'")

    # ดึงข้อมูลคำตอบที่ถูกต้อง
    correct_label = driver.find_elements(By.CSS_SELECTOR, "label.docssharedWizToggleLabeledContainer.LygNqb.N2RpBe.O4MBef.RDPZE")
    # รายการที่จะเก็บข้อมูลคำตอบที่ถูกต้อง
    correct_answers = []

    print(f"พบ {len(correct_label)} รายการที่ต้องตรวจสอบ\n")
    i = 1
    for idx, label in enumerate(correct_label):
        # ใช้ xpath เพื่อหา div ลูกตรงๆ ของ label
        div_children = label.find_elements(By.XPATH, "./div")
        
        # ตรวจสอบว่าใน div ลูกตรงๆ มี aria-label="ไม่ถูกต้อง"
        invalid_div = label.find_elements(By.XPATH, ".//div[@aria-label='ไม่ถูกต้อง']")
        
        # ข้ามกรณีที่พบ div ที่มี aria-label="ไม่ถูกต้อง"
        if invalid_div:
            # print(f"ข้อที่ {idx+1} ข้าม เพราะมี div ที่มี aria-label='ไม่ถูกต้อง'")
            continue

        correct_answers.append({
            "question": i,
            "anwser": label.text
        })

        print(f"\033[1;32mข้อที่ {i} ตอบ:\033[0m {label.text}")  # ใช้สีเขียวสำหรับข้อความที่ถูกต้อง
        
        i+=1
        print('-' * 50)  # แสดงเส้นแบ่งเพื่อให้อ่านง่ายขึ้น


    # บันทึกข้อมูลคำตอบที่ถูกต้องลงในไฟล์ JSON
    try:
        with open("correct_answers.json", "w", encoding="utf-8") as json_file:
            json.dump(correct_answers, json_file, ensure_ascii=False, indent=4)
            print("\n✅ บันทึกข้อมูลคะแนนที่ถูกต้องสําเร็จ!\n")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการบันทึกข้อมูล: {e}")

    # ปิดหน้าเว็บ
    time.sleep(3)
    driver.quit()

def answer_exams():
    delay = 2
    def open_website():
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-tensorflow')  # ปิดการใช้งาน TensorFlow
        options.add_argument('--disable-software-rasterizer')  # ปิดการประมวลผลกราฟฟิก
        options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        driver = webdriver.Chrome(options=options)

        driver.get(URL)

        time.sleep(delay)
        driver.execute_script("document.body.style.zoom='70%'")
        return driver

    driver = open_website()

    """

    กรอก Input Text

    """

    # Load environment variables from .env file
    SCHOOL = os.getenv('SCHOOL')
    NUMBER_STUDENT = os.getenv('NUMBER_STUDENT')
    PREFIX = os.getenv('PREFIX')
    NAME = os.getenv('NAME')
    CLASS = os.getenv('CLASS')
    NO = os.getenv('NO')

    # ค่าที่ต้องกรอกลงในแต่ละช่อง
    input_data = {
        "ชื่อโรงเรียน": SCHOOL,
        "เลขประจำตัวนักเรียน": NUMBER_STUDENT,
        "คำนำหน้าชื่อ": PREFIX,
        "ชื่อ-สกุล": NAME,
        "ระดับชั้น": CLASS,
        "เลขที่": NO
    }

    # ดึงข้อมูลหน้าเว็บ
    data = driver.page_source
    soup = bs4.BeautifulSoup(data, "html.parser")
    list_items = soup.select(
        '#mG61Hd > div.RH5hzf.RLS9Fe > div.lrKTG > div.o3Dpx > div')

    for index, item in enumerate(list_items, 1):
        text = item.text.split(" ")[0]  # ดึงเฉพาะข้อความหัวข้อ
        # Check text
        text_inputs = driver.find_elements(By.CSS_SELECTOR,
                                    f"#mG61Hd > div.RH5hzf.RLS9Fe > div.lrKTG > div.o3Dpx > div:nth-child({index}) input[type='text']")
        if text_inputs:
            text_inputs[0].send_keys(input_data[text])
            print(f'✅ กรอกข้อมูลช่อง "{text}" เสร็จ')

    """

    กรอก Input Radio, Dropdown

    """

    # ดึงข้อมูลหน้าเว็บ
    data = driver.page_source
    soup = bs4.BeautifulSoup(data, "html.parser")
    list_items = soup.select(
        '#mG61Hd > div.RH5hzf.RLS9Fe > div.lrKTG > div.o3Dpx > div')

    for index, item in enumerate(list_items, 1):
        text = item.text.split(" ")[0]  # ดึงเฉพาะข้อความหัวข้อ

        # ตรวจสอบ Dropdown ของ index ปัจจุบัน
        dropdowns = driver.find_elements(By.CSS_SELECTOR, 
            f"#mG61Hd > div.RH5hzf.RLS9Fe > div.lrKTG > div.o3Dpx > div:nth-child({index}) .MocG8c.HZ3kWc.mhLiyf.LMgvRb.KKjvXb.DEh1R")

        if dropdowns:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdowns[0])
            time.sleep(0.5)  # ให้เวลา UI โหลด

            print(f"📌 พบ Dropdown ในช่อง: {text}")

            # คลิกเปิด dropdown
            driver.execute_script("arguments[0].click();", dropdowns[0])
            time.sleep(1)

            # เลือกตัวเลือกอื่นใน radio dropdown other
            options = driver.find_elements(By.CSS_SELECTOR, 
                f"#mG61Hd > div.RH5hzf.RLS9Fe > div.lrKTG > div.o3Dpx > div:nth-child({index}) div[role='option']")
            
            valid_options = [
                opt for opt in options if opt.text.strip() != "เลือก"]
            
            # เลือกค่าจาก .env หากมี
            if text in input_data or options:
                selected_option = None
                for op in valid_options:
                    time.sleep(1)
                    option = op.text.replace('ม.', '')
                    # print(f"{option}, {input_data[text]}, {option == input_data[text]}")

                    if option == input_data[text]:
                        selected_option = op
                        print(f'เจอ {input_data[text]} selected_option: {op.text}')
                        break
                
                # ถ้าพบตัวเลือกที่ตรงกับค่าจาก .env ให้เลือก
                if selected_option:
                    driver.execute_script("arguments[0].scrollIntoView();", selected_option)
                    driver.execute_script("arguments[0].click();", selected_option)
                    print(f"✅ เลือก {input_data['ระดับชั้น']} ในช่อง {text}")
                else:
                    print(f"⚠️ ไม่พบค่าที่ตรงกันใน dropdown สำหรับ '{text}'")
            
            time.sleep(1)

    # กดปุ่มถัดไป เพื่อไปหน้าทำข้อสอบ
    want_click_name = 'ถัดไป'
    try:
        submit_button = driver.find_elements(By.CSS_SELECTOR, "div[role='button']")
        i = 0
        for btn in submit_button:
            if btn.text.strip() == want_click_name:  # เช็คข้อความปุ่มที่ trim ช่องว่าง
                driver.execute_script("arguments[0].click();", btn)
                print(f"\n###########📩 กดปุ่ม '{want_click_name}' สำเร็จ ###########\n")
                i+=1
        if i <= 0:
            print(f"❌ไม่พบปุ่ม '{want_click_name}'")

    except Exception as e:
        print(e)

    """

    นำคำตอบจาก JSON มากรอก Input Radio, Dropdown

    """

    # ดึงข้อมูลหน้าเว็บ
    data = driver.page_source
    soup = bs4.BeautifulSoup(data, "html.parser")
    list_items = soup.select('div[role=listitem]')

    # โหลด JSON
    with open('correct_answers.json', 'r', encoding='utf-8') as file:
        correct_answers = json.load(file)

    # สร้าง dictionary ของคำตอบ
    answer_dict = {item['question']: item['anwser'].strip() for item in correct_answers}

    # วนลูปผ่านแต่ละข้อในหน้าเว็บ
    for index, item in enumerate(list_items, 1):
        try:
            print(f"กำลังตรวจสอบข้อที่ {index}")
            
            # ดูว่ามีคำถามในข้อนี้หรือไม่
            question_elem = item.select_one('div[role="heading"]')
            if not question_elem:
                print(f"⚠️ ไม่พบหัวข้อคำถามในข้อที่ {index}")
                continue
                
            # ดึงหมายเลขข้อจากข้อความคำถาม
            question_text = question_elem.get_text().strip()
            question_num_match = re.search(r'(\d+)\.', question_text)
            
            if question_num_match:
                question_num = int(question_num_match.group(1))
                print(f"พบคำถามข้อที่: {question_num}")
                
                # ค้นหาคำตอบจาก dictionary
                if question_num in answer_dict:
                    correct_answer_text = answer_dict[question_num]
                    print(f"คำตอบที่ถูกต้องคือ: {correct_answer_text}")
                    
                    # หาตัวเลือกทั้งหมด
                    radio_options = item.select('div.Od2TWd.hYsg7c')
                    
                    # ตรวจสอบว่ามีตัวเลือกหรือไม่
                    if not radio_options:
                        print("⚠️ ไม่พบตัวเลือกในข้อนี้")
                        continue
                    
                    # หาตัวเลือกที่ตรงกับคำตอบที่ถูกต้อง
                    found_match = False
                    for radio in radio_options:
                        label_text = radio.get('aria-label', '').strip()
                        
                        # เช็คว่าตัวเลือกนี้ตรงกับคำตอบหรือไม่
                        if label_text == correct_answer_text or correct_answer_text.startswith(label_text[:2]):
                            # ใช้ selenium คลิกเลือก
                            radio_id = radio.get('id')
                            if radio_id:
                                try:
                                    driver.find_element(By.ID, radio_id).click()
                                    print(f"✅ เลือกตัวเลือก ID: {radio_id} - {label_text}")
                                    found_match = True
                                    break
                                except Exception as e:
                                    print(f"⚠️ ไม่สามารถคลิกตัวเลือก: {str(e)}")
                    
                    if not found_match:
                        print(f"⚠️ ไม่พบตัวเลือกที่ตรงกับคำตอบ: {correct_answer_text}")
                else:
                    print(f"⚠️ ไม่พบคำตอบสำหรับข้อที่ {question_num} ในไฟล์ JSON")
            else:
                print(f"⚠️ ไม่สามารถระบุหมายเลขข้อจากคำถาม: {question_text}")
        
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {str(e)}")


    # กดปุ่มส่ง เพื่อรับ 10คะแนนแบบโปรๆ
    want_click_name = 'ส่ง'
    try:
        submit_button = driver.find_elements(By.CSS_SELECTOR, "div[role='button']")
        i = 0
        for btn in submit_button:
            if btn.text.strip() == want_click_name:  # เช็คข้อความปุ่มที่ trim ช่องว่าง
                driver.execute_script("arguments[0].click();", btn)
                print(f"\n###########📩 กดปุ่ม '{want_click_name}' สำเร็จ ###########\n")
                i+=1
        if i <= 0:
            print(f"❌ไม่พบปุ่ม '{want_click_name}'")

    except Exception as e:
        print(e)

    # กดปุ่มดูคะแนนไปเพื่อแคปหน้าจอ
    want_click_name = 'ดูคะแนน'
    try:
        submit_button = driver.find_elements(By.CSS_SELECTOR, 'a[aria-label="ดูคะแนน"]')
        i = 0
        for btn in submit_button:
            if btn.text.strip() == want_click_name:  # เช็คข้อความปุ่มที่ trim ช่องว่าง
                driver.execute_script("arguments[0].click();", btn)
                print(f"\n###########📩 กดปุ่ม '{want_click_name}' สำเร็จ ###########\n")
                i+=1
        if i <= 0:
            print(f"❌ไม่พบปุ่ม '{want_click_name}'")

    except Exception as e:
        print(e)

    # สลับแท็บไปแท็บใหม่
    time.sleep(1)
    # ดึงรายการ window handles ทั้งหมด
    tabs = driver.window_handles

    # สลับไปยังแท็บใหม่ (แท็บล่าสุด)
    driver.switch_to.window(tabs[-1])

    print("✅ เปลี่ยนไปที่แท็บใหม่สำเร็จ!")

    try:
        # รอให้ Element ปรากฏ
        wait = WebDriverWait(driver, 10)
        score_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div > div:nth-child(2) > div:nth-child(1) > div > div.Dq4amc > div > div.N0gd6 > div.ahS2Le > div.tV8Uvb")))

        # ดึงคะแนน
        score_text = score_element.text
        print(f"คะแนนรวม: {score_text}")

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

    print("\n" + "="*50)
    print("🏆ภาระกิจทำข้อสอบอัตโนมัติเสร็จสิ้น💯")
    print("="*50 + "\n")

    # แคปหน้าจอ
    try:
        score = driver.find_elements(By.CSS_SELECTOR, 'div.tV8Uvb')
        driver.save_screenshot("mobile_screenshot.png")
        print("แคปหน้าจอเสร็จแล้ว! บันทึกที่ mobile_screenshot.png")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    find_answer_exams()
    print("✅ ดึงข้อมูลคะแนนที่ถูกต้องสําเร็จ!\n")

    # อ่านข้อมูลคะแนนที่ถูกต้องจากไฟล์ JSON
    answer_exams()