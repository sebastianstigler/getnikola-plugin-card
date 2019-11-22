Card for reStructuredText.

This plugin supports bootstrap 4.

The directiv has the follwing options:

- `title`: The title of the card.
- `class`: A list of additional classes for the card.
- `thumbnail`: The path to an image with a thumbnail (like the directive `thumbnail`).
- `image`: The path to an image. You can set either `thumbnail` or `image`. If you set both, `thumbnail` wins.
- `link`: A link. If `thumbnail` or `image` is set, the image is clickable. Without an image, the whole card is clickable.
- `qr_link`: Creates a QR-code image and uses the content als link for the image. If `image` or `link` is set, `qr_link` wins.
- `qr_text`: Like `qr_link` but no link is created. If `link` is set, it will be used.
- `alt`: The alt text of the image.
- `width`: A value with unit for the width of the card.
- `height`: The height of the card (like `width`)
- `style`: Further style elements for the card like `margin:10px;color:black;` ...

Example:

```

    .. card::
      :title: Title of the card
      :class: some additional classes
      :image: /path/to/image.xxx
      :alt: the alt text of the image
      :width: 300px

      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi accumsan, nulla sit amet aliquam molestie, nisi purus dignissim ante, non scelerisque diam ligula eu ex.

```

Requrires the python packages `pyqrcode` and `pypng`.
