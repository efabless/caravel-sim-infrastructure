{
  lib,
  buildPythonPackage,
  poetry-core,
  anytree,
  click,
  cocotb,
  cocotb-coverage,
  oyaml,
  prettytable,
  pyyaml,
  rich,
  ruamel-yaml,
  volare,
  tabulate,
}: let
  pyproject_toml = builtins.fromTOML (builtins.readFile ./cocotb/pyproject.toml);
in
  buildPythonPackage
  {
    name = "caravel_cocotb";
    version = pyproject_toml.tool.poetry.version;
    format = "pyproject";

    src = ./cocotb;

    nativeBuildInputs = [
      poetry-core
    ];

    propagatedBuildInputs = [
      anytree
      click
      cocotb
      cocotb-coverage
      oyaml
      prettytable
      pyyaml
      rich
      ruamel-yaml
      volare
      tabulate
    ];

    meta = {
      description = pyproject_toml.tool.poetry.description;
      homepage = "https://github.com/efabless/caravel-sim-infrastructure";
      license = lib.licenses.asl20;
      platforms = ["x86_64-linux"];
    };
  }
