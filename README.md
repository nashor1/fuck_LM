# fuck_LM

龙猫校园app远程完成阳光跑

这是一个用python，flask框架写的项目，运行文件为app.py
运行前请先安装依赖

本人使用的python环境为3.8.10

pip install -r requestment.txt

一、本地搭建项目默认路径为
阳光跑、早操签到网址
127.0.0.1:5000


此项目目前仅适用于无锡学院，项目中的阳光跑路线已设置为动态，会自动增加节点和圈数

早操签到的龙猫校园后台做了升级，后台根据北京时间判断用户提交
用户无法再通过更改本地时间来提交早操签到

二、服务器搭建项目
克隆本项目到服务器
git clone --depth=1 https://hub.fastgit.xyz/nashor1/fuck_LM.git
安装所需依赖
pip install -r requestment.txt

使用gunicorn框架搭建，即可实现公网部署
