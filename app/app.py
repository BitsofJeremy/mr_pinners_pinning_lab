"""pinning_lab app"""
# comment to remove monitoring with New Relic
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

# Import the app
from pinning_lab import app


if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
    )
