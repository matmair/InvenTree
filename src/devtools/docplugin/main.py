"""Plugin to keep solitified markdown around."""

import os
from pathlib import Path

import mkdocs
from mkdocs.config import base
from mkdocs.config import config_options as c


class MyPluginnConfig(base.Config):
    """Config options."""

    enabled = c.Type(bool, default=True)
    verbose = c.Type(bool, default=False)
    target = c.Type(str, default='')


class MyPlugin(mkdocs.plugins.BasePlugin[MyPluginnConfig]):
    """Plugin to keep solitified markdown around."""

    def on_config(self, config):
        """Ensure base dir exists."""
        cf_t = self.config['target']
        if cf_t:
            self.base = Path(cf_t)
        elif os.environ.get('SOLIDIFY_DIR'):
            self.base = Path(os.environ['SOLIDIFY_DIR'])
        else:
            self.base = Path('base_src')

        if not self.base.exists():
            self.base.mkdir(parents=True)

    def on_page_markdown(self, markdown: str, **kwargs) -> str:
        """Safe page mk."""
        if self.config['verbose']:
            print('Markdown content:', markdown)
        # Log file away
        trg = self.base.joinpath(kwargs['page'].file.src_path)
        if not trg.parent.exists():
            trg.parent.mkdir(parents=True)
        trg.write_text(markdown)
        return markdown
