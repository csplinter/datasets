import csv
import argparse
import shutil
from tempfile import NamedTemporaryFile


def convert_comma_separated_string_to_json_array(string):

    if string != '':
        string_list = string.replace(', ', ',').replace('"', '').replace('\'', '').split(',')
        return string_list
    else:
        return string


def remove_commas_clean_whitespace(string):
    return string.replace(',', '').strip()


def not_rated_if_not_exists(string):
    if string == '':
        return 'NR'
    return string


def date_added_if_not_exists(date_added, release_year):
    if date_added == '':
        return 'January 1, ' + release_year
    return date_added


def format_netflixdata():
    tempfile = NamedTemporaryFile(mode='w', delete=False, newline='\n')
    fields = ['show_id', 'type', 'title', 'director', 'cast', 'country', 'date_added',
              'release_year', 'rating', 'duration', 'listed_in', 'description']

    with open('netflix/netflixdata-original.csv', mode='r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if reader.line_num != 1:
                row['director'] = convert_comma_separated_string_to_json_array(row.get('director'))
                row['cast'] = convert_comma_separated_string_to_json_array(row.get('cast'))
                row['country'] = convert_comma_separated_string_to_json_array(row.get('country'))
                row['listed_in'] = convert_comma_separated_string_to_json_array(row.get('listed_in'))
                row['description'] = remove_commas_clean_whitespace(row.get('description'))
                row['date_added'] = date_added_if_not_exists(row.get('date_added').lstrip(), row.get('release_year'))
                row['rating'] = not_rated_if_not_exists(row.get('rating'))
                writer.writerow(row)
            else:
                writer.writerow(row)

        shutil.move(tempfile.name, "netflix/netflixdata-clean.csv")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', default='dataset', action='store')

    args = parser.parse_args()

    if args.dataset == 'netflix':
        format_netflixdata()


if __name__ == "__main__":
    main()
