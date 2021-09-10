import os
import shutil
import logging

from mkdocs.structure.files import File
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options


class BootprintSchema(BasePlugin):

    config_scheme = (
        ("include", config_options.Type(list, default=[])),
        ("css_file_path", config_options.Type(str, default='_theme_overrides/assets/stylesheets')),
        ("css_file_name", config_options.Type(str, default='bootprint.css')),
        ("output", config_options.Type(str, default="schema")),
        ("nav", config_options.Type(str, default="Schema")),
        ("tmp_folder", config_options.Type(str, default='/tmp/mkdocsBootprintSchemaTmp')),
        ("clean_tmp_folder", config_options.Type(bool, default=True)),
        ("auto_nav", config_options.Type(bool, default=True)),
        ("show_example", config_options.Type(str, default='all'))
    )

    def on_files(self, files, config):
        # Add json files within included files/directories to list
        locations = []

        for entry in self.config["include"]:
            if entry.endswith(".json"):
                locations.append(entry)

            elif os.path.isdir(entry):
                for root, dirs, filenames in os.walk(entry):
                    for file in filenames:
                        if file.endswith(".json"):
                            locations.append(os.path.join(root, file))

            else:
                logging.warning(f"Could not locate {entry}")

        if locations:
            ## Create all directory
            mk_dir = os.path.join(self.config['css_file_path'])
            if not os.path.isdir(mk_dir):
                os.makedirs(mk_dir, exist_ok=True)

            if not os.path.isdir(config['tmp_folder']):
                os.makedirs(config['tmp_folder'], exist_ok=True)


            ## Copy
            shutil.copyfile('./bootprint/bootprint.css', os.path.join(self.config['css_file_path'], self.config['css_file_name']))
            config['extra_css'].append(os.path.join(self.config['css_file_path'], self.config['css_file_name']))

            schema_list = []

            ## Path to Nav ##
            path=list(filter(None, self.config["nav"].split('/')))
            path.reverse()
            out_as_string = f"{{'{path.pop(0)}': schema_list}}"
            for item in path:
                out_as_string = f"{{'{item}':[{out_as_string}]}}"

            schema_dict = eval(f"{out_as_string}")

            for filepath in locations:
                file = os.path.basename(filepath)

                with open(filepath) as f:
                    # Check file is a schema file
                    data = f.read()
                    schema_syntax = ["$schema", "$ref"]

                    if any(x in data for x in schema_syntax):
                        path = os.path.join(config['docs_dir'],self.config['output'], file[:-5].md)
                        # write converted markdown file to this location
                        if not os.path.isdir(os.path.dirname(path)):
                            os.makedirs(os.path.dirname(path), exist_ok=True)

                        try:
                            os.system(f'bootprint -f ./bootprint/config.js json-schema {filepath} {self.config["tmp_folder"]}')
                            shutil.copyfile(os.path.join(self.config["tmp_folder"], 'index.md'), path)

                        except Exception:
                            logging.exception(
                                f"Exception handling {filepath}\n The file may not be valid Schema, consider excluding it."
                            )
                            continue

                        # Add to Files object
                        mkdfile = File(
                            f"{self.config['output']}/{file[:-5]}.md",
                            config['docs_dir'],
                            config["site_dir"],
                            config["use_directory_urls"],
                        )
                        files.append(mkdfile)

                        # Add to schema list
                        schema_list.append({f"{mkdfile.name}": f"{mkdfile.src_path}"})

                    else:
                        logging.warning(
                            f"{filepath} does not seem to be a valid Schema JSON file"
                        )

            # Add schemas to nav
            if self.config["auto_nav"]:
                config["nav"].append(schema_dict)

        return files