* Make a way for users to get entries from a certain time period
  * Use option to get logs from a certain year, month, or day
* Optimize data transfer time
  * Currently, the whole file has to be downloaded and then uploaded for the program to work
  * I could store it locally, but that would defeat the point of the project storing the file on Github and might risk security if the persons computer was compromised
  * Multithread so that while user is typing input, data is being fetched
* Delete last entry option in case a person regrets would rather not publish what they just wrote
* Make sure repository exists before trying to get information from it
  * If user deletes the repo, errors are thrown
