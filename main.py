from reader_csv import read_and_parse_csv
from processor_csv import log_processor
import writer_csv

def main ():
    data_grouped = read_and_parse_csv("logs.log")
    if data_grouped is not None:
        log_messages = log_processor(data_grouped)
    if log_messages:
       writer_csv.write_logs(log_messages)
       
if __name__ == "__main__":
    main()