import jinja2
import trafaret as t
from trafaret.contrib.rfc_3339 import DateTime
from .utils import gather_template_folders


def build_field(key, value, relations=None):
    extra = None
    name = key
    if isinstance(value, t.Int):
        v = "number"
    elif isinstance(value, (t.String, t.URL)):
        v = "string"
    elif isinstance(value, t.Email):
        v = "email"
    elif isinstance(value, t.Float):
        v = "float"
    elif isinstance(value, t.Enum):
        v = "choice"
    elif isinstance(value, (t.Dict, t.List)):
        v = "json"
    elif isinstance(value, (t.Bool, t.StrBool)):
        v = "boolean"
    elif isinstance(value, DateTime):
        v = "datetime"
    else:
        v = "string"
    return name, v, extra


def entity_description(entity_name, primary_key, schema):
    f = [build_field(s.name, s.trafaret) for s in schema.keys]
    e = {"name": entity_name,
         "pk": primary_key,
         "actions": ['show', 'edit', 'delete'],
         "sort_field": '_id',
         "per_page": 50,
         "description": "desc",
         "fields": [{"name": k, "type": v, "extra": e} for k, v, e in f]}
    return e


def generate_config(entities, base_url, template_name=None,
                    template_folder=None, desc=None, extra_context=None):
    template_name = template_name or 'config.j2'
    desc = desc or 'aiohttp_admin'

    context = {
        "admin_description": desc,
        "base_url": base_url if base_url.endswith("/") else base_url + '/' ,
        "entities": [entity_description(n, pk, s) for n, pk, s in entities],
        "extra_context": extra_context,
    }
    tf = gather_template_folders(template_folder)
    loader = jinja2.FileSystemLoader(tf)
    env = jinja2.Environment(loader=loader)
    template = env.get_template(template_name)
    text = template.render(context)
    print(text)
    return text
