# Telegram Group Cloner
A script to clone Telegram chats/groups wrote on Telethon. Albums supported.

## Usage:
1. Download [Python 3.10.10](https://www.python.org/downloads/release/python-31010/)
While installing check the Add Python to PATH box
2. Open cmd (WIN+R -> cmd -> enter), type
```sh
pip install Telethon```
3. Download and unpack archive
4. Go to folder of unpacked archive in cmd
```sh
cd path-to-files```
5. run python main.py


### Edit config.py file before use
API_ID - get from my.telegram.org
API_HASH - get from my.telegram.org

PHONE_NUMBER - phone number or name of .session file in source path (with no extension)

SOURCE and DESTINATION - can be get by forwarding any message from those channel or group to https://t.me/chatIDrobot Telegram Bot

COOL_DOWN - interval in seconds between sending a message to destination group


