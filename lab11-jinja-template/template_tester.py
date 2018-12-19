from jinja2 import Environment, FileSystemLoader
import yaml

env = Environment(loader=FileSystemLoader('./'))
#What template to use:
template = env.get_template('template.j2')
#With what vars fill template:
ac_vars = yaml.load(open('group_vars/routers.yaml'))
#What would be the result
print (template.render(ac_vars))
