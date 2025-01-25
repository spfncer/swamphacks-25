# Swamphacks 

[Gabriel Aldous](https://github.com/Sn00pyW00dst0ck), [John Spurrier](https://github.com/john-spurrier), [Spencer Fasulo](https://github.com/spfncer), [Benjamin Bryant](https://github.com/Bencb03)

## Comment-tary

**Comment-tary** is a Chrome Extension which allows users to share insights and reviews of any webpage, with the goal of providing its users with more insight into the trustworthiness of online pages and their contents. Powered by FastAPI, MongoDB, and ***(OTHERE HERE)***, Comment-tary provides a fast and reliable method to easily peer review online sources. With markdown editing support and its retro user interface styling, it brings about the "old-school" internet feel and trustworthiness to the "new-school" websites. 

### Installation

To install Comment-tary in your browser, navigate to the extensions store and search for 

### Developer Setup

> [!NOTE]
> Ensure that you have Python3.11 or higher installed before setting up the backend. 

First, git clone this repository, then refer to the following instructions to setup each part of the development environment locally.

#### Extension

#### Backend

First, create a `.env` file within the `/backend` directory, following the strucutre of the `sample.env` file. 
Add the appropriate fields to the `.env` file to point to your MongoDB instance.

To install dependencies of the FastAPI server, run the following commands within the `/backend` folder:
```
pip install -r requirements.txt
```

To run the FastAPI server, execute the following command from within the `/backend/src` folder: 
```
fastapi dev main.py
```

To install dependencies of the FastAPI server unit tests, run teh following command within the `/backend` folder:
```
pip install -r requirements.dev.txt
```

To run the project's unit tests, execute the following command from with in the `/backend` folder:
```
python -m pytest test
```

