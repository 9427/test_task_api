Все данные хранятся в таблице employees.  
Название в API|Содержимое|Тип данных
---|---|---
lastname|Фамилия|string
firstname|Имя|string
patronym|Отчество|string
birthyear|Год рождения|integer
id|Табельный номер|integer
salary|Оклад|Decimal
jobname|Должность|string
company|Юр. лицо|string
department|Подразделение|string

Методы API:  
------
#### Все сотрудники в базе  
```/api/v1/employees/all```  
Не принимает никаких аргументов, возвращает данные о сотрудниках в формате json.  
  
#### Поиск по базе  
```/api/v1/employees?firstname=Vasya&lastname=Pupkin```  
Находит всех сотрудников в базе, соответствующих данным аргументам.  Принимаемые аргументы: firstname, lastname, patronym, id.  
  
#### Добавление сотрудника  
```/api/v1/employees/add?lastname=Pupkin&firstname=Vasya&patronym=Ivanovich&birthyear=1994&id=1235&salary=60000&jobname=Junior Pomidor Developer&company=RedApple&department=Pomidor Team```  
Добавляет сотрудника в базу. Все аргументы являются обязательными, ID не должен совпадать с существующим.  
  
#### Изменение сотрудника  
```/api/v1/employees/update?search_id=1235&jobname=Middle Pomidor Developer&salary=140000```  
Изменяет данные сотрудника с нужным id в базе. id сотрудника для изменения должен быть целым числом, и записываться в search_id. Если какие-либо аргументы не будут указаны в запросе, они сохранят свое предыдущее значение.  
  
#### Удаление сотрудника  
```/api/v1/employees/delete?id=1235```  
Удаляет сотрудника, соответствующего поисковому запросу. Для предотвращения удаления всех данных при неправильно составленном запросе не удаляет больше одного сотрудника за раз. Принимает для поиска все аргументы из таблицы employees, но рекомендуется использовать id, так как он уникален.
