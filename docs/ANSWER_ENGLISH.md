
# Kapilan's MoovitaMix Data Pipeline Setup and Usage Guide

## Usage of the Solution

### Dependency

- Ensure you have **Python 3.7 or higher** installed on your system. 

### Setting Up The Environment

1.  **Install `virtualenv`** if you haven't already:

    > pip install virtualenv

2.  **Create a new virtual environment**:

    > virtualenv venv

3.  **Activate the virtual environment**:

- On Windows:


    > venv\Scripts\activate


- On macOS and Linux:


    > source venv/bin/activate


4.  **Navigate to the root directory of the project and install the package**: 

    > pip install . 

### Setting Environment Variables 

Before running the pipeline, you can set the following environment variables to customize the behavior:

-  `BASE_URL`: The base URL for the server (default is a predefined `DEFAULT_BASE_URL`)

-  `SCHEDULED_TIME`: The time at which the pipeline should run daily (default is a predefined `DEFAULT_SCHEDULED_TIME`)

-  `DATABASE_NAME`: The name of the database file (default is a predefined `DEFAULT_DATABASE_NAME`)

You can set these variables in your shell or create a `.env` file in the root directory with the following content:

```
BASE_URL=your_custom_base_url
SCHEDULED_TIME=your_custom_time
DATABASE_NAME=your_custom_database_name
```

### Running the Application

   1.  **Start the server**:

        Open a terminal and run:

        > start-server

   2.  **Run the pipeline once**:

        Open another terminal and run:

        > start-pipeline --test

   3.  **Run the pipeline when scheduled**:

        Open another terminal and run:

        > start-pipeline

   4.  **Run the Tests**:

        Open another terminal and run:

        > run-tests

### Additional Commands

- To see the help screen for the pipeline:

    > start-pipeline -h


### Notes

- The `start-pipeline` command will by default wait until the scheduled time to run. Use the `--test` flag to bypass this wait and run immediately.

- Make sure both the server and the pipeline are running for the full functionality of the application.

- The `run-tests` command will execute all the pytest tests in the project.