* Make a way for users to get entries from a certain time period
  * Use option to get logs from a certain year, month, or day
* Optimize data transfer time
  * Currently, the whole file has to be downloaded and then uploaded for the program to work
  * I could store it locally, but that would defeat the point of the project storing the file on Github and might risk security if the persons computer was compromised
* Delete last entry option in case a person regrets would rather not publish what they just wrote
* Updated date in .config would cause issues if using multiple different computers.
  * Maybe last updated date could be stored in comment under log content or could be determined from file contents
    * If data transfer time is optimized, this could become harder
      * One option, although unideal, would be to create a file in the github repo that stores the last updated date
        * If you could get the time or message of last commit you could accomplish the same function
