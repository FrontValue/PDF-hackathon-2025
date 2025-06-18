# PDF-hackathon-2025

Install and configure Python 3.8 or higher installed on your system.

Using homebrew, you can install Python with the following command:

```bash
brew install python
```

By installing Python, you will also get `pip3`, which is the package manager for Python.

## Installation

```bash
git clone https://github.com/yourusername/PDF-hackathon-2025.git
cd PDF-hackathon-2025
pip3 install -r requirements.txt
```

## Deploying changes and running the project

```bash
ssh frontvalue3@frontvalue3.fritz.box # connect to raspberry pi
hackathon # type password when asked

cd PDF-hackathon-2025 # open folder
git pull # pull changes from git repo
source venv/bin/activate # virtual environments
pip3 install -r requirements.txt # install packages if new once were added, if not - skip this part
python3 app.py # start to project
# to stop run: pkill -f app.py
```

## Start the project

To start the project, run the following command:

```bash
./start.sh
```

## Stopping the project

```bash
./stop.sh
```

To stop the project, run the following command:

```bash
./stop.sh
```
