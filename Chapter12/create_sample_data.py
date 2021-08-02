"""Script to populate lab checks and plot checks into abq database"""
import sys
from getpass import getpass
import random
import psycopg2 as pg

host = input('Database host (localhost): ') or 'localhost'
database = input('Database name (abq): ') or 'abq'
user = input('Database user: ')
password = getpass('Database password: ')

try:
    cx = pg.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
except pg.OperationalError as e:
    print('Connection failed')
    print(e)
    sys.exit()


lab_check_insert = """
INSERT INTO lab_checks (date, time, lab_id, lab_tech_id)
VALUES (CURRENT_DATE, %(time)s, %(lab_id)s, (SELECT id from lab_techs ORDER BY RANDOM() limit 1))
"""

plot_check_insert = """
INSERT INTO plot_checks (
  date, time, lab_id, plot, seed_sample, humidity, light, temperature,
  equipment_fault, blossoms, plants, fruit, max_height, min_height, median_height,
  notes
)
VALUES (
  CURRENT_DATE, %(time)s, %(lab_id)s, %(plot)s,
  (SELECT current_seed_sample FROM plots WHERE plot=%(plot)s and lab_id = %(lab_id)s),
  %(humidity)s, %(light)s, %(temperature)s,
  %(equipment_fault)s, %(blossoms)s, %(plants)s, %(fruit)s,
  %(max_height)s, %(min_height)s, %(median_height)s, %(notes)s
)
"""

cursor = cx.cursor()

for lab in ('A', 'B', 'C'):
    plants = random.randint(0, 10)
    blossoms = int(random.random() * 5 * plants)
    fruit = int(random.random() * 5 * plants)
    min_height = random.random() * 20
    max_height = random.random() * 10 + min_height
    for time in ('8:00', '12:00', '16:00', '20:00'):
        lc_data = {
            'time': time,
            'lab_id': lab,
        }
        plants = min(20, plants + random.choice([0, 0, 0, 0, 0, 0, 1]))
        blossoms += random.choice([0, 0, 0, 0, 0, 0, 1])
        fruit += random.choice([0, 0, 0, 0, 0, 0, 1])
        min_height += random.random() * .5
        max_height += random.random() * .5
        med_height = min_height + (random.random() * (max_height - min_height))
        cursor.execute(lab_check_insert, lc_data)
        for plot in range(1, 21):
            e_fault = random.randint(1, 10) > 9 #  10% chance of failure
            humidity = (random.random() * 4 + 21) if not e_fault else None
            light = (random.random() * .1 + .95) if not e_fault else None
            temperature = ((light ** 3) * 8 + 21) if light and not e_fault else None

            notes = random.choice([
                'Check Hydration system', 'Dry leaves', 'Roots exposed',
                'Check delayed', 'Skylight obscured'
            ]) if random.randint(1, 10) > 9 else ''
            pc_data = {
                'time': time,
                'lab_id': lab,
                'plot': plot,
                'equipment_fault': e_fault,
                'light': light,
                'humidity': humidity,
                'temperature': temperature,
                'plants': plants,
                'blossoms': blossoms,
                'fruit': fruit,
                'max_height': max_height,
                'min_height': min_height,
                'median_height': med_height,
                'notes': notes
              }
            cursor.execute(plot_check_insert, pc_data)
cx.commit()
