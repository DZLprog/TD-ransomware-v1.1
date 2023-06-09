### R1 :
Le nom de l'algorithme de chiffrement est AES, qui est un algorithme de chiffrement symétrique. Il est considéré comme robuste en raison de l'utilisation de clés de chiffrement plus longues, telles que 128, 192 et 256 bits, ce qui le rend plus résistant aux tentatives de piratage.

### R2 :
Il n'est pas recommandé de hacher directement le sel et la clef, car ce sont des données sensibles qui pourraient être perdues. De plus, un bon hashage de mot de passe doit être lent à calculer et difficile à inverser, ce qui peut ne pas être le cas avec un HMAC (code d'authentification de message basé sur une clé). Un bon hashage de mot de passe doit également inclure un sel, qui est une chaîne aléatoire ajoutée au mot de passe avant le hachage, pour renforcer sa robustesse contre les attaques. Contrairement au HMAC, lequel n'utilise pas de sel, le hashage de mot de passe avec un sel rend le processus de hachage plus sécurisé.

### R3 :
Il est conseillé de vérifier si un fichier token.bin existe déjà avant de créer un nouveau fichier en utilisant la méthode 'open("file",wb)'. Cette méthode peut créer un nouveau fichier s'il n'existe pas, mais elle écrase et remplace le fichier existant s'il y en a un. Il est donc important de vérifier si le fichier token.bin existe déjà pour éviter de perdre le token qui y est déjà enregistré.

### R4 :
Pour s'assurer que la clef est correcte, une méthode possible est d'utiliser une fonction nommée "check_key" qui enverra la clef candidate au CNC. Ensuite, une autre fonction sera créée au niveau du CNC pour comparer la clef candidate avec la bonne clef stockée dans le fichier key.bin. Si la clef candidate est correcte, la fonction retournera une valeur spécifique qui permettra de valider le processus de déchiffrement des fichiers en utilisant cette clef.
