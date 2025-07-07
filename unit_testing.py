from processor_csv import log_processor
from reader_csv import read_and_parse_csv


def test_csv(tmp_path):
    csv_content = """
    12:00:00,Job A,sTaRt,1
    12:01:00,Job B,STAR  T,2
    12:02:00,Job C,START,3
    12:0   3:00,Job A,end,1
    12:08:0 0,Job C,EN  D,3
    12:12:00,Job B,END,2
    """
    expected_output = [
        ("OK: Process Job A with PID 1 ended after 3.00 minutes"),
        ("ERROR: Process Job B with PID 2 ended after 11.00 minutes"),
        ("WARNING: Process Job C with PID 3 ended after 6.00 minutes"),]
    
    test_file = tmp_path / "test.csv"
    test_file.write_text(csv_content)

    data_grouped = read_and_parse_csv(str(test_file))
    actual_output = log_processor(data_grouped)
    
    assert expected_output == actual_output, f"Test failed for {test_file}"

def test_csv_with_multiple_starts_and_ends(tmp_path):
    csv_content = """
    12:00:00,Job A,START,1
    12:01:00,Job B,START,2
    12:03:00,Job B,START,2
    12:04:00,Job B,START,2
    12:05:00,Job B,START,2
    12:07:00,Job A,END,1
    12:12:00,Job B,END,2
    12:13:00,Job B,END,2
    """
    expected_output = [
        ("WARNING: Process Job A with PID 1 ended after 7.00 minutes"),
        ("ERROR: Process Job B with PID 2 ended after 11.00 minutes")]
    
    test_file = tmp_path / "test.csv"
    test_file.write_text(csv_content)

    data_grouped = read_and_parse_csv(str(test_file))
    actual_output = log_processor(data_grouped)

    assert expected_output == actual_output, f"Test failed for {test_file}"

def test_csv_with_just_start(tmp_path):
    csv_content = """
    12:00:00,Job A,START,1
    12:01:00,Job B,START,2
    12:03:00,Job B,START,2
    12:04:00,Job B,START,2
    12:05:00,Job B,START,2
    """
    expected_output = [
        ("ERROR: Process Job A with PID 1 didn't end"),
        ("ERROR: Process Job B with PID 2 didn't end")]
    
    test_file = tmp_path / "test.csv"
    test_file.write_text(csv_content)

    data_grouped = read_and_parse_csv(str(test_file))
    actual_output = log_processor(data_grouped)

    assert expected_output == actual_output, f"Test failed for {test_file}"

def test_csv_with_just_end(tmp_path):
    csv_content = """
    12:00:00,Job A,END,1
    12:01:00,Job B,START,2
    12:03:00,Job B,END,2
    """
    expected_output = [
        ("OK: Process Job B with PID 2 ended after 2.00 minutes")]
    
    test_file = tmp_path / "test.csv"
    test_file.write_text(csv_content)

    data_grouped = read_and_parse_csv(str(test_file))
    actual_output = log_processor(data_grouped)

    assert expected_output == actual_output, f"Test failed for {test_file}"

def test_csv_with_start_after_end(tmp_path):
    csv_content = """
    12:00:00,Job A,START,1
    12:01:00,Job A,END,1
    12:03:00,Job B,END,2
    12:04:00,Job B,START,2
    """
    expected_output = [
        ("OK: Process Job A with PID 1 ended after 1.00 minutes"),
        ("ERROR: Process Job B with PID 2 ended before it started")]
    
    test_file = tmp_path / "test.csv"
    test_file.write_text(csv_content)

    data_grouped = read_and_parse_csv(str(test_file))
    actual_output = log_processor(data_grouped)

    assert expected_output == actual_output, f"Test failed for {test_file}"

def test_csv_with_malformed_timestamp(tmp_path):
    csv_content = """
    12:00,Job A,START,1
    ,Job A,END,1
    12:03:00,Job B,START,2
    12:04:00,Job B,END,2
    """
    expected_output = [
        ("OK: Process Job B with PID 2 ended after 1.00 minutes")]
    
    test_file = tmp_path / "test.csv"
    test_file.write_text(csv_content)
    
    data_grouped = read_and_parse_csv(str(test_file))
    actual_output = log_processor(data_grouped)
    print(actual_output)

    assert expected_output == actual_output, f"Test failed for {test_file}"