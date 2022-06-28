# devops-netology
description of devops-netology repo

* - любой знак
**/.terraform/* - не помещать в индекс скрытый каталог .terrfarm, предпоследний по глубине и лююой предшествующей вложенности

*.tfstate 
*.tfstate.*
- не помещать в индекс файлы с расширением .tfstate или с куском текста в названии - .tfstate. и любыми строками в начале и в конце

*.crashlog - не помещать в индекс файлы с расширением .crachlog
*.tvars - то же самое для файлов с расширением *.tvars

игнорировать файлы:
override.tf
override.tf.json
заканчивающиеся на _override.tf и _override.tf.json


игнорировать с расширением .terraformrc и файл terraform.rc

