# 使用kivy制作一个聊天机器人

基于青云客聊天机器人实现GUI

Requirements: kivy urllib3

运行:

​	python chat.py



可以使用buildozer进行打包，打包时需要在.spec文件中的requierments处添加urllib3



PS: 本来是想用requests进行网页访问，但是buildozer找不到这个包，似乎是因为其封装了python的其他包，如需封装诸如此类的Python，需要先添加其依赖包，再将封装包的根目录一并打包，因为此应用功能单一简单，就没搞这么复杂。