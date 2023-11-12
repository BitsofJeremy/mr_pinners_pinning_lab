# manage.py

# Options:
# create the db:  python manage.py --create_db

import argparse
import sys

# Local Imports
from pinning_lab import app, db

# Logging
import logging
logger = logging.getLogger(__name__)


def main(**kwargs):
    if kwargs['create_db']:
        print("Creating Database, one moment")
        with app.app_context():
            # Init the DB
            db.create_all()

    print("FIN")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--create_db',
        help='Create the DB',
        action="store_true",
        required=False
    )

    args = parser.parse_args()

    # Convert the argparse.Namespace to a dictionary: vars(args)
    arg_dict = vars(args)
    # pass dictionary to main
    main(**arg_dict)
    sys.exit(0)
