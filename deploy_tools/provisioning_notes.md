Обеспечение работы нового сайта 
================================ 
## Необходимые пакеты:
* nginx
* Python 3.8
* virtualenv + pip * Git
* Git

например, в Ubuntu:
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get install nginx git python3.8 python3.8-venv

## Конфигурация виртуального узла Nginx

* см. nginx.template.conf
* заменить SITENAME, например, на staging.my-domain.com

## Служба Systemd

* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на staging.my-domain.com

## Структура папок:
Если допустить, что есть учетная запись пользователя в /root/username

/root/username 
└── sites
    └── SITENAME
        ├── database
        ├── source
        ├── static
        └── virtualenv