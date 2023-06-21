GPCRtrack
=========
A light-weight server for tracking GPCR sequences and expression requests.

## Installation
```
cd /path/to/GPCRtrack
conda env create -n GPCRtrack -f environment.yml
```

## Usage
### Start the server
```
cd /path/to/GPCRtrack
conda activate GPCRtrack
python manage.py runserver 0.0.0.0:8000
```
use tmux to keep the server running in the background.

## management
### Create a superuser
```python manage.py createsuperuser --username=Mu_Wang ```
### clean databases
```python manage.py flush ```
### import csv to databases
```python csv_import.py ```


