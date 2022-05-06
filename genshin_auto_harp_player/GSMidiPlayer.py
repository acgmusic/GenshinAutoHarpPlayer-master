from utils import setGenshinAsForegroundWindow, get_list_format
import pyautogui
import time
from PyQt5.Qt import QThread


class GSMidiPlayer(QThread):
    def __init__(self):
        super().__init__()
        self.is_paused = True
        self.cur_playing_midi = []
        self.cur_point = -1
        self.midi_duration = -1

    def position(self):
        return self.cur_point

    def duration(self):
        return self.midi_duration

    def setMedia(self, fp, speed=1):
        try:
            self.cur_playing_midi = get_list_format(fp, speed=speed)
        except FileNotFoundError as e:
            raise FileNotFoundError(e)
        except OSError as e:
            raise OSError(e)

        self.midi_duration = len(self.cur_playing_midi)
        if self.cur_playing_midi:
            self.cur_point = 0
        self.terminate()

    def isAudioAvailable(self):
        pass

    def play(self):
        setGenshinAsForegroundWindow()
        time.sleep(0.5)
        self.is_paused = False
        self.start()

    def run(self) -> None:
        # qmutex.lock()
        while (not self.is_paused) and (self.cur_point < self.midi_duration):
            if self.cur_point == 0:
                # print("播放开始")
                pyautogui.press('z')
                time.sleep(2)
            pyautogui.press(self.cur_playing_midi[self.cur_point]['key_list'])
            time.sleep(self.cur_playing_midi[self.cur_point]['wait_time'])
            # print(f"正在播放{self.cur_playing_midi[self.cur_point]['key_list']},"
            #       f"当前{self.cur_point},总{self.midi_duration}")
            self.cur_point += 1
        # print("播放完成/即将暂停")
        # qmutex.unlock()

    def pause(self):
        self.is_paused = True
        # print("暂停中")
