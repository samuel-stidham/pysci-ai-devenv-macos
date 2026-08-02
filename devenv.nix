{ pkgs, lib, config, ... }:

let
  # ── PYTHON VERSION ─────────────────────────────────────────────────
  # Single source of truth. Change this one line to "3.14" to test
  # forward compatibility, then re-enter the shell. nixpkgs-python (wired
  # up in devenv.yaml) resolves the exact CPython build, so both "3.13"
  # and "3.14" work with no other edits. The venv is rebuilt whenever the
  # interpreter changes, so switching versions reinstalls cleanly.
  pythonVersion = "3.13";

  # ── NATIVE LIBRARIES ───────────────────────────────────────────────
  # pip-built extensions link against these when a wheel builds from
  # source. On macOS arm64 nearly every package in requirements.txt ships
  # a prebuilt wheel with its dylibs bundled, so this list is for the
  # occasional source build, and no runtime library path is needed
  # (DYLD_* variables would fight SIP and the bundled-dylib wheels).
  #
  # GPU: torch's MPS (Metal) backend ships inside the default PyPI wheel
  # and needs no system packages and no environment at all.
  nativeLibs = with pkgs; [
    zlib
    hdf5                                 # h5py
    netcdf                               # netcdf4
    geos                                 # shapely
    gmp mpfr libmpc                      # gmpy2
    SDL2 SDL2_image SDL2_mixer SDL2_ttf  # pygame, kivy
    libjpeg libpng libtiff freetype      # pillow
    openblas                             # numpy, scipy BLAS/LAPACK backend
  ];
in
{
  # Build toolchain plus the two Python project managers. uv and poetry
  # live here, NOT in requirements.txt, on purpose. This devenv shell is
  # the fat base environment holding every scientific and AI library. An
  # individual project created inside it uses uv or poetry with a portable
  # lockfile, so the project reproduces with `uv sync` or `poetry install`
  # on a machine that has no Nix at all. That portability is the point:
  # Nix is not available everywhere, the project's own lockfile is.
  #
  # No gcc here: macOS source builds use the clang toolchain the Nix
  # stdenv already provides.
  packages = with pkgs; [
    gnumake
    cmake
    pkg-config
    ffmpeg
    uv

    # poetry comes from source on the current unstable pin (no cached
    # aarch64-darwin binary), and its nixpkgs build runs poetry's full
    # test suite, where three installer tests fail. The failures live in
    # poetry's own tests and say nothing about the tool working, so skip
    # the check phase rather than pinning nixpkgs back.
    (poetry.overridePythonAttrs (old: { doCheck = false; }))

    # JVM for the kotlin-jupyter-kernel in requirements.txt. That kernel
    # is a pip package that shells out to `java`, and this shell claims to
    # be self-contained: without this line the kernel would die at run
    # time on any machine with no stray JVM on PATH. 21 to match the JDK
    # the Linux box standardizes on, so notebooks agree across machines.
    temurin-bin-21
  ] ++ nativeLibs;

  languages.python = {
    enable = true;
    version = pythonVersion;

    # manylinux is a Linux-only wheel compatibility concept. Explicitly
    # off so the intent is visible when diffing against the Linux config.
    manylinux.enable = false;

    # The base environment. devenv creates the venv under $DEVENV_STATE,
    # activates it on shell entry, and runs pip against requirements.txt.
    # It tracks a checksum of the file and the interpreter, so pip only
    # reruns when one of them actually changes.
    venv = {
      enable = true;
      requirements = ./requirements.txt;
    };
  };

  enterShell = ''
    echo "── pysci-ai devenv ──────────────────────────────────────────"
    python --version
    echo "venv:   ''${VIRTUAL_ENV:-<none>}"
    echo "python: $(command -v python)"
    echo "GPU:    $(sysctl -n machdep.cpu.brand_string), torch MPS backend"
    echo "─────────────────────────────────────────────────────────────"
  '';
}
