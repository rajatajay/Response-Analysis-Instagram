import json
import csv
from datetime import date
import pandas as pd
import datetime
import time
import seaborn as sns
import matplotlib.pyplot as plt
import statistics

prev_last = 0
dys_wc = []

def json2csv():

    with open(r"C:\Users\Rajat\Desktop\Runny\Python\Regular\message_2.json") as file:
        data = json.load(file)

    fname = "message_2_csv.csv"

    with open(fname, "w", encoding='utf-8') as file:
        csv_file = csv.writer(file,lineterminator='\n')
        csv_file.writerow(["Name","TimeStamp","Message"])
        for item in data["messages"]:
            try:
                csv_file.writerow([item['sender_name'],item['timestamp_ms'],item['content']])
            except KeyError:
                csv_file.writerow([item['sender_name'],item['timestamp_ms'],"*photo/video sent*"])

def ts_day(midn_t):
    dt_object = date.fromtimestamp(midn_t)
    d2ts = dt_object.strftime("%m/%d/%y")
    return(d2ts)

def word_co(dr):
    word_count = []
    for x in range(0,len(dr)):
        sen = dr.iloc[x][2]
        word_count.append(len(sen.split()))
    return (word_count)

def t2d00(time_s):
    dt_object = date.fromtimestamp(time_s)
    d2ts = dt_object.strftime("%m/%d/%y")

    return (d2ts)

def init_t(time_s):
    
    dt_object = date.fromtimestamp(time_s)
    #print(dt_object)
    d2ts = dt_object.strftime("%m/%d/%y")
    #print(d2ts)
    ts = time.mktime(datetime.datetime.strptime(d2ts,"%m/%d/%y").timetuple())
    #print("1 ", ts)
    return (ts)

def ret_date(time):
    dt_object = date.fromtimestamp(time)
    return(dt_object)

def swap(dr):
    titles = ["Name","TimeStamp","Word Count", "Message"]
    dr = dr.reindex(columns = titles)
    return (dr)

def create_dict():
    dr = pd.read_csv(r"C:\Users\Rajat\Desktop\Runny\Python\message_1_csv.csv")
    dr = dr.iloc[::-1]
    
    dr["Word Count"] = word_co(dr)
    dr = swap(dr)

    dnt = {}

    init_time = dr.iloc[0][1]/1000
    fin_time = dr.iloc[-1][1]/1000
    i_ts = ret_date(init_time)
    f_tf = ret_date(fin_time)

    check = dr.iloc[0][1]/1000
    ts = init_t(check)*1000
    dif = f_tf - i_ts
    dayshift = 86400000 # a single day in milliseconds


    start = 0
    end = 0
    # ts = 1595534400000
    for x in range(0,len(dr)): #everyday after the last day
        if ((dr.iloc[x][1]) >= (ts + dayshift)):

            day = ts_day(ts/1000)
            end = x
            dnt[day] = dr.iloc[start:end,0:3]
            start = end
            ts = ts + dayshift
    
    i = 0
    
    for i in range(0,len(dr)): #collecting the final day as
        if (dr.iloc[i][1] >= ts):
            break
    
    day = ts_day(ts/1000)
    dnt[day] = dr.iloc[i:(len(dr)+1),0:3]

    return dnt

