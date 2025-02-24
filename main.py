from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import bs4
import time
import random
import pandas as pd
import json
import os
from dotenv import load_dotenv
load_dotenv()


URL = os.getenv('URL')

options = webdriver.ChromeOptions()
options.add_argument('--disable-tensorflow')  # ปิดการใช้งาน TensorFlow
options.add_argument('--disable-software-rasterizer')  # ปิดการประมวลผลกราฟฟิก
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options=options)

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