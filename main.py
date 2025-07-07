from reader_writer_csv import read_and_parse_csv, write_logs
from processor_csv import log_processor
import argparse


def main ():
    parser = argparse.ArgumentParser(description="Log Monitoring Application")
    parser.add_argument(
        "-i", "--input", type=str, default="logs.log",
        help="Path to input CSV log file"
    )

    args = parser.parse_args()

    data_grouped = read_and_parse_csv(args.input)
    if data_grouped is not None:
        log_messages = log_processor(data_grouped)
    if log_messages:
       write_logs(log_messages)
       
if __name__ == "__main__":
    main()