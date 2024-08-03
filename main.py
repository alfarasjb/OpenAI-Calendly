from src.app.app import AppointmentSetterApp
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    app = AppointmentSetterApp()
    app.main()
