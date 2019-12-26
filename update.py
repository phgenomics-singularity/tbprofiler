import pathlib
import click
import jinja2
import toml
import pendulum
import subprocess
import shlex


def load_template(name):
    '''
    Return the singularity recipe template as unicode text
    '''
    template = pathlib.Path(name).read_text()
    return template

@click.command()
@click.option("--version", default=None)
@click.option("--author", default=None)
@click.option("-c", "--config", default="config.toml")
def update_singularity(version, author, config):

    '''
    update the singularity recipe for new version of snippy
    '''

    config = toml.load('config.toml')

    if version is not None:
        config['version'] = version
    if author is not None:
        config['author'] = author
    
    loader = jinja2.FunctionLoader(load_template)
    env = jinja2.Environment(loader=loader)
    SINGULARITY_RECIPE = env.get_template("_singularity.j2").render(config)
    # create global version
    global_recipe = pathlib.Path("Singularity")
    global_recipe.write_text(SINGULARITY_RECIPE)



if __name__ == "__main__":
    update_singularity()
