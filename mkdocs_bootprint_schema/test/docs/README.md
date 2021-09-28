# mkdocs bootprint Schema plugin #

This is a plugin that create html page from json schema using BootPrint <https://github.com/bootprint/bootprint> tool.

## Setup ##

Install the plugin using pip and bootprint requirement:

```shell
# Bootprint, inspired from official repo
npm install -g bootprint \
npm install -g bootprint-json-schema

# Mkdocs plugin
pip install mkdocs-bootprint-schema
```

Activate the plugin in `mkdocs.yml`, then, specify folders and files that you want to include in `mkdocs.yml` relative to it's location:

```yaml
plugins:
  - search
  - bootprint_schema:
      include:
        - Path_To_JSONSchema
```

Define a theme overwride varaible in order to save css into

```yaml
theme:
  custom_dir: ./_theme_overrides
```

Specified directories will be scanned for schema json files, so consider specifying individual files for expansive directories.

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Usage ##

Just activate the plugin, specify directories and files in the manner shown above, and it will operate when normal mkdocs commands are used like `mkdocs serve'

## Options ##

- `auto_nav` : If true, generated markdown from JSON will be add to navigation path. Using `nav` (default `Schema`) entry (bool, default=True)
- `output` : Set export directory for markdown file, directory relative to `docs_dir` (str, default="/schema")
- `nav` : Set the navigation path when JSON schema will be find in web IHM (str, default="Schema"). Can be a complexe path (like /home/json/schema), but, it will not merge if existing path already exist *see note*.
- `show_example` : Using template than show, or not, example present un json schema. Seems to not work with bootprint (bool, default=True)
- `css_file_path` : Output folder for css file (str, default='assets/stylesheets')
- `css_file_name` : Output css file name (str, default='bootprint.css')
- `tmp_folder` : Temp folder using when generated file (str, default='/tmp/mkdocsBootprintSchemaTmp')
- `clean_tmp_folder` : Clean temp folder at the end (bool, default=True)

> **Notes** About `nav` : Nav path is adding to navigation without merge with existing path. If you want to show schema in existing section (referenced in classic nav), set `auto_nav` to false and refere it by yourself in classic nav.
> Example :
