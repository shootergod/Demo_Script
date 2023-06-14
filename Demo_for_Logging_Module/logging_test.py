import os
import logging
import logging.config

wd = os.path.dirname(__file__)
conf_path = os.path.join(wd, 'logging.conf')

# seting everything by read config file
logging.config.fileConfig(conf_path)

app_logger_name = 'applog'

# get root logger
root_logger = logging.getLogger()
# get self-defined app logger
app_logger = logging.getLogger(app_logger_name)


# logging: root logger
root_logger.debug(" [root logger] This is debug log")
root_logger.info(" [root logger] This is info log")
root_logger.warning(" [root logger] This is warning log")
root_logger.error(" [root logger] This is error log")
root_logger.critical(" [root logger] This is critical log")

# logging: app logger
app_logger.debug(" [app logger] This is debug log")
app_logger.info(" [app logger] This is info log")
app_logger.warning(" [app logger] This is warning log")
app_logger.error(" [app logger] This is error log")
app_logger.critical(" [app logger] This is critical log")