def analysis(prepdata, response_time, word_count, user_1, user_2):
    n_df = prepdata[["Date", response_time]].set_index("Date")

    for x in range (0, len(n_df)):
        milli_2_min = 60000

        temp_list = n_df.iloc[x][0]
        try:
            newlist = [i / milli_2_min for i in temp_list]
            if (statistics.mean(newlist) >= 400): #can be changed to adjust the plotted image so that outliers dont mess things up
                newlist = "remove"
                # pass
        except TypeError:
            newlist = [0]
        
        n_df.iloc[x][0] = newlist

        
    n_df = n_df[n_df[response_time] != "remove"]
    final_df = n_df
    # final_df

    # final_2 = final_df[response_time].apply(lambda x: pd.Series(x)).T.boxplot(figsize=(40,20),rot=45, fontsize = 20)
    dims = (120, 10)

    fig, ax = plt.subplots(figsize=dims)


    final_2 = final_df[response_time].apply(lambda x: pd.Series(x))
    final_2 = final_2.transpose()


    ax = sns.boxplot(data = final_2, width = 0.5, showfliers=False)
    title = user_2 + ' Response Analysis'
    ax.set_title(title, fontsize=40)
    ax.tick_params(axis='x', rotation= 90)
    # ax.set(xlabel='Date', ylabel='Response Time ')
    # ax.axes.set_title("Title",fontsize=50)
    ax.set_xlabel("Date",fontsize= 25)
    ax.set_ylabel("Response Time",fontsize= 25)
    ax.grid(b=True, which='major', color='black', linewidth=0.075)
    ax.grid(b=True, which='minor', color='black', linewidth=0.075)

    plt.savefig(user_2 + '.png', dpi=300)

def calc(x, a, df, calc_w_list, calc_dif_list):
    sum = 0
    calc_list = [0,0]

    dif = df.iloc[x][1] - df.iloc[a][1]
    for i in range(a, x):
        sum += df.iloc[i][2]
    calc_dif_list.append(dif)
    calc_w_list.append(sum)
    
    calc_list[0] = calc_dif_list
    calc_list[1] = calc_w_list
    
    return calc_list

def alt_calc(x, a, df, calc_w_list):
    w_sum = 0
    for i in range(a,(x+1)):
        w_sum += df.iloc[i][2]
    
    calc_w_list.append(w_sum)
    
    # print("alt_calc return is ", calc_w_list)
    
    return calc_w_list
    
def recr(start, end, df, calc_list, calc_w_list, calc_dif_list, user_1, user_2):

    for a in range(start,end): #177 is 9501

        if (df.iloc[a][0] == user_2):

            for x in range(a,end):

                if (df.iloc[x][0] == user_1):

                    calc_list = calc(x, a, df, calc_w_list, calc_dif_list)
                    start = x
                    if x != (end-1):
                        recr(start, end, df, calc_list, calc_w_list, calc_dif_list, user_1, user_2)
                    break
                    
                elif (x == (end-1)):
                    global prev_last
                    global dys_wc
                    
                    calc_w_list = alt_calc(x, a, df, calc_w_list)
                    
                    calc_list[1] = calc_w_list
                    dys_wc = calc_w_list
                    prev_last = df.iloc[a][1]
                    
                    break
            break
    
    return calc_list

def data_create(dnt, response_time, word_count, user_1, user_2):

    f_df = pd.DataFrame(columns = ['Date',response_time, word_count])

    count = 1
    for x in dnt:
        
        calc_w_list = []
        calc_dif_list = []
        calc_list = [0,0]

        df = dnt[x]
        end = len(dnt[x])

        start = 0
        check = df.drop_duplicates(subset = ["Name"])

        if (len(check) == 1 and check.iloc[0][0] == user_1):

            global prev_last
            global dys_wc
            temp_list = []
            temp_list.append(int(df.iloc[0][1]) - int(prev_last))

            f_df.loc[count, 'Date'] = x
            f_df.loc[count, response_time] = temp_list
            f_df.loc[count, word_count] = dys_wc

        elif (len(check) >= 1):

            final_list = recr(start, end, dnt[x], calc_list, calc_w_list, calc_dif_list, user_1, user_2)
            f_df.loc[count, 'Date'] = x
            f_df.loc[count, response_time] = final_list[0]
            f_df.loc[count, word_count] = final_list[1]

        count = count + 1
    
    return f_df

def main():
    
    dnt = create_dict()
    
    for x in dnt:
        name_check = dnt[x].drop_duplicates(subset = ["Name"])
        if (len(name_check) == 2):
            break

    user_1 = name_check.iloc[0][0] 
    user_2 = name_check.iloc[1][0] 

    response_time = user_2 + "_Response_Time"
    word_count = user_1 + "_Response_Total_Word_Count"

    prep_data = data_create(dnt, response_time, word_count, user_1, user_2)

    analysis(prep_data, response_time, word_count, user_1, user_2)

main()
