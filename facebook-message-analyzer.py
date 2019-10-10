import os
import json
import numpy as np
import pylab as pl
import datetime

CURRENT_DIRECTORY = os.getcwd()
NUMBER_TO_ANALYZE = 5000
MESSAGE_THRESHOLD = 1
MESSAGE_BOUND = 1000

def get_json_data(chat):
    try:
        json_location = CURRENT_DIRECTORY + "/messages/" + chat + "/message_1.json"
        with open(json_location) as json_file:
            json_data = json.load(json_file)
            return json_data
    except IOError:
        pass # some things the directory aren't messages (DS_Store, stickers_used, etc.)
    
chats = os.listdir(CURRENT_DIRECTORY + "/messages/")[:NUMBER_TO_ANALYZE]
sorted_chats = []
final_data_messages = {}
final_data_times = {}
final_data_words = {}
final_data_laugh = {}
final_data_profanity = {}
final_data_dayofweek = {}
invalid_message_count = 0

print('Analyzing ' + str(min(NUMBER_TO_ANALYZE, len(chats))) + ' chats...')

for chat in chats:
    url = chat + '/message_1.json'
    json_data = get_json_data(chat)
    print(chat)
    if json_data != None:
        messages = json_data["messages"]
        if len(messages) >= MESSAGE_THRESHOLD and len(messages) <= MESSAGE_BOUND:
            sorted_chats.append((len(messages), chat, messages))

sorted_chats.sort(reverse=True)

print('Finished processing chats...')

for i, (messages, chat, messages) in enumerate(sorted_chats):
    number_messages = {}
    person_to_times = {}
    number_words = {}
    laugh_meter = {}
    profanity_meter = {}
    number_each_day = {"Mon":0,"Tues":0,"Wed":0,"Thurs":0,"Fri":0,"Sat":0,"Sun":0}

    print(str(i) + " - " + str(len(messages)) + " messages - " + str(chat))

    for message in messages:
        try:
            name = message["sender_name"]
            time = message["timestamp_ms"]
            message_content = message["content"].lower()
            day = datetime.datetime.fromtimestamp(time/1000.0).weekday()
            
            if day == 0:
                day = "Mon"
            if day == 1:
                day = "Tues"
            if day == 2:
                day = "Wed"
            if day == 3:
                day = "Thurs"
            if day == 4:
                day = "Fri"
            if day == 5:
                day = "Sat"
            if day == 6:
                day = "Sun"
            
            number_messages[name] = number_messages.get(name, 0)
            number_messages[name] += 1

            person_to_times[name] = person_to_times.get(name, [])
            person_to_times[name].append(datetime.datetime.fromtimestamp(time/1000.0))

            number_words[name] = number_words.get(name, [])
            number_words[name].append(len(message_content.split()))
            
            laugh_meter[name] = laugh_meter.get(name, 0)
            laugh_meter[name] += message_content.count("lol")
            laugh_meter[name] += message_content.count("lmao")
            laugh_meter[name] += message_content.count("lmfao")
            laugh_meter[name] += message_content.count("lel")
            laugh_meter[name] += message_content.count("lul")
            
            profanity_meter[name] = profanity_meter.get(name, 0)
            profanity_meter[name] += message_content.count("fuck") # sorry you had to see these curse words
            profanity_meter[name] += message_content.count("shit") # i don't condone the use of these
            profanity_meter[name] += message_content.count("bitch")
            profanity_meter[name] += message_content.count("ass")
            profanity_meter[name] += message_content.count("damn")
            
            number_each_day[day] = number_each_day.get(day, 0)
            number_each_day[day] += 1
                             
        except KeyError:
            # happens for special cases like users who deactivated, unfriended, blocked
            invalid_message_count += 1

    final_data_messages[i] = number_messages
    final_data_times[i] = person_to_times
    final_data_words[i] = number_words
    final_data_laugh[i] = laugh_meter
    final_data_profanity[i] = profanity_meter
    final_data_dayofweek[i] = number_each_day
    

print('Found ' + str(invalid_message_count) + ' invalid messages...')
print('Found ' + str(len(sorted_chats)) + ' chats with ' + str(MESSAGE_THRESHOLD) + ' messages or more')

def plot_num_messages(chat_number):
    plotted_data = final_data_messages[chat_number]
    X = np.arange(len(plotted_data))
    pl.bar(X, list(plotted_data.values()), align='center', width=0.5, color = 'r', bottom = 0.3)
    pl.xticks(X, plotted_data.keys(), rotation = 90)
    pl.title('Number of Messages Sent')
    pl.xlabel('Person')
    pl.tight_layout()
    pl.show()
    
def plot_histogram_time(chat_number):
    person_to_times = final_data_times[chat_number]
    pl.xlabel('Time')
    pl.ylabel('Number of Messages')
    pl.title('# of Messages Over Time')
    colors = ['b', 'r', 'c', 'm', 'y', 'k', 'w', 'g']
    for i , person in enumerate(person_to_times):
        plotted_data = person_to_times[person]
        pl.hist(plotted_data, 100, alpha=0.3, label=person, facecolor=colors[i % len(colors)])
    pl.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    pl.xticks(rotation=90)
    pl.tight_layout()
    pl.show()

def plot_histogram_words(chat_number):
    temp = {}
    for person in final_data_words[chat_number]:
        temp[person] = np.average(final_data_words[chat_number][person])
    plotted_data = temp
    X = np.arange(len(plotted_data))
    pl.bar(X, list(plotted_data.values()), align='center', width=0.5, color = 'r', bottom = 0.3)
    pl.xticks(X, plotted_data.keys(), rotation = 90)
    pl.xlabel('Person')
    pl.title('Average Word Count')
    pl.tight_layout()
    pl.show()

def plot_histogram_laughter(chat_number):
    plotted_data = final_data_laugh[chat_number]
    X = np.arange(len(plotted_data))
    pl.bar(X, list(plotted_data.values()), align='center', width=0.5, color = 'r', bottom = 0.3)
    pl.xticks(X, plotted_data.keys(), rotation = 90)
    pl.title('Laughter Meter')
    pl.xlabel('Person')
    pl.ylabel('Number of Laughing Acronyms')
    pl.tight_layout()
    pl.show()
    
def plot_histogram_profanity(chat_number):
    plotted_data = final_data_profanity[chat_number]
    X = np.arange(len(plotted_data))
    pl.bar(X, list(plotted_data.values()), align='center', width=0.5, color = 'r', bottom = 0.3)
    pl.xticks(X, plotted_data.keys(), rotation = 90)
    pl.title('Profanity Meter')
    pl.xlabel('Person')
    pl.ylabel('Number of Bad Words')
    pl.tight_layout()
    pl.show()
    
def plot_histogram_dayofweek(chat_number):
    plotted_data = final_data_dayofweek[chat_number]
    X = np.arange(len(plotted_data))
    pl.bar(X, list(plotted_data.values()), align='center', width=0.5, color = 'r', bottom = 0.3)
    pl.xticks(X, plotted_data.keys(), rotation = 90)
    pl.title('Messages on Day of Week')
    pl.ylabel('Number of Messages')
    pl.xlabel('Day of Week')
    pl.tight_layout()
    pl.show()

def plot(chat_number):
    plot_num_messages(chat_number)
    plot_histogram_time(chat_number)
    plot_histogram_words(chat_number)
    plot_histogram_laughter(chat_number)
    plot_histogram_profanity(chat_number)
    plot_histogram_dayofweek(chat_number)

# CHANGE THIS NUMBER TO ANALYZE DIFFERENT CHATS
plot(0)