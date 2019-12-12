"""Card directive for reStructuredText."""


import os.path
import uuid
import logging
import sys

import pyqrcode

from docutils import nodes
from docutils.parsers.rst import Directive, directives
import logbook

from nikola.plugin_categories import RestExtension
from nikola.plugins.compile import rest


logger = logging.getLogger(__name__)


class Plugin(RestExtension):
    """Plugin for reST card directive."""

    name = "rest_card"

    def set_site(self, site):
        """Set Nikola site."""
        self.site = site
        directives.register_directive('card', Card)
        Card.site = site
        return super(Plugin, self).set_site(site)


class Card(Directive):
    """reST extension for inserting cards."""

    has_content = True
    optional_arguments = sys.maxsize
    option_spec = {
        'title': directives.unchanged,
        'class': directives.unchanged,
        'thumbnail': directives.unchanged,
        'image': directives.unchanged,
        'link': directives.unchanged,
        'qr_link': directives.unchanged,
        'qr_text': directives.unchanged,
        'alt': directives.unchanged,
        'width': directives.unchanged,
        'height': directives.unchanged,
        'style': directives.unchanged,
    }

    def rst2html(self, src):
        null_logger = logbook.Logger('NULL')
        null_logger.handlers = [logbook.NullHandler()]
        output, error_level, deps, _ = rest.rst2html(
            src, logger=null_logger, transforms=self.site.rst_transforms)

        return output

    def run(self):
        """Run the slides directive."""
        if len(self.content) == 0:  # pragma: no cover
            card_content = ""
        else:
            card_content = self.rst2html('\n'.join(self.content))

        card_title = self.options.get('title', None)
        card_class = self.options.get('class', '').strip().split('\n')
        card_thumbnail = self.options.get('thumbnail', None)
        card_image = self.options.get('image', None)
        card_link = self.options.get('link', None)
        card_qr_link = self.options.get('qr_link', None)
        card_qr_text = self.options.get('qr_text', None)
        card_alt = self.options.get('alt', None)
        card_width = self.options.get('width', None)
        card_height = self.options.get('height', None)
        card_style_ = self.options.get('style', None)

        card_class.insert(0, 'card')
        card_style = []
        if card_width is not None:
            card_style.append('width:{}'.format(card_width))
        if card_height is not None:
            card_style.append('height:{}'.format(card_height))
        if card_style_ is not None:
            card_style.append(card_style_)

        if card_thumbnail is not None:
            path, ext = os.path.splitext(card_thumbnail)
            card_image = path + '.thumbnail' + ext
            if card_link is None:
                card_link = card_thumbnail

        if card_alt is None:
            card_alt = card_title
        template_name = 'card_bootstrap4.tmpl'

        if card_qr_link is not None:
            card_link = card_qr_link
            code = pyqrcode.create(card_qr_link)
            image_as_str = code.png_as_base64_str(scale=5)
            card_image = 'data:image/png;base64,{}'.format(image_as_str)
        if card_qr_text is not None:
            code = pyqrcode.create(card_qr_text)
            image_as_str = code.png_as_base64_str(scale=5)
            card_image = 'data:image/png;base64,{}'.format(image_as_str)

        if self.site.invariant:  # for testing purposes
            hex_uuid4 = 'fixedvaluethatisnotauuid'
        else:
            hex_uuid4 = uuid.uuid4().hex


        output = self.site.template_system.render_template(
            template_name,
            None,
            {
                'hex_uuid4': hex_uuid4,
                'card_title': card_title,
                'card_class': " ".join(card_class),
                'card_image': card_image,
                'card_link': card_link,
                'card_alt': card_alt,
                'card_style': ";".join(card_style),
                'card_content': card_content,
            }
        )
        return [nodes.raw('', output, format='html')]

# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
