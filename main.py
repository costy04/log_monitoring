from reader_csv import read_and_parse_csv

def main ():
    data_grouped = read_and_parse_csv("logs.log")
    log_messages = []
    if data_grouped is not None:
        from processor_csv import log_processor
        log_messages = log_processor(data_grouped)
    print(len(log_messages))
    for message in log_messages:
        print(message)
if __name__ == "__main__":
    main()