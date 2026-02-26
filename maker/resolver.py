import os


def precise_recovery(input_file):
    with open(input_file, "rb") as f:
        data = f.read()

    # On commence par restaurer le fichier en mémoire
    # 1. On identifie les blocs 'CHEF'
    chunks = data.split(b"CHEF")

    # On va reconstruire le fichier en remettant les VRAIES signatures ZIP
    # Le ZIP suit toujours cet ordre :
    # [Local Headers...] puis [Central Directory...] puis [End of Central Directory]

    # Stratégie : On remplace les CHEF par les signatures standards dans l'ordre
    # On sait qu'il y a au moins 1 Local Header (03 04) et 1 End of CD (05 06)

    # On fait un remplacement intelligent :
    # - Le premier CHEF est forcément un Local Header (50 4B 03 04)
    # - Le dernier CHEF est forcément la Fin d'Archive (50 4B 05 06)
    # - Les CHEF au milieu sont soit d'autres fichiers, soit l'index (50 4B 01 02)

    # Pour simplifier et forcer l'extraction :
    # On remplace TOUT par PK\x03\x04 SAUF le dernier qui est PK\x05\x06

    print("[*] Restauration chirurgicale des headers...")

    # On répare d'abord tout en 'Local Header'
    repaired = data.replace(b"CHEF", b"\x50\x4b\x03\x04")

    # On répare la TOUTE DERNIÈRE signature (le footer) pour que l'archive soit valide
    last_sig_idx = repaired.rfind(b"\x50\x4b\x03\x04")
    if last_sig_idx != -1:
        repaired = (
            repaired[:last_sig_idx] + b"\x50\x4b\x05\x06" + repaired[last_sig_idx + 4 :]
        )

    with open("repaired_final.zip", "wb") as f:
        f.write(repaired)

    print("[+] Fichier 'repaired_final.zip' généré.")
    print("[*] Tentative d'extraction avec '7z x'...")

    # On utilise 'x' pour extraire avec les chemins complets
    os.system("7z x repaired_final.zip -y")


if __name__ == "__main__":
    precise_recovery("challenge_phantom.jpg")
