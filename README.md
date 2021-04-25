# AudioServer 

 A FastAPI service that simulates the behavior of an audio file server while using a SQL database. 

### Overview 
Audio file type can be one of the following:
1. Song
2. Podcast
3. Audiobook

### AudioMetaData 
- Song file fields:
    - ID – (mandatory, integer, unique)
    - Name of the song – (mandatory, string, cannot be larger than 100
    characters)
    - Duration in number of seconds – (mandatory, integer, positive)
    - Uploaded time – (mandatory, Datetime, cannot be in the past)
- Podcast file fields:
    - ID – (mandatory, integer, unique)
    - Name of the podcast – (mandatory, string, cannot be larger than 100
    characters)
    - Duration in number of seconds – (mandatory, integer, positive)
    - Uploaded time – (mandatory, Datetime, cannot be in the past)
    - Host – (mandatory, string, cannot be larger than 100 characters)
    - Participants – (optional, list of strings, each string cannot be larger than
    100 characters, maximum of 10 participants possible)
- Audiobook file fields:
    - ID – (mandatory, integer, unique)
    - Title of the audiobook – (mandatory, string, cannot be larger than 100
    characters)
    - Author of the title (mandatory, string, cannot be larger than 100
    characters)
    - Narrator - (mandatory, string, cannot be larger than 100 characters)
    - Duration in number of seconds – (mandatory, integer, positive)
    - Uploaded time – (mandatory, Datetime, cannot be in the past)


### API Description
Implemented create, read, upload, and delete endpoints for an audio file as defined below: 
- Create API: The request will have the following fields:
    - audioFileType – mandatory, one of the 3 audio types possible
    - audioFileMetadata – mandatory, dictionary, contains the metadata for one of the three audio files (song, podcast, audiobook)
- Delete API:
    - The route will be in the following format: `<audioFileType>/<audioFileID>`
- Update API:
    - The route be in the following format: `<audioFileType>/<audioFileID>`
    - The request body will be the same as the upload
- Get API:
    - The route `<audioFileType>/<audioFileID>` will return the specific audio
    file
    - The route `<audioFileType>` will return all the audio files of that type

## Project Setup 

### Requirements : 
#### Software required to run the service
1. Python 3.8+ 
2. MySQL DataBase

Create a databases for AudioServer and have the DataBase URL ready
#### Python Modules 
1. venv
2. FastAPI
3. SQLAlchemy
4. pydantic
5. uvicorn
6. python-decouple

Note : These can be installed through [requirements.txt](https://raw.githubusercontent.com/mohankumarpaluru/AudioServer/main/requirements.txt) provided

### Setup 

Clone this Repo and  open the repo root directory 

1. Setting up the virtual environment.
    ``` 
    $ python3.8 -m venv /path/to/AudioVenv
	$ source /path/to/AudioVenv/bin/activate
	(AudioVenv)$ pip install --upgrade pip
	(AudioVenv)$ pip install wheel
     ```
2. Install the service [Requirements](https://raw.githubusercontent.com/mohankumarpaluru/AudioServer/main/requirements.txt)
	```
	(AudioVenv)$ pip install -r requirements.txt 
	```
3. Create a `.env` file with the variables as below and store it in the root directory of the project (a .sample.env with parameters needed is provided)
	```
	DATABASE_URL=mysql+pymysql://user:passwd@localhost/audio_server
	AUDIO_SERVER_PORT=7201
	```

5.  Start the service
	```
	(AudioVenv)$ python3.8 run.py 
	```

After starting the service the API documentation can be found in the address below in the form of Swagger UI with interactive exploration, to call and test your API directly from the browser.
```
127.0.0.1:<AUDIO_SERVER_PORT>\docs
```
![Swagger UI](https://raw.githubusercontent.com/mohankumarpaluru/AudioServer/main/swagger_ui.png)

An Alternative Interactive API documentation web user interface With ReDoc is available at 
```
127.0.0.1:<AUDIO_SERVER_PORT>\redoc
```

## Using the Service
When the service is running, the below provided link can be used to test the service from browser/Postman
```
127.0.0.1:<AUDIO_SERVER_PORT>
```
The Request body for 

##### 1. Create
    url = / 
    method = Post
    content-type=application/json
    
   - Request body Schema :
        - song 
          
               {
                "audioFileType":"song",
                "audioFileMetadata":{
                    "id": "<any integer greater 0>",
                    "name":"<name of song, max length = 100>",
                    "duration":<time duration in seconds , greater than 0>
                    }
                }
        - podcast
            
	          {
               "audioFileType":"podcast",
               "audioFileMetadata":{
                    "id": <any integer greater 0>,
                    "name":"<name of podcast, max length = 100>",
                    "duration":<time duration in seconds , greater than 0>,
                    "host":"<hostname , max length = 100>",
                    "participants":"<name of participants , max length = 1000>"
                        }
              }      
        - audiobook
       
			  {
               "audioFileType":"audiobook",
                "audioFileMetadata":{
                    "id": <any integer greater than 0>,
                    "title":"<title of the book, max length = 100>",
                    "aurthor":"<name of aurthor , max length = 100>",
                    "narrator":"<name of narrator, max length = 100>",
                    "duration":<time duration in seconds , greater than 0>
                        }
              }                      

##### 2. Delete
    url = /{audio_type}/{audio_id}
    method = Delete
    content-type=application/json
##### 3. Update
    url = /{audio_type}/{audio_id}
    method = Put
    content-type=application/json
   - Request body Schema :
        - same as Create API
          
         
##### 4.  Get
To get all AudioFile by ID from an Audio Type

    
    url = /{audio_type}/{audio_id}
    method = Get
    content-type=application/json
To get all AudioFiles from an Audio Type
```
url = /{audio_type}
method = Get
content-type=application/json
```
#### Return Responses :
    - Action is successful: 200 OK
    - The request is invalid: 400 bad request
    - Any error: 500 internal server error

## References 
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
 - [FastAPI SQLAlchemy Documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/)
 - [Pydantic Schema Documentation](https://pydantic-docs.helpmanual.io/usage/schema/)
 - [Requests Documentation](https://docs.python-requests.org/en/master/)
