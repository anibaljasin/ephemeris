# Ephemeris

flask rest api to get ephemeris of the dates stored.

## Getting started

In case you want to test this project you need to follow the next steps:

### Dependencies

- Python 3+ is needed
- Clone this repo `git clone https://github.com/juniorjasin/ephemeris.git`
- Install requirements by doing `pip install -r requirements.txt`

### Run server

The server will be listening by default in the `localhost:4000`.

#### Run with python

- Execute the entrypoint file `$ python app.py`

#### Run with Docker

##### Build Dockerfile image

You can build the Dockerfile image and run it by doing:
```bash
$ docker build -t ephemeris:1.0 .
$ docker run -p 4000:4000 -ti --rm ephemeris:1.0
```

##### Use docker-compose

In case you want to use docker-compose, you need to do the following:
```bash
$ docker-compose build  # This is only necessary if you didn't build the image before
$ docker-compose up
```

### Populate database

The script `python ìnit_db.py` will create some ephemeris in the database.  


## API Usage 

To create you custom ephemeris in the database you can do the following:
```bash
$ curl -X POST localhost:4000/efemerides -d '{"name":"dia del lateral izquierdo", "date":"2020-07-20"}' -H 'Content-Type:Application/json'
{
    "ephemeris": {
        "id": 8,
        "name": "dia del lateral izquierdo",
        "date": "2020-07-20"
    }
} 
```

To retrieve an specific ephemeris you can do:
```bash
curl -X GET 'localhost:4000/efemerides?day=2020-04-29'                                                   master    
{
  "2020-04-29": "dia de la mascota", 
  "mes": {
    "01": "None", 
    "02": "None", 
    "03": "None", 
    "04": "None", 
    "05": "None", 
    "06": "None", 
    "07": "None", 
    "08": "None", 
    "09": "None", 
    "10": "None", 
    "11": "None", 
    "12": "None", 
    "13": "None", 
    "14": "None", 
    "15": "None", 
    "16": "None", 
    "17": "None", 
    "18": "None", 
    "19": "None", 
    "20": "None", 
    "21": "None", 
    "22": "None", 
    "23": "None", 
    "24": "None", 
    "25": "None", 
    "26": "None", 
    "27": "None", 
    "28": "None", 
    "29": "dia de la mascota", 
    "30": "None"
  }
}
``` 

### Run unit tests

To execute the unit test created you need to do the following:
```bash
$ python -m unittest discover test
...
...
----------------------------------------------------------------------
Ran 23 tests in 0.319s

OK
``` 


## Things to add/improve and known issues

- Add swagger
- Add user authentication
- Deploy to web server
- Render with SOAP view
- Cache for requests
- Take configuration from environment variables
- Improve `ìnit_db.py` by using sqlalchemy already created class 
- Take ephemeris from a real ephemeris api like `https://efemerides20.com/documentacion`
- Mount a volume for database so the data stored while using the docker containers won't be lost
- Remove the database from the project and create it if necessary
- Create Makefile to run some scripts to populate db, run tests, etc.
- Config logger properly

