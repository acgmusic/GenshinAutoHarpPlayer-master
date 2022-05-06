# GenshinAutoHarpPlayer-master
## 原神自动弹琴工具 v0.1.0

### 软件使用方法（1和2中选一个即可，不想折腾python环境的建议直接跳到第2种方法）
1. 在本地安装python环境，然后使用pip安装以下依赖库：
```cmd
pip install PyQt5
pip install pyautogui
pip install pywin32
pip install keyboard
pip install pretty_midi
```
然后使用**管理员权限**打开命令行窗口（否则无法调用键盘接口），进入`GenshinAutoHarpPlayer-master`所在目录，然后执行：
```cmd
python ./GenshinAutoHarpPlayer-master/genshin_auto_harp_player/main.py
```


2. 直接下载`原神自动弹琴工具便携版`（里面打包了完整的python环境），大概140M左右，适合没有python环境的同学。使用**管理员权限**打开目录下面的`自动弹琴工具.exe`。

3. 打开软件后，首先选择乐谱存放目录。`midi_example`文件夹下的是我自己扒带的可以完美播放的曲子。`midi_from_internet`文件夹下的是从[midishow](https://www.midishow.com/)这个网站上下载的，没有经过任何处理。本软件会使用一些简单的算法来保证乐谱可以在原神中正常播放，但是效果不是很好，因为原神的琴只能播放21个键，局限性太大。所以想要提升效果的话，建议有能力的同学自己尝试修改midi文件。

4. 如果需要更换播放目录，则务必在更换完目录后重启软件。

5. 添加了以下3个播放快捷键：
* ctrl + shift + space: 播放/暂停
* ctrl + shift + left: 上一曲
* ctrl + shift + right: 下一曲

6. 添加了倍速播放功能。

7. 目前不支持直接使用文本来播放。如果需要的人多的话可以考虑做一下，主要是效果不太好，用文本编辑还不如用midi编辑器更快一点。


## automatic piano playing tool for Genshin Impact v0.1.0
### HOW TO USE 
(Choose one of step1 and step2)
1. Install the python environment, and then pip install the following dependent libraries:
```cmd
pip install PyQt5
pip install pyautogui
pip install pywin32
pip install keyboard
pip install pretty_ midi
```
Then use **administrator rights** to open the command line window (otherwise, the keyboard interface cannot be called), enter the directory where `genshinautoharpplayer master` is located, and then execute:
```cmd
python ./ GenshinAutoHarpPlayer-master/genshin_ auto_ harp_ player/main. py
```
2. Directly download the portable version of `原神自动弹琴工具便携版` (which is packaged with a complete Python environment), about 140M, which is suitable for those without Python environment. Use **administrator rights** to open the `自动弹琴工具.exe` under the directory。
3. After opening the software, first select the music score storage directory `midi_ Example`.Under the folder is the music I transcribed with my ears and they can play perfectly. `midi_from_internet` folder are midi files which were downloaded from [midishow](https://www.midishow.com/) without any processing. This software will use some simple algorithms to ensure that the music score can be played normally in genshin, but the performance is not very well, because the harp piano in genshin can only play 21 keys, which is too limited to play a nice piece of music. Therefore, if you want to improve the effect, it is recommended to modify MIDI files with your midi editor.
4. If you need to change the playback directory, be sure to restart the software after changing the directory.
5. Add the following three play shortcuts:
* CTRL + Shift + space: play / pause
* CTRL + Shift + left: previous song
* CTRL + Shift + right: next song
6. Speed changer is added.
7. At present, it is not supported to play directly with a text file. I may add this function later. The main reason is that the effect is not very good. Using text editing is not as fast as using MIDI editor.


