import tkinter as tk
from tkinter import ttk
from tkinter import *  # GUI
import pymysql  # 관계형 데이터베이스 활용
import bcrypt  # 비밀번호 해싱
import re  # 정규 표현식 사용
import math
from math import trunc

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        # 프로젝트 이름 정하기
        self.title("Login and Sign Up Example")
        self.geometry("600x400")
        self.config(bg="#f0f0f0")

        self.id = str

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
    def register_user(self, id, pw):
        try:
            hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
            sql = "INSERT INTO user (id, pw) VALUES (%s, %s)"
            self.cursor.execute(sql, (id, hashed_pw))
            self.db.commit()
            print("register success")
            return True
        except Exception as e:
            print(f"Error: {e}")
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

    # 회원가입 시 패스워드 기준 확인
    def validate_password(self, pw):
        if len(pw) < 10:
            return False
        elif not re.search(r'[A-Z]', pw):
            return False
        return True

# 로그인 화면
class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Login")
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

        login_button = ttk.Button(self, text="Login", command=self.login)
        login_button.grid(row=3, column=1, pady=5)

        sign_up_button = ttk.Button(self, text="Go to Sign Up",
                                    command=lambda: controller.show_frame(SignUpScreen))
        sign_up_button.grid(row=4, column=1, pady=5)

    def login(self):
        id = self.id.get()
        pw = self.pw.get()
        if self.controller.validate_login(id, pw):
            print("Login successful")
            self.controller.id = id
            #self.controller.hide_frame(LoginScreen) show_frame에 흡수
            self.controller.show_frame(MainScreen)
            # 로그인 성공 후 할 작업 추가
        else:
            print("Invalid ID or password")

# 회원가입 화면
class SignUpScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Sign Up")
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
        if self.controller.validate_password(pw):
            if self.controller.register_user(id, pw):
                print("Sign up successful")
                self.controller.show_frame(LoginScreen)
                #self.controller.hide_frame(SignUpScreen)
            else:
                self.show_popup("Sign Up Failed", "Failed to register user.")
        else:
            self.show_popup("Invalid Password", "Password must be at least 10 characters long and contain at least one uppercase letter")

    def show_popup(self, title, message):
        popup = tk.Toplevel(self)
        popup.title(title)
        label = tk.Label(popup, text=message)
        label.pack(side="top", fill="x", pady=10)
        ok_button = tk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack(side="right", pady=5)


# 프로그램 시작 시 초기 화면
class StartScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Calculator")

        label.grid(row=0, column=1, pady=20)

        login_button = ttk.Button(self, text="Login",
                                  command=lambda: controller.show_frame(LoginScreen))
        login_button.grid(row=1, column=1, pady=5)

        sign_up_button = ttk.Button(self, text="Go to Sign Up",
                                    command=lambda: controller.show_frame(SignUpScreen))
        sign_up_button.grid(row=2, column=1, pady=5)

        go_to_main_button = ttk.Button(self, text="Go to Main Screen", command=lambda: controller.show_frame(MainScreen))
        go_to_main_button.grid(row=3, column=1, pady=5)


