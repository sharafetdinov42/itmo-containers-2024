# itmo-containers-2024
## Отчет по практике #3: Работа с Kubernetes

### 1. Запуск minikube
- Шаг 1: Установлен и запущен minikube

![Запуск](screens\2.jpg?raw=true)

### 2. Решение проблемы с доступом к репозиторию https://registry.k8s.io

- Шаг 2: Исправлено путем добавления DNS-сервера с помощью команды:
  ```
  sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
  ```

### 3. Проверка установки Kubernetes
- Шаг 3: Проведена проверка установки и корректной работы кластера

![Проверка_1](screens\3.jpg?raw=true)

![Проверка_1](screens\4.jpg?raw=true)

![Проверка_3](screens\5.jpg?raw=true)

### 4. Создание объектов Kubernetes
- Шаг 4: Созданы Kubernetes объекты на основе предоставленных манифестов

![Создание манифестов](screens\6.jpg?raw=true)

### 5. Проверка работоспособности
- Шаг 5: Проверка:
  - Работоспособности подов

![Проверка подов 1](screens\10.jpg?raw=true)

![Проверка подов 2](screens\11.jpg?raw=true)

  - Логов Nextcloud

![Логи](screens\7.jpg?raw=true)

  - Экспозиции сервисов

![Экспозиции](screens\8.jpg?raw=true)

### 6. Настройка туннелирования трафика
- Шаг 6: Настроено туннелирование трафика через minikube service для доступа к приложению

![Туннелирование](screens\12.jpg?raw=true)

### 7. Доступ к приложению
- Шаг 7: Доступ к Nextcloud через сгенерированную URL

![Доступ к Nextcloud](screens\13.jpg?raw=true)

### 8. Работа с Kubernetes Dashboard
- Шаг 8: Установка и доступ к Kubernetes Dashboard

![доступ к Kubernetes Dashboard](screens\13.jpg?raw=true)

![Дашборд](screens\9.jpg?raw=true)

## Вопросы
1.  **Важен ли порядок выполнения этих манифестов? Почему?**        
    Ответ: Да, В Kubernetes важно соблюдать порядок применения манифестов, так как некоторые ресурсы зависят друг от друга. Например, если ConfigMap или Secret, необходимые для развертывания, ещё не созданы, то Deployment не сможет успешно запуститься. Аналогично, Service не будет функционировать до тех пор, пока не будут созданы поды, на которые он будет направлять трафик.
2.  **Что (и почему) произойдет, если отскейлить количество реплик postgres-deployment в 0, затем обратно в 1, после чего попробовать снова зайти на Nextcloud?**   
    Что произойдет:
     - При отскейлинге реплик postgres-deployment до 0, все экземпляры базы данных будут удалены.
     - База данных станет недоступной, что приведет к потере связи для Nextcloud.
    
   - Почему:
     - Без активных реплик базы данных нет возможности обрабатывать запросы.
     - Nextcloud не сможет подключаться к базе данных для выполнения операций.

   - После возвращения количества реплик к 1:
     - База данных восстановит доступность, но...
    
   - Чтобы Nextcloud снова заработал:
     - Необходимо перезапустить поды (контейнеры) Nextcloud, чтобы он автоматически установил соединение с вновь доступной базой данных.

   В результате, хотя базы данных после возвращения к 1 реплике восстанавливает работоспособность, для возобновления работы Nextcloud требуется дополнительное действие — перезапуск его подов для обновления подключения к базе данных.