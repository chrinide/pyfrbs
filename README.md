#### Описание прикладного программного интерфейса сервиса

##### Получить список всех переменных

```
GET /api/variables
```

###### Пример выходных данных

```
{
  "variables": [
    {
      "id": 1,
      "max": 100.0,
      "min": -100.0,
      "name": "первая переменная",
      "name_id": 1,
      "validated": true
    },
    {
      "id": 2,
      "max": 1.0,
      "min": 0.0,
      "name": "вторая переменная",
      "name_id": 2,
      "validated": true
    },
    {
      "id": 3,
      "max": 50.0,
      "min": 0.0,
      "name": "третья переменная",
      "name_id": 3,
      "validated": false
    }
  ]
}
```

##### Получить информацию о переменной

```
GET /api/variables/[id]
```

###### Пример выходных данных

```
{
  "variables": {
    "id": 1,
    "max": 100.0,
    "min": -100.0,
    "name": "первая переменная",
    "name_id": 1,
    "validated": true
  }
}
```

##### Создать новую переменную

```
POST /api/variables
```

###### Пример входных данных

```
{
  "id": 4,
  "max": 1.0,
  "min": -1.0,
  "name": "четвёртая переменная",
  "name_id": 4,
  "validated": false
}
```

##### Модифицировать переменную

```
PUT /api/variables/[id]
```

###### Пример входных данных

```
{
  "id": 4,
  "max": 10.0,
  "min": -10.0,
  "name": "четвёртая переменная",
  "name_id": 4,
  "validated": true
}
```

##### Удалить переменную

```
DELETE /api/variables/[id]
```

##### Передать задачу для машины вывода

```
POST /api/tasks
```

###### Пример входных данных

```
{ 
  "inputs": [ 
	{ 
	  "variable": 1, 
	  "value": 10.0 
	}, 
	{ 
	  "variable": 2, 
	  "value": 0.0 
	} 
  ],
  "output": 3
}
```

###### Пример выходных данных

```
{
  "output": 43.0
}
```

---

[![Building Status](https://travis-ci.org/the0/pyfrbs.svg?branch=master)](https://travis-ci.org/the0/pyfrbs.svg?branch=master)
[![Coverage Status](https://coveralls.io/r/the0/pyfrbs?branch=master)](https://coveralls.io/r/the0/pyfrbs?branch=master)
