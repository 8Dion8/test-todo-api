# test-todo-api
Тестовое задание.


# Запуск
```bash
docker build -t "test-todo-api" .
docker run -p 15243:15243 test-todo-api
```

# Базовый функционал
```bash
# Все таски
-> curl http://localhost:15243/api/v1/tasks
[]

# Добавить таску
-> curl -X POST http://localhost:15243/api/v1/tasks \
        -H "Content-Type: application/json" \
        -d '{"text": "Buy groceries", "status": "in progress"}'
{"id":1,"status":"in progress","text":"Buy groceries"}

-> curl http://localhost:15243/api/v1/tasks
[{"id":1,"status":"in progress","text":"Buy groceries"}]

# Все таски с фильтром
-> curl http://localhost:15243/api/v1/tasks?status=completed
[]

# Апдейт статуса таски
-> curl -X PUT http://localhost:15243/api/v1/tasks/1/status \
            -H "Content-Type: application/json" \
            -d '{"status": "completed"}'

{"id":1,"status":"completed","text":"Buy groceries"}


-> curl http://localhost:15243/api/v1/tasks?status=completed
[{"id":1,"status":"completed","text":"Buy groceries"}]

# Удаление таски
-> curl -X DELETE http://localhost:15243/api/v1/tasks/1
{"message":"Task 1 deleted"}

-> curl http://localhost:15243/api/v1/tasks
[]
```
