import datetime as dt
import argparse

Day_dict = {
    "SUN": "Sunday", "MON": "Monday", "TUE": "Tuesday", "WED": "Wednesday",
    "THU": "Thursday", "FRI": "Friday", "SAT": "Saturday"
}

def get_days(day_of_week):
    days = []
    for day in day_of_week.split(","):
        # print(Day_dict[day])
        days.append(Day_dict[day])
    return ",".join(days)


def get_mawm_job_details(input_filepath):
    with open(input_filepath,'r') as file:
        job_details = [line.strip() for line in file]
    return job_details


def create_job_details_file(output_file_path, data):
    with open(output_file_path,'w') as file:
        for line in data:
            file.writelines(line+ '\n')


def main():
    parser = argparse.ArgumentParser(description='parse input')
    parser.add_argument("input_file")
    parser.add_argument("output_file")

    args = parser.parse_args()
    input = args.input_file
    output = args.output_file

    #job_details = ["0 0 6 * * ?", "0 0 05 * * ?", "0 15 2 ? * SUN *", "0 15 2 ? * SUN,TUE *"]
    job_details = get_mawm_job_details(input)

    converted_job_details = []
    for job_schedule in job_details:
        #print(job_schedule)
        job = job_schedule.split()
        min = job[1]
        hour = job[2]
        day_of_week = job[5]

        hour_string = ''
        #
        if hour == '*':
            hour_string = 'every hour'
        if min == '*':
            formatted_time = 'every minute '
        else:
            # Parse the 24-hour format time
            time_obj = dt.datetime.strptime(f"{hour}:{min}", "%H:%M")
            # Format to 12-hour with AM/PM
            formatted_time = time_obj.strftime("%I:%M %p")

        day_of_week_string = 'every day' if (day_of_week == '?' or day_of_week == '*') else 'every ' + get_days(day_of_week)
        converted_job_details.append(f"The job runs {day_of_week_string} at {hour_string} {formatted_time}")

        create_job_details_file(output, converted_job_details)

if __name__ == '__main__':
    main()