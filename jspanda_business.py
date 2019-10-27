from application import create_app
import logging

_logger = logging.getLogger(__name__)
logging.basicConfig()
_logger.setLevel(logging.INFO)

app = create_app()

if __name__ == '__main__':
    _logger.info("Let the show start...")
    app.run(host='0.0.0.0')
