from src.services.calendly import Calendly


if __name__ == "__main__":
    cal = Calendly()
    print(cal.list_user_availability_schedules())
