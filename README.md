
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

  `track_id=[integer]`<br>
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

