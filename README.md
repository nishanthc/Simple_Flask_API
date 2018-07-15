#
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

    curl http://localhost:5000/todos -d "id=4525&title=The Songs Name&artist=The Artists Name&duration=150&2018-05-17 16:56:21 new" -X POST -v
