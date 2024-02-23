import sys

def state_code_to_string(state_code):
    """Converts a state code to its corresponding string value.

    Args:
    state_code: An integer representing the state code.

    Returns:
    The string value corresponding to the state code, or "Unknown" if the code
    is invalid.
    """

    state_map = {
        0: "power off",
        1: "power on",
        2: "discharge",
        3: "charge",
        4: "charge complete",
        5: "host mode",
        6: "shutdown",
        7: "error",
        8: "undefined",
    }

    return state_map.get(state_code, "Unknown")

def parse_binary_data(hex_data):
    """Parses a 64-bit hex number into slices and parse them in binary and decimal.

    Args:
    hex_data: The 64-bit number in hex format.

    Returns:
    The parsed data.
    """
    # Convert hex to binary string
    binary_data = bin(int(hex_data, 16))[2:].zfill(64)

    # Define slice ranges (inclusive)
    slice_ranges = {
        "type ": (4, 7),
        "time1": (36, 39),
        "time2": (24,31),
        "time3": (16,23),
        "time4": (8,15),
        "time5": (0,3),
        "state": (32, 35),
        "charge": (40, 47),
        "temp": (48, 55),
        "tail": (56, 63),
    }

    btime = ""
    state = ""
    charge = ""
    temp = ""
    # Parse each slice
    for name, (start, end) in slice_ranges.items():
        slice_binary = binary_data[start:end + 1]
        slice_decimal = int(slice_binary, 2)
        
        if name == "charge":
            # print(f"{name}: Binary: {slice_binary}, Decimal: {slice_decimal}")
            charge = slice_decimal / 2.0
        if name == "temp":
            # print(f"{name}: Binary: {slice_binary}, Decimal: {slice_decimal}")
            temp = (slice_decimal / 2.0) - 20
        if name == "state":
            state = state_code_to_string (int(slice_binary, 2))
        if name in ("time1", "time2", "time3", "time4", "time5"):
            btime += slice_binary
    # print (btime)
    dtime = int(btime, 2)
    return {"time": dtime, "state": state, "state_of_charge": charge, "temperature": temp}

def test_parse_bits(test_data):
    for t in test_data:
        result = parse_binary_data(t["payload"])
        assert result["time"] == t["decoded"]["time"]
        assert result["state"] == t["decoded"]["state"]
        assert result["state_of_charge"] == t["decoded"]["state_of_charge"]
        assert result["temperature"] == t["decoded"]["temperature"]
        print(result)

def get_test_data():
    # Run the test
    test_data = (
        {
            "payload": "F1E6E63676C75000",
            "decoded": {
                "time": 1668181615,
                "state": "error",
                "state_of_charge": 99.5,
                "temperature": 20.0
            }
        },
        {
            "payload": "9164293726C85400",
            "decoded": {
                "time": 1668453961,
                "state": "discharge",
                "state_of_charge": 100.0,
                "temperature": 22.0

            }
        },
        {
            "payload": "6188293726C75C00",
            "decoded": {
                "time": 1668454534,
                "state": "discharge",
                "state_of_charge": 99.5,
                "temperature": 26.0
            }
        }
    )
    return test_data

# test_parse_bits(get_test_data())

def make_input():
    input = {
                "device": "device1",
                "payload": get_test_data()[0]["payload"]
            }
    return input

def make_log_str(device, parsed_data):
    output = parsed_data
    print(parsed_data)
    log_str = f'{{"device": "{device}", "time": {output["time"]}, "state": "{output["state"]}", "state_of_charge": {output["state_of_charge"]}, "temperature": {output["temperature"]}}}'
    return log_str

if __name__ == "__main__":
    input = make_input()
    output = parse_binary_data(input["payload"])
    log_str = make_log_str(input["device"], output)
    print (log_str, file=sys.stdout)