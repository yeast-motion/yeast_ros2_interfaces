import jinja2
import json
import pathlib
import argparse
import glob
import os

parser = argparse.ArgumentParser(description='Render script')
parser.add_argument('--src-dir', action='store', dest='src_dir', default='')
parser.add_argument('--dst-dir', action='store', dest='dst_dir', default='')
parser.add_argument('--template', action='store', dest='template', default='')
args = parser.parse_args()

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
ROOT_DIRECTORY = os.path.dirname(SCRIPT_DIRECTORY)

template_file = os.path.realpath(args.template)

schema_dir = os.path.realpath(args.src_dir)
schema_files = glob.glob(f'{schema_dir}/*.json')

msg_dir = os.path.realpath(args.dst_dir)

type_map = {
    'number' : 'float32',
    'boolean' : 'bool'
}

for schema_file in schema_files:
    if os.stat(schema_file).st_size == 0:
        continue

    structures = {}
    msg_name = ''

    with open(schema_file, 'r') as stream:
        json_data = json.load(stream)

        msg_name = json_data['title']

        for struct in json_data['properties']:
            if 'type' in json_data['properties'][struct]:
                if json_data['properties'][struct]['type'] == 'array':
                    type = json_data['properties'][struct]['items']['type']
                    if type in type_map.keys():
                        type = type_map[type]
                    type = f'{type}[]'
                else:
                    type = json_data['properties'][struct]['type']
                    if type in type_map.keys():
                        type = type_map[type]

                structures[struct.lower()] = type

            elif '$ref' in json_data['properties'][struct]:
                type = json_data['properties'][struct]['$ref']
                type = type.replace('.schema.json', '')
                structures[struct.lower()] = type
    
    schema_basename = os.path.basename(schema_file)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('/'), trim_blocks=True)
    msg_template = env.get_template(template_file)
    msg_result = msg_template.render(structures=structures, schema_name=schema_basename)
    f = open(f'{msg_dir}/{msg_name}.msg', 'w')
    f.write(msg_result)
    f.close()

# python3 template/render_jinja.py --template template/msg.j2 --src-dir yeast-schema/data_definitions/ --dst-dir msg/
