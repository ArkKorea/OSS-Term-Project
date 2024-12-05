import tkinter as tk
from tkinter import ttk
import pymysql  # 관계형 데이터베이스 활용
import bcrypt  # 비밀번호 해싱
import re  # 정규 표현식 사용
import exercise as ex # 만든 운동 함수 사용

#각 페이지 뭐 있을지 만들기
#모든 페이지의 부모 클래스
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Health Care Project")
        self.geometry("600x400")

        self.id = ""

        # 데이터베이스 연결
        self.db = pymysql.connect(
            user='root',
            passwd='root',
            host='127.0.0.1',
            db='testdb',
            charset='utf8'
        )
        self.cursor = self.db.cursor()

        # 프레임 컨테이너
        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill="both")
        self.frames = {}
        self.current_frame = None

        self.show_frame(StartScreen)

    def show_frame(self, frame_class):
        page_name = frame_class.__name__
        if page_name == "StartScreen" and self.current_frame.__class__.__name__ == "MainScreen":
            self.id = ""
        frame = self.frames.get(page_name)
        if frame is None:
            frame = frame_class(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.tkraise()

        if self.current_frame is not None and self.current_frame != frame:
            self.current_frame.destroy()
            del self.frames[self.current_frame.__class__.__name__]
        
        self.current_frame = frame

    # 회원가입 내용 DB 저장
    def register_user(self, id, pw, first_name, last_name):
        try:
            hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
            sql = "INSERT INTO user (id, pw, first_name, last_name) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql, (id, hashed_pw, first_name, last_name))
            self.db.commit()
            return True
        except Exception as e:
            return False

    # 로그인 확인
    def validate_login(self, id, pw):
        sql = "SELECT pw FROM user WHERE id = %s"
        self.cursor.execute(sql, (id,))
        result = self.cursor.fetchone()
        if result:
            stored_pw = result[0]
            return bcrypt.checkpw(pw.encode('utf-8'), stored_pw.encode('utf-8'))
        return False

    # 회원가입 시 패스워드 기준 확인 10자 이상 20자 미만, 대문자 포함
    def validate_password(self, pw):
        if len(pw) <= 10 and len(pw) > 20:
            return False
        elif not re.search(r'[A-Z]', pw):
            return False
        return True
    
    def show_popup(self, title, message):
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.geometry("300x80")
        label = tk.Label(popup, text=message)
        label.pack(side="top", fill="x", pady=10)
        ok_button = tk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack(side="right", pady=5)

# 로그인 화면
class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Login", font=("Arial", 15))
        label.grid(row=0, column=1, pady=10)

        self.id = tk.StringVar()
        self.pw = tk.StringVar()

        id_label = ttk.Label(self, text="ID")
        id_label.grid(row=1, column=0, pady=5)
        id_entry = ttk.Entry(self, textvariable=self.id)
        id_entry.grid(row=1, column=1, pady=5)

        pw_label = ttk.Label(self, text="Password")
        pw_label.grid(row=2, column=0, pady=5)
        pw_entry = ttk.Entry(self, textvariable=self.pw, show="*")
        pw_entry.grid(row=2, column=1, pady=5)

        login_button = ttk.Button(self, text="로그인", command=self.login)
        login_button.grid(row=3, column=1, pady=5)

        sign_up_button = ttk.Button(self, text="회원가입",
                                    command=lambda: controller.show_frame(SignUpScreen))
        sign_up_button.grid(row=4, column=1, pady=5)

        go_to_start = ttk.Button(self, text="시작화면", command=lambda: controller.show_frame(StartScreen))
        go_to_start.grid(row=5, column=1, pady=5)

    def login(self):
        id = self.id.get()
        pw = self.pw.get()
        if self.controller.validate_login(id, pw):
            self.controller.id = id
            self.controller.show_frame(MainScreen)
        else:
            self.controller.show_popup("Login Failed", "아이디 혹은 비밀번호를 확인하세요")

# 회원가입 화면
class SignUpScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="회원가입", font=("Arial", 15))
        label.grid(row=0, column=1, pady=10, columnspan=2)

        self.id = tk.StringVar()
        self.pw = tk.StringVar()
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()

        first_name_label = ttk.Label(self, text="First Name")
        first_name_label.grid(row=1, column=0, pady=5)
        first_name_entry = ttk.Entry(self, textvariable=self.first_name)
        first_name_entry.grid(row=1, column=1, pady=5)

        last_name_label = ttk.Label(self, text="Last Name")
        last_name_label.grid(row=2, column=0, pady=5)
        last_name_entry = ttk.Entry(self, textvariable=self.last_name)
        last_name_entry.grid(row=2, column=1, pady=5)

        id_label = ttk.Label(self, text="ID")
        id_label.grid(row=3, column=0, pady=5)
        id_entry = ttk.Entry(self, textvariable=self.id)
        id_entry.grid(row=3, column=1, pady=5)

        pw_label = ttk.Label(self, text="Password")
        pw_label.grid(row=4, column=0, pady=5)
        pw_entry = ttk.Entry(self, textvariable=self.pw, show="*")
        pw_entry.grid(row=4, column=1, pady=5)

        sign_up_button = ttk.Button(self, text="Sign Up", command=self.sign_up)
        sign_up_button.grid(row=5, column=1, pady=5)

        back_button = ttk.Button(self, text="Back to Login",
                                 command=lambda: controller.show_frame(LoginScreen))
        back_button.grid(row=6, column=1, pady=5)

    def sign_up(self):
        id = self.id.get()
        pw = self.pw.get()
        first_name = self.first_name.get()
        last_name = self.last_name.get()

        if self.controller.validate_password(pw):
            if self.controller.register_user(id, pw, first_name, last_name):
                self.controller.show_popup("Sign Up Successed", "회원가입을 성공했습니다.")
                self.controller.show_frame(LoginScreen)
            else:
                self.controller.show_popup("Sign Up Failed", "회원가입에 실패했습니다.")
        else:
            self.controller.show_popup("Invalid Password", "비밀번호는 10자 이상 20자 이하, 대문자를 포함해야 합니다.")

