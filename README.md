# Using Python for extracting and loading data

In this lab, you will write a set of scripts that will download a file of addresses from the web, geocode those addresses using the Census Bulk Geocoding API, and load the resulting data into a database. These are the types of scripts that would be used in a data pipeline.

The scripts that you'll populate are:
* _pipeline_01_download_addresses.py_
* _pipeline_02_geocode_addresses.py_
* _pipeline_03_insert_addresses.py_ **OR** _pipeline_03_insert_addresses.sql_

For this lab you may need a Python environment with the packages `requests`, `pandas`, `sqlalchemy`, and `psycopg2-binary` installed. You may choose whatever tool you are comfortable with to manage your Python environment, but in the examples below I use _poetry_ to manage my environment, and I have included files in this folder for using poetry. Once you open this folder in your terminal, you can run the following command to install the required packages:

```bash
poetry install
```
__________

## Building data pipelines

Generally, the core steps of any data pipeline are:

* **Extract** -- Retrieve data from somewhere outside of your system and cache it somewhere in your system with minimal alteration.
* **Load** -- Take some data from your system and insert it into a transactional or analytical database.
* **Transform** -- Do some work on the data in your system to get it closer to a format/structure appropriate for the purposes of querying and analysis.

Sometimes you'll hear of **ETL** or **ELT**, implying that there's some correct order to these processes. In practice, there are often several iterations of each of these steps in a pipeline (James Densmore refers to a common pattern as "EtLT" in chapter 3 of the _Data Pipelines Pocket Reference_ available online at [O'Reilly for Higher Education](http://pwp.library.upenn.edu.proxy.library.upenn.edu/loggedin/pwp/pw-oreilly.html) through the UPenn Library).

## I. Extracting data from a remote URL

In an extract process there are two distinct steps:
1. Download or export data from some remote service, then
2. Save the file somewhere predictable in your system (today we're just going to save to our local machine).

Sometimes you might want to add a date and/or time into the file name of the file that you save, so that you can differentiate it from files that you downloaded before. The methods `date.today()` or `datetime.now()` from the `datetime` module could be useful in that case.

The following sample code requests data from a URL on the web, and saves the content of the response to a local file that includes the date when the download took place:

```python
import datetime as dt
import requests

response = requests.get('<URL of data>')

outfile_path = f'data/name_of_file_{dt.date.today()}.csv'
with open(outfile_path, mode='wb') as outfile:
    outfile.write(response.content)
```

> **Writing to a file**
>
> The basic way to open a file for writing in Python is to use the `open(...)` function. Usually we'll use `open` along with a `with` block, because closing the file will be taken care of automatically when we're dont with it.
>
> We can open files in different "modes". Above, we opened our file for writing (`w`) in binary mode (`b`). Since `response.content` is simply a string of bytes (it could be a JSON string, an image, a shapefile, ...), opening our file for writing in binary mode is usually safest. See the [Python docs](https://docs.python.org/3/library/functions.html#open) for more info about file modes.

**Complete the _pipeline_01_download_addresses.py_ script so that it downloads data from the URL https://storage.googleapis.com/mjumbewu_musa_509/lab04_pipelines_and_web_services/get_latest_addresses and saves that data to a file. Inspecting the response content or headers may be helpful to understand the data first. You can use tools like `curl`, [Postman](https://www.postman.com/), or just Python. For example, the following Python snippet will give you the value of the `Content-Type` header:**

```python
import requests
response = requests.get('https://storage.googleapis.com/mjumbewu_musa_509/lab04_pipelines_and_web_services/get_latest_addresses')
response.headers['Content-Type']
```

**Once you have completed the Python script, you can run it from your terminal with:**

```bash
poetry run python pipeline_01_download_addresses.py
```

## II. Extracting data from an API endpoint

Using an API endpoint is _fundamentally_ the same as downloading a static file from a server. In both cases what happens is:

1. **Client sends request** - You use a client (like your web browser, the `curl` command, or the `requests` library) to send an HTTP request to a server.
2. **Server processes request** - The server receives your request and decides what data to return to you. That data could be pre-generated, i.e. a static file, or dynamically generated based on your request.
3. **Server sends response** - The server constructs and sends a response with the appropriate data based on your request.
4. **Client processes response** - Your client receives the response.

The main functional difference is that, often (but not always) with API endpoints there is some additional context that we send with a request that may change the response that we get back.

### How do we send extra context?

> The precise way that we send additional context to an API endpoint depends on the request **method** that we're using:
> * Requests using the method **GET** usually have this content sent in the form of "query parameters" in the request URL
> * Requests using the method **POST** usually send extra content in the request body
>
> When we use a library like `requests` we usually don't have to worry about which way the extra context is being sent.

Using the `requests` library in Python, we can send request parameters using a dictionary in a `data` argument, like this:

```python
import requests

response = requests.get(
    '<URL of API endpoint>',
    data={
        'param_1': 'value_1',
        'param_2': 'value_2',
    })
```

Some API endpoints will also allow (or require) us to send files along as extra context with our request. This will usually require us to make a **POST** request, as files get added into the request body, and **GET** requests don't allow us to include additional data in the request body. In Python, using `requests`, this looks like:

```python
import requests

with open('<Path to file>', mode='rb') as opened_file:
    response = requests.post(
        '<URL of API endpoint>',
        data={
            'param_1': 'value_1',
            'param_2': 'value_2',
        },
        files={
            'file_label_1': opened_file,
        })
```

Note that the file is opened for reading (`r`) in binary (`b`) mode. Doing so is strongly recommended by the [Requests documentation](https://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file).

**Complete the _pipeline_02_geocode_addresses.py_ script so that it geocodes the addresses from the file downloaded in the first extract step. You can run your script with:**

```bash
poetry run python pipeline_02_geocode_addresses.py
```

## III. Loading data into the database

We don't have to use a single language to do everything in our pipeline. That's one of the advantages of chunking up our pipeline into different steps. For example, we can extract our data with python, and then choose to load our data using Python _or_ SQL, using some other tool to tie the parts of our pipeline together later.

To load data into the database with Python we _could_:
* Use the `create_engine` function to create a SQLAlcehmy database engine to connect to our database, then
* Use the `read_csv` function to load our data into a Pandas Dataframe, and finally
* Use the `to_sql` function to write our dataframe to a database.

For example:

```python
import pandas as pd
import sqlalchemy as sqa

db = sqa.create_engine('postgresql://[dbuser]:[dbpassword]@localhost:5432/[dbname]')

# If our CSV file doesn't have a header, we can explicitly provide one.
column_names = ['field_name1', 'field_name2', 'field_name3']
df = pd.read_csv('[file path]', names=column_names)
df.to_sql('[table name]', db)
```

Alternatively, we could use SQL to load our data into the database using `create table` and `copy` commands.

**Fill out either the _pipeline_03_insert_addresses.py_ or the _pipeline_03_insert_addresses.sql_ file to complete your pipeline. In the Python script, use the Pandas [`to_sql`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html) documentation to make sure you can explain why I used each of the parameters that I did for that function.**

**You can run the python file with the command:**

```bash
poetry run python pipeline_03_insert_addresses.py
```

**Or run the sql file with the command (replacing `[database_name]` with he name of your database):**

```bash
psql [database_name] < pipeline_03_insert_addresses.sql
```
