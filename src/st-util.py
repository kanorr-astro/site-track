#Utility functions for project SITE-TRACK

month_day = [-1, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, -1, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]


def leap_year(year) ->bool:
    if (year % 4) == 0:
        return True
    else:
        return False
    
def month_to_day(month) ->float:
    if leap_year(year) == True:
        return month_day[month+11]
    else:
        return month_day[month-1]


year = 2001
month = 3

print(leap_year(year))
print(month_to_day(month))
