**Instructions**
----

Start the server by running api.py<br><br>
By default the server will start on port 5000.

**Show Track**
----
  Returns json data about a single track.

* **URL**

  /track/:track_id

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `track_id=[integer]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"track": [{"id": "5", "title": "Paparazzi", "artist": "Lady GaGa", "duration": "199", "last_play": ' \
       '"2016-02-23 08:24:37"}]}`

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{\"message\": \"track 100000 doesn\'t exist\"}`

* **Sample Call:**

    curl http://localhost:5000/tracks/10

**Filter Tracks by Name**
----
  Filters tracks by title their title.

* **URL**

  /track/filter_by_name

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `filter_text= [string]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
    "tracks": [
        {
            "id": "3667",
            "title": "I Get The Sweetest Feeling",
            "artist": "Jackie Wilson",
            "duration": "165",
            "last_play": "2018-05-17 14:05:28"
        }
    ]
}`



* **Sample Call:**

    curl http://localhost:5000/tracks/filter_by_name/I%20Get%20The%20Sweetest%20Feeling
    
**Create new track**
----
  Adds a new track and returns json data about the track

* **URL**

  /track

* **Method:**

  `POST`

*  **URL Params**

   **Required:**

   None

* **Data Params**

  `id=[integer]`<br>
 `title=[string]`<br>
 `artist=[string]`<br>
 `duration=[integer]`<br>
 `lastplay=[datetime]`
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"track": [{"id": "1436", "title": "A new song!", "artist": "A New Artist", "duration": "259", "last_play": ' \
       '"2018-02-23 08:24:37"}]}`

* **Error Responses:**

  * **Code:** 409 CONFLICT <br />
    **Content:** `{"message": "track 1 already exists"}`


* **Sample Call:**

    curl http://localhost:5000/tracks -d "id=4525&title=The Songs Name&artist=The Artists Name&duration=150&2018-05-17 16:56:21 new" -X POST -v


**Last Played**
----
  Returns last 100 played tracks (the latest first).

* **URL**

  /last_played

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
    "tracks": [
        {
            "id": "394",
            "title": "Love Generation",
            "artist": "Bob Sinclar / Gary Nesta Pine",
            "duration": "172",
            "last_play": "2018-05-17 16:59:11"
        },
        {
            "id": "583",
            "title": "Jus.....`


* **Sample Call:**

    curl http://localhost:5000/last_played
    
    
 **Artists**
----
  Returns all artists along with the number of tracks they have and their most recently played track.

* **URL**

  /artists

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
    "tracks": [
        {
    "artists": [
        {
            "artist": "Belinda Carlisle",
            "plays": 3,
            "last_played_track": "Heaven Is A Place On Earth"
        },..`


* **Sample Call:**

    curl http://localhost:5000/artists