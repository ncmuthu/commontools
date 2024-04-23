
import yaml
from ruamel.yaml import YAML

def replace_values_in_yaml_template(template_file, replacements):
    yaml = YAML()
    with open(template_file, 'r') as file:
        yaml_content = yaml.load(file)

    for key, value in replacements.items():
        if key in yaml_content:
            yaml_content[key] = value

    return yaml_content

def create_yaml_file(file_path, yaml_content):
    yaml = YAML()
    with open(file_path, 'w') as file:
        yaml.dump(yaml_content, file)

"""
def replace_values_in_yaml_template(template_file, replacements):
    with open(template_file, 'r') as file:
        yaml_content = yaml.safe_load(file)

    for key, value in replacements.items():
        if key in yaml_content:
            yaml_content[key] = value

    return yaml_content

def create_yaml_file(file_path, yaml_content):
    with open(file_path, 'w') as file:
        yaml.dump(yaml_content, file, default_flow_style=False)
"""

# Example usage
template_file = "template.yml"
replacements = {
    "name": "new_repo_name",
    "project_code": "new_project_code",
    "approver": "new_approver_name"
}
output_file = "final.yml"

updated_yaml_content = replace_values_in_yaml_template(template_file, replacements)
create_yaml_file(output_file, updated_yaml_content)
