# Task 1 

## Get started

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


# Submission questions

## What assumptions did you have to make?

I've assumed that the latest copy of the data is canonical, and I've
not made any checks to see whether the data is corrupt. If the status
code is 200, then I assume it's legitimate data.

## Which technologies did you choose? Why?

My constraints was an hour of my time to get a fully working program,
so I chose Python and Flask as I'm most familiar with these having
most recently architected and built an API at `https://api.felix.com`
on this framework. They are my go to tools during hackathons, and I
know them well.

As a lanaguge, Python is strongly typed while not requiring type
annotations, it has a 'truthy' behaviour to empty containers (lists,
dicts etc) which I find makes it very fast to build and prototype
in. It's also synchronous so you don't have to worry about threads
etc, and debugging the code is very straightforward.

## What technical compromises did you have to make in order to achieve your solution? What is the severity of this tech debt, and what would a path to resolving it look like?

The caching technology itself is limited; caching is done in memory in
a dict (a hash map) which while quick is not going to scale and means
that we cannot have a shared cache among nodes in a cluster so there
is lots of duplication, cache misses. Because, it's in memory it's not
persistent, restarting the server or node wipes the cache. It is at
the very least a hash map, so it's O(1) so it's optimal
algorithmically.

Our implementation is mainly flawed because we don't know about the
data in Bob's API we are unable to make an optimization to caching
other than the data we have is probably the canonical data. There is
no documentation, no guarantee of service and no standards that we know
of that Bob adheres to.

The severity of the debt is quite bad, as it's a bad foundation if you
don't have any documentation or understanding on the upstream API. We
also don't have any long term data about the latency or performance of
the API, so the API could start taking seconds or minutes to return
data and it directly affects our performance. Ultimately, how 'severe'
it is in a business sense if whether this is going to customer facing
and whether it's a core part of the product. If it's a prototype piece
it doesn't need to be fast, but if it's customer facing and 2secs means
they don't convert to a sale then that's very severe.

The path to resolving the cache would be to not reinvent the wheel and 
make use of the avaialable products (redis, varish etc) and services
(GCP Memory Store, AWS Elasticache etc) which scale very well, have
near infinite storage and tooling to help monitor the health, performance
and availability of the cache,

# How do we run your code?

See [Get started](./Get started) above.

# What future features do you think we might be able to build based on this API?

Flock insures drones in flight, so I'll keep to features that make
sense within that context.

The drones are priced, and in various currencies, we could connect to
an FX API (xe.com etc) to resolve the price to a given currency to
normalise the data. This allows us to assess the cost of underlying
asset, it's likely to be a key component of insuring it.

The number of flights, and corresponding number of crashes gives us a
probability that a drone will crash, it's id and name allow us to track
this unique entity in the collection.

A basic algorithm such as:

```
price * probability_of_crash * premium * tax
```

... gets us to a rough insurance premium that we may wish to charge
the client.

If the API could be updated so that we could update the information
about the drone, i.e. it accept PUT requests to update the number of
crashes or better yet accepted POST requests and kept and immutable
log of the events then we could build a real-time resource whereby 
the insurance fluctuates based on the unit crashing, similar units 
crashing etc.

