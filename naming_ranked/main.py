"""
main file
"""

from crawl_names import crawl, DATA_DIR
from ranking_graphics_gui import run_gui

START_YEAR = 1900
END_YEAR = 2010
COLORS = ["red", "purple", "green", "blue", "yellow", "pink"]
RANK = 200


def main():
    years = []
    for year in range(START_YEAR, END_YEAR + 1, 10):
        years.append(year)
    crawl(years)
    run_gui(years, RANK, DATA_DIR, COLORS)


if __name__ == "__main__":
    main()
