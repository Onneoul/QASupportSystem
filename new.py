import pyautogui
import time

# ��� �ð� ���� (1.5 ��)
delay = 1.5

try:
    while True:
        # "z" Ű�� �� �� ������
        pyautogui.press('z')
        pyautogui.press('z')
        
        # ���
        time.sleep(delay)
except KeyboardInterrupt:
    # Ctrl+C�� ���� ���α׷��� ������ �� �ֽ��ϴ�.
    pass