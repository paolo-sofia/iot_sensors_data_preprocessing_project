## Demo

To start the demo, assuming you have docker installed, cd into the project directory
and run the following command:

```
docker compose build
docker compose up -d
```

Once started, open your web browser and go to the following url:

```
http://localhost:8501/
```

Here you can access the web ui. Give it a bit of time since all the containers needs to be started.
After a while you should see a little form where you can customize the kind of data you want to get.
Hit the submit button to send the requests, then wait a little, and you should see an output. If everything went
well, a table with the computed statistics on the data will be shown, elsewhere you'll see an error message.

## Solution

### Architecture

![architecture.jpg](docs%2Farchitecture.jpg)

The proposed solution is based on 3 different tools:

- **kafka** for data streaming
- **spark** for processing data
- **api** for sending user requests through the web ui

The main idea was to build an architecture with scalability and fault tolerance in mind, thinking about the fact that in
this kind of scenario many new sensors can be added or removed, so the system should be ready for this. Another think
that was accounted for was the user interaction, here an assumpion was made, that is that the user is not reqeusting
data in real time, but as the assignment suggests, only requests data once in a while based on a specific time frame, so
I assumed that the amount of api requests was not large.
The programming language used is python, both for personal preference and also for speed on development, since
personally I've been coding in python for the last 2 years.

### Why Kafka and spark?

They're both excellent tools when it comes to scalability and fault tolerance, for kafka we can instanciate a single
broker at the beginning, and we can increase the number of brokers if the demand increases. The same approach can be
used
for spark, we can create a single worker, and we can increase the number of workers if the demand increases.
For the fault tolerance part, Kafka can replicate data accross partitions and brokers so it is a good solution if we
want to have always data available and not lose them. For spark, we can use a similar approach, since the master can
recreate a worker if one fails, so we always have a worker running

### Why the api?

I thought the best solution for this kind of situation is to use an api for the user to interact with the database and
get the data needed. As said before, also for the api we can scale up the number of processes (an idea would be to
autoscale replicas) as the number of requests increases, and also adding a load balancer.

### Optional Task

This solution is optimal also for the optional task. Indeed, if we would like to build a data pipeline for model
predictions, we could just add a new spark worker that reads the data from the kafka topic, and preprocess them to feed
them to the prediction model. Obviously the prediction model could be implemented as a second api call, using tools like
seldon or similar, in which the api accepts the features and outputs the model prediction.
This solution is also optimal if we want to train machine learning models. For instance, we could attach a kafka
connector sink like the bigquery sink or postgres one, to save the data to a db to be used later for the training of a
machine learning model.   
So to recap, the components needed to add this extension are:

- a new Spark worker that reads data from Kafka topic (Kafka consumer)
- a new api call that accepts model feature as input and returns the model prediction
  Pipeline flow:
- data are read into spark
- spark pre-process data to build features for model prediction
- api call
  An important thing to take into account is to preprocess the data accurately, like standardize/normalize data if
  needed, apply one hot encoding and usual machine learning preprocess steps.

### Web UI

For the web ui I used a python library called streamlit, I used it mainly because it's really easy to set up. In the ui
you'll see a simple form and a submit button. Always keep an eye in the top right corner, if the ui is doing something
in the background (like waiting for the api response), you'll see some icons changing and the message "RUNNING", so wait
until this message disappear.

### Cons of the solution

As said before the cons of this solution is that we do not have a dashboard that updates in real time, since the api
reads the data in a specific timeframe and returns the computed values. Another cons are that the api call needs a bit
of time to execute, since the spark worker has to compute all the statistics about the requested data.

