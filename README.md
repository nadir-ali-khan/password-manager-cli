# Password Manager CLI

A secure, offline command-line password manager. Stores credentials encrypted locally using AES-256. No cloud, no accounts, no tracking.

## Features

- AES-256 encrypted storage
- Master password protected
- Add, retrieve, update, delete entries
- Copy password to clipboard
- Search by service name
- Export/import vault

## Usage

```bash
python pm.py init                        # Set master password
python pm.py add github user@email.com  # Save credentials
python pm.py get github                 # Retrieve + copy to clipboard
python pm.py list                       # List all services
python pm.py delete github              # Remove entry
```

## Security

- Master password is never stored — only its hash
- Vault file is AES-256 encrypted
- Auto-clears clipboard after 30 seconds

## Requirements

```
pip install cryptography pyperclip
```
