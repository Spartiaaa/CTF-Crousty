import struct


def create_polyglot_corrupted(jpg_path, zip_path, output_path):
    # 1. Lecture des composants
    with open(jpg_path, "rb") as f:
        jpg_data = f.read()
    with open(zip_path, "rb") as f:
        zip_data = f.read()

    if len(zip_data) > 65533:
        raise ValueError("Archive ZIP trop volumineuse pour un segment COM (64KB max).")

    # 2. Construction du segment COM (FF FE) - JPEG est en Big Endian ('>')
    marker = b"\xff\xfe"
    size = struct.pack(">H", len(zip_data) + 2)

    # 3. Assemblage du Polyglotte (SOI + COM + ZIP + Reste du JPEG)
    polyglot = bytearray(jpg_data[:2] + marker + size + zip_data + jpg_data[2:])

    print(f"[*] Fichier polyglotte assemblé : {output_path}")

    # 4. Phase de Sabotage (Niveau Insane)
    # On cherche la signature du Central Directory Header (50 4B 01 02)
    cd_signature = b"\x50\x4b\x01\x02"
    cd_offset = polyglot.find(cd_signature)

    if cd_offset != -1:
        print(f"[*] Central Directory trouvé à l'offset : {hex(cd_offset)}")

        # Sabotage 1 : Corruption de la signature (PK\x01\x02 -> PK\x00\x00)
        # Cela rend l'archive illisible pour les extracteurs standards
        polyglot[cd_offset + 2 : cd_offset + 4] = b"\x00\x00"

        # Sabotage 2 : "Version needed to extract" (Offset +6 dans le CD)
        # On injecte une version absurde (0xFFFF) en Little Endian ('<')
        # On utilise struct pour illustrer la manipulation binaire propre
        version_insane = struct.pack("<H", 0xFFFF)
        polyglot[cd_offset + 6 : cd_offset + 8] = version_insane

        print("[!] Sabotage des headers ZIP effectué avec succès.")
    else:
        print("[?] Alerte : Central Directory non détecté. Vérifiez l'archive source.")

    # 5. Écriture du fichier final
    with open(output_path, "wb") as f:
        f.write(polyglot)

    print(f"[+] Challenge généré : {output_path}")


if __name__ == "__main__":
    # Assurez-vous que tasty.jpeg et tasty_secret.zip sont dans le répertoire
    try:
        create_polyglot_corrupted(
            "tasty_template.jpeg", "tasty_secret.zip", "crousty_chall.jpg"
        )
    except FileNotFoundError:
        print("[!] Erreur : Fichiers sources introuvables.")
