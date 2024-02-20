# graduation_project_web_end
Django框架下的Web端应用

## 安装需要的依赖
```angular2html
pip install -r requirements.txt
```


## 编写.env文件
```angular2html
echo DEBUG=True > .env
echo DATABASE_URL=mysql://user:password@localhost:3306/dbname >> .env
```


## 运行
```angular2html
python manage.py runserver
```