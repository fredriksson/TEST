import random
import urllib
import bisect
import uuid
import package_gen_duration
import time
import datetime
# url = "http://yax.ymcnetwork.com/track"

url = "http://10.1.1.33:3000/import"


def project_profile(date_start, duration, http_post_enable):
    for x in range(1, duration):
        #################### treate date increase daliy and transfer into ctime format #################

        ISOFMT = '%Y-%m-%d %H:%M:%S'
        date_start_1 = datetime.datetime(*time.strptime(time.strftime(date_start), ISOFMT)[:6])
        print date_start_1
        #print "x" ,x

        current_date_orignal = str(date_start_1 + datetime.timedelta(x))

        current_date = time.strptime(current_date_orignal, "%Y-%m-%d %H:%M:%S")
        #print current_date

        event_gen(current_date, x, http_post_enable)

        print "--------- one day end --------------"


def event_gen(current_date, x, http_post_enable):
    datetime_input = int(time.mktime(current_date))  # ####### transfer current_date into ctime	#########

    amount_birth = int(10 * (x ** 0.5) + random.randint(-3, x))

    daily_user_list = []  # create a list for reuse distinct_id, clear this daily




    ####################### daily event as follow #####################

    for daily_birth in range(amount_birth):

        def random_time(datetime_input):

            date_with_random = datetime.datetime.utcfromtimestamp(datetime_input) + datetime.timedelta(
                hours=random.randint(0, 14))

            date_with_random_1 = time.strptime(str(date_with_random), "%Y-%m-%d %H:%M:%S")

            date_random_ctime = int(time.mktime(date_with_random_1))

            return date_random_ctime


        ####################### Country code generate in term of weight in list #########################

        breakpoints = []
        country_list = {'AL': 0.1, 'AU': 0.1, 'AT': 0.1, 'BE': 0.1, 'BR': 0.2, 'CA': 0.4, 'CL': 0.1, 'CN': 0.3,
                        'CO': 0.1, 'EG': 0.1, 'FR': 0.1, 'DE': 0.1, 'GR': 0.1, 'HK': 0.1, 'IN': 0.2, 'ID': 0.1,
                        'IL': 0.1, 'IT': 0.1, 'JP': 0.2, 'KP': 0.1, 'MX': 0.1, 'ES': 0.1, 'SG': 0.1, 'TR': 0.1,
                        'GB': 0.1, 'US': 0.3}

        items = country_list.keys()

        mysum = 0

        for ii in items:
            mysum += country_list[ii]
            breakpoints.append(mysum)

        def getitem(breakpoints, items):
            score = random.random() * breakpoints[-1]
            ii = bisect.bisect(breakpoints, score)
            return items[ii]

        country_code = getitem(breakpoints, items)

        ##################  Country code generate end ##############################



        ################# Generate distinct_id ###################################
        distinct_id = str(country_code + "-" + str(uuid.uuid1()))

        daily_user_list.append(distinct_id)  # append all distince_id (in one day) into list



        ########################## YA0birth/start  as follow ###################

        YA0birth = package_gen_duration.package_generator("YA0birth", "2.0.2", "8416e32af87f11e284c212313b0ace15",
                                                          random_time(datetime_input), distinct_id)

        http_post(YA0birth, YA0birth)

        YA0start = package_gen_duration.package_generator("YA0start", "2.0.2", "8416e32af87f11e284c212313b0ace15",
                                                          random_time(datetime_input),
                                                          distinct_id)  # After YA0birth, matched one YA0start
        ##rex_YA0start = urllib.urlopen(url,YA0start)

        http_post(YA0start, YA0start)


        #########################  YA0session ############################

        #print "send YA0session"

        YA0session = package_gen_duration.package_generator("YA0session", "2.0.2", "8416e32af87f11e284c212313b0ace15",
                                                            random_time(datetime_input), distinct_id)

        http_post(YA0session, YA0session)

        #rex_YA0session = urllib.urlopen(url,YA0session)

        #print datetime_input


        ######################### Retention as follow #####################
        if len(
                daily_user_list) == amount_birth:  # when all distinct_id are pushed into list, do as follow(retention start)

            print "--------start retetion----------"

            fate_percentage = [0.55, 0.49, 0.43, 0.37, 0.31, 0.25, 0.22, 0.21,
                               0.19, 0.18, 0.17, 0.16, 0.158, 0.154, 0.149, 0.146, 0.142, 0.139, 0.136, 0.133, 0.13,
                               0.127, 0.125, 0.123, 0.12, 0.118, 0.116, 0.115, 0.113, 0.111, 0.109, 0.108, 0.106, 0.105,
                               0.104, 0.102, 0.101, 0.1, 0.099, 0.098, 0.097, 0.096, 0.095, 0.0938, 0.093, 0.092, 0.091,
                               0.09, 0.089, 0.088, 0.087, 0.086, 0.085, 0.084, 0.083, 0.082, 0.081, 0.8,
                               0.079,0.078]  ######## array of retention rate ########

            for fade_rate in range(1, len(fate_percentage)):
                ######## go through the whole daily dirstinct_id and select randomly for 8 days
                ######## add offset days to current datetime_offset_1 ############

                dateArray = datetime.datetime.utcfromtimestamp(datetime_input)  # transfer to common date format

                datetime_offset = dateArray + datetime.timedelta(fade_rate)  # Add date increasement (1-9)

                #####print datetime_offset



                datetime_offset_format = time.strptime(str(datetime_offset),
                                                       "%Y-%m-%d %H:%M:%S")  # Transfer to date time format

                datetime_offset_1 = int(
                    time.mktime(datetime_offset_format))  # Transfer to ctime format, put int function

                ######print datetime_offset_1

                real_percentage = fate_percentage[fade_rate] + random.uniform(-0.003, 0.005)
                print "++++",real_percentage

                ####print "datetime_offset",datetime_offset

                sample_amount = int(
                    len(daily_user_list) * real_percentage)  # define how many retention users in advance(percentage)

                print "================== retention of the day:", fade_rate, "=================="

                for daily_retention in range(sample_amount):
                    ####print "###",daily_retention


                    YA0start_retention = package_gen_duration.package_generator("YA0start", "2.0.2",
                                                                                "8416e32af87f11e284c212313b0ace15",
                                                                                random_time(datetime_offset_1),
                                                                                daily_user_list[daily_retention])

                    http_post(YA0start_retention, http_post_enable)

                    #rex_YA0start_retention = urllib.urlopen(url,YA0start_retention)

                    YA0charge = package_gen_duration.package_generator("YA0charge", "2.0.2",
                                                                       "8416e32af87f11e284c212313b0ace15",
                                                                       random_time(datetime_offset_1),
                                                                       daily_user_list[daily_retention])

                    http_post(YA0charge, http_post_enable)
                    #rex_YA0start_retention = urllib.urlopen(url,YA0charge)


##################################	Retention Event end ######################################

def http_post(event, http_post_enable):
    if http_post_enable == 1:


        http_post_event = urllib.urlopen(url, event)


    elif http_post_enable == 0:

        pass


if __name__ == '__main__':
    #event_generator("YA0birth")
    #event_generator("YA0start")
    #event_generator("YA0session")
    #event_generator("YA0charge")
    #user_retention()
    date_start = "2014-6-24 00:00:00"
    duration = 66

    project_profile(date_start, duration, http_post_enable=0)




