import datetime

from colorama import Fore

from outwiker.utilites.textfile import readTextFile
from outwiker.core.changelogfactory import ChangeLogFactory

from .defines import PLUGINS_LIST
from .buildfacts import BuildFacts


def show_plugins_info():
    facts = BuildFacts()

    print('{:<20}{:<20}{}'.format('Plugin', 'Version', 'Release date'))
    for plugin in PLUGINS_LIST:
        changelog_path = facts.getPluginChangelogPath(plugin)
        changelog_txt = readTextFile(changelog_path)
        changelog = ChangeLogFactory.fromString(changelog_txt, '')
        latest_version = changelog.latestVersion

        date_str = (latest_version.date.strftime('%d.%m.%Y')
                    if latest_version.date else '-')

        color = ''
        if latest_version.date is None:
            color = Fore.RED
        elif latest_version.date.date() == datetime.date.today():
            color = Fore.GREEN

        print('{color}{name:.<20}{version:.<20}{date:^10}'.format(
            color=color,
            name=plugin,
            version=str(latest_version.version),
            date=date_str
        ))
