# recollection

This django project is only composed as of now of one application (words)
that allows you to store Japanese Words and English Words in an easy manner.
You can add readings to your words.
It also automatically tracks kanjis used in Japanese words and allows for easy lookup through either readings or kanjis. 

- create a .env file at the root of the project
- put values for the following variables:
    - ```POSTGRES_USER=recollectionuser```
    - ```POSTGRES_PASSWORD=12345```
    - ```POSTGRES_DB=recollection```
    - ```SECRET_KEY=thisisaveryveryverysecretkey```
- use ```docker-compose up``` to start the project
- use ```docker exec -it recollection_web_1 python manage.py migrate``` to make the necessary migrations
