# class Template:
#     """
#     Class for managing blog templates.
#     """
#     template_path: str
#     template_name: str = ''
#     template_body: str = ''

#     def __init__(self, template_path: str = 'templates'):
#         self.template_path = template_path

#     def load_template(self, template_name: str):
#         """
#         Load a template file.
#         """
#         template_file = os.path.join(self.template_path, template_name)
#         if not os.path.exists(template_file):
#             raise FileNotFoundError(f"Template file '{template_file}' not found.")
#         with open(template_file, 'r', encoding='utf-8') as file:
#             self.template_body = file.read()

#     def render_template(self, context: dict):
#         """
#         Render a template with the given context.
#         """
#         template = jinja2.Template(self.template_body)
#         return template.render(context)
