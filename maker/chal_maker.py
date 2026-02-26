import struct


def create_blackout_phantom(jpg_path, zip_path, output_path):
    with open(jpg_path, "rb") as f:
        jpg_data = f.read()
    with open(zip_path, "rb") as f:
        zip_data = f.read()

    # Insertion dans le JPEG
    marker = b"\xff\xfe"
    size = struct.pack(">H", len(zip_data) + 2)
    polyglot = bytearray(jpg_data[:2] + marker + size + zip_data + jpg_data[2:])

    # Liste des signatures à saboter (toutes font 4 octets)
    # 1. Local Header, 2. Central Directory, 3. End of Central Directory
    signatures = [b"\x50\x4b\x03\x04", b"\x50\x4b\x01\x02", b"\x50\x4b\x05\x06"]
    new_sig = b"CHEF"

    count = 0
    for sig in signatures:
        while sig in polyglot:
            idx = polyglot.find(sig)
            polyglot[idx : idx + 4] = new_sig
            count += 1

    with open(output_path, "wb") as f:
        f.write(polyglot)

    print(f"[+] Signatures sabotées : {count}")
    print(f"[!] Challenge généré : {output_path}")


if __name__ == "__main__":
    create_blackout_phantom("tasty_base.jpeg", "tasty_secret.zip", "crousty_chall.jpg")
