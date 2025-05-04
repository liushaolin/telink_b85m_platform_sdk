# telink_b85m_platform_sdk

This project forked from [telink-semi/telink_b85m_platform_sdk](https://github.com/telink-semi/telink_b85m_platform_sdk).
主要目的简化工程的编译和运行调试。

## 使用方法

需要安装python, git完本项目之后，在上级目录执行`tools\init.bat`，会自动解压TC32、生成所有工程的Makefile。

运行当前目录的`setup_tlsr.bat`，会生成对应的path环境变量，每次首次进入时均需调用。
之后执行如下命令进行验证：`cd demo\vendor\AUDIO_Demo && make all` 即可。

烧录重启硬件：`make bfr` or `make b`.

参考如下页面：
- [windows平台开发环境搭建](https://github.com/Ai-Thinker-Open/Telink_825X_SDK/blob/master/start_windows.md)
- [Telink SIG Mesh SDK](https://gitee.com/anson_lwang/Telink_SIG_Mesh)

## TC32 下载

下载地址：
- Windows： [tc32-win.rar](http://shyboy.oss-cn-shenzhen.aliyuncs.com/readonly/tc32_win.rar)
- Linux: [tc32_gcc_v2.0.tar.bz2](https://shyboy.oss-cn-shenzhen.aliyuncs.com/readonly/tc32_gcc_v2.0.tar.bz2)
- MAC OS: [tc32-mac.zip](http://shyboy.oss-cn-shenzhen.aliyuncs.com/readonly/tc32-mac.zip)

## 其他工具

- wget: [wget-for-windows](https://github.com/lifenjoiner/wget-for-windows)
- unrar: [UnRAR for Windows](https://www.rarlab.com/rar_add.htm)