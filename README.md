# hbm

A Django-based project.

## Overview

This repository contains the source code for a Django project. The structure and dependencies suggest it is designed for web application development using Django and Django REST Framework, with additional support for authentication, email handling, social login, and more.

## Project Structure

- `duinisveldbreugem/`  
- `floriway/`
- `hbm_app/`  
- `hbm_project/`  
- `static/`  
- `manage.py`  
- `requirements.txt`  

The main Django project appears to be in the `hbm_project/` directory, with at least one application in `hbm_app/`. There are other directories (`duinisveldbreugem`, `floriway`) which may contain additional apps or modules.

## Main Features

Based on the dependencies and structure, the project includes:

- Django framework (3.2.8)
- REST API support (`djangorestframework`)
- Authentication (JWT, Djoser, social-auth)
- Email and mail parsing capabilities
- Rate limiting and filtering
- Pre-commit hooks and linting tools for code quality
- Support for Excel, XML files, and pandas for data processing

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nexusameer/hbm.git
   cd hbm
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Usage

- Start the local server and access the project at `http://127.0.0.1:8000/`.
- Explore the apps and APIs as defined in the Django project.

## Requirements

See `requirements.txt` for the full list of dependencies.

## Contributing

Contributions are welcome. Please fork the repository and open a pull request.

## License

This project does not currently specify a license.
