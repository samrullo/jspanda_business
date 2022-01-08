# flask run on Windows
```flask run``` doesn't work on Windows, because the application looks for exact file ```flask```, where on Windows it is ```flask.exe```

The solution is to run below instead

```
$ python -m flask run
```