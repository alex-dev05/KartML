from pywinauto.application import Application
import pywinauto.mouse as mouse
from pywinauto.controls.win32_controls import ButtonWrapper
import time

#app = Application.start(cmd_line="C:\Poli\Dizertatie\Repo_Github\KartML\Export\ControlledByHuman\MachineLearning_Karts.exe")
app = Application(backend="win32").start(cmd_line="C:\Poli\Dizertatie\Repo_Github\KartML\Export\ControlledByHuman\MachineLearning_Karts.exe")
#app = Application(backend="win32").start(cmd_line="C:\Folder\Wow.exe")
app.Play.click()
#app.UnityWndClass.PLAY.click()
#app.window(best_match='MachineLearning_Karts', top_level_only=False).child_window(best_match='PLAY').click()
#time.sleep(10)
#dlg = app['MachineLearning_Karts.exe']
#dlg.print_control_identifiers()
#dlg.set_focus()
#mouse.click(coords=(1000, 900))


#app.MainWindow.Wait('ready')
#vbapp = app.window_(title_re="MachineLearning_Karts")
#vbButton1 = ButtonWrapper(vbapp.Button.WrapperObject("PLAY")).Click