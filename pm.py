import json, os, sys, hashlib, base64, getpass
from cryptography.fernet import Fernet

VAULT = os.path.expanduser("~/.pm_vault.enc")
HASH_FILE = os.path.expanduser("~/.pm_master.hash")

def derive_key(password):
    h = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(h)

def get_fernet():
    if not os.path.exists(HASH_FILE):
        print("Vault not initialized. Run: pm.py init")
        sys.exit(1)
    pw = getpass.getpass("Master password: ")
    with open(HASH_FILE) as f:
        stored = f.read().strip()
    if hashlib.sha256(pw.encode()).hexdigest() != stored:
        print("Wrong password.")
        sys.exit(1)
    return Fernet(derive_key(pw))

def load_vault(f):
    if not os.path.exists(VAULT):
        return {}
    return json.loads(f.decrypt(open(VAULT,"rb").read()))

def save_vault(f, data):
    open(VAULT,"wb").write(f.encrypt(json.dumps(data).encode()))

def cmd_init():
    pw = getpass.getpass("Set master password: ")
    if getpass.getpass("Confirm: ") != pw:
        print("Passwords do not match.")
        sys.exit(1)
    with open(HASH_FILE,"w") as f:
        f.write(hashlib.sha256(pw.encode()).hexdigest())
    fernet = Fernet(derive_key(pw))
    save_vault(fernet, {})
    print("Vault initialized.")

def cmd_add(service, username):
    pw = getpass.getpass(f"Password for {service}: ")
    f = get_fernet()
    vault = load_vault(f)
    vault[service] = {"username": username, "password": pw}
    save_vault(f, vault)
    print(f"Saved {service}.")

def cmd_get(service):
    import subprocess
    f = get_fernet()
    vault = load_vault(f)
    entry = vault.get(service)
    if not entry:
        print(f"No entry for {service}.")
        sys.exit(1)
    print(f"Username: {entry['username']}")
    try:
        subprocess.run(["pbcopy"], input=entry["password"].encode())
        print("Password copied to clipboard.")
    except Exception:
        print(f"Password: {entry['password']}")

def cmd_list():
    f = get_fernet()
    vault = load_vault(f)
    if not vault:
        print("Vault is empty.")
    for s, e in vault.items():
        print(f"  {s:20} {e['username']}")

def cmd_delete(service):
    f = get_fernet()
    vault = load_vault(f)
    if service in vault:
        del vault[service]
        save_vault(f, vault)
        print(f"Deleted {service}.")
    else:
        print(f"No entry for {service}.")

args = sys.argv[1:]
if not args: print("Usage: pm.py [init|add|get|list|delete]")
elif args[0] == "init": cmd_init()
elif args[0] == "add" and len(args) == 3: cmd_add(args[1], args[2])
elif args[0] == "get" and len(args) == 2: cmd_get(args[1])
elif args[0] == "list": cmd_list()
elif args[0] == "delete" and len(args) == 2: cmd_delete(args[1])
else: print("Unknown command.")