class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
                        
        menu_frame = tk.Frame(self, bg="lightgrey")
        menu_frame.grid(row=1, column=0, columnspan=5, sticky="s")    

        my_page_button = ttk.Button(menu_frame, text="마이페이지", command=lambda: controller.show_frame(MyPageScreen))
        my_page_button.grid(row=0, column=0, padx=5, pady=5)
        my_page_button.config(style="TButton")

        edit_button = ttk.Button(menu_frame, text="즐겨찾기", command=lambda: controller.show_frame(BookmarkScreen))
        edit_button.grid(row=0, column=1, padx=5, pady=5)

        option_button = ttk.Button(menu_frame, text="옵션", command=lambda: controller.show_frame(OptionScreen))
        option_button.grid(row=0, column=2, padx=5, pady=5)

        logout_button = ttk.Button(menu_frame, text="로그아웃", command=lambda: controller.show_frame(StartScreen))
        logout_button.grid(row=0, column=3, padx=5 ,pady=5)

        quit_button = ttk.Button(menu_frame, text="종료", command=lambda: controller.quit())
        quit_button.grid(row=0, column=4, padx=5, pady=5)

        self.attribute_list = tk.Listbox(self, width=60, selectmode="extended")
        self.set_attribute_list()
        self.attribute_list.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsw")
        self.attribute_list.bind("<<ListboxSelect>>", self.get_attribute_infomation)

    # 리스트박스 내용 선언 
    def set_attribute_list(self):
        self.attribute_list.insert(0, f"삼성전자")
        self.attribute_list.insert(1, f"attribute 2")
        self.attribute_list.insert(2, f"attribute 3")
        self.attribute_list.insert(3, f"attribute 4")
        self.attribute_list.insert(4, f"attribute 5")

    # 0 : id, 1 : name, 2 : price
    def get_attribute_infomation(self, event):
        selected_index = self.attribute_list.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_value = self.attribute_list.get(selected_index)
            sql = "SELECT * FROM Attribute WHERE A_name = %s"
            self.controller.cursor.execute(sql, (selected_value,))
            result = self.controller.cursor.fetchone()
            self.show_attribute_popup(result)
    
    # 선택한 항목 정보 팝업 
    def show_attribute_popup(self, attribute_info):
        popup = tk.Toplevel(self)
        popup.title(attribute_info[0])
        popup.geometry("300x200")
        
        arg_name = ttk.Label(popup, text=attribute_info[0])
        arg_name.pack(side="top", fill="x", pady=10)
        
        arg_price = ttk.Label(popup, text=math.trunc(attribute_info[1]))
        arg_price.pack(side="top", fill="x", pady=10)
        
        popup_menu = tk.Frame(popup)
        popup_menu.pack(side="bottom", fill="x", pady=10)

        save_button = ttk.Button(popup_menu, text="저장", command=lambda: self.save_attribute(attribute_info[0]))
        save_button.pack(side="left", padx=5, pady=5)

        delete_button = ttk.Button(popup_menu, text="삭제", command=lambda: self.delete_attribute(attribute_info[0]))
        delete_button.pack(side="left", padx=5, pady=5)

        back_button = ttk.Button(popup_menu, text="닫기", command=popup.destroy)
        back_button.pack(side="left", padx=5, pady=5)

    # 즐겨찾기 추가
    def save_attribute(self, name):
        try:
            sql = "INSERT INTO Bookmark (id, A_name) VALUES (%s, %s)"
            self.controller.cursor.execute(sql, (self.controller.id, name))
            self.controller.db.commit()
            print("save success")
        except Exception as e:
            print(f"Error: {e}")

    # 즐겨찾기 삭제
    def delete_attribute(self, name):
        try:
            sql = "DELETE FROM Bookmark WHERE id = %s AND A_name = %s"
            self.controller.cursor.execute(sql, (self.controller.id, name))
            self.controller.db.commit()
            print("delete success")
        except Exception as e:
            print(f"Error: {e}")

class OptionScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="환경설정 페이지")
        label.grid(row=0, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(self, text="Back to Main", command=lambda: controller.show_frame(MainScreen))
        back_button.grid(row=1, column=0, pady=5)

class MyPageScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="My Page")
        label.grid(row=0, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(self, text="Back to Main", command=lambda: controller.show_frame(MainScreen))
        back_button.grid(row=1, column=0, pady=5)

class BookmarkScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = tk.Label(self, text="Bookmark")
        label.grid(row=0, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(self, text="Back to Main", command=lambda: controller.show_frame(MainScreen))
        back_button.grid(row=1, column=0, pady=5)

# main.py 만들어서 옮기기
if __name__ == "__main__":
    app = Application()
    app.mainloop()
