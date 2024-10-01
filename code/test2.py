import math

# Координати станцій
stations = {
    "source1": (0, 0),
    "source2": (0, 100),
    "source3": (100, 0)
}

# Час прибуття сигналів (мілісекунди з початку епохи Unix)
timestamps = {
    "source1": 1727634385901.099,
    "source2": 1727634385901.2444,
    "source3": 1727634385901.3098
}


def calculate_time_differences(timestamps):
    """
    Calculate time differences between signal arrivals at each station.

    Args:
        timestamps (dict): Timestamps of signal arrivals at each station.

    Returns:
        dict: Time differences between signal arrivals at each station.
    """
    delta_t12 = timestamps["source2"] - timestamps["source1"]
    delta_t13 = timestamps["source3"] - timestamps["source1"]
    delta_t23 = timestamps["source3"] - timestamps["source2"]

    return {
        "delta_t12": delta_t12,
        "delta_t13": delta_t13,
        "delta_t23": delta_t23
    }


def calculate_distance_differences(time_differences):
    """
    Calculate distance differences between signal source and each station.

    Args:
        time_differences (dict): Time differences between signal arrivals at each station.

    Returns:
        dict: Distance differences between signal source and each station.
    """
    speed_of_light = 299792458  # m/s
    timestamp_conversion_factor = 1e-3  # convert milliseconds to seconds

    delta_t12 = time_differences["delta_t12"] * timestamp_conversion_factor
    delta_t13 = time_differences["delta_t13"] * timestamp_conversion_factor
    delta_t23 = time_differences["delta_t23"] * timestamp_conversion_factor

    delta_d12 = speed_of_light * delta_t12
    delta_d13 = speed_of_light * delta_t13
    delta_d23 = speed_of_light * delta_t23

    return {
        "delta_d12": delta_d12,
        "delta_d13": delta_d13,
        "delta_d23": delta_d23
    }


def solve_trilateration(stations, distance_differences):
    """
    Solve for the signal source location using trilateration.

    Args:
        stations (dict): Coordinates of the stations.
        distance_differences (dict): Distance differences between signal source and each station.

    Returns:
        tuple: Signal source location (x, y).
    """
    x1, y1 = stations["source1"]
    x2, y2 = stations["source2"]
    x3, y3 = stations["source3"]

    delta_d12 = distance_differences["delta_d12"]
    delta_d13 = distance_differences["delta_d13"]
    delta_d23 = distance_differences["delta_d23"]

    # Calculate coefficients for the system of equations
    a = 2 * (x2 - x1)
    b = 2 * (y2 - y1)
    c = x2 ** 2 - x1 ** 2 + y2 ** 2 - y1 ** 2 - delta_d12 ** 2

    d = 2 * (x3 - x1)
    e = 2 * (y3 - y1)
    f = x3 ** 2 - x1 ** 2 + y3 ** 2 - y1 ** 2 - delta_d13 ** 2

    g = 2 * (x3 - x2)
    h = 2 * (y3 - y2)
    i = x3 ** 2 - x2 ** 2 + y3 ** 2 - y2 ** 2 - delta_d23 ** 2

    # Solve the system of equations using substitution
    x = (c * e - f * b + f * a - c * d) / (a * e - b * d)
    y = (c * h - i * b + i * a - c * g) / (a * h - b * g)

    return x, y


def normalize_timestamps(timestamps):
    """
    Normalize timestamps by subtracting the minimum timestamp value.

    Args:
        timestamps (dict): Timestamps of signal arrivals at each station.

    Returns:
        dict: Normalized timestamps.
    """
    min_timestamp = min(timestamps.values())
    normalized_timestamps = {key: value - min_timestamp for key, value in timestamps.items()}
    return normalized_timestamps




def main():
    # Normalize timestamps
    normalized_timestamps = normalize_timestamps(timestamps)

    # Calculate time differences using normalized timestamps
    time_differences = calculate_time_differences(normalized_timestamps)
    distance_differences = calculate_distance_differences(time_differences)
    signal_source_location = solve_trilateration(stations, distance_differences)

    print("Signal source location:", signal_source_location)


if __name__ == "__main__":
    main()