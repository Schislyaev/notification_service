from croniter import croniter


def format_cron(schedule: dict) -> str:
    cron_schedule = {
        'minute': '*',
        'hour': '*',
        'day': '*',
        'month': '*',
        'day_of_week': '*',
        'second': '*',
    }

    for key, value in schedule.items():
        cron_schedule[key] = value

    return ' '.join([value for value in cron_schedule.values()])


def validate_cron(schedule: dict) -> bool:
    cron = format_cron(schedule=schedule)
    try:
        croniter(cron)
        return True
    except ValueError:
        return False
