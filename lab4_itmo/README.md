
# Лабораторная работа 4 

### Ход работы

#### 0. Сборка и загрузка образа приложения в minikube
```bash
docker build -t llm-app:latest .
minikube image load llm-app:latest
```

#### 1. Запуск minikube
```bash
minikube start
```

#### 2. Применение манифестов secret
```bash
kubectl apply -f llm-secret.yaml
```

#### 3. Развертывание PostgreSQL
```bash
kubectl apply -f db_deploy.yaml
kubectl apply -f db_service.yaml
```

#### 4. Развертывание приложения
```bash
kubectl apply -f app_deploy.yaml
kubectl apply -f app_service.yaml
```

#### 5. Проверка подов
```bash
kubectl get pods
```

#### 6. Тестирование сервиса
```bash
minikube service llm-app-service --url




