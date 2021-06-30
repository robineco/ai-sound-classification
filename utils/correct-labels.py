import os
import csv
from shutil import copyfile

data_file = ''

with open(data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Columns are: {row}')
            line_count += 1
        else:
            file_name = row[2]
            name = os.path.splitext(os.path.basename(file_name))[0]
            label = row[4]
            corrected_label = row[5]

            if corrected_label == '0':
                if label == 'city':
                    print('[NORMAL] city: ', file_name)
                    copyfile(
                        file_name,
                        'snippets/output/city/' + name + '_city.wav'
                    )
                elif label == 'multiple-cars':
                    print('[NORMAL] multiple: ', file_name)
                    copyfile(
                        file_name,
                        'snippets/output/multiple-cars/' + name + '_multiple-cars.wav'
                    )
                elif label == 'single-cars':
                    print('[NORMAL] single-car: ', file_name)
                    copyfile(
                        file_name,
                        'snippets/output/single-car/' + name + '_single-car.wav'
                    )
                else:
                    print(file_name)
            elif corrected_label == 'city':
                print('[CORRECTED] city: ', file_name)
                copyfile(
                    file_name,
                    'snippets/output/city/' + name + '_city.wav'
                )
            elif corrected_label == 'multiple-cars':
                print('[CORRECTED] multiple-cars: ', file_name)
                copyfile(
                    file_name,
                    'snippets/output/multiple-cars/' + name + '_multiple-cars.wav'
                )
            elif corrected_label == 'single-cars':
                print('[CORRECTED] single-car: ', file_name)
                copyfile(
                    file_name,
                    'snippets/output/single-car/' + name + '_single-car.wav'
                )

            line_count += 1
