import argparse
import hashlib
import os
import platform
import re
import sys
import tarfile
import textwrap
import warnings
import zipfile
from urllib.request import urlretrieve

from packaging.version import parse as parse_version

# BEGIN CHECKSUMS

checksums_traefik = {
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_darwin_arm64.tar.gz': '04a24884738847b0e4099726f43d1f33d02f012b028472bd29f5d7695d2498fd',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_linux_armv6.tar.gz': '07b265cb3c414f3c7b7b4243b650994917745b1d97d0cb977d739fe525220589',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_windows_amd64.zip': '0d8ecb76351942f361eb4e3ce056ed41b8f24909d8954e55a98268aeb12a30b8',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_linux_s390x.tar.gz': '1a344e1daa45830a47506c06ea4ed701cc6fb32f723352d94a9b7c7de2dd8fcd',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_linux_arm64.tar.gz': '2019696d1953b709dffc046f4c74c76b4800ea7b4eac7b80a5907e1cebcbc698',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_freebsd_armv5.tar.gz': '247b98bcb46717b17c25eb42919be48a12290bbb7e3369ece784b3b1d2b9f9ac',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_linux_armv5.tar.gz': '3687144d0ed4309ea53b40392bfd8a12f56e7a81d6347b2beb3f8192ad38ef28',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_linux_armv7.tar.gz': '56d24e76193b64c55e39833f6a673042874f934c57b4a0a55aa4a37d244d20fe',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_darwin_amd64.tar.gz': '5c3ae92616b1ebf37bf470f76f311d253272415711ab2477f21b46388cd7788a',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_linux_amd64.tar.gz': '7820cf981271df558ab260dc2fa3705378e74d71ba87a34cf644b5004756f27f',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_freebsd_armv7.tar.gz': '8ca24e2736b61c07acf687ecdafb38c78b51400dcd2ebefdcb0360dddc9297f4',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_linux_386.tar.gz': '90fd5a2f262b252be468de729b8d99c7b3e632c4f26e061b6c3d2e1310541c8b',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_openbsd_amd64.tar.gz': 'a9414b7bedce0a653c1b720063251e1f99b7a90c707f20ddf3836f3073421bde',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_openbsd_386.tar.gz': 'b29328851e48adda1ffa32ec2b2e4c3152c9969963fe2210f41b2fe29617ab60',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_freebsd_amd64.tar.gz': 'bdcfb75f04726136b9184b4916cffd9b140476d57c1279cb84089c1dad14e5be',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_freebsd_armv6.tar.gz': 'd677ad52458a030958a657fbeff747faa03b91dc2a39a77a069a4f51bce28ea6',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_windows_386.zip': 'ebe6e4beb63f22f51b76f58c6f70d33c80792f08ab85373916d9eca24d28db27',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_linux_ppc64le.tar.gz': 'f0a6a7b2ddd633ddf21fd22aa0913d73eed809d56c627ef2796de8e4975294d2',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_freebsd_386.tar.gz': 'f68fd5b33a944da62c46539060f47e76f958982302d9ed5baf057fcf27d8eb28',
    'https://github.com/traefik/traefik/releases/download/v2.8.8/traefik_v2.8.8_windows_arm64.zip': 'fd5407d0128d830daab8fdb070567674d33ae1f44da79f54bc521668938711b5',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_linux_386.tar.gz': '0b8bebe1f267c5ecfe93e5efe6a8e37d1b4ed1005123580731ac828ab0de1fdd',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_openbsd_amd64.tar.gz': '0edc9e1df8a46a2d1e7587bd8609eb225847b75e5d4f7017c112f4f997260403',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_linux_s390x.tar.gz': '217bfb04d3f4b25c9ac683e500591a41abceaad572795f91fe69d207adfb8e55',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_freebsd_386.tar.gz': '2ccd0fb64ce2165675a28f4b5b52220992ed1216a483106333c421959a66124b',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_linux_arm64.tar.gz': '2e5c8f6b2fb49a4dc89c86fe37b951d947d760f42a9aa11018a36eefd033368c',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_darwin_amd64.tar.gz': '313843d030730117bcbd81230b2c736a83f2e4e276d845b6c9cb87828b3f7e2a',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_linux_armv7.tar.gz': '31e2b385bc511ff4c669d30319b9d38f1d01b6b3661c9126cfd2a8f234066576',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_windows_amd64.zip': '3601d1dad0a26cdd65f9715d4563e4db408bf76ae5633d11e1d0afb08f4cee69',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_windows_386.zip': '3d2856c47d337cd43eeefd9fbaced1dd9cb25db35028717e8d73ca1690b4a288',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_linux_amd64.tar.gz': '3ea5332c28980aaf8b7d0958379a62e77b4259efb2dac4cce733c8eb67b4ebe6',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_windows_arm64.zip': '4d069d00c1b694534a6892dc66d070fa1c092b6a8e06a634f7c67a3d1d6db73c',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_freebsd_amd64.tar.gz': '6d802496eca8466775c430fd7be59f5f492d234853934ed95834e9b763159020',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_openbsd_386.tar.gz': '8edf52c62234107fb751f2e574cd90a658adb33c6ec03970e3350be0cf336f4e',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_darwin_arm64.tar.gz': '960f90f64c25b34797813bdbdbfd86a4b7bc4958b569ec77a1cc3e816e76a920',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_linux_armv6.tar.gz': 'bffe96ff2b7f38379a181a37b4ae97545af7f79d7a5b77db8db2ac451bff09fb',
    'https://github.com/traefik/traefik/releases/download/v2.9.8/traefik_v2.9.8_linux_ppc64le.tar.gz': 'f733e015b2e8b154f42a83a7e39cf17cfe5398ea6ca77410fafd37c15a76aa76',
}

