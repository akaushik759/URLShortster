# URL Shortster
An API to shorten long URLs

## Table of Contents

   * [Technologies used](#technologies-used)
   * [Installation / Usage](#installation--usage)
      * [Dependencies](#dependencies)
      * [Setup & Running it](#setup-and-running-it)
      * [Testing](#testing)
   * [Database Schema](#database-schema)
   * [Algorithm / Explanation](#algorithm--explanation)
   * [Scripts to maintain the database](#scripts-to-maintain-the-database)
   * [API Endpoints](#api-endpoints)
      * [Create a short url](#create-a-short-url)
      * [Redirect using short url](#redirect-using-short-url)
      * [Get stats of a short url](#get-stats-of-a-short-url)
      * [Delete short url](#delete-short-url)



## Technologies used
* **[Python3](https://www.python.org/downloads/)**
* **[Flask](flask.pocoo.org/)**
* **[MongoDB](https://www.mongodb.com/try/download/community)** 
* **[Redis](https://redis.io/download)** 
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)**


## Installation / Usage

* These instructions are for a Ubuntu system (specifically Ubuntu 18.04)

 #### Dependencies
* Please ensure that you have python3 installed, after which you may create a virtual environment, the steps are mentioned [here](https://naysan.ca/2019/08/05/install-python-3-virtualenv-on-ubuntu/).

* Git clone this repo to your PC
    ```
        $ git clone git@github.com:akaushik759/URLShortster.git
    ```

* Then proceed to install the dependencies from the requirements.txt, using the command below
    ```
        $ pip install -r requirements.txt
    ```
* Install Redis Server in your system, the steps are mentioned [here](https://linuxize.com/post/how-to-install-and-configure-redis-on-ubuntu-18-04/).

* Then in a new terminal start the Redis server by using the command below

    ```
        $ redis-server
    ```
* Incase it shows "Creating Server TCP listening socket :6379: bind: Address already in use" error, then this [article](https://stackoverflow.com/a/57087763/7821772) shall help you fix it

* After fixing any errors, the Redis server should be listening at localhost port 6379



 #### Setup and Running it
* In the project directory run the following commands
    ```
    (venv)$ export FLASK_APP=run.py
    (venv)$ export FLASK_DEBUG=1
    (venv)$ flask run
    ```
* The above commands will start the server at localhost port 5000

* I have avoided using environment variable since there weren't any sensitive personal keys, all are generic ids

 #### Testing
* On a new terminal, goto the tests folder and run the following commands:

* To test the /create endpoint
    ```
    (venv)$ pytest test_create_url.py -s
    ```
* To test the /< shortcode > endpoint
    ```
    (venv)$ pytest test_redirect_url.py -s
    ```
* To test the /< shortcode >/stats endpoint
    ```
    (venv)$ pytest test_stats_url.py -s
    ```
* To test the /< shortcode >/delete endpoint
    ```
    (venv)$ pytest test_delete_url.py -s
    ```
## Database Schema
 
 #### URL Collection (Contains all the urls with their respective short urls)
 
```
Fields :
	_id - ObjectID (autogenerated)
	original_url - URL (required)
	short_code - string (required, unique)
	timestamp - datetime
	access_times - string
	unique_id - string (required)
```
 #### ShortURL Collection (Contains all short urls generated for use)
 
```
Fields :
	_id - ObjectID (autogenerated)
	short_code - string (required, unique)
	used - boolean (required)
```
## Algorithm / Explanation

URL shortening service helps you to share short urls instead of long URLs. 

This API helps you shorten urls by automatically alloting a short 6 letter short code (a-zA-Z0-9), or by providing your custom short url (which should be >= 4 characters).

The direct approach to building the backend of this would be -
	
*	User enters original url, take the url, use some algorithm and hash it to generate a short custom url. 

*	Some hash algorithms are MD5, SHA256, etc. Since we are using only 62 characters, the possible combinations of short urls could be 62^6 = 57 billion combinations, that would easily suffice our requirements.
	So we could provide the original url and hash it using any of the algorithms, however these algorithms usually generate a string of more than 8 characters, but we need of only 6 characters, the normal approach would be to use only the first 6 of the generated hash, but that could increase the chances of collision, since we don't know what the first 6 characters represents and whether it would be unique.

*	Another concern would be that we would be hashing the original urls, so if 2 users provide the same original urls, they would get the same hased short url, which would be a difficult problem to deal with.

*	We could get around this by making our own hashing algorithm, I thought of combining datetime with an autoincrementing counter which appends to the datetime, but that would require fetching the last count from the database and then increasing, there are 2 problems with this -
		1. More queries to the database
		2. When multiple urls are being requested at the same time the collision chances increases, so we have to keep increasing the counter until one is unique

*	I thought of skipping this entire problem by keeping short urls separately generated and ready to use. 
	Advantages of this approach :
		1. No queries to database to see if short url already taken
		2. No chances of duplication/collision
		3. Short URLs can be generated via a background script and added to the database 

*	A possible problem could be, what if short urls gets over. We can deal with this by already keeping more than enough in our database ready, and since 57 billion strings are possible, we would not run out of strings.

*	Since there is no authentication system for this API, each url creation returns a unique id (generated by hashing the short url), which the user needs to provide in the request header to view the analytics or delete the url

*	So the final algorithms are :
	1. Create without custom url

	User enters original id (without a custom short url) and sends a request
	The system, fetches an unused short url from the ShortURL database and allots it to this given id and stores it in the URL database, at the same time updates the ShortURL db that this custom url is now used.
	The response contains a unique id which the user needs inorder to check analytics or delete the short url 
	
	2. Create with custom url

	User enters original id, with custom url and sends a request
	The system checks if the custom url has been used from the ShortURL db, if not then allots it and updates the ShortURL db else returns a failure response
	The response contains a unique id which the user needs inorder to check analytics or delete the short url
	
	3. Redirect 

	User enters the short url, its first checked in the cache (all urls which are requested more than 100 times are cached so that highly active urls are fetched faster), if not present then in the database, the corresponding datetime is marked for analytics
	
	4. Stats

	User enters custom url, also they need to provide the unique_id which was given to them during url creation, so that they can view the url analytics.
	
	5. Delete

	User enters custom url, also they need to provide the unique_id which was given to them during url creation, so that they can delete the url.
	
	6. Each generated url will have an expiry period of 6 months, i.e. after 6 months all expired urls will be deleted and the corresponding short urls free to be reused

## Scripts to maintain the database

* To add new short urls of length 6 to the ShortURL database, run the following command
    ```
    (venv)$ python scripts/short_url_generator.py
    ```
* To delete expired urls from the database, run the following command
    ```
    (venv)$ python scripts/expired_url_deleter.py
    ```

## API Endpoints

 #### Create a short url 
```
	1. /create

	POST - Used to create a short url with or without a custom url

	Input : original url(required), custom url (optional, length >=4)

	Header : {"Content-Type":"application/json; charset=utf-8"}
	
	Output : 
		Success - { 
				'status':'success', 
				'message':'', 
				'data': 
					{
						'_id':{'$oid':''},
						'original_url':'',
						'short_code':'',
						'timestamp':'',
						'unique_id':''
					}
				} 201
		Error - {'status':'error', 'message':''} 400/422/500

	Example :
	{
		"message": "successfully alloted short custom URL", 
  		"status": "success",
  		"data": {
    				"_id": {"$oid": "5fd703eaf90eaadea5810303"}, 
    				"original_url": "https://www.google.com", 
    				"short_code": "abcc", 
    				"timestamp": {"$date": 1607926757144}, 
    				"unique_id": "fuzRCRfewhztb2r7s8zScH"
  			}
  
	}
```
 #### Redirect using short url 
```
	1. /<shortcode>

	GET - Used to access the short url to get the original url

	Input : 
	
	Output : 
		Success - {'status':'success', 'message':'', 'data':} 200
		Error - {'status':'error', 'message':''} 400/500

	Example :
	{
		"message": "successfully found the original url", 
  		"status": "success",
  		"data": {
    				"original_url": "https://www.google.com"
  			}
  
	}
```
 #### Get stats of a short url
```
	1. /<shortcode>/stats

	GET - Used to get stats of a short url

	Input : 

	Header : {"Content-Type":"application/json; charset=utf-8", "unique_id":"<id>"}
	
	Output : 
		Success - {'status':'success', 'message':'', 'data':} 200
		Error - {'status':'error', 'message':''} 400/422/500

	Example :
	{
		"message": "successfully found the original url", 
  		"status": "success",
  		"data": {
    				"access_times": [
      					"2020-12-14 06:50:27.703653+00:00", 
      					"2020-12-14 06:50:27.714914+00:00"
    					], 
    				"count": 2, 
    				"last_accessed_time": "2020-12-14 06:50:27.714914+00:00", 
    				"registration_time": "Mon, 14 Dec 2020 06:50:19 GMT"
  			}
  
	}
```
 #### Delete short url
```
	1. /<shortcode>/delete

	DELETE - Used to delete the short url

	Input : 

	Header : {"Content-Type":"application/json; charset=utf-8", "unique_id":"<id>"}
	
	Output : 
		Success - {'status':'success', 'message':''} 200
		Error - {'status':'error', 'message':''} 400/422/500

	Example :
	{
		"message": "successfully deleted the url", 
  		"status": "success"
  
	}
```
