# AI Agent Guidelines

## Description Files

This folder contains subfolders with the source code of OutWiker plugins.

Each plugin contains a `plugin.xml` file with information about the plugin, which includes:
- plugin name (inside the `name` tag);
- plugin version (inside the `version` tag);
- required API version (inside the `api` tag).

Each plugin is accompanied by a `versions.xml` file with information about the different plugin versions, which includes:
- plugin version with the release date (the `version` tag);
- list of changes in each version (the `changes` tags for English and Russian);
- required API version (inside the `api` tag).

## Plugin Implementation

The main plugin class is usually contained in the `plugin.py` file and inherits from the `outwiker.api.core.plugins.Plugin` base class.

### Public API

- Plugins must use only the public API from `outwiker.api.*`.
- Do not import from internal modules such as `outwiker.core.*`, `outwiker.gui.*`, or `outwiker.app.*`.

### Localization

- Localization files live in the `locale/` subfolder of the plugin.
- Path pattern: `locale/<lang>/LC_MESSAGES/<plugin_name>.po` (plus the compiled `<plugin_name>.mo`).
- The `<plugin_name>.pot` template is stored in the plugin's `locale/` folder.

### Testing

- Plugin tests live outside the plugin folder, in `src/outwiker/tests/plugins/<plugin_name>/`.
