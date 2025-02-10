# XenManager

***Edit /etc/nixos/configuration.nix:***

environment.systemPackages = with pkgs; [
  python3
  (python3.withPackages (ps: with ps; [ pip ]))
  (python3.withPackages (ps: with ps; [ pyqt6 ]))
  xorg.libxcb
  libxkbcommon
  xorg.xcbutil
  xorg.xcbutilimage
  xorg.xcbutilwm
  xorg.xcbutilkeysyms
];

***Apply the changes:***

sudo nixos-rebuild switch
