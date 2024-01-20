# python image
FROM python:3.11.6

WORKDIR /Project-1-EasyA

# installs system dependencies for Tkinter
RUN apt-get update -y && apt-get install -y tk

RUN pip install Pillow
# copies app source code to container
COPY . .
# runs Tkinter application
CMD ["python3", "launchGUI.py"]
