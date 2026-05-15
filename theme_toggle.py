import os
import sys
import tkinter as tk
import winreg
import ctypes

# ── Windows theme helpers ───────────────────────────────────────────────────

REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
HWND_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x001A
SMTO_ABORTIFHUNG = 0x0002


def get_theme_mode() -> bool:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH) as key:
            return bool(winreg.QueryValueEx(key, "AppsUseLightTheme")[0])
    except FileNotFoundError:
        return True


def set_theme_mode(light: bool) -> bool:
    value = 1 if light else 0
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, value)
            winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, value)
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0,
            "ImmersiveColorSet", SMTO_ABORTIFHUNG, 5000, None,
        )
        return True
    except Exception:
        return False


# ── Apple-style toggle with animation ───────────────────────────────────────

class AppleToggle(tk.Canvas):
    H = 36
    W = 62
    TRACK_ON = "#34c759"
    TRACK_OFF = "#e9e9ec"
    HANDLE_COLOR = "white"
    SHADOW_COLOR = "#d4d4d4"

    def __init__(self, master, initial=False, on_toggle=None, **kw):
        super().__init__(master, width=self.W, height=self.H,
                         highlightthickness=0, bd=0, **kw)
        self._on = initial
        self._callback = on_toggle
        self._animating = False
        self._draw(self._handle_x())
        self.bind("<Button-1>", self._click)

    def _handle_x(self):
        r = self.H // 2
        return self.W - r - 3 if self._on else r + 3

    def _draw(self, cx=None):
        self.delete("all")
        w, h = self.W, self.H
        r = h // 2
        if cx is None:
            cx = self._handle_x()
        ratio = (cx - (r + 3)) / (w - 2 * r - 6)  # 0 = off, 1 = on

        self.create_rounded_rect(1, 1, w - 1, h - 1, r - 1,
                                 fill=self.TRACK_ON if ratio > 0.5 else self.TRACK_OFF,
                                 outline="")

        hr = r - 8
        self.create_oval(cx - hr + 1, h // 2 - hr + 1, cx + hr + 1, h // 2 + hr + 1,
                         fill=self.SHADOW_COLOR, outline="")
        self.create_oval(cx - hr, h // 2 - hr, cx + hr, h // 2 + hr,
                         fill=self.HANDLE_COLOR, outline="")

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kw):
        self.create_arc(x1, y1, x1 + r * 2, y1 + r * 2, start=90, extent=90, **kw)
        self.create_arc(x2 - r * 2, y1, x2, y1 + r * 2, start=0, extent=90, **kw)
        self.create_arc(x1, y2 - r * 2, x1 + r * 2, y2, start=180, extent=90, **kw)
        self.create_arc(x2 - r * 2, y2 - r * 2, x2, y2, start=270, extent=90, **kw)
        self.create_rectangle(x1 + r, y1, x2 - r, y2, **kw)
        self.create_rectangle(x1, y1 + r, x2, y2 - r, **kw)

    def _animate(self, target_on):
        w, h = self.W, self.H
        r = h // 2
        start_x = self._handle_x()
        end_x = w - r - 3 if target_on else r + 3
        steps = 10
        delay = 12
        self._animating = True

        def step(i):
            if i > steps:
                self._on = target_on
                self._animating = False
                self._draw()
                if self._callback:
                    self._callback(target_on)
                return
            t = i / steps
            # ease-out cubic
            t = 1 - (1 - t) ** 3
            cx = start_x + (end_x - start_x) * t
            self._draw(cx)
            self.after(delay, lambda i=i: step(i + 1))

        step(1)

    def _click(self, _):
        if not self._animating:
            self._animate(not self._on)

    def set(self, v: bool):
        if self._on != v and not self._animating:
            self._animate(v)


# ── App ────────────────────────────────────────────────────────────────────

class ThemeApp:
    LIGHT_BG = "#f5f5f7"
    DARK_BG = "#1d1d1f"
    LIGHT_CARD = "#ffffff"
    DARK_CARD = "#2c2c2e"
    ACCENT = "#0071e3"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(" ")
        self.root.resizable(False, False)
        self.root.iconbitmap(self._icon_path())
        self.root.configure(bg=self.LIGHT_BG)

        self._light = get_theme_mode()
        self._container = tk.Frame(self.root, bg=self.LIGHT_BG)
        self._container.pack(fill="both", expand=True)
        self._container.columnconfigure(0, weight=1)

        self._build_ui()
        self._apply_theme()
        self._center(280, 270)

        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self._quit)

    @staticmethod
    def _icon_path():
        try:
            base = sys._MEIPASS
        except AttributeError:
            base = os.path.dirname(__file__)
        return os.path.join(base, "logo.ico")

    def _build_ui(self):
        # ── icon ──
        self.icon = tk.Label(self._container, font=("Segoe UI Emoji", 44))
        self.icon.grid(row=0, column=0, pady=(28, 4))

        # ── status ──
        self.status_lbl = tk.Label(
            self._container, font=("Microsoft YaHei UI", 22, "bold")
        )
        self.status_lbl.grid(row=1, column=0, pady=(0, 18))

        # ── toggle ──
        self.toggle = AppleToggle(
            self._container, initial=self._light, on_toggle=self._on_toggle
        )
        self.toggle.grid(row=2, column=0, pady=(0, 0))

        # ── quit ──
        self.quit_btn = tk.Label(
            self._container, text="退出",
            font=("Microsoft YaHei UI", 9), cursor="hand2",
        )
        self.quit_btn.grid(row=3, column=0, pady=(22, 18))
        self.quit_btn.bind("<Button-1>", lambda _: self._quit())
        self.quit_btn.bind("<Enter>", lambda _: self.quit_btn.configure(
            font=("Microsoft YaHei UI", 9, "underline")))
        self.quit_btn.bind("<Leave>", lambda _: self.quit_btn.configure(
            font=("Microsoft YaHei UI", 9)))

    def _apply_theme(self):
        bg = self.LIGHT_BG if self._light else self.DARK_BG
        fg = "#1d1d1f" if self._light else "#f5f5f7"
        sub = "#86868b" if self._light else "#98989d"

        self.root.configure(bg=bg)
        self._container.configure(bg=bg)
        self.icon.configure(text="☀️" if self._light else "🌙", bg=bg)
        self.status_lbl.configure(
            text="浅色" if self._light else "深色",
            fg=fg, bg=bg,
        )
        self.toggle.configure(bg=bg)
        self.quit_btn.configure(fg=sub, bg=bg)

    def _on_toggle(self, light):
        self._light = light
        set_theme_mode(light)
        self._apply_theme()

    def _center(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    def _quit(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ThemeApp().run()
