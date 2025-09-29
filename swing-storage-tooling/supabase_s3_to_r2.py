import logging
import time
from rclone_python import rclone


swing_listings_file = "swing_listing.txt"
completed_swings_file = "migrated_swings.txt"
swing_number = -1


def get_logger(name='s3_to_r2', log_file='s3_to_r2.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger


def supabase_s3_to_r2(swing_listing, swing_count):
    global swing_number
    logger = get_logger()
    cur_swing_count = 0
    with open(completed_swings_file) as cmp_fp:
        completed_swings = set(s_nr.strip() for s_nr in cmp_fp.readlines())
    total_number_of_swings = sum(1 for _ in open(swing_listing))
    logger.info(f"Currently there are {total_number_of_swings} listed for migration")
    logger.info(f"{len(completed_swings)}/{total_number_of_swings} swings already migrated")
    logger.info(f"Starting migration of: {swing_count} swings")
    with open(swing_listing) as ucmp_fp, open(completed_swings_file, 'a') as cmp_fp:
        for swing_number in ucmp_fp:
            swing_number = swing_number.strip()
            if swing_number in completed_swings:
                logger.debug(f"Already processed swing: {swing_number}")
                continue
            logger.info(f"Working on swing: {swing_number}")
            rclone.copy(f"supabase:swings/{swing_number}", f"elva-r2:elva-swings/{swing_number}", ignore_existing=True)
            cmp_fp.write(f"{swing_number}\n")
            cur_swing_count += 1
            if swing_count > 0 and cur_swing_count >= swing_count:
                logger.info("Reached the swing count buffer, exiting.")
                break


if __name__ == "__main__":
    logger = get_logger()
    start_of_execution = time.time()
    try:
        supabase_s3_to_r2(swing_listings_file, 800)
    except KeyboardInterrupt:
        logger.info(f"Forcefully stopped at swing: {swing_number}")
    logger.info(f"Execution took: ~{time.time() - start_of_execution:.2f}")
