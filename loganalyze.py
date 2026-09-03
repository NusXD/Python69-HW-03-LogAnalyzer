def analyze_user_activity(log_file_path: str) -> dict:
    actions = {} #เก็บแบบ ทำอะไรไป : ครั้ง
    user_time = {} #เก็บเป็น user: เวลา
    users = set() #เก็บไม่ซ้ำ
    login_times = [] #เก็บเวลา คือทีแต่ เวลา เรียงงกัน 
    
    
    with open(log_file_path, "r") as file: # เปิดไฟล์ log แบบอ่านอย่างเดียว
        for line in file:  #อ่านที่ละบรรทัด
            data = line.split() # แยกข้อมูลแต่ละช่อง

            if len(data) != 4: #อันนี้ ถ้าไม่ครบ 4 อย่างทำ loop ต่อไป
                continue

            date, user, action, time = data # 4 อย่าง

            try: #อันนี้คือแปลงเวลาเป็น float ถ้าไม่ใช่ตัวเลขก็ข้ามไป
                time = float(time)
            except ValueError:
                continue

            actions[action] = actions.get(action, 0) + 1 #อันนี้คือเก็บจำนวนครั้งที่ทำ action นั้นๆ แบบ actions.get(action, 0) + 1 คือถ้าไม่มี action อันนี้ ก็เริ่มจาก 0 มีแล้วก็ +1
            users.add(user) #เก็บ user แบบไม่ซ้ำ

            if action == "login": #ถ้า action เป็น login 
                login_times.append(time) #เก็บเวลาของ login เท่านั้น
                user_time[user] = time #เก็บ user ที่ login และเวลา login ของ user นั้นๆ
 
    average = sum(login_times) / len(login_times) if login_times else 0 #คำนวณค่าเฉลี่ยของเวลา login ถ้า login_times ไม่มีข้อมูลเซ็ทเป็น 0
    most_active = max(user_time, key=user_time.get) if user_time else None #หาผู้ใช้ที่ active มากที่สุด โดยใช้ max() กับ user_time และ key=user_time.get เพื่อหาค่ามากที่สุด ถ้าไม่มี user_time ก็เซ็ทเป็น None

    return { 
        "action_counts": actions,
        "average_session_time": average,
        "most_active_user": most_active,
        "total_users": len(users)
    }


if __name__ == "__main__":
    result = analyze_user_activity("activity.log")
    from pprint import pprint
    pprint(result)

# {'action_counts': {'login': 2, 'logout': 2, 'submit': 1, 'view': 2},
#  'average_session_time': 160.0,
#  'most_active_user': 'u002',
#  'total_users': 2}

# 2025-08-01T10:00:00 u001 login 120
# 2025-08-01T10:02:05 u002 login 200
# 2025-08-01T10:04:00 u001 view 0
# 2025-08-01T10:06:30 u001 submit 30
# 2025-08-01T10:07:00 u002 view 0
# 2025-08-01T10:07:30 u002 logout 0
# 2025-08-01T10:09:00 u001 logout 0
