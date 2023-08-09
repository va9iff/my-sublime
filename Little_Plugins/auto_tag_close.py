"""
when you type <div and press tab, it'll complete it like this
<div    ->    <div></div>    (cursor at middle)    <div>|</div>
supports classes <div.hi    ->    <div class="hi"></div>
also self closing <br    ->    <br/>

"""

import sublime
import sublime_plugin

class AutoTagCloseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            # Get the current cursor position
            cursor_position = region.begin()

            # Get the current line
            line = self.view.line(cursor_position)

            # Get the content of the line before the cursor
            line_before_content = self.view.substr(sublime.Region(line.begin(), cursor_position))

            # Find the position of the last occurrence of the desired character
            character = '<'
            character_position = line_before_content.rfind(character)

            # Check if the character is found
            if character_position != -1:
                # Calculate the new content
                adding_content, move_cursor = line_completer(line_before_content[character_position:])
                new_content = line_before_content[:character_position + 1] + adding_content


                # Replace the content before the cursor
                self.view.replace(edit, sublime.Region(line.begin(), cursor_position), new_content)

                # set the cursor in between the tags
                self.view.sel().clear()
                new_cursor_position = line.begin() + character_position + move_cursor + 1
                self.view.sel().add(sublime.Region(new_cursor_position, new_cursor_position))

self_closers = [
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "keygen",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr"
]



# the result will be replaced after the "<" for the line.
# should be triggered on tab when the line has "<" in it.
# passed argument is the part after "<" in the line
# <tag-name.class <tag-name#id
def line_completer(line_after_gt):
    move_cursor = 0
    result = "" # it's the part after the <
    class_name = None
    tag_string = line_after_gt.split("<")[1].strip() # [0] == ""
    tag_name = "tagname"

    if "." in tag_string:
        tag_name, class_name = tag_string.split('.')
    else:
        tag_name = tag_string


    if tag_name in self_closers:
        before = '{tag_name}>'.format(tag_name=tag_name)
        after = ''
    elif class_name:
        before = '{tag_name} class="{class_name}">'.format(class_name=class_name, tag_name=tag_name)
        after = '</{tag_name}>'.format(tag_name=tag_name)
    else:
        before = '{tag_name}>'.format(tag_name=tag_name)
        after = '</{tag_name}>'.format(tag_name=tag_name)

    result = before + after
    move_cursor = len(before)

    return result,move_cursor

"""
<u></u>

<fasad></fasad>
<hi class="me"></hi>

<hi></hi>


<hi></hi>
<hi></hi>
"""

