from itertools import count


class Loader:

    def __init__(self, working_status: bool, start_working_time):
        self.working = working_status
        self.available_time = start_working_time


class Truck:
    _counter = count(0)

    def __init__(self, truck_id: int, loading_dur: int, hauling_dur: int, dumping_dur: int, returning_dur: int,
                 truck_status: str, time: object, max_round: int):
        self.index = next(self._counter)
        self.id = truck_id
        self.loading_duration = loading_dur
        self.hauling_duration = hauling_dur
        self.dumping_duration = dumping_dur
        self.returning_duration = returning_dur
        self.event_time = time.now
        self.status = truck_status
        self.round = 0
        self.working = False
        self.starting_activity = 0
        self.finishing_activity = 0
        self.maximum_round = max_round
        self.gone = False

    def process(self, time: object, loader: object, writable_text_file):
        if not self.gone:
            if self.status == "returning":
                if not loader.working:
                    if time.type == "simulation":
                        self.round = self.round + 1
                    return self.load(time, loader, writable_text_file)
                else:
                    self.starting_activity = time.now
                    self.finishing_activity = time.now + self.loading_duration
                    write_this = "{} Truck {} stays in the queue. therefore it could not start loading at {}".format(
                        time.type, self.id, time.now)
                    # print(write_this)
                    writable_text_file.write(write_this + "\n")

            elif self.status == "loading":
                return self.haul(time, writable_text_file)

            elif self.status == "hauling":
                return self.dump(time, writable_text_file)

            elif self.status == "dumping":
                return self.truck_return(time, writable_text_file)

            else:
                write_this = "ERROR: Truck {} is {} at time {}. Something is not right!".format(
                    self.id, self.status, time.now)
                writable_text_file.write(write_this + "\n")
                return None, None, None

    def load(self, time: object, loader: object, writable_text_file):

        write_this = "{} Truck {} started Loading at {}".format(
            time.type, self.id, time.now)
        # print(write_this)
        writable_text_file.write(write_this + "\n")

        start_time = time.now
        time.add(self.loading_duration)

        write_this = "{} Truck {} finished Loading at {}".format(
            time.type, self.id, time.now)
        # print(write_this)
        writable_text_file.write(write_this + "\n")

        finish_time = time.now

        if time.type == "simulation":
            loader.working = True
            loader.available_time = finish_time
            self.status = "loading"
            self.starting_activity = start_time
            self.finishing_activity = finish_time

        time.reset(self.loading_duration)
        return start_time, finish_time, self.index, self.status, self.round

    def haul(self, time: object, writable_text_file):

        write_this = "{} Truck {} started hauling at {}".format(
            time.type, self.id, time.now)
        # print(write_this)
        writable_text_file.write(write_this + "\n")

        start_time = time.now
        time.add(self.hauling_duration)

        write_this = "{} Truck {} finished hauling at {}".format(
            time.type, self.id, time.now)
        # print(write_this)
        writable_text_file.write(write_this + "\n")

        finish_time = time.now

        if time.type == "simulation":
            self.status = "hauling"
            self.starting_activity = start_time
            self.finishing_activity = finish_time

        time.reset(self.hauling_duration)
        return start_time, finish_time, self.index, self.status, self.round

    def dump(self, time: object, writable_text_file):

        write_this = "{} Truck {} started dumping at {}".format(
            time.type, self.id, time.now)
        # print(write_this)
        writable_text_file.write(write_this + "\n")
        start_time = time.now
        time.add(self.dumping_duration)

        write_this = "{} Truck {} finished dumping at {}".format(
            time.type, self.id, time.now)
        # print(write_this)
        writable_text_file.write(write_this + "\n")

        finish_time = time.now

        if time.type == "simulation":
            self.status = "dumping"
            self.starting_activity = start_time
            self.finishing_activity = finish_time

        time.reset(self.dumping_duration)
        return start_time, finish_time, self.index, self.status, self.round

    def truck_return(self, time: object, writable_text_file):
        """
        docstring
        """
        write_this = "{} Truck {} started returning at {}".format(
            time.type, self.id, time.now)
        # print(write_this)
        writable_text_file.write(write_this + "\n")

        start_time = time.now
        time.add(self.returning_duration)

        write_this = "{} Truck {} finished returning at {}".format(
            time.type, self.id, time.now)
        # print(write_this)
        writable_text_file.write(write_this + "\n")

        finish_time = time.now

        if time.type == "simulation":
            self.status = "returning"
            self.starting_activity = start_time
            self.finishing_activity = finish_time

        time.reset(self.returning_duration)
        return start_time, finish_time, self.index, self.status, self.round
