from djamago import Topic, Callback, Expression
import random


class Markdown(Topic):
    @Callback([
        (100, Expression(r'whatis(".*markdown.*")')),
    ])
    def whatis(node, id, var):
        node.topics = (
            (100, 'markdown'),
            (50, 'main'),
        )
        node.response = random.choice([
            note_doc
        ])

    @Callback([
        (100, Expression(r'R:70(".*(?:markdown|\btip\b).*")')),
    ])
    def tip(node, id, var):
        node.topics = (
            (100, 'markdown'),
            (50, 'main'),
        )
        node.response = random.choice(note_tips)


note_doc = """\
Here is an example of markdown code for a documentation that guides users on
using the markdown syntax in Note:

**Markdown Syntax**
--------------------

### Headers

To create a header, use the `#` symbol followed by the header text.

```
# Heading 1
## Heading 2
### Heading 3
```

### Bold and Italic Text

To create bold text, surround the text with `**` symbols.

```
**This text will be bold**
```

To create italic text, surround the text with `*` symbols.

```
*This text will be italic*
```

### Lists

To create an unordered list, use the `*` symbol followed by the list item.

```
* Item 1
* Item 2
* Item 3
```

To create an ordered list, use the `1.` symbol followed by the list item.

```
1. Item 1
2. Item 2
3. Item 3
```

### Mentions

To mention another user, use the `@` symbol followed by the username.

```
@johnDoe
```

This will create a link to the user's profile.

### Example Usage

Here is an example of how you can use the markdown syntax in Note:

```
# Welcome to Note!

This is an **example** of a note that mentions another user.

I would like to thank @johnDoe for his contribution to this project.

Here is a list of items:

* Item 1
* Item 2 @janeDoe
* Item 3

Best,
@antimonyTeam
```

This documentation will be updated regularly to include more features and
examples of the markdown syntax in Note. If you have any questions or need
further assistance, please don't hesitate to ask.

**Happy Writing!**
"""


note_tips = [
    "#Tip\nUse `*` to quote italic texts\ne.g `*hello*` -> *hello*",
    "#Tip\nUse `**` to quote bold texts\ne.g `**hello**` -> **hello**",
    "#Tip\nAdd images with `![image replacement](image url)`",
    "#Tip\nMention users with `@user:{username}` syntax",
]
