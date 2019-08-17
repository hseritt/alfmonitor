
SUBSYSTEM_STARTUP_MSG = 'Starting {} subsystem.'
SHUTDOWN_MSG = 'Shutdown requested by user. Shutting down.'
SVC_START_MSG = 'AlfMonitor service started at {}'
ACTVE_AGENTS_MSG = 'Active Agents {}'
INACTIVE_MAIL_MSG = (
    'Mail agent is not active and will not be run. '
    'Warning: Email alerts will not sent.'
)
START_AGENT_MSG = 'Starting agent: {}'
ENGINE_SLEEP_MSG = (
    'Alfmonitor engine sleeping for '
    '{} seconds until next run.'
)
SCRIPT_CALL_MSG = 'This script should only be called by engine.py.'
MAIL_INIT_MSG = 'Mailer subsystem initialized.'
MAIL_START_MSG = 'Mailer subsystem enabled, started and ready.'
MAIL_SEARCH_MSG = 'Searching for alarms to mail.'
ALARM_MSG = (
    'An alarm was generated: \n\n'
    '{}\n\n'
    'This event occurred at {}\n'
    'Connection time was {} ms.\n\n'
)
SEND_TO_MSG = 'Sending alert email to the following: {}'
MAIL_SLEEP_MSG = 'Mailer subsystem sleeping for {} seconds.'
DISABLED_MAIL_MSG = (
    'Mailer subsystem disabled. '
    'Mailer subsystem will not be started. '
    'Warning: emails for alarms will not be sent.'
)
RUN_AGENT_MSG = 'Running {} Agent.'
NO_PROFILE_CONFIGURED_MSG = (
    'No profiles configured for {} agent. '
    'Consult documentation about profile configuration.'
)
MISSING_AGENT_MSG = "Check that the agent's name is not misspelled or missing."
