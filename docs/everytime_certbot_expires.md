# One stupid thing I have to do if I end up docker-compose down and docker-compose up

I will have to re-install all python libraries
Otherwise I will keep on getting internal server error with no indication of what the hell is wrong

And as usual I have to do 

- ```systemctl start jspanda```
- ```nginx -s reload```

I added ```entrypoint``` to ```jspanda``` container with ```python -m pip install -r /app/requirements.txt``` command and hoping next time I don't have to manually reinstall python libraries.

