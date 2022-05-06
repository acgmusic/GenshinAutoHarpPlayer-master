import win32com.client
import win32gui
import os
from PyQt5.QtCore import QObject, pyqtSignal
import keyboard
from midi_converter import midi_converter


values = list("zxcvbnmasdfghjqwertyu")
keys_basic = [36, 38, 40, 41, 43, 45, 47]
keys = keys_basic + [x + 12 for x in keys_basic] + [x + 24 for x in keys_basic]
MIDI_MAP = {keys[i]: values[i] for i in range(len(keys))}


def windowEnumerationHandler(hwnd, windowlist):
    windowlist.append((hwnd, win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd)))


def setGenshinAsForegroundWindow():
    windowlist = []
    win32gui.EnumWindows(windowEnumerationHandler, windowlist)
    for i in windowlist:
        if ("原神" in i[1].lower() or "genshin" in i[1].lower() or "げんし" in i[1].lower()) and i[2] == 'UnityWndClass':
            win32gui.ShowWindow(i[0], 4)
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            win32gui.SetForegroundWindow(i[0])
            break


def get_list_format(midi_file, speed=1):
    # midi_data = pretty_midi.PrettyMIDI(midi_file=midi_file)
    midi_data = midi_converter(load_fp=midi_file)
    try:
        notes = midi_data.instruments[0].notes
    except IndexError:
        return []
    notes.sort(key=lambda x: x.start)
    play_list = []
    i = 0
    while i < len(notes):
        cur_time = notes[i].start
        note_list_temp = []
        while i < len(notes) and notes[i].start == cur_time:
            note_list_temp.append(notes[i])
            i += 1
        key_list = list(set([MIDI_MAP[note.pitch] for note in note_list_temp]))  # 去重
        wait_time = notes[i].start - cur_time if i < len(notes) else 1
        wait_time /= speed
        play_list.append({'key_list': key_list, 'wait_time': wait_time})
    return play_list


def get_border_image_url(fn):
    path = os.path.join(os.path.dirname(__file__), f'resource/image/', fn)
    return f'QPushButton{{border-image: url({path})}}'.replace('\\', '/')


class KeyBoardManager(QObject):
    nextSignal = pyqtSignal()
    prevSignal = pyqtSignal()
    playSignal = pyqtSignal()

    def start(self):
        keyboard.add_hotkey("ctrl+shift+right", self.nextSignal.emit, suppress=True)
        keyboard.add_hotkey("ctrl+shift+left", self.prevSignal.emit, suppress=True)
        keyboard.add_hotkey("ctrl+shift+space", self.playSignal.emit, suppress=True)


if __name__ == '__main__':
    print(get_border_image_url("play.png"))
