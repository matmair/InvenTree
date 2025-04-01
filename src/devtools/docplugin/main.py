"""Plugin to keep solitified markdown around."""

from pathlib import Path

import mkdocs
from mkdocs.config import base
from mkdocs.config import config_options as c


class MyPluginnConfig(base.Config):
    """Config options."""

    enabled = c.Type(bool, default=True)
    verbose = c.Type(bool, default=False)


BASE = Path('base_src')


class MyPlugin(mkdocs.plugins.BasePlugin[MyPluginnConfig]):
    """Plugin to keep solitified markdown around."""

    def on_page_markdown(self, markdown: str, **kwargs) -> str:
        """Safe page mk."""
        if self.config['verbose']:
            print('Markdown content:', markdown)
        # Log file away
        trg = BASE.joinpath(kwargs['page'].file.src_path)
        if not trg.parent.exists():
            trg.parent.mkdir(parents=True)
        trg.write_text(markdown)
        return markdown
