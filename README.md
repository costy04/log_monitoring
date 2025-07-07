## Requirements
    • Python 3.12.0 installed 
    • Pandas installed (pip install pandas==2.1.4)
    • Pytest installed (pip install pytest==8.4.1)
## How to use
```bash
To run the file: python main.py (for the default input file) or python main.py -i path_to_input_file
The main.py takes a CSV file as an input and writes in another .txt file (log.txt) the output
To run the unit tests: pytest unit_testing.py
```

```bash
By default the application will import a file named logs.log from the same directory as the application but the user can provide a path to another file. The file structure needs to be as follows:
    • HH:MM:SS is a timestamp in hours, minutes, and seconds.
    • The job description.
    • Each log entry is either the “START” or “END” of a process.
    • Each job has a PID associated with it e.g., 46578.

```
## How it works
The application reads the CSV file using pandas. After the reading part, it will remove the lines with an invalid timestamp and group the data by PID and Description.

After the CSV is parsed, the processor function will take every group and calculate the duration of every process if it is possible, if it is not, it will log.

Corner cases:
```
    • A process that has invalid TIMESTAMP
        - in this case the application will remove that line entirely
    • Multiple processes may share the same PID, but occur at different points in time
        - to solve this a group by PID and Description was used
    • A process that has a START but not an END
        - in this case, an error will show saying that the process didn't finish
    • A process that has a END but not a START
        - in this case the applcaition will ignore the END without a START
    • A process that has the START timestamp after the END timestamp (start_time > end_time)
        - in this case, an error will show saying that the process ended before it started
    • A process that has multiple STARTs and ENDs
        - in this case the application will take for calculate the duration the first START and the first END
```
#