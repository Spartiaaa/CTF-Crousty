
L'agent infiltré **"Mr. crous"** a réussi à intercepter une image provenant du serveur privé d'un célèbre chef cuisinier soupçonné d'espionnage industriel.

Nos analystes de premier niveau ont simplement conclu : _"C'est une belle  de tasty crousty, mais elle ne contient rien d'intéressant. `strings` ne renvoie que du bruit."_

Pourtant, la taille du fichier est suspecte pour une simple image de cette résolution, et une note manuscrite sur le bureau du chef disait :

> _"La vérité est encapsulée dans les commentaires. Si tu ne vois pas le secret, c'est que tu ne regardes pas avec les bons yeux."_

**Votre mission :** 1. Analysez la structure profonde du fichier `challenge_hard.jpg`. 2. Identifiez la double nature de ce spécimen. 3. Extrayez le flag dissimulé par le Chef.

---

## Hints

1. **Niveau 1 :** Les apparences sont trompeuses. Un fichier peut être deux choses à la fois sans que l'une ne corrompe l'autre.
    
2. **Niveau 2 :** Regardez de très près le début du fichier (les premiers octets). `FF D8` est là, mais que vient faire ce `PK` si tôt ?
    
3. **Niveau 3 :** Le standard JPEG autorise des segments de "commentaires" (`COM`). Et si ce commentaire était plus grand qu'un simple texte ?