# END CHECKSUMS

machine_map = {
    "x86_64": "amd64",
}


def checksum_file(path):
    """Compute the sha256 checksum of a path"""
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def install_traefik(prefix, plat, traefik_version):
    plat = plat.replace("-", "_")
    if "windows" in plat:
        traefik_archive_extension = "zip"
        traefik_bin = os.path.join(prefix, "traefik.exe")
    else:
        traefik_archive_extension = "tar.gz"
        traefik_bin = os.path.join(prefix, "traefik")

    traefik_archive = (
        "traefik_v" + traefik_version + "_" + plat + "." + traefik_archive_extension
    )
    traefik_archive_path = os.path.join(prefix, traefik_archive)

    traefik_url = (
        "https://github.com/traefik/traefik/releases"
        f"/download/v{traefik_version}/{traefik_archive}"
    )

    if os.path.exists(traefik_bin) and os.path.exists(traefik_archive_path):
        print("Traefik already exists")
        if traefik_url not in checksums_traefik:
            warnings.warn(
                f"Traefik {traefik_version} not tested !",
                stacklevel=2,
            )
            os.chmod(traefik_bin, 0o755)
            print("--- Done ---")
            return
        else:
            if checksum_file(traefik_archive_path) == checksums_traefik[traefik_url]:
                os.chmod(traefik_bin, 0o755)
                print("--- Done ---")
                return
            else:
                print(f"checksum mismatch on {traefik_archive_path}")
                os.remove(traefik_archive_path)
                os.remove(traefik_bin)

    print(f"Downloading traefik {traefik_version} from {traefik_url}...")
    urlretrieve(traefik_url, traefik_archive_path)

    if traefik_url in checksums_traefik:
        if checksum_file(traefik_archive_path) != checksums_traefik[traefik_url]:
            raise OSError("Checksum failed")
    else:
        warnings.warn(
            f"Traefik {traefik_version} not tested !",
            stacklevel=2,
        )

    print("Extracting the archive...")
    if traefik_archive_extension == "tar.gz":
        with tarfile.open(traefik_archive_path, "r") as tar_ref:
            tar_ref.extract("traefik", prefix)
    else:
        with zipfile.ZipFile(traefik_archive_path, "r") as zip_ref:
            zip_ref.extract("traefik.exe", prefix)
    os.chmod(traefik_bin, 0o755)
    print(f"Installed {traefik_bin}")
    os.unlink(traefik_archive_path)
    print("--- Done ---")


def main():
    # extract supported and default versions from urls
    _version_pat = re.compile(r"v\d+\.\d+\.\d+")
    _versions = set()
    for url in checksums_traefik:
        _versions.update(_version_pat.findall(url))
    available_versions = sorted(_versions, key=parse_version, reverse=True)

    parser = argparse.ArgumentParser(
        description="Dependencies intaller",
        epilog=textwrap.dedent(
            f"""\
            Checksums available for traefik versions: {', '.join(available_versions)}
            """
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--output",
        dest="installation_dir",
        default="./dependencies",
        help=textwrap.dedent(
            """\
            The installation directory (absolute or relative path).
            If it doesn't exist, it will be created.
            If no directory is provided, it defaults to:
            --- %(default)s ---
            """
        ),
    )

    machine = platform.machine()
    machine = machine_map.get(machine, machine)
    default_platform = f"{sys.platform}-{machine}"

    parser.add_argument(
        "--platform",
        dest="plat",
        default=default_platform,
        help=textwrap.dedent(
            """\
            The platform to download for.
            If no platform is provided, it defaults to:
            --- %(default)s ---
            """
        ),
    )

    parser.add_argument(
        "--traefik",
        action="store_true",
        help="DEPRECATED, IGNORED",
    )

    parser.add_argument(
        "--traefik-version",
        dest="traefik_version",
        default="2.9.8",
        help=textwrap.dedent(
            """\
            The version of traefik to download.
            If no version is provided, it defaults to:
            --- %(default)s ---
            """
        ),
    )
    if "--etcd" in sys.argv:
        sys.exit(
            "Installing etcd is no longer supported. Visit https://github.com/etcd-io/etcd/releases/"
        )
    if "--consul" in sys.argv:
        sys.exit(
            "Installing consul is no longer supported. Visit https://developer.hashicorp.com/consul/downloads"
        )

    args = parser.parse_args()
    deps_dir = args.installation_dir
    plat = args.plat
    traefik_version = args.traefik_version.lstrip("v")

    if args.traefik:
        print(
            "Specifying --traefik is deprecated and ignored. Only installing traefik is supported.",
            file=sys.stderr,
        )

    if os.path.exists(deps_dir):
        print(f"Using existing output directory {deps_dir}...")
    else:
        print(f"Creating output directory {deps_dir}...")
        os.makedirs(deps_dir)

    install_traefik(deps_dir, plat, traefik_version)


if __name__ == "__main__":
    main()