# 프로그램 시작 시 초기 화면
class StartScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Health Care Project", font=("Arial",15))

        label.grid(row=0, column=1, pady=20)

        login_button = ttk.Button(self, text="로그인",
                                  command=lambda: controller.show_frame(LoginScreen))
        login_button.grid(row=1, column=1, pady=5)

        sign_up_button = ttk.Button(self, text="회원가입",
                                    command=lambda: controller.show_frame(SignUpScreen))
        sign_up_button.grid(row=2, column=1, pady=5)

#환경설정 창 제거
class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller   
        
        main_label = tk.Label(self, text="운동 목록", font=("Arial", 15))
        main_label.grid(row=0, column=0, pady=5, sticky="w")

        self.attribute_list = tk.Listbox(self, width=60, selectmode="browse")
        self.set_attribute_list()
        self.attribute_list.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.attribute_list.bind("<<ListboxSelect>>", self.get_attribute_infomation)

        menu_frame = tk.Frame(self, bg="lightgrey")
        menu_frame.grid(row=2, column=0, columnspan=5, sticky="sew")

        my_page_button = ttk.Button(menu_frame, text="마이페이지", command=lambda: controller.show_frame(MyPageScreen))
        my_page_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        bookmark_button = ttk.Button(menu_frame, text="즐겨찾기", command=lambda: controller.show_frame(BookmarkScreen))
        bookmark_button.grid(row=0, column=1, padx=5, pady=5)

        logout_button = ttk.Button(menu_frame, text="로그아웃", command=lambda: controller.show_frame(StartScreen))
        logout_button.grid(row=0, column=2, padx=5 ,pady=5)

        quit_button = ttk.Button(menu_frame, text="종료", command=lambda: controller.quit())
        quit_button.grid(row=0, column=3, columnspan=2, padx=5, pady=5, sticky="e")

    # 리스트박스 내용 선언 
    def set_attribute_list(self):
        _list = ["Squat 10회","Squat 20회","Squat 30회","Lunge 10회","Lunge 20회",
                 "Lunge 30회","Push Up 10회","Push Up 20회","Push Up 30회"]
        for idx, value in enumerate(_list):
            self.attribute_list.insert(idx, value)

    # 0 : e_id, 1 : e_name, 2 : e_repeat
    def get_attribute_infomation(self, event):
        selected_index = self.attribute_list.curselection()
        if selected_index:
            selected_index = selected_index[0] + 1
            sql = "SELECT * FROM exercise WHERE e_id = %s"
            self.controller.cursor.execute(sql, (selected_index,))
            result = self.controller.cursor.fetchone()
            self.show_attribute_popup(result)
    
    # 선택한 항목 정보 팝업 
    def show_attribute_popup(self, attribute_info):
        popup = tk.Toplevel(self)
        popup.title(attribute_info[1])
        popup.geometry("400x200")

        exercise_name = ttk.Label(popup, text=attribute_info[1])
        exercise_name.pack(side="top", fill="x", pady=10)
        
        repeat_count = ttk.Label(popup,text=f"반복횟수 : {attribute_info[2]}회")
        repeat_count.pack(side="top", fill="x", pady=10)

        popup_menu = tk.Frame(popup)
        popup_menu.pack(side="bottom", fill="x", pady=10)
        
        start_button = ttk.Button(popup_menu, text="시작", command=lambda: self.do_exercise(attribute_info[1], attribute_info[2]))
        start_button.pack(side="left", padx=5, pady=5)

        save_button = ttk.Button(popup_menu, text="저장", command=lambda: self.save_attribute(attribute_info[0]))
        save_button.pack(side="left", padx=5, pady=5)

        delete_button = ttk.Button(popup_menu, text="삭제", command=lambda: self.delete_attribute(attribute_info[0]))
        delete_button.pack(side="left", padx=5, pady=5)

        close_button = ttk.Button(popup_menu, text="닫기", command=popup.destroy)
        close_button.pack(side="left", padx=5, pady=5)

    # 즐겨찾기 추가
    def save_attribute(self, e_id):
        try:
            sql = "INSERT INTO Bookmark VALUES (%s, %s)"
            self.controller.cursor.execute(sql, (self.controller.id, e_id))
            self.controller.db.commit()
            self.controller.show_popup("Successed", "즐겨찾기에 등록되었습니다.")
        except Exception as e:
            self.controller.show_popup("Error", "이미 즐겨찾기에 등록된 운동입니다.")

    # 즐겨찾기 삭제
    def delete_attribute(self, e_id):
        sql = "DELETE FROM Bookmark WHERE id = %s AND e_id = %s"
        self.controller.cursor.execute(sql, (self.controller.id, e_id))
        #정상 제거 확인
        if self.controller.cursor.rowcount == 0:
            self.controller.show_popup("Failed", "즐겨찾기에 없는 운동입니다.")
        else:
            self.controller.show_popup("Successed", "즐겨찾기에서 제거되었습니다.")
        self.controller.db.commit()
        
    #운동하는 실제 함수 작성 상현이꺼 임포트
    def do_exercise(self, name, repeat):
        is_complete = ex.exercise(name, repeat)
        if is_complete:
            sql = "SELECT total FROM user WHERE id = %s"
            self.controller.cursor.execute(sql, (self.controller.id))
            total = self.controller.cursor.fetchone()[0] + 1
            sql = "UPDATE user SET total = %s WHERE id = %s"
            self.controller.cursor.execute(sql, (total, self.controller.id))
            self.controller.db.commit()
            self.controller.show_popup("Successed", "운동을 성공적으로 마무리 했습니다.")
        else:
            self.controller.show_popup("Failed", "운동을 실패했습니다. 다시 도전하세요!")

class MyPageScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        sql = "SELECT id, first_name, last_name, total FROM USER WHERE id = %s"
        self.controller.cursor.execute(sql, (self.controller.id))
        user_information = self.controller.cursor.fetchone()

        label = tk.Label(self, text="마이페이지", font=("Arial", 15))
        label.grid(row=0, column=0, pady=5)

        user_name = tk.Label(self, text=f"이름 : {user_information[2]} {user_information[1]}")
        user_name.grid(row=1, column=0, pady=5, sticky="w")

        user_id = tk.Label(self, text=f"아이디 : {user_information[0]}")
        user_id.grid(row=2, column=0, pady=5, sticky="w")

        user_total = tk.Label(self, text=f"총 운동횟수 : {user_information[3]}")
        user_total.grid(row=3, column=0, pady=5, sticky="w")

        back_button = ttk.Button(self, text="돌아가기", command=lambda: controller.show_frame(MainScreen))
        back_button.grid(row=4, column=0, pady=5)

#즐겨찾기에 넣은 애들을 리스트 박스로 쭉 나열하기
#즐겨찾기 목록 클릭 시 똑같이 팝업 나오게 수정하기
class BookmarkScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="즐겨찾기", font=("Arial",15))
        label.grid(row=0, column=0, pady=5)

        sql = "SELECT exercise.e_name, exercise.e_repeat FROM bookmark, user, exercise WHERE bookmark.e_id = exercise.e_id AND bookmark.id = user.id AND user.id =  %s"
        self.controller.cursor.execute(sql, (self.controller.id))
        self.controller.db.commit()

        self.bookmark_list = tk.Listbox(self, width=60, selectmode="extended")
        row = self.controller.cursor.fetchone()
        while row:
            self.bookmark_list.insert(0, row)
            row = self.controller.cursor.fetchone()

        self.bookmark_list.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsw")

        back_button = ttk.Button(self, text="Back to Main", command=lambda: controller.show_frame(MainScreen))
        back_button.grid(row=2, column=0, pady=5)

# main.py 만들어서 옮기기
if __name__ == "__main__":
    app = Application()
    app.mainloop()
