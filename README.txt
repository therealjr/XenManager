# XenManager

***Edit /etc/nixos/configuration.nix:***

environment.systemPackages = with pkgs; [
  python3
  pyqt6
  xorg.libxcb
  xorg.libxkbcommon
  xorg.xcbutil
  xorg.xcbutilimage
  xorg.xcbutilwm
  xorg.xcbutilkeysyms
];

***Apply the changes:***

sudo nixos-rebuild switch
