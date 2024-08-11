import tkinter as tk
import pyautogui
import math
import ctypes
import win32gui
import win32con

def set_click_through(hwnd):
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(
        hwnd,
        win32con.GWL_EXSTYLE,
        ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT,
    )
    ctypes.windll.user32.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,
        0,
        0,
        0,
        0,
        win32con.SWP_NOSIZE
        | win32con.SWP_NOMOVE
        | win32con.SWP_NOACTIVATE
        | win32con.SWP_NOZORDER,
    )

def get_window_rect_by_title(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        return rect
    return None

def draw_trajectory():
    canvas.delete("all")
    window_rect = get_window_rect_by_title("Rocket Bot Royale")
    if window_rect:
        win_x, win_y, win_w, win_h = window_rect
        win_width = win_w - win_x
        win_height = win_h - win_y

        center_x = win_x + win_width // 2 + offset_x
        center_y = win_y + win_height // 2 + offset_y
    else:
        center_x = screen_width // 2 + offset_x
        center_y = screen_height // 2 + offset_y

    mouse_x, mouse_y = pyautogui.position()
    rel_x = mouse_x - center_x
    rel_y = mouse_y - center_y
    angle = math.atan2(-rel_y, rel_x)

    gravity = 2.17
    time_step = 0.5
    initial_speed = 50

    last_screen_x = center_x
    last_screen_y = center_y

    for t in range(0, 2000):
        t *= time_step
        x = initial_speed * t * math.cos(angle)
        y = initial_speed * t * math.sin(angle) - 0.5 * gravity * t**2

        screen_x = center_x + x
        screen_y = center_y - y

        if (
            screen_x < 0
            or screen_x > screen_width
            or screen_y > screen_height
        ):
            break

        canvas.create_line(
            last_screen_x, last_screen_y, screen_x, screen_y, fill="red", width=6
        )

        last_screen_x = screen_x
        last_screen_y = screen_y

    root.after(16, draw_trajectory)

root = tk.Tk()
root.attributes("-transparentcolor", "black")
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.5)
root.overrideredirect(True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

offset_x = 0
offset_y = 10

canvas = tk.Canvas(
    root, width=screen_width, height=screen_height, bg="black", highlightthickness=0
)
canvas.pack()

root.update_idletasks()
root.update()

hwnd = win32gui.GetParent(root.winfo_id())
set_click_through(hwnd)

draw_trajectory()

root.mainloop()
