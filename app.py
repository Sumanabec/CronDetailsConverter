import datetime as dt
import argparse
import sys

Day_dict = {
    "SUN": "Sunday", "MON": "Monday", "TUE": "Tuesday", "WED": "Wednesday",
    "THU": "Thursday", "FRI": "Friday", "SAT": "Saturday"
}

def get_days(day_of_week):
    days = []
    for day in day_of_week.split(","):
        try:
        # print(Day_dict[day])
            days.append(Day_dict[day])
        except KeyError:
            print(f"[ERROR] invalid day abbreviation: {day}")
    return ",".join(days)


def get_mawm_job_details(input_filepath):
    try:
        with open(input_filepath,'r') as file:
            job_details = [line.strip() for line in file]
        return job_details
    except FileNotFoundError:
        print(f"File not Found: {input_filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"[Error] failed to read file: {e}")
        sys.exit(1)


def create_job_details_file(output_file_path, data):
    try:
        with open(output_file_path,'a') as file:
            file.writelines((dt.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")+ "\n")
            for line in data:
                file.writelines(line+ '\n')
            file.writelines("######################## \n\n\n")
    except Exception as e:
        print(f"Failed to write to the file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='parse input')
    parser.add_argument("input_file")
    parser.add_argument("output_file")

    try:
        args = parser.parse_args()
        input = args.input_file
        output = args.output_file
    except Exception as e:
        print(f"Arguement parsing failed: {e}")
        sys.exit(1)

    #job_details = ["0 0 6 * * ?", "0 0 05 * * ?", "0 15 2 ? * SUN *", "0 15 2 ? * SUN,TUE *"]
    job_details = get_mawm_job_details(input)

    converted_job_details = []
    for job_schedule in job_details:
        job_exp = job_schedule.split()

        if len(job_exp) < 6:
            converted_job_details.append(f"Incomplete cron Expression: {job_schedule}")
        else:
            min = job_exp[1]
            hour = job_exp[2]
            day_of_week = job_exp[5]

            hour_string = ''
            if hour == '*':
                hour_string = 'every hour'

            if min == '*':
                formatted_time = 'every minute '
            else:
                try:
                    # Parse the 24-hour format time
                    time_obj = dt.datetime.strptime(f"{hour}:{min}", "%H:%M")
                    # Format to 12-hour with AM/PM
                    formatted_time = time_obj.strftime("%I:%M %p")
                except ValueError:
                    formatted_time = f"{hour}:{min}"
                    print("Please provide correct time to get in AM/PM format")

            day_of_week_string = 'every day' if (day_of_week == '?' or day_of_week == '*') else 'every ' + get_days(
                day_of_week)
            converted_job_details.append(f"The job runs {day_of_week_string} at {hour_string} {formatted_time}")
    create_job_details_file(output, converted_job_details)

if __name__ == '__main__':
    main()