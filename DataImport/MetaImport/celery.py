from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery(
    'MetaImport',
    broker='redis://localhost:6379/3',
    include=['MetaImport.ctasks']
)

# Optional configuration, see the application user guide.
app.conf.update(
    broker_transport_options = {'visibility_timeout': 60 * 10 },
    result_expires=3600,
)

app.task(
    )

if __name__ == '__main__':
    app.start()
