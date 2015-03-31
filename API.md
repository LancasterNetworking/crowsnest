# API

Call the API, get data.

### Sessions

Get data regarding user sessions

#### List Sessions
Find all sessions currently being tracked by the application

`URL = HOST:PORT + '/api/sessions'`

**Example URL**

http://10.0.0.3:8080/api/sessions

**Example Response**
````json
{
  "sessions": [
    "10.0.0.1 10.0.0.2 1426522231", 
    "10.0.0.1 10.0.0.2 1426522374"
  ]
}
````

#### Session Data
Return all data for specific session IDs. Get data for multiple sessions with one query by separating `session_id`s with commas.

`URL = HOST:PORT + '/api/sessions/' + session_id`

**Example URL**

http://10.0.0.3:8080/api/sessions/10.0.0.1%2010.0.0.2%201426522231

* Note, because session identifiers are delimetered by spaces, you'll need to replace those spaces with `%20` as found in the example URL.

**Example Response**
````json
{
  "10.0.0.1 10.0.0.2 1426522231": [
    {
      "mimeType": "video/mp4",
      "src_ip": "10.0.0.1",
      "timestamp": 1426522232,
      "file_": "bunny_2s1.m4s",
      "host": "10.0.0.2",
      "height": "360",
      "startWithSAP": "1",
      "width": "480",
      "bandwidth": "334349",
      "codecs": "avc1",
      "duration": 2,
      "path": "/bunny_2s/bunny_2s_400kbit/bunny_2s1.m4s",
      "bitrate": 400,
      "id": "6"
    }
  ]
}
````

##### Optional Fields

It's possible to retrieve only the fields that are useful for your application by using the "fields" query string parameter.

Field			| Description
:--------------	| :---------- 
mimeType		| Internet media type, indicates the type of content requested
src_ip			| IP address of the client requesting content
timestamp		| Epoch time when the get request was received
file_			| The file requested
host			| Destination IP/hostname of the get request
height			| Height of the requested video in pixels
width			| Width of the requested video in pixels
startsWithSAP	| *N/A*
bandwidth		| Size of the requested segment in bytes (please confirm?)
codecs			| The codec the requested segment has been encoded with
duration		| The duration of the segment in seconds
path			| The full path as present in the URL
bitrate			| The bitrate of the video segment
id				| *N/A*

**Example URL**

http://10.0.0.3:8080/api/sessions/10.0.0.1%2010.0.0.2%201426522231?fields=timestamp,file_

**Example Response**
````json
{
  "10.0.0.1 10.0.0.2 1426522231": [
    {
      "timestamp": 1426522232,
      "file_": "bunny_2s1.m4s"
    },
    {
      "timestamp": 1426522232,
      "file_": "bunny_2s1.m4s"
    }
  ]
}
````

##### Newest only

Append `mostRecent=True` to your URL to get the single most recent record for each session

**Example URL**

http://10.0.0.3:8080/api/sessions/10.0.0.1%2010.0.0.2%201426522231?fields=timestamp,bitrate&mostRecent=True

**Example Response**
````json
{
  "10.0.0.1 10.0.0.2 1426522231": [
    {
      "timestamp": 1426522232,
      "file_": "bunny_2s1.m4s"
    },
    {
      "timestamp": 1426522232,
      "file_": "bunny_2s1.m4s"
    }
  ]
}
````