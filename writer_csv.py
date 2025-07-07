def write_logs(logs):
    with open("log.txt", "w") as log_file:
        for row in logs:
            # Only write if there are at least 5 elements in the tuple
            if len(row) >= 5:
                log_file.write(f"{row}\n")