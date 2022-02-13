# estimate

Прект в разработке.
Доступен по адресу: <a href="http://estimate.ml/estimate", target="_blank">http://estimate.ml/estimate</a>

Приложение для подготовки смет с материалами и видами работ, ценами с возможностью 
создания шаблонов, созданием повышающих коэффициентов, и других плюшек


После сборки

sudo docker-compose exec web python manage.py migrate --noinput
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic

Если есть то импортировать то
sudo docker-compose exec web python manage.py loaddata fixtures/base_dump.json

