import time
from django.contrib.auth.models import User
from django.core.mail import send_mail
from agents.messages import (
    MAIL_INIT_MSG, MAIL_START_MSG, MAIL_SEARCH_MSG, ALARM_MSG,
    SEND_TO_MSG, MAIL_SLEEP_MSG, DISABLED_MAIL_MSG
)
from agents.models import Alarm
from alfmonitor.lib.alflogger import logger
from alfmonitor.settings import (
    MAIL_FAIL_SILENTLY, MAILER_RUN_FREQUENCY, MAILER_ENABLED, MAIL_FROM
)


LOGGER = logger(__name__)


class Mailer(object):

    def __init__(self):
        LOGGER.info(MAIL_INIT_MSG)

    def run(self):
        """ Runs mail agent."""
        if MAILER_ENABLED:
            LOGGER.info(MAIL_START_MSG)
            while True:
                LOGGER.debug(MAIL_SEARCH_MSG)
                alarms = Alarm.objects.filter(
                    is_active=True,
                    profile__is_active=True
                )

                for alarm in alarms:
                    subject = f'{alarm.profile.agent.name}: ' + \
                        f'{alarm.profile.name} {alarm.alarm_type}'

                    message = ALARM_MSG.format(
                        subject, alarm.event_time, alarm.connect_time
                    )

                    admin_list = alarm.profile.admins.all()

                    if len(admin_list) == 0:
                        admin_list = [User.objects.get(username='admin'), ]

                    try:
                        LOGGER.debug(
                            SEND_TO_MSG.format(
                                ', '.join(
                                    [user.email for user in admin_list]
                                )
                            )
                        )
                        send_mail(
                            subject,
                            message,
                            MAIL_FROM,
                            [user.email for user in admin_list],
                            fail_silently=MAIL_FAIL_SILENTLY
                        )
                    except Exception as err:
                        LOGGER.exception(err)

                LOGGER.debug(
                    MAIL_SLEEP_MSG.format(
                        MAILER_RUN_FREQUENCY
                    )
                )
                time.sleep(MAILER_RUN_FREQUENCY)

        else:
            LOGGER.info(
                DISABLED_MAIL_MSG
            )
