# windows主题切换（ThemeToggle）

[中文](#中文) | [English](#english)

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

> 一键切换 Windows 深色/浅色主题的桌面工具。
> A desktop tool to toggle Windows dark/light theme with one click.

---

## 中文

一键切换 Windows 10/11 深色/浅色系统主题，苹果风格滑动开关，即开即用。

### 功能特性

- **一键切换** — 点击开关即可切换 Windows 系统主题（浅色 ↔ 深色）
- **联动切换** — 同时切换应用模式和系统模式
- **实时生效** — 通过系统广播即时应用主题变更，无需重启
- **苹果风格 UI** — 圆角滑动开关，带缓动动画
- **窗口置顶** — 始终在最前，即开即用
- **绿色单文件** — 打包为独立 exe，无需安装

### 快速开始

从 [Releases](../../releases) 页面下载最新版 `ThemeToggle.exe`，双击运行即可。

### 开发指南

```bash
# 安装依赖
pip install pyinstaller

# 打包为单文件 exe
pyinstaller --onefile --windowed --name "ThemeToggle" theme_toggle.py
```

产物位于 `dist/ThemeToggle.exe`。

### 技术原理

- 使用 Python + tkinter 构建图形界面
- 通过修改注册表 `AppsUseLightTheme` / `SystemUsesLightTheme` 切换主题
- 使用 `SendMessageTimeout` 广播 `ImmersiveColorSet` 消息，实时生效
- 使用 PyInstaller 打包为单文件 exe

---

## English

A lightweight desktop tool for toggling Windows 10/11 dark/light system theme, featuring an Apple-style toggle interface.

### Features

- **One-click toggle** — switch between light and dark mode with a single click
- **Dual switching** — toggles both app and system theme simultaneously
- **Instant effect** — applies changes immediately via system broadcast, no reboot required
- **Apple-style UI** — rounded toggle with easing animation
- **Always on top** — window stays in foreground, ready to use at any time
- **Portable** — single-file exe, no installation needed

### Quick Start

Download the latest `ThemeToggle.exe` from the [Releases](../../releases) page and double-click to run.

### Development

```bash
# Install dependencies
pip install pyinstaller

# Build single-file executable
pyinstaller --onefile --windowed --name "ThemeToggle" theme_toggle.py
```

Output is at `dist/ThemeToggle.exe`.

### How It Works

- Built with Python + tkinter
- Modifies registry keys `AppsUseLightTheme` and `SystemUsesLightTheme`
- Broadcasts `ImmersiveColorSet` via `SendMessageTimeout` for instant system-wide effect
- Packaged with PyInstaller as a single executable

---

## License

MIT
