import pyautogui
import time

# 대기 시간 설정 (1.5 초)
delay = 1.5

try:
    while True:
        # "z" 키를 두 번 누르기
        pyautogui.press('z')
        pyautogui.press('z')
        
        # 대기
        time.sleep(delay)
except KeyboardInterrupt:
    # Ctrl+C를 눌러 프로그램을 중지할 수 있습니다.
    pass