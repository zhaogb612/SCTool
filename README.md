# SCTools - 系统工具箱

一个基于 PyQt5 开发的 Windows 系统工具集合，集成了多种常用的系统维护、磁盘管理、硬件检测等工具。

**本项目采用 AI 辅助开发完成，提升了开发效率和代码质量。**

---

## 功能特性

### 系统工具
- PCMaster - 系统维护和优化工具集
- Win11轻松设置 - Windows 11设置工具
- WinNTSetup - Windows安装工具
- EasyRC - 系统安装工具
- HEU KMS激活 - 系统激活工具
- ResHacker - 资源工具

### 磁盘工具
- CrystalDiskInfo - 硬盘信息检测工具
- CrystalDiskMark - 硬盘性能测试工具
- DiskGenius - 磁盘分区和数据恢复工具
- WizTree - 磁盘空间分析工具
- 分区助手 - 分区助手工具
- Recuva - 文件恢复工具

### 硬件检测
- 图拉丁硬件检测 - 硬件信息检测工具
- AIDA64 - 系统信息和硬件检测工具
- GPU-Z - GPU信息检测工具
- ChipGenius - USB设备信息检测工具
- Monitorinfo - 显示器信息检测工具
- 鼠标测试 - 鼠标测试工具
- MOUSERATE - 鼠标回报率测试工具
- 键盘测试 - 键盘测试工具
- BIOSBackup - BIOS备份工具

### 系统优化
- CCleaner - 系统清理和优化工具
- HiBit卸载器 - 软件卸载工具
- Dism++ - Windows系统维护工具
- ContextMenuManager - 右键菜单管理工具
- CrystalMark Retro - 系统性能测试工具

### 其他工具
- NDM - 多线程下载器
- Motrix - 下载器
- QBittorrent - 种子下载器
- Windows超级管理器 - Windows系统设置和监管工具
- 定时关机 - 定时关机工具
- 定时闹钟 - 定时闹钟工具
- 图片爬取 - 图片爬取工具
- Everything - 文件快速搜索工具

---

## 技术栈

- Python 3
- PyQt5 - GUI 框架
- 支持 Windows 系统

---

## 使用方法

### 直接运行
```bash
python main.py
```

### 打包运行
项目已包含打包脚本：
- `build.bat` - 基础打包脚本
- `build_simple.bat` - 简化打包脚本
- `build_custom.bat` - 自定义打包脚本

打包生成的可执行文件位于 `dist/` 目录。

---

## 项目结构

```
SCTools/
├── main.py                    # 主程序入口
├── src/
│   ├── ui/
│   │   └── main_window.py    # 主窗口界面
│   ├── tools/
│   │   ├── tool_manager.py   # 工具管理器
│   │   ├── system_tools/     # 系统工具目录
│   │   ├── disk_tools/       # 磁盘工具目录
│   │   ├── hardware_detection/ # 硬件检测工具目录
│   │   ├── system_optimization/ # 系统优化工具目录
│   │   └── other_tools/      # 其他工具目录
│   └── navigation/
│       └── navigation_manager.py # 导航管理器
├── dist/                     # 打包输出目录
├── build/                    # 构建临时目录
└── README.md                 # 项目说明
```

---

## 特色功能

### 主题切换
- 自动检测系统主题（亮色/深色模式）
- 支持手动切换主题
- 自适应系统主题设置

### 工具管理
- 分类管理各类工具
- 搜索工具功能
- 一键启动工具

### 用户界面
- 简洁美观的界面设计
- 工具按钮提示
- 响应式布局

---

## 系统要求

- Windows 7/8/10/11
- Python 3.7+（运行源代码时需要）

---

## 开发说明

本项目采用 AI 辅助开发，包括：
- 代码结构设计
- UI 界面布局
- 功能模块实现
- 文档编写

AI 辅助大大提升了开发效率，帮助快速完成项目搭建和功能实现。

---

## 许可证

本项目仅供学习和个人使用，请勿用于商业用途。

---

## 致谢

感谢所有开源工具的开发者，以及 AI 辅助工具的支持。
