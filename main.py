#######################################################################################
# 프로그램 : 파주염가 판서공파(국파공파 4세) 가승보 Ver 1.0 F                  (2024.03.25)
# 가상환경 : Command Prompt 창의 d:\venvJason\yeomsFamily> 다음에 Scripts\activate를 입력하고 실행한다.
# 실행파일 : pyinstaller --hiddenimport win32timezone -w -F --add-binary "d:\venvJason\yeomsFamily\pythoncom310.dll;." --add-data .\*.ttf;.\ --add-data .\assets\source\*;assets\source\ --add-data .\assets\userdb\*;assets\userdb\ --add-data .\assets\photos\*;assets\photos\ --add-data .\assets\images\*;assets\images\ --add-data .\assets\fonts\*;assets\fonts\ --add-data .\assets\texts\*;assets\texts\ --add-data .\assets\pdfdata\*;assets\pdfdata\ main.py
#           또는 pyinstaller --noconfirm --onedir --console "main.py" 로 컴파일 한 후 assets 디렉토리 복사
#           - (yeomsFamily) D:\venvjason>yeomsFamily> 에 위의 명령어를 복사해서 실행한다.
#           - 한글폰트 *.ttf 파일을 실행파일이 있는 곳에 복사 해 준다.
#           - 에러발생 시 "바이러스 및 위험방지 설정" 옵션 해제 후 컴타일한다.
# 사 용 자 : User ID = yeomdh, Password = 1234
# 디 버 깅 : kvhot . --top 50 --left 1550 또는 reloadium run main.py
#######################################################################################

from kivymd.app import MDApp                               # Material Design compliant widgets 모듈
from kivy.core.window import Window                        # 윈도우 생성 모듈
from kivy.lang import Builder                              # kv 파일 읽기 모듈
from kivy.uix.screenmanager import ScreenManager           # 스크린 생성 모듈
from kivymd.uix.list import MDListItem, MDListItemHeadlineText # 리스트 생성 모듈
from kivymd.uix.pickers import MDModalDatePicker           # 날짜 선택 모듈
from kivy.core.text import LabelBase                       # 한글폰트 지정 모듈
import sqlite3                                             # 사용자 DB 모듈
import time                                                # 시스템 시간 모듈
import os, sys                                             # 시스템 모듈 / file path
from win32api import GetSystemMetrics                      # 윈도우 사용자 / 모니터 크기 설정
import kivymd.icon_definitions                             # 아이콘 모듈 / 실행파일 에러 방지
import threading                                           # Progress bar 멀티 쓰레딩
from kivy.properties import BooleanProperty                # Progress bar 멀티 쓰레딩
from kivy.clock import Clock                               # Progress bar 멀티 쓰레딩
# -------------------------------------------------------- 사용자 정의 모듈
from assets.source.yeoms_screens import (LoginScreen, SignupScreen, RootlistScreen, 
                                         RootdataScreen, MrootlistScreen, MrootdataScreen, 
                                         StoryScreen, OtherScreen, OtherdataScreen,
                                         PhotodataScreen, PDFReaderScreen, ViewerScreen,
                                         MapViewScreen)
from assets.source.yeoms_popup import (CorrectPopup, InvalidPopup, SpacePopup, NumberPopup, 
                                        EmptyPopup, UserPopup, SavedPopup, ProgressPopup,
                                        InfoPopup)

# -------------------------------------------------------- 윈도우 창 설정
screenx = GetSystemMetrics(0)                              # 해상도 가로 크기
screeny = GetSystemMetrics(1)                              # 해상도 세로 크기
prg_sizex = 400                                            # 프로그램 가로 크기
prg_sizey = 780                                            # 프로그램 세로 크기
Window.size = (prg_sizex, prg_sizey)                       # 초기 창 크기
Window.minimum_width = prg_sizex                           # 최소 가로 크기
Window.minimum_height = prg_sizey                          # 최소 세로 크기
Window.clearcolor = (1, 1, 1, 1)                           # 화면 배경색
Window.left = (screenx - prg_sizex)/2                      # 화면의 가로 중앙
Window.top = (screeny - prg_sizey)/2                       # 화면의 세로 중앙

