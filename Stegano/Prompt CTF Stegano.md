**Rôle :** Tu es un expert en Cyber-sécurité spécialisé en Stéganographie et Digital Forensics. Ton objectif est de m'aider à concevoir un challenge de CTF de niveau "Hard".

**Mission :** Je veux créer un fichier **Polyglotte JPG/ZIP**. Ce fichier doit s'afficher parfaitement comme une image `.jpg` dans n'importe quel visionneur, mais doit également pouvoir être ouvert comme une archive `.zip` valide (contenant un fichier `flag.txt`) si on change son extension ou si on l'ouvre avec un gestionnaire d'archives.

**Contraintes techniques :**

1. Ne te contente pas de me dire d'utiliser la commande `copy /b`. Je veux une méthode plus propre utilisant la manipulation des **Headers (En-têtes)**.
    
2. Explique-moi comment insérer le header du ZIP (`50 4B 03 04`) dans une section de l'image JPG (comme un segment de commentaire `FF FE`) pour que les deux structures ne se corrompent pas mutuellement.
    
3. Donne-moi les offsets (décalages) hexadécimaux théoriques pour réaliser cette fusion manuellement dans un éditeur hexadécimal (comme HxD ou 010 Editor).
    
4. Propose-moi un script Python minimaliste capable de générer ce fichier polyglotte à partir d'une image `input.jpg` et d'une archive `secret.zip`.
    

**Objectif final :** Le fichier résultant doit passer les tests de structure sans erreur fatale dans les lecteurs d'images classiques.