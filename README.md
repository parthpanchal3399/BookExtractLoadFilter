# Book Database Project

This project consists of three phases: Collect, Prepare, and Access. Each phase builds upon the previous one to create a comprehensive book database system.

## Demo

Watch the demo video: [YouTube Demo](https://www.youtube.com/watch?v=abiD6zVLpGo)

## Project Structure

1. CollectPhase
2. PreparePhase
3. AccessPhase

**Note:** Output from one phase is used as input to the next. Execute the projects in the order listed above.

## Requirements

- Python 3.10 (strict requirement for AccessPhase due to XQuery library compatibility)
- MySQL Server

## Setup

1. Clone the repository:
   
`git clone https://github.com/parthpanchal3399/BookExtractLoadFilter.git`

2. Install virtualenv:

`pip install virtualenv`

## Phase 1: CollectPhase

1. Navigate to the CollectPhase directory:

`cd CollectPhase`


2. Create and activate a virtual environment:

`python -m venv .venv`

`.venv/Scripts/activate`


3. Install dependencies:

`pip install -r requirements.txt`


4. Run the collection script:

`python CollectMain.py --output "Path_to_XML_Output" --schema "Books.xsd"`



## Phase 2: PreparePhase

1. Ensure MySQL Server is running and note down its credentials.

2. Navigate to the PreparePhase directory:

`cd PreparePhase`


3. Create and activate a virtual environment:

`python -m venv .venv`

`.venv/Scripts/activate`


4. Install dependencies:

`pip install -r requirements.txt`


5. Run the preparation script:

`python PrepareMain.py --server MySQLServerName --username MySQL_Username --password MySQL_Password --input "Path_to_XML_output_from_CollectPhase"`


Note: `--password` is optional and can be skipped if no password is set.

Default MySQL settings (unless changed during installation):
- Server: localhost
- Username: root
- Password: (empty)

## Phase 3: AccessPhase

1. Ensure MySQL Server is running.

2. Navigate to the AccessPhase directory:

`cd AccessPhase`


3. Create and activate a virtual environment:

`python -m venv .venv`

`.venv/Scripts/activate`


4. Install dependencies:

`pip install -r requirements.txt`


5. Run the Django development server:

`python manage.py runserver`


6. Open the URL displayed in the console in your web browser.

## Web Application Features

The web application has two main components:

1. SQL Filters
2. XQuery Filters

When applying a filter, the corresponding SQL Query or XQuery is displayed in the textbox, and the resulting rows are populated in the table.





