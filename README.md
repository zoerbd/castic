# castic

Graphical fullstack webmanagement for restic.

# Requiremets

...

# Building

1. Change directory to wherever you have the directory, including this file.
2. Just execute the basic setup with: ```pip install -e .```
3. Recommended: Optionally if you want a full setup to be created by an interactive installer, run this command: ```src/bin/installme.py```

# Test webapp
I used gunicorn for testing and deploying the app.
Example:
	```gunicorn castic.wsgi:application```
