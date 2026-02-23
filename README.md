1. Выбор и настройка модели детекции:   

    По умолчанию Bento Service работает на yoloe-26x-seg.pt
    При использованний базовой модели:
    1. self.model.set_classes(self.classes) ракоментировать эту строчку в modelservice.py
    2. labels.append(CLASSES_MAP.get(self.classes[cls_id], self.classes[cls_id])) - раскоментировать эт строчку в modelservice.py
    3. uv run BentoService/bentomodel.py - из корня. Cохранения модели.


    Fine-Tune:
    1. Запустить сначала обычную модель yoloe-26x-seg.pt чтобы скачался yoloe-26x-seg.pt файл.
    1. Загрузить нужные картинки в images/train
    2. Загрузить нужный CSV в yolo_dataset/csv
    3. Заменить классы в convert_csv_to_yolo.py в переменной label_map на ваши.
    4. Заменить классы в dataset.yaml на ваши.
    3. uv run BentoService/FineTune/convert_csv_to_yolo.py - из корня.
    4. uv run BentoService/FineTune/fine_tune.py - из корня.
    5. Дождаться конца обучения, зайти в папку runs->yolo_finetuned->weights->best.pt
    6. Заменить модель в BentoService везде на best.pt
    7. Либо раскоментировать просто готовые строки которые сами заберут лучшую модель.
    8. uv run BentoService/bentomodel.py - из корня. Сохранение получившейся модели.

    Fine-Tune Kaggle/Collab:
    1. При слабом компьютере, перенести весь тот же самый код с прошлого пункта на kaggle
    2. Заранее подгрузить туда Pt и Dataset
    3. После обучения забрать pt и положить в папку KaggleModel
    4. Заменить имя конечного файла в bentomodel.py на имя своей модели.
    5. uv run BentoService/bentomodel.py - из корня. Сохранение получившейся модели.

    После всех проделнанных действий выше (1 из 3 на выбор) Запуско осуществляется одинакого для всех.
    Сборка образа осуществляется одинаково для всех.

    Локальный запуск:
    1. uv run bentoml serve BentoService.modelservice:Detector - из корня.
    2. Переходим по указанному в консоли URL и тестируем.

    Сборка контейнера:
    1. uv run bentoml build -f bentofile.detect.yaml.
    2. uv run bentoml containerize war-detector:lastest --image-tag war-detector:latest --opt progress=plain (необязательный флаг в конце)
    3. docker build -f dockerfile.fix -t war-detector:fixed
    4. Все команд нужно выполнить ничего не меняя.

Запуск всех микросервисов:

Запуск контейнеров:
    1. docker compose up

Запуск бота:
    1. cd TgGraphBot
    1. uv run -m bot.main
    2. Перейти в бота и пользоаться

Запуск микросервиса VideoProduce:

    1. Запуск микросервиса backend_VideoProduce (Бекенд):
        1. cd backend_VideoProduce
        2. uv run -m app.main
        3. FastAPI слушает на пору 8000.
    Запустит сервер фаст апи который примет любые видео загрузить их в один бакет разделит по папкам (с какой камеры), загрузит информацию о видео с какой камеры снято, какой путь minio имеет и когда создано в БД (PostgreSQL). Нарежет видео на фреймы сложит все фреймы в отдельный бакет, со структурой папок где сначлаа каждая папка - каждая камреа, и в каждой папке, каждая папка это фейрмы конкретного видео. Отправит всю инфрмацию о нерезанных фреймах в топик кафки в микросерис детекции. И будет слушать другой топик о том что фреймы обработаны, получив такое сообщение обновит в БД на статус (processe) - обработано.

    2. Запуск микросервиса frontend_VideoProduce (Фронтенд)
        1.
        2. Слушает на порту 8501

Тестирование Graphql локально:
    1. cd TgGraphBot
    1. Тестирование Graphql запросов локально -> uv run graphapi.py
    2. Перейти по URL в чате.


