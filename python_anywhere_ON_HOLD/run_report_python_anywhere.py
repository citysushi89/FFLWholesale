# Program specifically for listing on Python Anywhere which will have its own time to run
# Do not need time elements because Python Anywhere will do that


# TODO update: with new wholesalers as added
# If time.now is in the list, runs the reports

from mge_wholesale_functionality import get_mge_wholesale_data
get_mge_wholesale_data()
from grice_wholesale_functionality.py import get_grice_wholesale_data
get_grice_wholesale_data()
from chattanooga_shooting_functionality.py import get_chattanooga_shooting_data
get_chattanooga_shooting_data()
from second_amendment_wholesale_functionality.py import get_second_amendment_wholesale_data
get_second_amendment_wholesale_data()
from orion_wholesale_functionality.py import get_orion_wholesale_data
get_orion_wholesale_data()

