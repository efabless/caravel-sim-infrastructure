{
  buildPythonPackage,
  fetchPypi,
  setuptools,
  setuptools-scm,
  cocotb,
  python-constraint,
  pyyaml,
  version ? "1.2.0",
  sha256 ? "sha256-CsCvWb6XrKSOuFKBdEKxXWQvDrSQX7qPvZ7j2mpANlw=",
}: let
  self = buildPythonPackage {
    pname = "cocotb-coverage";
    inherit version;

    src = fetchPypi {
      inherit (self) pname version;
      inherit sha256;
    };

    build-system = [
      setuptools
      setuptools-scm
    ];

    dependencies = [
      cocotb
      python-constraint
      pyyaml
    ];
  };
in
  self
