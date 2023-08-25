import configparser
import os
import sys
import time
from pydub import AudioSegment
from pydub.playback import play

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

# 设置歌曲延迟(秒)，可能播放的时候没有对接上
musicDelay = int(config.get("music", "musicdelay"))
print("musicDelay: " + str(musicDelay))
# 选择音乐类型 1 为 Shed A Light(启动の小曲) 2 为 门酱DDD 的 “原神，启动！！！” 3 为 超级无敌整合版你也可以在 ProgramNeededFiles 中添加更多mp3
launchMusicStyle = int(config.get("music", "launchmusicstyle"))
print("launchMusicStyle: " + str(launchMusicStyle))

# 构建音乐文件路径
time.sleep(musicDelay)
music_path = os.path.join(get_executable_dir(), "RunningFiles", "Music", f"{launchMusicStyle}.mp3")
play(AudioSegment.from_file(music_path))
