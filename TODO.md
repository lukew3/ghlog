
* Make sure repository exists before trying to get information from it
  * If user deletes the remote repo, errors are thrown

* Option to delete last entry in case a person regrets would rather not publish what they just wrote

* Make a logo for the app

* Make README in Github actions instead of locally if possible
  * Might require adding token as repo secret

* It might be cool to have a progress bar when creating a README if it takes a long time when the repo gets bigger
  * Found this code:
  ```
  import time
  from tqdm import tqdm
  for _ in tqdm(range(100)):
    time.sleep(1)
  ```
    * I would have to calculate the number of files in the specified range before grabbing their data. That might take a lot of time to get, which kind of ruins the whole thing. However, I might be able to get it quickly, I just havent tried it yet.

* If there already is an encryption key in config, decrypt and re-encrypt logs currently in Repository
  * Currently, logs are just encrypted twice, thus making the data umreadable

* Could combine all files from a day into one after the day has passed. That would help with fetch times.
