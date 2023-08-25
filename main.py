import os
import subprocess
import time
import cv2
import numpy as np
import pyautogui
import win32com.client
import win32con
import win32gui
import configparser
import sys
# import threading
# import pyaudio
from PIL import ImageGrab
# from pydub import AudioSegment
# from pydub.playback import play

# 文件父目录读取器
def get_executable_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.split(os.path.realpath(__file__))[0]

# 读取配置文件
config = configparser.ConfigParser()
config.read(os.path.join(get_executable_dir(), "config.ini"), encoding="utf-8")
config.write(open(os.path.join(get_executable_dir(), "config.ini"), "w", encoding="utf-8"))

# 读取配置值并保存到变量中
print("debug")
# 是否读取桌面图标来原神启动，默认关闭
readShortcut = config.get("launch", "readshortcut")
print("readShortcut: " + str(readShortcut))
# 如果不读取桌面上的图标，那请改为你的 YuanShen.exe 绝对路径位置
gameLocation = config.get("launch", "gamelocation")
gameLocation = os.path.abspath(gameLocation)
print("gameLocation: " + gameLocation)
# 设置每n秒扫描一次屏幕且检测是否要原神启动！如果为0，那么没有延迟直接启动！这样做是为了性能
scaningScreenDelay = int(config.get("check", "scaningscreendelay"))
print("scaningScreenDelay: " + str(scaningScreenDelay))
# 设置如果屏幕纯白率大于等于n(%)时原神启动！
launchWhitePercentage = int(config.get("check", "launchwhitepercentage"))
print("launchWhitePercentage: " + str(launchWhitePercentage))
# # 是否在原神启动时后台播放启动音乐，默认有两种可供选择
# playLaunchMusic = config.getboolean("music", "playlaunchmusic")
# print("playLaunchMusic: " + str(playLaunchMusic))
# if (playLaunchMusic == True):
#     # 设置歌曲延迟(秒)，可能播放的时候没有对接上
#     musicDelay = int(config.get("music", "musicdelay"))
#     print("musicDelay: " + str(musicDelay))
#     # 选择音乐类型 1 为 Shed A Light(启动の小曲) 2 为 门酱DDD 的 “原神，启动！！！” 3 为 超级无敌整合版你也可以在 ProgramNeededFiles 中添加更多mp3
#     launchMusicStyle = int(config.get("music", "launchmusicstyle"))
#     print("launchMusicStyle: " + str(launchMusicStyle))

# 检查原神是否已经启动
if os.system('tasklist /FI "IMAGENAME eq YuanShen.exe" 2>NUL | find /I /N "YuanShen.exe">NUL') == 0:
    print("Fail: Genshin Impact is launched.")
    os.system('pause')
    exit()
# 获取屏幕分辨率
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False # 关闭FailSafe

print('White percentage checking start.')

while True:
    # 截图
    screenshot = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(0, 0, screen_width, screen_height))), cv2.COLOR_BGR2RGB)
    # 计算屏幕白色像素比例
    white_pixels = np.count_nonzero(screenshot >= [250, 250, 250])
    total_pixels = screenshot.shape[0] * screenshot.shape[1]
    white_percentage = white_pixels / total_pixels * 100
    print(f"whitePercentage: {white_percentage}%")
    # 判断是否满足启动条件
    if white_percentage >= launchWhitePercentage:
        break
    time.sleep(scaningScreenDelay) # 每 scaningScreenDelay 秒截图一次

print('White percentage >=' + str(launchWhitePercentage) + ' end checking.')

# 如果需要那么做，就解析快捷方式获取安装路径
if (readShortcut):
    shortcut = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\原神\原神.lnk' # 获取快捷方式路径
    shell = win32com.client.Dispatch("WScript.Shell")
    install_dir = shell.CreateShortCut(shortcut)
    install_dir = install_dir.TargetPath.replace('launcher.exe', '')
    game_exe = os.path.join(install_dir, 'Genshin Impact Game', 'YuanShen.exe') # 拼接启动路径
# 但是 也可以使用绝对路径~
elif (readShortcut == False):
    game_exe = gameLocation

# 创建过渡用的白色图片
transition_steps = 35
white_image = np.full((screen_height, screen_width, 3), 255, dtype=np.uint8)

# 创建过渡窗口并置顶
cv2.namedWindow('Transition', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Transition', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
transition_window = pyautogui.getWindowsWithTitle("Transition")[0]
pyautogui.moveTo(transition_window.left, transition_window.top)
time.sleep(0.5)
cv2.imshow('Transition', screenshot)
hwnd = win32gui.FindWindow(None, "Transition")
CVRECT = cv2.getWindowImageRect("Transition")
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, screen_width, screen_height,
                        win32con.SWP_SHOWWINDOW)

# 原神，启动！
if readShortcut == True:
    subprocess.Popen(game_exe)
else:
    subprocess.Popen([gameLocation])
subprocess.Popen("musicplayer")
# 进行过渡并在过渡窗口上显示
for step in range(transition_steps):
    alpha = (step + 1) / transition_steps
    blended_image = cv2.addWeighted(screenshot, 1 - alpha, white_image, alpha, 0)
    cv2.imshow('Transition', blended_image)
    cv2.waitKey(10)

# 枚举窗口,找到名称包含"原神"的窗口
while True:
    windows = pyautogui.getWindowsWithTitle("原神")
    if windows:
        # 找到窗口并置顶
        time.sleep(5)
        window = windows[0]
        pyautogui.moveTo(window.left, window.top)
        print(f"原神，启动！")
        break
# time.sleep(musicDelay) # 音乐延迟
# # 如果允许播放音乐 则播放振奋人心的 原神！！！启动！！！
# if (launchMusicStyle == True):
#     # 这行代码搞了我一个下午 ↓
#         threading.Thread(target=lambda: play(AudioSegment.from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "RunningFiles", "Music", f"{launchMusicStyle}.mp3")))).start()
#         # ↑
time.sleep(1)
cv2.destroyWindow('Transition')