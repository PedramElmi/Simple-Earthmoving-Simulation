class Time:
    def __init__(self, time_type) -> None:
        self.type = time_type
        self.now = 0

    def add(self, duration):
        self.now += duration
        return self.now

    def reset(self, duration):
        self.now -= duration


def read_csv_truck_data(csv_file_path: str):
    import csv
    with open(csv_file_path, "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=",", quotechar='"')
        data = [row for row in reader]
    data = data[1:]
    for index0, first in enumerate(data):
        for index1, second in enumerate(first):
            try:
                data[index0][index1] = eval(second)
            except NameError:
                continue
    return data


def write_csv(filepath: str, data_list: list):
    import csv
    data_list.insert(0, ["start", "finish", "ID", "activity"])
    with open(filepath, 'w') as file:
        for event in data_list:
            wr = csv.writer(file)
            wr.writerow(event)
    return None
