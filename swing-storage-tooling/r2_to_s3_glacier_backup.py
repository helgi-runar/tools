# A simple backup script to backup swing backend videos from R2 to AWS S3 Glacier Deep Archive
# Note: You need valid rclone credentials in config
#
import os
from dotenv import load_dotenv
import psycopg2
import logging
import sys
import time

from rclone_python import rclone


load_dotenv()
r2_rclone_remote = "elva-r2"
glacier_rclone_remote = "glacier-backup"
# Ideally this would be queried from s3, but there is no quick way of doing that so we keep it around manually.
last_uploaded_swing_file = ".last_uploaded_swing"


def get_swing_count():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_DATABASE", "postgres"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT", 5432)),
        sslmode=os.getenv("PGSSLMODE", "require"),
    )
    with conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM swings;")
        return cur.fetchone()[0]


def get_logger(name='r2_to_glacier', log_file='r2_to_glacier.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger


def r2_to_s3_glacier_backup(last_uploaded_swing: int, swing_count: int):
    logger = get_logger()
    max_swing_id = get_swing_count()
    if max_swing_id <= last_uploaded_swing:
        logger.info("No swings need backup.")
        return

    cur_swing_count = 0
    logger.info(f"Currently there are a total of {max_swing_id} swings in R2")
    logger.info(f"{last_uploaded_swing}/{max_swing_id} swings are already backed up.")
    logger.info(f"Starting backup of (up to): {swing_count} swings")
    try:
        for swing_number in range(last_uploaded_swing + 1, max_swing_id):
            logger.info(f"Working on swing: {swing_number}")
            rclone.copy(f"{r2_rclone_remote}:elva-swings/{swing_number}/recordings",
                        f"{glacier_rclone_remote}:swings-backup/{swing_number}/recordings/",
                        ignore_existing=True,
                        args=["--s3-storage-class", "DEEP_ARCHIVE"])
            update_last_uploaded_swing(swing_number)
            cur_swing_count += 1
            if swing_count > 0 and cur_swing_count >= swing_count:
                logger.info("Reached the swing count buffer, exiting.")
                break
    except KeyboardInterrupt:
        logger.info(f"Forcefully stopped at swing: {swing_number}")


def update_last_uploaded_swing(swing_id: int):
    with open(last_uploaded_swing_file, 'w') as fp:
        fp.write(f"{swing_id}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You must supply the number of swings to backup:", file=sys.stderr)
        print(f"Usage:\n    python3 {__file__} NUMBER_OF_SWINGS\n", file=sys.stderr)
        exit(1)
    logger = get_logger()
    start_of_execution = time.time()
    last_uploaded_swing = -1
    with open(last_uploaded_swing_file, 'r') as fp:
        last_uploaded_swing = int(fp.read().strip())
    r2_to_s3_glacier_backup(last_uploaded_swing, int(sys.argv[1]))
    logger.info(f"Execution took: ~{time.time() - start_of_execution:.2f}")
