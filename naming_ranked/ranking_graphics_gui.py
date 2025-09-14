"""
This file creates the line graph for names in different ranks
"""

import os

import tkinter

import utils

CANVAS_MARGIN = 30
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 600
LINE_WIDTH = 2
TEXT_SPACE = 2


def run_gui(
        years: list[int],
        max_rank: int,
        data_dir: str,
        colors: list[str]
) -> None:
    """
    initializes the tk window
    """
    name_dict = {}
    # read and add every files' name, year, and rank into name_dict
    for year in years:
        filepath = os.path.join(data_dir, f"{year}.txt")
        utils.add_names_from_file(filepath, name_dict)

    root = tkinter.Tk()
    canvas = make_background(
        root,
        years,
        max_rank,
        CANVAS_WIDTH,
        CANVAS_HEIGHT,
        name_dict,
        colors
    )
    create_fixed_lines(canvas, years, max_rank)
    root.mainloop()


def create_fixed_lines(
        canvas: tkinter.Canvas,
        years: list[int],
        max_rank: int
) -> None:
    """
    create horizontal and vertical lines in the canvas
    """
    canvas.create_line(
        CANVAS_MARGIN,
        CANVAS_MARGIN,
        CANVAS_WIDTH - CANVAS_MARGIN,
        CANVAS_MARGIN
    )  # create upper horizontal line
    canvas.create_line(
        CANVAS_MARGIN,
        CANVAS_HEIGHT - CANVAS_MARGIN,
        CANVAS_WIDTH - CANVAS_MARGIN,
        CANVAS_HEIGHT - CANVAS_MARGIN
    )  # create lower horizontal line
    canvas.create_text(
        CANVAS_MARGIN - TEXT_SPACE,
        CANVAS_MARGIN - 20,
        text="rank",
        anchor='e'
    )
    canvas.create_text(
        CANVAS_MARGIN - TEXT_SPACE,
        CANVAS_MARGIN,
        text='1',
        anchor='e'
    )
    canvas.create_text(
        CANVAS_MARGIN - TEXT_SPACE,
        CANVAS_HEIGHT - CANVAS_MARGIN,
        text=max_rank,
        anchor='e'
    )
    canvas.create_text(
        CANVAS_WIDTH,
        CANVAS_HEIGHT - CANVAS_MARGIN,
        text="year",
        anchor='e'
    )
    # create vertical lines corresponding to each year
    for index in range(len(years)):
        curr_x = get_curr_x(years, index)
        canvas.create_line(curr_x, 0, curr_x, CANVAS_HEIGHT)
        canvas.create_text(
            curr_x + TEXT_SPACE,
            CANVAS_HEIGHT - CANVAS_MARGIN,
            text=years[index],
            anchor="nw"
        )


def make_background(
        root: tkinter.Tk,
        years: list[int],
        max_rank: int,
        canvas_width: int,
        canvas_height: int,
        name_dict: dict[str, dict[int, int]],
        colors: list[str]
) -> tkinter.Canvas:
    """
    create required grid, text, and entry for the window
    """
    name_label = tkinter.Label(root, text="Name:", padx=7)
    name_label.grid(column=0, row=0, sticky='w')
    name_entry = tkinter.Entry(root, width=40, borderwidth=2)
    name_entry.grid(column=1, row=0, sticky='w')
    name_entry.focus()
    name_text = tkinter.Text(root, height=2, width=70, borderwidth=3)
    name_text.grid(column=2, row=0, sticky='w')

    search_label = tkinter.Label(root, text="Search:", padx=7)
    search_label.grid(column=0, row=1, sticky='w')
    search_entry = tkinter.Entry(root, width=40, borderwidth=2)
    search_entry.grid(column=1, row=1, sticky='w')
    search_text = tkinter.Text(root, height=2, width=70, borderwidth=3)
    search_text.grid(column=2, row=1, sticky='w')

    labelframe1 = tkinter.LabelFrame(root, height=10, width=canvas_width, borderwidth=0)
    labelframe1.grid(columnspan=10, row=2, sticky='w')

    canvas = tkinter.Canvas(root, height=canvas_height, width=canvas_width)
    canvas.grid(columnspan=10, row=3, sticky='w')

    labelframe2 = tkinter.LabelFrame(root, height=10, width=canvas_width, borderwidth=0)
    labelframe2.grid(columnspan=10, row=4, sticky='w')

    name_entry.bind(
        "<Return>",
        lambda event: process_draw(
            canvas,
            years,
            max_rank,
            name_entry,
            name_text,
            name_dict,
            colors
        )
    )  # draw line graph after hitting the return key in name_entry
    search_entry.bind(
        "<Return>",
        lambda event: process_search(
            search_entry,
            search_text,
            name_dict
        )
    )  # search for the corresponding name after hitting the return key in search_entry

    return canvas