# -------------------------------------------------------- 참조 파일의 절대경로 "\\"
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# -------------------------------------------------------- 프로그램 설정
class YeomsFamilyApp(MDApp):
    title = "Roots of Yeom's Family."                      # 윈도우 창 제목
    
    def build(self):
        global sm                                          # 전역변수 선언
        sm = ScreenManager()                               # ScreenManager 객체 생성
        self.load_all_kv_files()                           # kv 파일 읽어오기
        self.load_all_widget_files()                       # widget 파일 읽어오기
        # 한글폰트 지정 - 적용 안 되는 위젯에서는 markup=True 및 [font=ttffilename]...[/font] 사용
        text_path = resource_path(".\\assets\\fonts\\KoPubBatangMedium.ttf")
        LabelBase.register(name="han_font", fn_regular=f"{text_path}")
        return self.string                                 # 주 화면 속성 리턴

    def load_all_kv_files(self):
        kv_popup = resource_path(".\\assets\\source\\yeoms_popup.kv")
        kv_screens = resource_path(".\\assets\\source\\yeoms_screens.kv")
        self.string = Builder.load_file(kv_popup)
        self.string = Builder.load_file(kv_screens)
        
    def load_all_widget_files(self):
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(RootlistScreen(name='rootlist'))
        sm.add_widget(RootdataScreen(name='rootdata'))
        sm.add_widget(MrootlistScreen(name='mrootlist'))
        sm.add_widget(MrootdataScreen(name='mrootdata'))
        sm.add_widget(StoryScreen(name='story'))
        sm.add_widget(OtherScreen(name='other'))
        sm.add_widget(OtherdataScreen(name='otherdata'))
        sm.add_widget(PhotodataScreen(name='photodata'))
        sm.add_widget(PDFReaderScreen(name='pdfreader'))
        sm.add_widget(ViewerScreen(name='viewer'))
        sm.add_widget(MapViewScreen(name='mapview'))
        
        # 각각의 화면에 기본 이미지 불러오기
        self.string.get_screen('login').ids.login_title.source = resource_path(".\\assets\\images\\title.png")
        self.string.get_screen('login').ids.login_photo.source = resource_path(".\\assets\\images\\M1TH_P.gif")
        self.string.get_screen('login').ids.login_login.source = resource_path(".\\assets\\images\\login.png")
        self.string.get_screen('signup').ids.signup_img.source = resource_path(".\\assets\\images\\signup.png")
        self.string.get_screen('menu').ids.menu_img.source = resource_path(".\\assets\\images\\M1TH_P.gif")
        self.string.get_screen('other').ids.other_img.source = resource_path(".\\assets\\images\\M1TH_P.gif")
        return sm

    # ---------------------------------------------------- 달력 보여주기
    def show_date_picker(self):
        date_dialog = MDModalDatePicker()
        date_dialog.open()

    # ---------------------------------------------------- Check Log In
    def check_login(self):
        global now, today

        now = time.localtime()
        today = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

        self.setting_database()

        # 창에 입력한 아이디 및 비밀번호 읽어오기
        username = self.string.get_screen('login').ids.username_text_field.text
        password = self.string.get_screen('login').ids.password_text_field.text
        # 입력한 아이디 및 비밀번호로 사용자 찾기
        if cursor.execute("SELECT * FROM `Admin` WHERE `username` = ? AND `password` = ?",
                          (username, password)):
            if cursor.fetchone() is not None:
                # 로그인에 성공했으므로 로그인 버튼 비활성화
                self.string.get_screen('login').ids.login_button.disabled = True
                # Main Screen으로 가기 버튼 활성화
                self.string.get_screen('login').ids.gohome_button.disabled = False
                # 신규가입 버튼 비활성화
                self.string.get_screen('login').ids.forgot_button.disabled = True
                # 입력창의 아이디 비밀번호 지우기
                self.clear_login()
                # 로그인 성공 메시지 창 보여주기
                self.correct_popup()
                # 창의 Tool Bar에 접속한 사용자 보여주기
                self.string.get_screen('menu').ids.menu_top.text = f"MENU / User : {username}"
            else:
                # 로그인에 실패하면 에러메시지를 보여준 후 User ID, password를 지우고 다시 입력대기
                self.invalid_popup()
                self.clear_login()
        cursor.close()
        conn.close()

    # ---------------------------------------------------- 입력된 로그인 자료를 리셋
    def clear_login(self):
        self.string.get_screen('login').ids.username_text_field.text = ""
        self.string.get_screen('login').ids.password_text_field.text = ""

    # ---------------------------------------------------- 사용자 데이타베이스 구성
    def setting_database(self):
        global conn, cursor
        # Data Base 파일을 연결
        conn = sqlite3.connect(resource_path(".\\assets\\userdb\\Yeom_User.db"))
        cursor = conn.cursor()
        # 사용자 테이블이 없다면 신규로 생성 / "\"는 긴 문장 줄 비꾸기
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `Admin` (admin_id INTEGER PRIMARY KEY \
                AUTOINCREMENT NOT NULL,username TEXT, email TEXT, password TEXT)")
        # 사용자 비밀번호를 읽어옴
        cursor.execute(
            "SELECT * FROM `Admin` WHERE `username` = '%s' AND `password` = '%s'")

        # 읽어온 자료 한개씩 cursor.fetchons()
        result = cursor.fetchone()
        # 만일 관리자 정보가 설정되지 않아서 비어있다면 기본 아이디와 이메일 비밀번호 설정 및 저장
        if cursor.fetchone():
            pass
        elif result is None:
            cursor.execute("INSERT or REPLACE INTO Admin VALUES(?,?,?,?);",
                           (1, 'yeomdh', 'yeomdh@naver.com', '1234'))
            conn.commit()

    # ---------------------------------------------------- 사용자 신규 가입
    def check_signup(self):
        global now, today

        now = time.localtime()
        today = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

        self.setting_database()

        # 아이디 및 비밀번호 읽어오기
        username = self.string.get_screen('signup').ids.username_input.text
        email = self.string.get_screen('signup').ids.email_input.text
        password = self.string.get_screen('signup').ids.password_input.text
        self.username_text = username
        username_check_false = True

        # 입력된 값을 검사 - 에러메시지 보여주기
        try:
            int(self.username_text)
        except (ValueError, Exception):
            username_check_false = False

        if username_check_false:                           # 아이디에 숫자만 입력하면 에러메시지
            self.number_popup()
        elif len(username.split()) > 1:                    # 아이디에 공백이 있으면 에러메시지
            self.space_popup()
        elif email == "" or password == "":                # 이메일 또는 비밀번호를 비워두면 에러메시지
            self.empty_popup()
        # username 이 동일한 사람 찾기,  admin_id가 0인 사용자는 없으나 Error 방지를 위해 추가
        elif cursor.execute("SELECT * FROM `Admin` WHERE `admin_id` = ? \
            OR `username` = ?", (0, username)):
            if cursor.fetchone() is not None:              # 이미 가입된 아이디 일 때
                self.user_popup()
                self.clear_login()
            else:                                          # 사용가능한 아이디 일때
                # 데이터 숫자를 Count
                rowlist = []
                cursor.execute("SELECT count(*) from Admin")
                rowlist = cursor.fetchall()
                # [(4,)] 형식의 rowlist 값에서 숫자만 선택한 다음 새로 저장할 사용자의 admin_id를 결정
                count_id = rowlist[0][0] + 1
                # Saved 메시지를 보여준 후 user, password를 저장
                cursor.execute("INSERT INTO Admin VALUES(?,?,?,?);",
                               (count_id, username, email, password))
                conn.commit()
                self.saved_popup()
                self.clear_login()
                self.move_login()
        cursor.close()
        conn.close()

    # ---------------------------------------------------- 특정 화면으로 이동하기
    def move_login(self):
        self.root.transition.direction = "right"
        self.root.current = 'login'
        
    def move_menu(self):
        self.root.transition.direction = "left"
        self.root.current = 'menu'

    # ---------------------------------------------------- Popup Message 보여주기
    def correct_popup(self):                               # 로그인 성공
        the_popup = CorrectPopup()
        the_popup.open()

    def invalid_popup(self):                               # 로그인 실패
        the_popup = InvalidPopup()
        the_popup.open()

    def space_popup(self):                                 # 공간 입력
        the_popup = SpacePopup()
        the_popup.open()

    def number_popup(self):                                # 숫자만 입력
        the_popup = NumberPopup()
        the_popup.open()

    def empty_popup(self):                                 # Email, PWD 미 입력
        the_popup = EmptyPopup()
        the_popup.open()

    def user_popup(self):                                  # 이미 가입된 아이디
        the_popup = UserPopup()
        the_popup.open()

    def saved_popup(self):                                 # 신규가입 등록
        the_popup = SavedPopup()
        the_popup.open()
        
    def info_popup(self):                                  # 프로그램 코딩자 정보
        the_popup = InfoPopup()
        the_popup.open()
        
    def progress_popup(function):                          # PDF Reading Progress bar Function
        def progress_threading(app, *args, **kwargs):
            # 다른 파일의 다른 클래스에 있는 메소드 호출하기
            # prg = PDFReaderScreen()                        # 해당 클래스의 인스턴스를 생성
            # prg.pdf_display()                              # 생성된 인스턴스를 통해 메소드를 호출
            the_popup = ProgressPopup()  
            app.done = False                               # Popup dismiss False
            # When app.done is set to True, then popup.dismiss is fired
            app.bind(done=the_popup.dismiss)  
            the_popup.open()                               # Show popup
            Clock.schedule_once(lambda x: threading.Thread(target=function, args=[app, the_popup, *args], kwargs=kwargs).start())
            # t2 = threading.Thread(target=function, args=[app, the_popup, *args], kwargs=kwargs)  # Create thread
            # t2.start()
            return # t2
        return progress_threading
    
    done = BooleanProperty(False)                          # Preoress bar Status
    @progress_popup                                        # Progress 진행 중 메시지
    def progress_msg(self, the_popup):
        the_popup.text = 'Start PDF file reading ...'
        time.sleep(0.5)
        the_popup.progress = 20
        the_popup.text = '20 % Reading Complete ...'
        time.sleep(1)
        the_popup.progress = 50
        the_popup.text = '50 % Reading Complete ...'
        time.sleep(1)
        the_popup.progress = 80
        the_popup.text = '80 % Reading Complete ...'
        time.sleep(0.5)
        the_popup.progress = 100
        the_popup.text = 'Reading Cpmplete !'
        time.sleep(0.5)
        self.done = True

    # ---------------------------------------------------- 상계 스크롤 리스트 데이터
    def rootlist_clear(self):
        rscreen = self.root.get_screen('rootlist')
        rscreen.ids.rootlist_items.clear_widgets()
        
    def rootlist_search_value(self, val: str) -> list:     # 검색 자료
        root_names = ['01세 염형명', '02세 염위', '03세 염가칭', '04세 염현', '05세 염한', '06세 염덕방', '07세 염신약', '08세 염극모', \
                    '09세 염후', '10세 염수장', '11세 염순언', '12세 염승익', '13세 염세충', '14세 염제신(중시조)']
        new_list = []                                      # 찾은 데이터를 저장할 리스트 변수 선언
        # 데이터 검색 ... root_names 리스트를 하나씩 읽어서 find_text에 넘겨줌
        for find_text in root_names:
            if val in find_text:                           # 찾는 문자(val)가 find_text에 포함되어 있다면
                new_list.append(find_text)                 # new_list에 find_text를 첨가한다.
        
        # 해당 스크린 정보 불러와서 깨끗히 지우기
        rscreen = self.root.get_screen('rootlist')
        self.rootlist_clear()
        for yeomsroot in new_list:                         # 새로운 new_list를 하나씩 yeomsroot에 넘겨줌
            if len(new_list) < 15:                         # yeomsroot 데이터를 화면에 보여준다.
                items = MDListItem(
                        MDListItemHeadlineText(
                            markup = True,
                            text = f"[font=KoPubBatangMedium]파주염가 상계 {int(yeomsroot[0:2])}세 - '{yeomsroot[4:]}' - 자세히 보기[/font]" 
                        ),
                        id = str(yeomsroot[0:2]),          # 현재 리스트아이템의 번호만 추출
                        pos_hint = {"center_y": .5},
                        size_hint_x = 1,
                        on_release = rscreen.rootlist_action_items   # 클릭시 호출할 함수
                    )
                rscreen.ids.rootlist_items.add_widget(items)
        # 검색 결과를 보여준 후 검색창 초기화 
        rscreen.ids.rootlist_search_value.text = ""
    
    # ---------------------------------------------------- 국파공파 스크롤 리스트 데이터
    def mrootlist_clear(self):
        mrscreen = self.root.get_screen('mrootlist')
        mrscreen.ids.mrootlist_items.clear_widgets()
        
    def mrootlist_search_value(self, val: str) -> list:     # 검색 자료
        mroot_names = ['01세 염제신', '02세 염국보', '03세 염치용', '04세 염증', '05세 염순검', \
                        '06세 염말건', '07세 염순학', '08세 염언수', '09세 염귀인', '10세 염홍립', \
                        '11세 염무의', '12세 염준철', '13세 염창번', '14세 염흥갑', '15세 염취환', \
                        '16세 염필만', '17세 염판정', '18세 염병주', '19세 염규훈', '20세 염덕균', \
                        '20세 염백균', '20세 염당균', '20세 염철호']
        new_list = []
        # 데이터 검색 ... mroot_names 리스트를 하나씩 읽어서 find_text에 넘겨줌
        for find_text in mroot_names:
            if val in find_text:                           # 찾는 문자(val)가 find_text에 포함되어 있다면
                new_list.append(find_text)                 # new_list에 find_text를 첨가한다.
        
        # 해당 스크린 정보 불러와서 깨끗히 지우기
        mrscreen = self.root.get_screen('mrootlist')
        self.mrootlist_clear()
        for yeomsroot in new_list:                         # 새로운 new_list를 하나씩 yeomsroot에 넘겨줌
            if len(new_list) < 24:                         # yeomsroot 데이터를 화면에 보여준다.
                items = MDListItem(
                        MDListItemHeadlineText(
                            markup = True,
                            text = f"[font=KoPubBatangMedium]파주염가 {int(yeomsroot[0:2])}세 - '{yeomsroot[4:]}' - 자세히 보기[/font]" 
                        ),
                        id = yeomsroot[4:],                # 현재 리스트아이템의 이름만 추출
                        pos_hint = {"center_y": .5},
                        size_hint_x = 1,
                        on_release = mrscreen.mrootlist_action_items   # 클릭시 호출할 함수
                    )
                mrscreen.ids.mrootlist_items.add_widget(items)
        # 검색 결과를 보여준 후 검색창 초기화 
        mrscreen.ids.mrootlist_search_value.text = ""
        
    # ---------------------------------------------------- 이미지 갤러리
    def view_file_selected(self, filename):
        # 해당 스크린을 호출하여 깨끗히 지우기
        vrscreen = self.root.get_screen('viewer')
        vrscreen.ids.viewer_image.clear_widgets()
        try:
            # 이미지창에 선택한 이미지 출력하기
            vrscreen.ids.viewer_image.source = filename[0]
            # 선택한 파일 경로 보여주기
            directory = vrscreen.ids.viewer_image.source
            vrscreen.ids.viewer_directory.text = f"File : {directory}"
        except:
            pass
    
if __name__ == '__main__':
    YeomsFamilyApp().run()
    