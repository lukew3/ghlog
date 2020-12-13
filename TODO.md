* Make a way for users to get entries from a certain time period
  * Use option to get logs from a certain year or month
  * Day already done

* Optimize data transfer time
  * Currently, the whole file has to be downloaded and then uploaded for the program to work
  * I could store it locally, but that would defeat the point of the project storing the file on Github and might risk security if the persons computer was compromised
  * Multithread so that while user is typing input, data is being fetched

* Make sure repository exists before trying to get information from it
  * If user deletes the remote repo, errors are thrown

* Option to delete last entry in case a person regrets would rather not publish what they just wrote

* Add option to save local copy of repo to make the application faster