def process_draw(
        canvas: tkinter.Canvas,
        years: list[int],
        max_rank: int,
        name_entry: tkinter.Entry,
        name_text: tkinter.Text,
        name_dict: dict[str, dict[int, int]],
        colors: list[str]
) -> None:
    """
    handle the condition of the function draw_names
    """
    raw_names = name_entry.get().split()
    unique_names = list(dict.fromkeys(name.capitalize() for name in raw_names))  # truncate repeated names
    invalid_names = None
    valid_names = None
    is_invalid = False

    if unique_names:
        invalid_names = [name for name in unique_names if name not in name_dict]  # collect names not in files
        valid_names = [name for name in unique_names if name in name_dict]  # collect names in files

    if invalid_names:
        name_text.delete("1.0", tkinter.END)
        if len(invalid_names) == 1:
            out = invalid_names[0] + " is not a valid name"
        else:
            out = ", ".join(invalid_names) + " are not valid names"  # print invalid names in tkinter.text
        name_text.insert("1.0", out)
        is_invalid = True

    name_limit = len(colors)  # maximum lines can be drawn equals the number of colors
    if valid_names:
        if len(valid_names) > name_limit:
            valid_names = valid_names[:name_limit]  # truncate the names exceeding the limit
            if is_invalid:
                name_text.insert(tkinter.END, f"\nExceeding input limit of {name_limit}")
            else:
                name_text.delete("1.0", tkinter.END)
                name_text.insert("1.0", f"Exceeding input limit of {name_limit}")
        else:
            if not is_invalid:
                name_text.delete("1.0", tkinter.END)
        draw_names(canvas, years, max_rank, valid_names, name_dict, colors)  # draw the line graph


def process_search(
        search_entry: tkinter.Entry,
        search_text: tkinter.Text,
        name_dict: dict[str, dict[int, int]]
) -> None:
    """
    handle the condition of the function search_names
    """
    target = ''.join(search_entry.get().split())
    if target:
        target_names = search_names(target, name_dict)
        target_string = ", ".join(target_names)
        search_text.delete("1.0", tkinter.END)
        if target_string:
            search_text.insert("1.0", target_string)
        else:
            search_text.insert("1.0", "There is no corresponding names in data.")


def draw_names(
        canvas: tkinter.Canvas,
        years: list[int],
        max_rank: int,
        valid_names: list[str],
        name_dict: dict[str, dict[int, int]],
        colors: list[str]
) -> None:
    """
    draw the line graph
    """
    canvas.delete("all")
    create_fixed_lines(canvas, years, max_rank)
    curr_color_idx = 0
    curr_box_x = get_curr_x(years, len(years) - 1)
    curr_box_y = CANVAS_MARGIN + 10

    for name in valid_names:
        coords = []
        curr_color = colors[curr_color_idx]
        for index, year in enumerate(years):
            if year in name_dict[name]:
                rank = name_dict[name][year]
                curr_x = get_curr_x(years, index)
                scaler = (CANVAS_HEIGHT-CANVAS_MARGIN*2)/max_rank
                curr_y = CANVAS_MARGIN + rank*scaler
                coords.append(curr_x)
                coords.append(curr_y)
            else:
                curr_x = get_curr_x(years, index)
                curr_y = CANVAS_HEIGHT - CANVAS_MARGIN
                coords.append(curr_x)
                coords.append(curr_y)

        canvas.create_text(
            curr_box_x + TEXT_SPACE,
            curr_box_y,
            text=name,
            anchor='w'
        )  # create label
        canvas.create_line(
            curr_box_x + 75,
            curr_box_y,
            curr_box_x + 100,
            curr_box_y,
            width=LINE_WIDTH,
            fill=curr_color
        )  # create label

        curr_box_y += 20
        canvas.create_line(coords, width=LINE_WIDTH, fill=curr_color)  # connect dots with a line
        curr_color_idx = (curr_color_idx+1) % len(colors)  # change to a different color


def search_names(target: str, name_dict: dict[str, dict[int, int]]) -> list[str]:
    """
    search the names corresponding to targets
    """
    target_names = []
    for name in name_dict:
        if target.lower() in name.lower():
            target_names.append(name)
    return target_names


def get_curr_x(years: list[int], index: int) -> float:
    """
    get an x coordinate for a specified horizontal line
    """
    space_length = (CANVAS_WIDTH - 2*CANVAS_MARGIN) / len(years)
    curr_x = CANVAS_MARGIN + space_length*index
    return curr_x
