<p align="center">
  <img src="Docs/icon.png" width="250">  
</p>

<p align="center">
   <b>BrickBuddy</b> is a desktop Lego app for creating <br> and managing wishlists and collections.
</p>


## About the project

BrickBuddy is a desktop application designed for Lego enthusiasts to manage their Lego sets effectively. Whether you're organizing your collections, creating wishlists, or adding notes to your favorite sets, BrickBuddy provides a user-friendly interface to streamline your Lego hobby.


## Features 
- View Lego sets based on themes
- Wishlist sets 
- Create custom collections
- Add notes to sets, collections, and wishlisted items
- Easily add, remove, and update items


## Prerequisites
1. [Download Python](https://www.python.org/downloads/) (v3.12+)


## Installation
1. Clone the project from GitHub:
```bash
git clone https://github.com/MiraZzle/brick-buddy.git
cd brick-buddy

```
2. Change directory to the project:
```bash
cd brick-buddy
```

## Virtual Environment and Dependencies
1. Initialize Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
2. Install Dependencies
```bash
pip install -r requirements.txt
```

## API key
This project uses the BrickSet API to fetch Lego set information. To use the API:
1. Request Brickset [web services key](https://brickset.com/tools/webservices/requestkey)
2. Copy the API key into a file named `brickset_api_key.txt` in the root directory of the project.

## Running the Application
To run BrickBuddy, execute:
```bash
python main.py
```

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests.
