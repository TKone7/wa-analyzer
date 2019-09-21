# wa-analyzer

### WhatsApp Analyzer
This little Python command line tool allows you to analyze any of your direct chats in WhatsApp.

### Step 1: Install Python
You need to install python in order to run the script. See details here [install Python 3](https://docs.python-guide.org/starting/installation/).
### Step 2: Clone the Project with Git, install dependencies, and run it

For Mac / Linux, open your terminal and execute the following commands:

```
git clone https://github.com/TKone7/wa-analyzer.git
cd wa-analyzer
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```
On Windows you can open PowerShell and execute the following commands:

```
git clone https://github.com/superquest/digital-cash.git
cd .\wa-analyzer\
py -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

### Command Line Interface
You can run the main.py script with two different commands. The `test` command runs some automated testings which should all run without any errors.

The `analyze` command is used to parse an exported Whatsapp chat. The path to the file must be specified for example like this:
```
main.py analyze /home/peter/git/wa-analyzer/chat-xyz.txt
```
The additional parameter `--daily` gives a breakdown on a daily basis (how many messages per day and person). With '--limit' the maximum number of rows can be restricted. `--listall` shows all available results.
```
Whatsapp analyzer.

Usage:
  main.py test
  main.py analyze <filename>   [--daily] [--limit=<row> |--listall]

Options:
  -h --help     Show this screen.
  --listall     Always show all records.
  --limit=<row> Limits number of records [default: 20].
  --daily       Shows details on a daily level
```
