# Task 1 

A simple API written for
https://github.com/flockcover/tech-screen-instructions/blob/master/Task1.md. To
get it running you'll need to install Python 3.x as it uses features from the 
3.x branch.

Once you have Python 3 installed call, install the dependencies with:

```
pip install -r requirements.txt
```

And run the API with 

```
python api.py
```

To see it working, I suggest you use curl in a seperate terminal i.e.

```
curl http://127.0.0.1:5000/api/v0/drones
curl http://127.0.0.1:5000/api/v0/drones/1
```

The API is set to log out information to the console so check the console
for how, if and when caching has been set.


