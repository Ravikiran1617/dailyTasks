import logging

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def process_data():
    logging.info("Processing started")
    try:
        result = 10 / 2
        logging.info("Processing successful")
        return result
    except Exception as e:
        logging.error(f"Error occurred: {e}")

process_data()
