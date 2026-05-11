# ThemeToggle

一键切换 Windows 深色/浅色主题的桌面工具。

## 使用方法

从 [Releases](../../releases) 下载最新版 `ThemeToggle.exe`，双击运行即可。

点击开关即可切换 Windows 系统主题（浅色 ↔ 深色）。

## 功能

- 一键切换 Windows 10/11 深色/浅色模式
- 同时切换应用和系统主题
- 苹果风格交互界面，带滑动动画
- 窗口始终置顶，即开即用

## 技术说明

- 使用 Python + tkinter 构建
- 通过修改注册表 `AppsUseLightTheme` / `SystemUsesLightTheme` 切换主题
- 使用 `SendMessageTimeout` 广播主题变更，实时生效
- 使用 PyInstaller 打包为单文件 exe

## 开发

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "ThemeToggle" theme_toggle.py
```
