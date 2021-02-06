from .config_access import set_token, get_token, get_remote_name, make_encryption_key, get_encryption_key, get_config_file, make_empty_config, remove_encryption_key
from github import Github
from tqdm import tqdm


def mod_fetch(datestring, today):
    """ Returns logs from the passed date (Use format yyyy/mm/dd)"""
    output_lines = []
    output = ""
    token = get_token()
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(get_remote_name())
    if today and datestring == '':
        datestring = datetime.now().strftime("%Y/%m/%d")
    try:
        if datestring == '':
            contents = repo.get_contents("entries")
        else:
            contents = repo.get_contents("entries/" + datestring)

        # Count number of files; This takes about half a second for 20 files
        file_count = 0
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                file_count += 1

        # initialize progress bar
        pbar = tqdm(total=file_count)
        # Get file contents and add to output_lines
        if datestring == '':
            contents = repo.get_contents("entries")
        else:
            contents = repo.get_contents("entries/" + datestring)

        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                log_contents = file_content.decoded_content.decode()
                if get_encryption_key() != '':
                    log_contents = decrypt_text(log_contents)
                output_lines.append(log_contents)
                pbar.update(1)
        output = '\n'.join(output_lines)
        pbar.close()
    except Exception as ex:
        print(ex)
        output = "No entries found for specified day(s)"
    print(output)

