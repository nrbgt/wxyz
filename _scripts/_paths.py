""" paths, versions and other metadata for wxyz
"""
import json
import os
import platform
import re
import site
import sys
from pathlib import Path

RUNNING_IN_CI = bool(json.loads(os.environ.get("RUNNING_IN_CI", "false")))
RUNNING_IN_BINDER = bool(json.loads(os.environ.get("RUNNING_IN_BINDER", "false")))

PY = Path(sys.executable)
OS = platform.system()
PY_VER = "".join(map(str, sys.version_info[:2]))

SCRIPTS = Path(__file__).parent
ROOT = SCRIPTS.parent

BUILD = ROOT / "build"
OK = BUILD / "ok"

SRC = ROOT / "src"
PY_SRC = SRC / "py"
TS_SRC = SRC / "ts"
DODO = ROOT / "dodo.py"
ALL_SRC_PY = sorted([*PY_SRC.rglob("*.py")])
ALL_PY = sorted([DODO, *SCRIPTS.glob("*.py"), *ALL_SRC_PY])


DIST = ROOT / "dist"
IPYNB_HTML = DIST / "notebooks"

TEST_OUT = DIST / "test_output"
ROBOT_OUT = TEST_OUT / "robot"
LAB = ROOT / "lab"

ATEST = ROOT / "atest"
ATEST_OUT = ATEST / "output"

CI = ROOT / "ci"

PY_SETUP = [*PY_SRC.glob("*/setup.py")]
PY_VERSION = {
    pys: re.findall(
        r"""__version__ = ["](.*)["]""",
        next((pys.parent / "src" / "wxyz").rglob("_version.py")).read_text(),
    )[0]
    for pys in PY_SETUP
}
SITE_PKGS = Path(site.getsitepackages()[0])

YARN_LOCK = ROOT / "yarn.lock"
YARN_INTEGRITY = ROOT / "node_modules" / ".yarn-integrity"
ROOT_PACKAGE = ROOT / "package.json"
TS_PACKAGE = [*TS_SRC.glob("*/package.json")]
THIRD_PARTY_EXTENSIONS = ["bqplot@0.5.6", "@jupyter-widgets/jupyterlab-manager@2.0.0"]
WXYZ_LAB_EXTENSIONS = [
    tsp.parent for tsp in TS_PACKAGE if "wxyz-meta" not in tsp.parent.name
]
ALL_LABEXTENSIONS = [*THIRD_PARTY_EXTENSIONS, *WXYZ_LAB_EXTENSIONS]
ALL_TS = sum(
    [
        [*(tsp.parent / "src").rglob("*.ts"), *(tsp.parent / "style").rglob("*")]
        for tsp in TS_PACKAGE
    ],
    [],
)
TS_PACKAGE_CONTENT = {tsp: json.loads(tsp.read_text()) for tsp in TS_PACKAGE}
TS_TARBALLS = [
    tsp.parent / f"""deathbeds-{tsp.parent.name}-{tsp_json["version"]}.tgz"""
    for tsp, tsp_json in TS_PACKAGE_CONTENT.items()
]


CONDA_ORDER = ["core", "html", "lab", "datagrid", "svg", "tpl-jjinja", "yaml"]

CONDA_BUILD_ARGS = [
    "conda-build",
    "-c",
    "conda-forge",
    "--output-folder",
    DIST / "conda-bld",
]

WHEELS = [
    DIST / "bdist_wheel" / f"{pys.parent.name}-{version}-py3-none-any.whl"
    for pys, version in PY_VERSION.items()
]

IPYNB = PY_SRC / "wxyz_notebooks" / "src" / "wxyz" / "notebooks"
DESIGN_IPYNB = IPYNB / "Design"

# this is duplicated in wxyz.notebook.tests
ALL_IPYNB = sorted(
    [
        ipynb
        for ipynb in IPYNB.rglob("*.ipynb")
        if ".ipynb_checkpoints" not in str(ipynb)
        and str(DESIGN_IPYNB) not in str(ipynb)
    ]
)

ALL_PRETTIER = sorted(
    [
        *CI.glob("*.yml"),
        *PY_SRC.rglob("*.md"),
        *ROOT.glob("*.json"),
        *ROOT.glob("*.md"),
        *ROOT.glob("*.yml"),
        *TS_SRC.rglob("*.css"),
        *TS_SRC.rglob("*.json"),
        *TS_SRC.rglob("*.md"),
        *TS_SRC.rglob("*.ts"),
        *TS_SRC.rglob("*.yml"),
    ]
)

ALL_ROBOT = [*ATEST.rglob("*.robot")]
