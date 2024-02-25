let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    pkgs.nodePackages.pyright
    pkgs.python3Packages.pandas
  ];
}

