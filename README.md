# URL Shortster
An API to shorten long URLs


## Technologies used
* **[Python3](https://www.python.org/downloads/)**
* **[Flask](flask.pocoo.org/)**
* **[MongoDB](https://www.mongodb.com/try/download/community)** 
* **[Redis](https://redis.io/download)** 
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)**


## Installation / Usage

* These instructions are for a Ubuntu system (specifically Ubuntu 18.04)

* #### Dependencies
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



* #### Setup and Running it
* In the project directory run the following commands
    ```
        $ export FLASK_APP=run.py
        $ export FLASK_DEBUG=1
        $ flask run
    ```
* The above commands will start the server at localhost port 5000

* I have avoided using environment variable since there weren't any sensitive personal keys, all are generic ids

* #### Testing
    On a new terminal, goto the tests folder and run the following commands:

* To test the /create endpoint
    ```
    (venv)$ pytest test_create_url.py -s
    ```
* To test the /<shortcode> endpoint
    ```
    (venv)$ pytest test_redirect_url.py -s
    ```
* To test the /<shortcode>/stats endpoint
    ```
    (venv)$ pytest test_stats_url.py -s
    ```
* To test the /<shortcode>/delete endpoint
    ```
    (venv)$ pytest test_delete_url.py -s
    ```
