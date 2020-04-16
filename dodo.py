from pathlib import Path
import sys
import site


DODO = Path(__file__)
ROOT = DODO.parent
CI = ROOT / "ci"
SRC = ROOT / "src"
TS = SRC / "ts"
PY = SRC / "py"
PY_SETUP = [*PY.glob("*/setup.py")]
SITE_PKGS = Path(site.getsitepackages()[0])


DOIT_CONFIG = {
    'backend': 'sqlite3',
}


def task_setup():
    yield dict(
        basename="js_setup",
        doc="☕ setup",
        file_dep=[ROOT / "yarn.lock"],
        targets=[ROOT / "node_modules" / ".yarn-integrity"],
        actions=[["jlpm", "--prefer-offline"], ["jlpm", "lerna", "bootstrap"]]
    )

    for setup_py in PY_SETUP:
        pkg = setup_py.parent

        yield dict(
            basename=f"py_setup_{pkg.name}",
            doc=f"🐍 setup {pkg.name}",
            file_dep=[setup_py, pkg / "setup.cfg"],
            targets=[SITE_PKGS / f"{pkg.name}.egg-link".replace("_", "-")],
            actions=[
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-e",
                    str(pkg),
                    "--ignore-installed",
                    "--no-deps",
                ]
            ]
        )


def task_lint():
    yield dict(
        basename="prettier",
        doc="prettier",
        file_dep=[
            *ROOT.glob("*.yml"),
            *ROOT.glob("*.json"),
            *TS.rglob("*.ts"),
            *TS.rglob("*.css"),
            *TS.rglob("*.json"),
            *CI.rglob("*.yml")
        ],
        actions=[["jlpm", "lint"]]
    )
