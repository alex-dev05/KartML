from pywinauto.application import Application

from pywinauto.keyboard import send_keys, KeySequenceError
import time

#app = Application.start(cmd_line="C:\Poli\Dizertatie\Repo_Github\KartML\Export\ControlledByHuman\MachineLearning_Karts.exe")
app = Application(backend="win32").start(cmd_line="C:\Poli\Dizertatie\Repo_Github\KartML\Export\ControlledByHuman\MachineLearning_Karts.exe")
#app = Application(backend="win32").start(cmd_line="C:\Folder\Wow.exe")
time.sleep(5)
send_keys("{SPACE}")
time.sleep(5)
send_keys("{SPACE}")
