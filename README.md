# Flask Mongo Songs API
The application includes Flask for the API, Mongodb for the database and Mongo Express for the monitoring of the database data. 
Applications can work with docker containers

Configuration
---
Should create .env file with default.env for using of API. API can work with default values. If need to change, can change values
    
    cp default.env .env
    
Install
----
After installation, you should be waiting a few munites for service deploying

    docker-compose up -d --build

Initializing Data
----
After installation can be sent a GET request to the below endpoint. Have examples data in the data directory
    
    /api/songs/initial


Usage
---
After data initializing, can use API with postman collections and could reach with postman_collections directory.

    http://localhost:1996/api/songs

Endpoints
---
    Listing Songs | GET | {{base_url}}/api/songs?page=1&page_size=20&level=13&message=Opa
    Get Song Rating Score | GET | {{base_url}}/api/songs/6218eb4930c300f0494a5907/score
    Add rating to song | PUT | {{base_url}}/api/songs/6218eb4930c300f0494a5907/rating
    initializing of data | GET | {{base_url}}/api/songs/initial
    Add Song | DELETE | {{base_url}}/api/songs
