:: 创建表结构
python manage.py migrate

:: 让Django知道我们在我们的模型有一些变更
python manage.py makemigrations dataModel

:: 创建表结构
python manage.py migrate dataModel