import argparse
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from src import simulation
from src import constants


parser = argparse.ArgumentParser()
parser.add_argument(
    "-w",
    "--window-size",
    metavar=("<width>", "<height>"),
    nargs=2,
    type=int,
    help="Specify the window width and height in pixels.",
    default=constants.DEEFAULT_WINDOW_SIZE
)
parser.add_argument(
    "-c",
    "--cell-width",
    metavar="<width>",
    type=int,
    help="Specify the cell width in pixels.",
    default=constants.DEFAULT_CELL_WIDTH
)
args = parser.parse_args()

simulation.Wireworld(args.window_size, args.cell_width).run()
