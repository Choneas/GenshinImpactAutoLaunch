# Genshin Impact Auto Launch
![Alt text](./RunningFiles/genshin_launch_meme.png)

## About

forked from
[YinBuLiao/GenshinImpact_Start](https://github.com/YinBuLiao/GenshinImpact_Start)

Uses [config.ini](.\config.ini) to make a personalize Genshin Impact Launching style.

## Features
- **pyparaser** Read the configuration file
- **pydub** Music play module
- **threading** Multi-thread music play

## Build
Build scripts is not in Release. You should download the ZIP of all the repo.
1. `cd` to the program's folder.
2. `pip install -r install_requirements.py`
3. `cd` to where the `main.py` in.
4. `pyinstaller main.py --icon=favicon.ico`
5. (If you want the program to be a single exe file)\
   `pyinstaller --onefile main.py --upx-dir="Your path" --icon=favicon.ico`
## Configurations

``` ini
[launch]
readshortcut = false # Use the shortcut icon in desktop to detect Genshin Impact's path
gamelocation = YuanShen.exe # If `readshortcut` is `false`, type your Genshin Impact executeable file's path here.
[check]
scaningscreendelay = 3 # Second(s). Scaning screen delay(Screenshot for checking the white percentage) 
launchwhitepercentage = 90 # Recommended to test this before your showcase. It maybe > 100
[music]
playlaunchmusic = true # Play music while launching?
musicdelay = 3 # Set the music delay.(For slow devices)
launchmusicstyle = 3 # Music file name in `Music` folder. Default: 1. Shed a Light(Clip) 2. 门酱DDD's 原神启动(the program cover image) 3. Both
```

## FAQ
### Why the music doesn't play while launching?
If you want to play music while launching, you should make sure the `ffmpeg` is in your `path`.
### Why the music plays late?
I recommended to run `musicplayer.exe` just once before launching. Remember to set the `musicDelay` value.

## TO-DO
1. Support Genshin Impact(Not YuanShen)
2. Change the configuration file to `.toml` or `.yml` not `.ini`
3. Alaways running in background silently.
4. Translate this ↓

## 如何下载ffmpeg且添加到环境变量中?
首先 从[BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds/releases/tag/latest)**中下载 ffmpeg-master-latest-win64-lgpl.zip 文件**然后解压到合适的位置**

![解压ffmpeg.zip](./FFmpegInstallHelp/unzip.png)

接着 按下 Windows 键 依次输入 p a t h 四个字母 打开环境变量配置

![打开环境变量配置](./FFmpegInstallHelp/openpathset.png)

在新窗口中 点击右下角的 环境变量 按钮

![打开环境变量配置窗口](./FFmpegInstallHelp/systeminfowindow.png)

请按照图片操作 如果需要放大 尝试 Ctrl + 鼠标滚轮 或者在项目 FFMpegInstallHelp 文件夹中打开image.png

![设置环境变量](./FFmpegInstallHelp/image.png)

测试: 按下 Win 键 + R 输入 `cmd` 点击确定

在弹出的窗口中 输入以下命令

`ffmpeg`

如果有一大串英文 说明安装成功