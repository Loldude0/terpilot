tmp_time_data = {
    "CMSC330": {"0101":["1130050", None, "1130050", None, None], "0102": ["1130050", None, "0930050", None, None]},
    "CMSC351": {"0101":["0830050", None, "1330050", None, None], "0102": ["1130050", None," 0930050", None, None]},
    "ENGL101": {"0101":[None, "0800075", None, None, "1600050"], "0102": ["1130050", None, "0930050", None, None]}
}

def check_time_slot(time_table,day,start_time,duration):
    start_hour = int(start_time[:2])
    start_minute = int(start_time[2:])
    duration = int(int(duration)/10)
    return (time_table[day*24*6 + start_hour*6 + int(start_minute/10)] == False) & (time_table[day*24*6 + start_hour*6 + int(start_minute/10) + duration] == False)

def generate_schedule_aux(class_lst, time_table, idx, lst, res):
    class_names = list(class_lst.keys()) # ["CMSC330", "CMSC351", "ENGL101]
    #print(class_names)
    sections = class_lst[class_names[idx]] # {"0101":["1130050", None, "1130050", None, None], "0102": ["1130050", None, "0930050", None, None]}
    section_names = sections.keys()
    for section_name in section_names:
        time_lst = sections[section_name]
        cpy_time_table = time_table.copy()
        for i in range(5): # for each day
            time = time_lst[i]
            if time is not None:
                start_time = time[:4]
                duration = time[4:]
                if not check_time_slot(time_table, i, start_time, duration):
                    break
                for j in range(int(int(duration)/10)):
                    cpy_time_table[i*24*6 + int(start_time[:2])*6 + int(int(start_time[2:4])/10) + j] = True
        else:
            lst_cpy = lst.copy()
            lst_cpy.append(class_names[idx]+"_"+section_name)
            if idx == len(class_names) - 1:
                res.append(lst_cpy)
                break
            generate_schedule_aux(class_lst, cpy_time_table, idx+1, lst_cpy, res)
                    

def generate_schedule(lst):
    class_lst = tmp_time_data
    res = []
    time_table = [False] * 5 * 24 * 6
    generate_schedule_aux(class_lst, time_table, 0, [], res)
    print(res)

if __name__ == "__main__":
    generate_schedule(["CMSC330", "CMSC351", "ENGL101"])