"""
"""


def main():
    args = _init_argparse()

    return


def _init_argparse():
    import argparse
    parser = argparse.ArgumentParser()

    # parser.add_argument("-e", "--evolve",
    #                     action="store_true", dest="evolve", default=False,
    #                     help="Evolve the binaries over time.")
    # parser.add_argument("-a", "--analyze",
    #                     action="store_true", dest="analyze", default=False,
    #                     help="Analyze the binaries after evolution.")
    # parser.add_argument("-p",
    #                     action="store_true", dest="plot", default=False,
    #                     help="Plot (default) results of analysis and evolution.")
    # parser.add_argument("--plot",
    #                     type=int, nargs='*', dest="plot", default=False,
    #                     help="Plot results of analysis and evolution.")
    # parser.add_argument("-i", "--in",
    #                     type=str, dest="input", default=None,
    #                     help="Input directory (look for `evolution` and `settings` objects)")
    # parser.add_argument("-o", "--out",
    #                     type=str, dest="output", default=None,
    #                     help="Output directory")
    # parser.add_argument("--sets",
    #                     type=str, dest="sets", default=None,
    #                     help="Name for configuration file from which to take settings.")
    # parser.add_argument("--name",
    #                     type=str, dest="name", default=None,
    #                     help="Name of this simulation run, for output directory etc.")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
