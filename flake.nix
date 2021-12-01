{
  description = "A very basic flake";

  inputs = {
     nixpkgs.url = "github:costrouc/nixpkgs/python-terraformpy";
  };

  outputs = { self, nixpkgs }:
      let
        pkgs = nixpkgs.legacyPackages.x86_64-linux;
      in {
       devShell.x86_64-linux = pkgs.mkShell {
         buildInputs = [
           pkgs.python3Packages.terraformpy
           pkgs.python3Packages.pydantic
         ];
       };
  };
}
