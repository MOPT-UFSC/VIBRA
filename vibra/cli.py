def run_interface(project_path: str | None = None, open_last: bool = False):
    from vibra import launch

    if open_last:
        print('Sorry, "--last" does not work yet =(')

    launch.main()

def run_analysis(working_dir: str, print_log: bool):
    from vibra.utils.subprocess import analysis_subprocess

    try:
        analysis_subprocess.main(is_resume=False, working_dir=working_dir, print_log=print_log)
    except Exception:
        import sys
        import traceback
        import json

        text = traceback.format_exc()
        print(
            "VIBRA_EXCEPTION|" + json.dumps({"traceback": text}),
            flush=True,
        )
        sys.exit(1)

def continue_analysis(working_dir: str, print_log: bool):
    from vibra.utils.subprocess import analysis_subprocess

    try:
        analysis_subprocess.main(is_resume=True, working_dir=working_dir, print_log=print_log)
    except Exception:
        import sys
        import traceback
        import json

        text = traceback.format_exc()
        print(
            "VIBRA_EXCEPTION|" + json.dumps({"traceback": text}),
            flush=True,
        )
        sys.exit(1)

def generate_mesh(working_dir: str):
    from vibra.utils.subprocess import generate_mesh_subprocess

    try:
        generate_mesh_subprocess.main(working_dir)
    except Exception:
        import sys
        import traceback
        import json

        text = traceback.format_exc()
        print(
            "VIBRA_EXCEPTION|" + json.dumps({"traceback": text}),
            flush=True,
        )
        sys.exit(1)


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Vibra command line interface")
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Path to a .vibra project file to open in the interface.",
    )
    parser.add_argument("--last", action="store_true", help="Open the last opened project in the interface.")
    parser.add_argument(
        "--run-analysis",
        metavar="WORKING_DIR",
        help="Run the analysis in WORKING_DIR without opening the interface.",
    )
    parser.add_argument(
        "--continue-analysis",
        metavar="WORKING_DIR",
        help="Continue the analysis in WORKING_DIR without opening the interface.",
    )
    parser.add_argument(
        "--generate-mesh",
        metavar="WORKING_DIR",
        help="Generate the mesh in WORKING_DIR without opening the interface.",
    )
    parser.add_argument(
        "--print_log",
        action="store_true",
        help="Print logs in terminal.",
    )

    args = parser.parse_args()

    if args.run_analysis is not None:
        run_analysis(args.run_analysis, print_log=args.print_log)
    elif args.continue_analysis is not None:
        continue_analysis(args.continue_analysis, print_log=args.print_log)
    elif args.generate_mesh is not None:
        generate_mesh(args.generate_mesh)
    else:
        run_interface(args.path, open_last=args.last)


if __name__ == "__main__":
    main()
