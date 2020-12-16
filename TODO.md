
* Make sure repository exists before trying to get information from it
  * If user deletes the remote repo, errors are thrown

* Option to delete last entry in case a person regrets would rather not publish what they just wrote

* Make a logo for the app

* Make README in Github actions instead of locally if possible
  * Might require adding token as repo secret

* Make sure that folders are written as double digits even if their number is less than 10.
  * January should be saved as '01' not '1'
    * Same thing for days

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
