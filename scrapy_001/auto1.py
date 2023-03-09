import pyautogui

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()
# pyautogui.moveTo(100, 150)
# pyautogui.click()
#  鼠标向下移动10像素
pyautogui.moveRel(0, 10)
pyautogui.doubleClick()
#  用缓动/渐变函数让鼠标2秒后移动到(500,500)位置Hello world！
#  use tweening/easing function to move mouse over 2 seconds.
pyautogui.moveTo(600, 300, duration=2, tween=pyautogui.easeInOutQuad)
#  在每次输入之间暂停0.25秒
pyautogui.typewrite('Hello world!', interval=0.25)
pyautogui.press('esc')
pyautogui.keyDown('shift')
pyautogui.press(['left', 'left', 'left', 'left', 'left', 'left'])
pyautogui.keyUp('shift')
pyautogui.hotkey('ctrl', 'c')