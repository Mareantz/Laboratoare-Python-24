# The build_xml_element function receives the following parameters: tag, content, and key-value elements given as
# name-parameters. Build and return a string that represents the corresponding XML element. Example:
# build_xml_element ("a", "Hello there", href =" http://python.org ", _class =" my-link ", id= " someid ") returns
# the string = "<a href="http://python.org "_class = " my-link " id = " someid "> Hello there </a>"

def build_xml_element(tag: str, content: str, **kwargs) -> str:
    attributes = ' '.join([f'{key}="{value}"' for key, value in kwargs.items()])
    return f'<{tag} {attributes}> {content} </{tag}>'


print(build_xml_element("a", "Hello there", href="http://python.org", _class="my-link", id="someid"))
