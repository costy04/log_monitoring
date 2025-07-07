from reader_csv import read_and_parse_csv

def main ():
    data_grouped = read_and_parse_csv("logs.log")
    print("Data grouped by PID:")
    if data_grouped is not None:
        for pid, group in data_grouped:
            print(f"PID: {pid}")
            print(group)

if __name__ == "__main__":
    main()