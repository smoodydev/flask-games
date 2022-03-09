import csv

@app.route("/tryread")
def insert():
    last = ""
    with open('All_Pokemon.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                print(f'\t{row[0]} {row[1]} {row[2]} {row[3]} {row[14]} {row[41]} {row[42]} ')
                line_count += 1
            else:
                db.session.add(Pokemon(number=int(float(row[0])), name=row[1],    type_one=row[2],  type_two=row[3],  generation=int(float((row[14]))), height=row[41],  weight=row[42] ))
                db.session.commit()
                print(f'\t{row[0]} {row[1]} {row[2]} {row[3]} {row[14]} {row[41]} {row[42]} ')
                line_count += 1
        print(f'Processed {line_count} lines.')
    return "tried"

