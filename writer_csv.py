def write_logs(logs):
    with open("log.txt", "w") as log_file:
        for row in logs:
            log_file.write(f"{row}\n")