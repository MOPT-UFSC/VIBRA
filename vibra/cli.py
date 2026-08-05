def run_interface(project_path: str | None = None, open_last: bool = False):
    from vibra import launch

    if open_last:
        print('Sorry, "--last" does not work yet =(')

    launch.main()


def run_analysis(working_dir: str):
    from vibra.cli_runners import analysis_subprocess

    try:
        analysis_subprocess.main(is_resume=False, working_dir=working_dir)
    except Exception:
        print("Working dir does not propperly configure an analysis.")


def continue_analysis(working_dir: str):
    from vibra.cli_runners import analysis_subprocess

    try:
        analysis_subprocess.main(is_resume=True, working_dir=working_dir)
    except Exception:
        print("Working dir does not propperly configure an analysis.")


def generate_mesh(working_dir: str):
    from vibra.cli_runners import generate_mesh_subprocess

    try:
        generate_mesh_subprocess.main(working_dir)
    except Exception:
        print("Working dir does not propperly configure an analysis.")


def preview(script_path: str):
    from vibra.cli_runners import dynamic_preview

    try:
        dynamic_preview.main(script_path)
    except Exception:
        print("Working dir does not propperly configure an analysis.")


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
        "--preview",
        metavar="SCRIPT_PATH",
        help="Creates a renderer to preview the script running.",
    )

    args = parser.parse_args()

    if args.run_analysis is not None:
        run_analysis(args.run_analysis)

    elif args.continue_analysis is not None:
        continue_analysis(args.continue_analysis)

    elif args.generate_mesh is not None:
        generate_mesh(args.generate_mesh)

    elif args.preview is not None:
        preview(args.preview)

    else:
        run_interface(args.path, open_last=args.last)


if __name__ == "__main__":
    main()
