from invoke import task

MAIN_CONTAINERS = [
    'postgres',
]


def up_container(
    context,
    containers: tuple[str],
    detach=True,
    **kwargs,
):
    """Bring up containers and run them.

    Add `d` kwarg to run them in background.

    """
    print(f'Bring up {", ".join(containers)} containers')

    up_cmd = (
        f'docker-compose up '
        f'{"-d " if detach else ""}'
        f'{" ".join(containers)}'
    )
    context.run(up_cmd)


def wait_for_database(context):
    """Ensure that database is up and ready to accept connections.

    Function called just once during subsequent calls of management commands.

    """
    if hasattr(wait_for_database, '_called'):
        return
    up_container(context, ('postgres', ), detach=True)
    context.run(
        ' '.join([
            'python3',
            'manage.py',
            'wait_for_database',
            '--stable 0'
        ]),
    )
    wait_for_database._called = True


@task
def manage(context, command, watchers=()):
    """Run django manage commands."""
    wait_for_database(context)
    context.run(
        ' '.join(['python3', 'manage.py', command]),
        watchers=watchers,
    )


@task
def run(context):
    """Run development web-server."""
    print('Running server')
    manage(context, 'runserver_plus 0.0.0.0:8000 --keep-meta-shutdown')


@task
def run_tests(context):
    """Run tests."""
    print('Run pytest')
    manage(context, command=' '.join(['test', '--verbosity=3']))
