#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具管理模块
"""


class Tool:
    """工具类"""
    
    def __init__(self, name, description, category, path=None):
        self.name = name
        self.description = description
        self.category = category
        self.path = path
    
    def run(self):
        """运行工具"""
        if self.path:
            import os
            if os.path.exists(self.path):
                os.startfile(self.path)
            else:
                print(f"工具路径不存在: {self.path}")
        else:
            print(f"工具路径未设置: {self.name}")


class SystemTool(Tool):
    """系统工具类"""
    
    def __init__(self, name, description, path=None):
        super().__init__(name, description, "system", path)


class NetworkTool(Tool):
    """网络工具类"""
    
    def __init__(self, name, description, path=None):
        super().__init__(name, description, "network", path)


class EfficiencyTool(Tool):
    """效率工具类"""
    
    def __init__(self, name, description, path=None):
        super().__init__(name, description, "efficiency", path)


class ToolManager:
    """工具管理器"""
    
    def __init__(self):
        self.tools = []
        self.init_tools()
    
    def init_tools(self):
        """初始化工具"""
        # 从目录加载工具
        tool_directory = "D:\\myblog\\SCTools\\src\\tools"
        self.load_tools_from_directory(tool_directory)
    
    def load_tools_from_directory(self, tool_directory):
        """从目录加载工具"""
        import os
        
        # 系统工具
        system_tools = [
            SystemTool("PCMaster", "系统维护和优化工具集", os.path.join(tool_directory, "system_tools", "PCMaster_6.25_Portable", "pcmaster.exe")),
            SystemTool("Win11轻松设置", "Windows 11设置工具", os.path.join(tool_directory, "system_tools", "Windows11轻松设置_1.09_Portable", "Windows11轻松设置.exe")),
            SystemTool("WinNTSetup", "Windows安装工具", os.path.join(tool_directory, "system_tools", "WinNTSetup_5.4.1.0_64bit_Portable", "WinNTSetup_x64.exe")),
            SystemTool("EasyRC", "系统安装工具", os.path.join(tool_directory, "system_tools", "EasyRC", "EasyRCV3.exe")),
            SystemTool("HEU KMS激活", "系统激活工具", os.path.join(tool_directory, "system_tools", "HEU_KMS_Activator_HorseEdition.exe")),
            SystemTool("ResHacker", "资源工具", os.path.join(tool_directory, "system_tools", "ResHacker", "ResHacker4.exe"))
        ]
        
        # 磁盘工具
        disk_tools = [
            SystemTool("CrystalDiskInfo", "硬盘信息检测工具", os.path.join(tool_directory, "disk_tools", "CrystalDiskInfo", "CrystalDiskInfoPortable.exe")),
            SystemTool("CrystalDiskMark", "硬盘性能测试工具", os.path.join(tool_directory, "disk_tools", "CrystalDiskMark", "CrystalDiskMarkPortable.exe")),
            SystemTool("DiskGenius", "磁盘分区和数据恢复工具", os.path.join(tool_directory, "disk_tools", "DiskGenius Pro", "DiskGenius.exe")),
            SystemTool("WizTree", "磁盘空间分析工具", os.path.join(tool_directory, "disk_tools", "WizTree_4.23_Portable", "WizTree64.exe")),
            SystemTool("分区助手", "分区助手工具", os.path.join(tool_directory, "disk_tools", "PartAssist.exe")),
            SystemTool("Recuva", "文件恢复工具", os.path.join(tool_directory, "disk_tools", "Recuva64.exe"))
        ]
        
        # 系统安装
        install_tools = []
        
        # 搜索工具
        search_tools = []
        

        
        # 性能测试
        benchmark_tools = []
        
        # 硬件检测
        hardware_tools = [
            SystemTool("图拉丁硬件检测", "硬件信息检测工具", os.path.join(tool_directory, "hardware_detection", "图拉丁硬件检测", "图拉丁硬件检测.exe")),
            SystemTool("AIDA64", "系统信息和硬件检测工具", os.path.join(tool_directory, "hardware_detection", "AIDA64.exe")),
            SystemTool("GPU-Z", "GPU信息检测工具", os.path.join(tool_directory, "hardware_detection", "GPU-Z.exe")),
            SystemTool("ChipGenius", "USB设备信息检测工具", os.path.join(tool_directory, "hardware_detection", "ChipGenius.exe")),
            SystemTool("Monitorinfo", "显示器信息检测工具", os.path.join(tool_directory, "hardware_detection", "monitorinfo.exe")),
            SystemTool("鼠标测试", "鼠标测试工具", os.path.join(tool_directory, "hardware_detection", "鼠标测试软件AresonMouseTestProgram.exe")),
            SystemTool("MOUSERATE", "鼠标回报率测试工具", os.path.join(tool_directory, "hardware_detection", "MOUSERATE.EXE")),
            SystemTool("键盘测试", "键盘测试工具", os.path.join(tool_directory, "hardware_detection", "Keyboard Test Utility.exe")),
            SystemTool("BIOSBackup", "BIOS备份工具", os.path.join(tool_directory, "hardware_detection", "BIOSBackup.exe"))
        ]
        
        # 系统优化
        optimization_tools = [
            SystemTool("CCleaner", "系统清理和优化工具", os.path.join(tool_directory, "system_optimization", "CCleaner pro 6.15.10623 绿色版", "CCleaner64.exe")),
            SystemTool("HiBit卸载器", "软件卸载工具", os.path.join(tool_directory, "system_optimization", "HiBit_Uninstaller_3.2.55_Single.exe")),
            SystemTool("Dism++", "Windows系统维护工具", os.path.join(tool_directory, "system_optimization", "Dism++_10.1.1002.1_Portable", "Dism++x64.exe")),
            SystemTool("ContextMenuManager", "右键菜单管理工具", os.path.join(tool_directory, "system_optimization", "ContextMenuManager.exe")),
            SystemTool("CrystalMark Retro", "系统性能测试工具", os.path.join(tool_directory, "system_optimization", "CrystalMark Retro", "CrystalMarkRetroPortable.exe"))
        ]
        
        # 数据恢复
        recovery_tools = []
        
        # 其他工具
        other_tools = [
            SystemTool("NDM", "多线程下载器", os.path.join(tool_directory, "other_tools", "Neat Download Manager", "NeatDM.exe")),
            SystemTool("Motrix", "下载器", os.path.join(tool_directory, "other_tools", "Motrix-1.8.19-win", "Motrix.exe")),
            SystemTool("QBittorrent", "种子下载器", os.path.join(tool_directory, "other_tools", "qBittorrent", "qbittorrent.exe")),
            SystemTool("Windows超级管理器", "Windows系统设置和监管工具", os.path.join(tool_directory, "other_tools", "Windowscjglq.exe")),
            SystemTool("定时关机", "定时关机工具", os.path.join(tool_directory, "other_tools", "定时关机 .exe")),
            SystemTool("定时闹钟", "定时闹钟工具", os.path.join(tool_directory, "other_tools", "定时闹钟.exe")),
            SystemTool("图片爬取", "图片爬取工具", os.path.join(tool_directory, "other_tools", "图片爬取.exe")),
            SystemTool("Everything", "文件快速搜索工具", os.path.join(tool_directory, "other_tools", "Everything", "EverythingPortable.exe"))
        ]
        
        # 添加到工具列表
        self.tools.extend(system_tools)
        self.tools.extend(disk_tools)
        self.tools.extend(install_tools)
        self.tools.extend(hardware_tools)
        self.tools.extend(optimization_tools)
        self.tools.extend(recovery_tools)
        self.tools.extend(other_tools)
    
    def get_system_tools(self):
        """获取系统工具"""
        return [tool for tool in self.tools if tool.category == "system"]
    
    def get_network_tools(self):
        """获取网络工具"""
        return [tool for tool in self.tools if tool.category == "network"]
    
    def get_efficiency_tools(self):
        """获取效率工具"""
        return [tool for tool in self.tools if tool.category == "efficiency"]
    
    def search_tools(self, keyword):
        """搜索工具"""
        keyword = keyword.lower()
        return [tool for tool in self.tools if keyword in tool.name.lower() or keyword in tool.description.lower()]
    
    def get_tool_by_name(self, name):
        """根据工具名称获取工具对象"""
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None
