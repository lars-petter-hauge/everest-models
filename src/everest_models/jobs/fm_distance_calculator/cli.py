from pathlib import Path

from everest_models.jobs.shared.resinsight import ResInsight

from .parser import build_argument_parser
from .tasks import run


def main_entry_point(args=None) -> int:
    parser = build_argument_parser()
    options = parser.parse_args(args)

    if options.lint:
        parser.exit()

    if options.egrid is None and options.case_name is None:
        parser.error("Provide --case_name or --egrid")
    egrid_path = (
        options.egrid
        if options.egrid is not None
        else Path(f"{options.case_name}.EGRID")
    ).resolve()
    if not egrid_path.is_file():
        parser.error(f"EGRID not found: {egrid_path}")

    with ResInsight(options.resinsight) as instance:
        case = instance.project.load_case(str(egrid_path))
        if case is None:
            raise RuntimeError(f"ResInsight could not load case: {egrid_path}")
        return run(options.config, case)
