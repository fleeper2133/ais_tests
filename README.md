# Vue 3 + TypeScript + Vite

This template should help get you started developing with Vue 3 and TypeScript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about the recommended Project Setup and IDE Support in the [Vue Docs TypeScript Guide](https://vuejs.org/guide/typescript/overview.html#project-setup).

Команда для переноса данных в БД 
python manage.py parser_api
Сразу после запускаюся ротации

Команды для создания ротаций в курсах:
1. Для всех курсов разово:
python manage.py all_course_rotation

2. Для одного конкретного курса (при необходимости)
python manage.py make_rotation --course 1 --count 100
Создаёт ротацию для курса с id 1 на 100 вопросов