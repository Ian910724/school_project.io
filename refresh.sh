#!/bin/bash

# 進入到本地資料夾
cd /home/pi/Desktop/Project/data_base/passenger

# 添加所有更改到暫存區
git add .

# 提交更改
git commit -m "Auto upload files"

# 推送到遠端存儲庫
git push origin data_base
