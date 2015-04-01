Нечёткая лингвистическая система, основанная на правилах Мамдани-типа
---------------------------------------------------------------------

Ядром системы является база знаний, представленных в виде нечётких правил. Представлена скриптом `schema.sql` для СУБД PostgreSQL.

Работа с базой знаний осуществляется через сервис, реализующий соответствующий программный интерфейс. Представлен файлами `service.py` и `service_run.py`, написан на python3 с использованием фреймворка Flask.

Имеется также графический интерфейс эксперта, предназначенный для просмотра, анализа и редактирования информации, накопленной в базе знаний. Написан на python3 с использованием библиотек psycopg2 и PyQt5. В данный момент подключается напрямую к базе, но в последующем будет переведён на программный интерфейс.

Подробнее можно почитать в [документации](https://pyfrbs.readthedocs.org).

---
[![Build Status](https://travis-ci.org/the0/pyfrbs.svg?branch=master)](https://travis-ci.org/the0/pyfrbs)
[![Coverage Status](https://coveralls.io/repos/the0/pyfrbs/badge.svg)](https://coveralls.io/r/the0/pyfrbs)
[![Docs Status](https://readthedocs.org/projects/pyfrbs/badge/?version=latest)](https://pyfrbs.readthedocs.org)
