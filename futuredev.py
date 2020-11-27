# import logging

# logging.basicConfig(filename="log",level= logging.INFO,
#                            format="%(asctime)s:%(message)s")



# machine_logger = logging.getLogger()
# machine_logger.setLevel(logging.INFO)
# machine_formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")
# machine_file_handler = logging.FileHandler("log")
# machine_file_handler.setFormatter(machine_formatter)
# machine_logger.addHandler(machine_file_handler)

# def log_machine(original_function):

#     def wrapper(self, time: object, loader: object):
#         logging.info(time.type, "Truck {} started at {}".format(self.id, time.now))
#         return original_function(self, time, loader)
#         # logging.info(time.type, "Truck {} finished {} at {}".format(self.id,original_function.__name__, time.now))
#         # return output
#     return wrapper 


# def logger(original_function):
#     logging.basicConfig(filename="program.log", level=logging.INFO)
#     def wrapper(self, time: object, loader: object):
#         logging.info("run {} truck {}".format(original_function.__name__,self.id))
#         return original_function(self, time, loader)
#     return wrapper 
