import pandas as pd

def get_status_based_on_duration(duration_minutes: float) -> str:
    # This function classifies the process status based on the duration in minutes.
    if duration_minutes >= 10:
        return "ERROR"
    elif duration_minutes >= 5:
        return "WARNING"
    else:
        return "OK"

def log_processor(data_grouped: pd.core.groupby.generic.DataFrameGroupBy) -> list[str]:
    # This function processes the grouped data and generates log messages based on the duration of processes.

    log_messages = []

    # Iterate through each group in the grouped data
    for (pid, description), group in data_grouped:
        print(f"Processing PID: {pid} and Description: {group['Description'].iloc[0] if not group.empty else 'N/A'}")
        print("Group size: %d" % len(group))

        if pid is None or pid == 'nan':
            continue

        # Filter the group for START and END statuses
        start_rows = group[group['Status'] == 'START']
        end_rows = group[group['Status'] == 'END']

        # Proceed only if START exists without an END
        if not start_rows.empty and end_rows.empty:
            #If multiple STARTs exist, take the first one showed (decided by the timestamp)
            first_start = start_rows.nsmallest(1, 'Timestamp')
            start_time = first_start['Timestamp'].iloc[0]
            log_messages.append(f"ERROR: Process {description} with PID {pid} didn't end")
            continue

        # Proceed only if both START and END exist
        if not start_rows.empty and not end_rows.empty:

            # If multiple STARTs and multiple ENDs exist, take the first START and the first END showed (decided by the timestamp)
            first_start = start_rows.nsmallest(1, 'Timestamp')
            first_end = end_rows.nsmallest(1, 'Timestamp')

            start_time = first_start['Timestamp'].iloc[0]
            end_time = first_end['Timestamp'].iloc[0]

            # Skip if the end time is before the start time (invalid case)
            if start_time > end_time:
                log_messages.append(f"ERROR: Process {description} with PID {pid} ended before it started")
                continue

            # Calculate the duration in minutes
            duration_minutes = (end_time - start_time).total_seconds() / 60
            
            description = start_rows['Description'].iloc[0]

            # Classify process based on duration thresholds
            status = get_status_based_on_duration(duration_minutes)

            log_messages.append(f"{status}: Process {description} with PID {pid} ended after {duration_minutes:.2f} minutes")

    return log_messages