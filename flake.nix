{
  description = "A very basic flake";

  inputs = {
     nixpkgs.url = "github:costrouc/nixpkgs/python-terraformpy";
  };

  outputs = { self, nixpkgs }:
      let
        pkgs = nixpkgs.legacyPackages.x86_64-linux;

        pythonPackages = pkgs.python3Packages;
      in {
       devShell.x86_64-linux = pkgs.mkShell {
         buildInputs = [
           pythonPackages.terraformpy
           pythonPackages.pydantic
           # development
           pythonPackages.pytest
         ];
       };
  };
}
