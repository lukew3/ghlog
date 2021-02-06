

def mod_config(encrypt, decrypt, new_token, new_repo_name):
    """ Configure ghlog. See ghlog config --help for options """
    if encrypt:
        activate_encryption()
    if decrypt:
        remove_encryption()
    if new_token is not None:
        set_token(new_token)
    if new_repo_name is not None:
        # Check if repo exists before creating it
        create_repo(repo_name=new_repo_name)


def encrypt_text(input):
    encoded = input.encode()
    f = Fernet(get_encryption_key())
    encrypted = f.encrypt(encoded)
    return encrypted


def decrypt_text(input):
    encoded = input.encode()
    f = Fernet(get_encryption_key())
    decrypted = f.decrypt(encoded)
    output = decrypted.decode()
    return output


def activate_encryption():
    make_encryption_key()
    encrypted_line = ""
    token = get_token()
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(get_remote_name())
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            # The 2 lines below remove files that are in the root directory, which are not logs
            if (file_content.path)[7] != '/':
                continue
            encrypted_line = encrypt_text(file_content.decoded_content.decode())
            file = repo.get_contents(file_content.path, ref="main")
            repo.update_file(file_content.path, "Encrypt logs", encrypted_line, file.sha, branch="main")


def remove_encryption():
    decrypted_line = ""
    token = get_token()
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(get_remote_name())
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            # The 2 lines below remove files that are in the root directory, which are not logs
            if (file_content.path)[7] != '/':
                continue
            decrypted_line = decrypt_text(file_content.decoded_content.decode())
            file = repo.get_contents(file_content.path, ref="main")
            repo.update_file(file_content.path, "Decrypt logs", decrypted_line, file.sha, branch="main")
    remove_encryption_key()
