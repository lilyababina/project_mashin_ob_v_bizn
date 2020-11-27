# python-flask-docker
Итоговый проект (пример) курса "Машинное обучение в бизнесе"

Стек:

ML: sklearn, pandas, numpy
API: flask
Данные: с kaggle - https://www.kaggle.com/spscientist/students-performance-in-exams

Задача: предсказать по данным обучения пол ученика (поле gender). Бинарная классификация

Используемые признаки:

- race/ethnicity (категория)
- parental level of education(категория)
- lunch(категория)
- test preparation course(категория)
- math score(значение)
- reading score(значение)
- writing score(значение)

Преобразования признаков: категориальные - OHE, числовые значения - стандартизация

Модель: logreg

### Клонируем репозиторий и создаем образ
```

$ git clone https://github.com/lilyababina/masinnoe_obu4_v_biznese/tree/main/project/GB_docker_flask.git
$ cd GB_docker_flask
$ docker build -t 1/gb_docker_flask_ .
```

### Запускаем контейнер
```
$ docker run -d -p 8180:8180 -p 8181:8181 1/gb_docker_flask_
```

### Переходим на localhost:8181
