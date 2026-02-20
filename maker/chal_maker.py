import struct


def create_polyglot(jpg_path, zip_path, output_path):
    with open(jpg_path, "rb") as f:
        jpg_data = f.read()

    with open(zip_path, "rb") as f:
        zip_data = f.read()

    if len(zip_data) > 65533:
        raise ValueError(
            "Le fichier ZIP est trop gros pour un segment JPEG COM (max 64KB)."
        )

    # Construction du segment Commentaire (FF FE)
    marker = b"\xff\xfe"
    size = struct.pack(">H", len(zip_data) + 2)

    # Injection du ZIP juste après le header SOI (FF D8)
    polyglot = jpg_data[:2] + marker + size + zip_data + jpg_data[2:]

    with open(output_path, "wb") as f:
        f.write(polyglot)

    # On calcule l'offset AVANT de l'afficher pour éviter l'erreur de syntaxe
    zip_offset = polyglot.find(b"\x50\x4b\x03\x04")

    print(f"[*] Fichier polyglotte généré : {output_path}")
    if zip_offset != -1:
        print(f"[*] Signature ZIP trouvée à l'offset : {hex(zip_offset)}")
    else:
        print("[!] Attention : Signature ZIP non trouvée dans le fichier final.")


if __name__ == "__main__":
    # Vérifie bien que ces fichiers existent dans ton dossier "CTF Box - Stegano"
    create_polyglot("tasty.jpeg", "tasty_secret.zip", "challenge_hard.jpg")
