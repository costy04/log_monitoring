import pandas as pd

def log_processor(data_grouped: pd.core.groupby.generic.DataFrameGroupBy) -> list[str]:
    # This function processes the grouped data and generates log messages based on the duration of processes.

    log_messages = []

    # Iterate through each group in the grouped data
    for pid, group in data_grouped:
        print(f"Processing PID: {pid}")
        print("Group size: %d" % len(group))

        if pid is None or pid == 'nan':
            continue

        # Filter the group for START and END statuses
        start_rows = group[group['Status'] == 'START']
        end_rows = group[group['Status'] == 'END']

        # Proceed only if both START and END exist
        if not start_rows.empty and not end_rows.empty:
            start_time = start_rows['Timestamp'].iloc[0]
            end_time = end_rows['Timestamp'].iloc[0]

            # Skip if the end time is before the start time (invalid case)
            if start_time > end_time:
                log_messages.append(f"ERROR: Process {description} with PID {pid} ended before it started")
                continue

            # Calculate the duration in minutes
            duration = (end_time - start_time)
            duration_minutes = duration.total_seconds() / 60
            description = start_rows['Description'].iloc[0]

            # Classify process based on duration thresholds
            if duration_minutes >= 10:
                status = "ERROR"
            elif duration_minutes >= 5:
                status = "WARNING"
            else:
                status = "OK"

            log_messages.append(f"{status}: Process {description} with PID {pid} ended after {duration_minutes:.2f} minutes")

    return log_messages