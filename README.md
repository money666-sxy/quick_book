# quick_book
## 首先执行命令将项目拉取下来并安装相关依赖
```
yum install -y git 

https://github.com/money666-sxy/quick_book.git

pip3 install pipreqs

pipreqs . --encoding=utf8 --force

pip3 install -r requirements.txt
```
## 完成以上操作之后即可运行
> 提取图书关键字
> python3 crawle_book.py
> 提取电影关键字
> python3 crawle_movie.py
