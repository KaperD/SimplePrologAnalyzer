## Анализатор

На вход принимается имя файла или строка (с флагами -s или --string). Программа в консольном выводе сообщит, корректен ли код. В случае, если код корректен, создаст .svg файл с деревом обхода.

## Сборка

```bash
$ mkdir bin
$ javac -d bin/ src/main/Main.java src/main/parser/* src/main/lexer/* src/main/svgDraw/* src/test/Tests.java src/test/assertions/*
$ java --class-path bin/ Main filename #запуск анализатора на файле filename
$ java --class-path bin/ Main -s 'f :- g.' #запуск анализатора на строке
$ java --class-path bin/ Tests #запуск тестов
```

