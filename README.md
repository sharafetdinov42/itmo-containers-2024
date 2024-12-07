
# itmo-containers-2024

## Отчет по практике #3: Работа с Kubernetes

### 1. Запуск minikube
- **Шаг 1**: Установлен и запущен minikube

![Запуск](https://github.com/sharafetdinov42/itmo-containers-2024/raw/lab3/screens/2.jpg)

---

### 2. Решение проблемы с доступом к репозиторию https://registry.k8s.io
- **Шаг 2**: Исправлено путем добавления DNS-сервера с помощью команды:
  ```bash
  sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
  ```

---

### 3. Проверка установки Kubernetes
- **Шаг 3**: Проведена проверка установки и корректной работы кластера

![Проверка 1](https://github.com/sharafetdinov42/itmo-containers-2024/raw/lab3/screens/3.jpg)  
![Проверка 2](https://github.com/sharafetdinov42/itmo-containers-2024/raw/lab3/screens/4.jpg)  
![Проверка 3](https://github.com/sharafetdinov42/itmo-containers-2024/raw/lab3/screens/5.jpg)

---

### 4. Создание объектов Kubernetes
- **Шаг 4**: Созданы Kubernetes объекты на основе предоставленных манифестов

![Создание манифестов](https://github.com/sharafetdinov42/itmo-containers-2024/raw/lab3/screens/6.jpg)

---

### 5. Проверка работоспособности
- **Шаг 5**: Проверка:
  - Работоспособности подов:

![Проверка подов 1](https://github.com/sharafetdinov42/itmo-containers-2024/raw/lab3/screens/10.jpg)  
![Проверка подов 2](https://github.com/sharafetdinov42/itmo-containers-2024/raw/lab3/screens/11.jpg)

  - Логов Nextcloud:

![Логи](https://github.com/sharafetdinov42/itmo-containers-2024/raw/lab3/screens/7.jpg)

  - Экспозиции сервисов:

![Экспозиции](https://github.com/sharafetdinov42/itmo-containers-2024/raw/lab3/screens/8.jpg)

---

### 6. Настройка туннелирования трафика
- **Шаг 6**: Настроено туннелирование трафика через `minikube service` для доступа к приложению

![Туннелирование](https://github.com/sharafetdinov42/itmo-containers-2024/raw/lab3/screens/12.jpg)

---

### 7. Доступ к приложению
- **Шаг 7**: Доступ к Nextcloud через сгенерированную URL

![Доступ к Nextcloud](https://github.com/sharafetdinov42/itmo-containers-2024/raw/lab3/screens/13.jpg)

---

### 8. Работа с Kubernetes Dashboard
- **Шаг 8**: Установка и доступ к Kubernetes Dashboard

![Доступ к Kubernetes Dashboard](https://github.com/sharafetdinov42/itmo-containers-2024/raw/lab3/screens/13.jpg)  
![Дашборд](https://github.com/sharafetdinov42/itmo-containers-2024/raw/lab3/screens/9.jpg)

---

## Вопросы
1. **Важен ли порядок выполнения этих манифестов? Почему?**  
   **Ответ**: Да, в Kubernetes важно соблюдать порядок применения манифестов, так как некоторые ресурсы зависят друг от друга. Например:
   - Если `ConfigMap` или `Secret`, необходимые для развертывания, ещё не созданы, то `Deployment` не сможет успешно запуститься.
   - Аналогично, `Service` не будет функционировать до тех пор, пока не будут созданы поды, на которые он будет направлять трафик.

2. **Что (и почему) произойдет, если отскейлить количество реплик `postgres-deployment` в 0, затем обратно в 1, после чего попробовать снова зайти на Nextcloud?**  
   **Что произойдет**:
   - При отскейлинге реплик `postgres-deployment` до 0, все экземпляры базы данных будут удалены.
   - База данных станет недоступной, что приведет к потере связи для Nextcloud.
   
   **Почему**:
   - Без активных реплик базы данных нет возможности обрабатывать запросы.
   - Nextcloud не сможет подключаться к базе данных для выполнения операций.

   **После возвращения количества реплик к 1**:
   - База данных восстановит доступность, но...
   
   **Чтобы Nextcloud снова заработал**:
   - Необходимо перезапустить поды (контейнеры) Nextcloud, чтобы он автоматически установил соединение с вновь доступной базой данных.

   В результате, хотя база данных после возвращения к 1 реплике восстанавливает работоспособность, для возобновления работы Nextcloud требуется дополнительное действие — перезапуск его подов для обновления подключения к базе данных.
