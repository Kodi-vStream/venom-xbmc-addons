# -*- coding: utf-8 -*-
#
# Code From https://github.com/movieshark/waaw/
#

from io import BytesIO
from tempfile import NamedTemporaryFile

import xbmcgui
from xbmcgui import Control
from xbmcvfs import translatePath


class CaptchaWindow(xbmcgui.WindowDialog):
    def __init__(self, image: bytes, width: int, height: int):
        self.orig_image = BytesIO(image)
        self.width = width
        self.height = height
        self.temp_file = self.create_temp_image()
        self.border_img = None
        self.frame_x = (self.getWidth() - self.width) // 2  # Centered horizontally
        self.frame_y = (self.getHeight() - self.height) // 2  # Centered vertically
        self.left_arrow = None
        self.right_arrow = None
        self.top_arrow = None
        self.bottom_arrow = None
        self.submit_button = None
        self.finished = False
        self.orig_x = self.frame_x
        self.orig_y = self.frame_y
        self.add_controls()

    def create_temp_image(self):
        
        filePath = 'special://home/userdata/addon_data/plugin.video.vstream/Captcha.raw'
        import xbmcvfs
        downloaded_image = xbmcvfs.File(filePath, 'wb')
        downloaded_image.write(self.orig_image.read())
        downloaded_image.close()
        return ""
        
        #temp_file = NamedTemporaryFile(suffix=".jpg")
        #self.orig_image.seek(0)
        #temp_file.write(self.orig_image.read())
        #temp_file.flush()
        #return temp_file

    @property
    def border_img_path(self):
        return translatePath(
            "special://home/addons/plugin.video.vstream/resources/lib/waaw/resources/media/border90.png"
        )

    @property
    def solution_x(self):
        return self.frame_x - self.orig_x + 45

    @property
    def solution_y(self):
        return self.frame_y - self.orig_y + 45

    def add_controls(self):
        # Define arrow directions, corresponding labels, and sizes
        arrow_info = {
            "top": ("^", 150, 75),  # Increase width and height
            "bottom": ("v", 150, 75),  # Increase width and height
            "left": ("<", 75, 150),  # Increase width and height
            "right": (">", 75, 150),  # Increase width and height
        }

        # Adjust this value to control the space between the button and arrows
        arrow_margin = 10

        # Calculate arrow positions and create arrow buttons
        for direction, (label, width, height) in arrow_info.items():
            if direction == "top":
                x = self.frame_x + (self.width - width) // 2
                y = self.frame_y - height - arrow_margin
            elif direction == "bottom":
                x = self.frame_x + (self.width - width) // 2
                y = self.frame_y + self.height + arrow_margin
            elif direction == "left":
                x = self.frame_x - width - arrow_margin
                y = self.frame_y + (self.height - height) // 2
            elif direction == "right":
                x = self.frame_x + self.width + arrow_margin
                y = self.frame_y + (self.height - height) // 2

            textOffsetX = (width - len(label) * 12) // 2  # Center text horizontally
            textOffsetY = (height - 12) // 2  # Center text vertically

            button = xbmcgui.ControlButton(
                x,
                y,
                width,
                height,
                label,
                textOffsetX=textOffsetX,
                textOffsetY=textOffsetY,
            )

            # Add arrow button
            self.addControl(button)
            if direction == "top":
                self.top_arrow = button
            elif direction == "bottom":
                self.bottom_arrow = button
            elif direction == "left":
                self.left_arrow = button
            elif direction == "right":
                self.right_arrow = button

        captcha_image = xbmcgui.ControlImage(
            #self.frame_x, self.frame_y, self.width, self.height, self.temp_file.name
            self.frame_x, self.frame_y, self.width, self.height, 'special://home/userdata/addon_data/plugin.video.vstream/Captcha.raw'
        )
        self.addControl(captcha_image)

        # Calculate the position of the Submit button
        submit_button_width = 200
        submit_button_height = 100
        submit_button_x = self.frame_x + (self.width - submit_button_width) // 2
        submit_button_y = self.frame_y + (self.height - submit_button_height) // 2
        textOffsetX = (
            submit_button_width - len("Submit") * 12
        ) // 2  # Center text horizontally
        textOffsetY = (submit_button_height - 12) // 2  # Center text vertically

        submit_button = xbmcgui.ControlButton(
            submit_button_x,
            submit_button_y,
            submit_button_width,
            submit_button_height,
            " Submit",
            textOffsetX=textOffsetX,
            textOffsetY=textOffsetY,
        )
        self.addControl(submit_button)
        self.submit_button = submit_button

        self.border_img = xbmcgui.ControlImage(
            self.frame_x, self.frame_y, 90, 90, self.border_img_path
        )
        self.addControl(self.border_img)

    def update_border_img(self, x: int, y: int):
        self.border_img.setPosition(self.frame_x + x, self.frame_y + y)

    def close(self) -> None:
        #self.temp_file.close()
        return super().close()

    def onControl(self, control: Control) -> None:
        # if left arrow is clicked and border is not at the left edge, move left
        if control.getId() == self.left_arrow.getId() and self.frame_x > self.orig_x:
            self.frame_x -= 10
            self.update_border_img(0, 0)
        # if right arrow is clicked and border is not at the right edge, move right
        elif (
            control.getId() == self.right_arrow.getId()
            and self.frame_x < self.orig_x + self.width - 90
        ):
            self.frame_x += 10
            self.update_border_img(0, 0)
        # if up arrow is clicked and border is not at the top edge, move up
        elif control.getId() == self.top_arrow.getId() and self.frame_y > self.orig_y:
            self.frame_y -= 10
            self.update_border_img(0, 0)
        # if down arrow is clicked and border is not at the bottom edge, move down
        elif (
            control.getId() == self.bottom_arrow.getId()
            and self.frame_y < self.orig_y + self.height - 90
        ):
            self.frame_y += 10
            self.update_border_img(0, 0)
        # if submit button is clicked, close
        elif control.getId() == self.submit_button.getId():
            self.finished = True
            self.close()
        else:
            super().onControl(control)

    def onAction(self, action: xbmcgui.Action) -> None:
        # if left arrow is pressed and border is not at the left edge, move left
        if action == xbmcgui.ACTION_MOVE_LEFT and self.frame_x > self.orig_x:
            self.frame_x -= 10
            self.update_border_img(0, 0)
        # if right arrow is pressed and border is not at the right edge, move right
        elif (
            action == xbmcgui.ACTION_MOVE_RIGHT
            and self.frame_x < self.orig_x + self.width - 90
        ):
            self.frame_x += 10
            self.update_border_img(0, 0)
        # if up arrow is pressed and border is not at the top edge, move up
        elif action == xbmcgui.ACTION_MOVE_UP and self.frame_y > self.orig_y:
            self.frame_y -= 10
            self.update_border_img(0, 0)
        # if down arrow is pressed and border is not at the bottom edge, move down
        elif (
            action == xbmcgui.ACTION_MOVE_DOWN
            and self.frame_y < self.orig_y + self.height - 90
        ):
            self.frame_y += 10
            self.update_border_img(0, 0)
        # if enter is pressed, close
        elif action == xbmcgui.ACTION_SELECT_ITEM:
            self.finished = True
            self.close()
        # if close button is pressed, close
        if action == xbmcgui.ACTION_NAV_BACK:
            self.close()
        else:
            super().onAction(action)
