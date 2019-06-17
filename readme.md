Authors: Ping Tian-Sen & Tas Emine  
Project: AI_Auto

# Intelligence artificielle
## Simulation de conduite

Ce projet a été réalisé dans le cadre du cours AI5L. Le but étant de concevoir et développer
une intelligence artificielle pour la conduite d'une voiture autonome. L'idée est que
la voiture doit rester sur la route et roule de manière autonome.

### Idée
L'idée qui a été développé pour pouvoir réaliser cette simulation de conduite, quand on détecte une certaine zone (bordure de route) sur la route, que ce soit à gauche ou à droite l'action qui doit être faite est de faire s'éloigner la voiture de cette bordure.
Donc pour finir on voudrait avoir 2 classifieurs, pour détecter les obstacles à gauche ou à droite, et en les combinants ensemble prendre une décision.


### Apprentissage
L'apprentissage qui a été effectué pour pouvoir réaliser cette simulation était,
- Détecter le pattern sur la route

Nous nous sommes basé sur le modèle d'apprentissage SVM linéaire & HOG (Histogram of oriented gradients). Ce modèle sera expliqué plus bas.

### Description des fichiers et répertoires
Il y a 5 fichiers de code :
- **box_selector.py**, c'est grâce à lui qu'il est possible de sélectionner une zone sur l'image, c'est cette zone sélectionnée qui sera le pattern à détecter

- **gather_annotations.py**, c'est avec ce fichier qu'on va sauvegarder les données pour pouvoir faire le training, les fichiers sont sauvés sous la forme npy, qui est un format très performant pour la lecture de données. Les données sauvées sont les zones sélectionnées à l'aide de box_selector et les images correspondantes

- **detector.py**, c'est l'algorithme d'apprentissage, il va essayer de détecter les zones sélectionner(pattern) sur de la route

- **train.py**, c'est le fichier qui va faire la phase d'entrainement et ainsi créer le modèle de classifier pour pouvoir faire le test phase

- **test.py**, c'est le fichier qui va réaliser la phase de test

Il y a plusieurs fichiers de données :
- annotations.npy, annoL.npy, annoR.npy, ces fichiers contiennent les informations sur les zones sélectionnées pour le training
- images.npy, imgL.npy, imgR.npy, ces fichiers contiennent les images pour le training
- detector.svm, dctL.svm, dctR.svm, ce sont les modèles de classifier pour le test

Les répertoires contiennent les différentes images pour l'entrainement et le test
On a utilisé les images des différents angles de la caméra
- Training, TNL, TNR
- Test, TTL, TTR



### Comment démarrer la Simulation
Dans le répertoire il y a un fichier **drive.py**.
C'est lui qui est utilisé pour
se connecter avec le logiciel de simulateur de voiture.

**Drive.py** reçoit les images à partir du simulateur, et
retourne les actions au simulateur (s'il faut tourner ou pas). Tout cela se réalise répétitivement de manière.

Donc il suffit de d'abord lancer ce fichier drive.py avec comme paramètres :
```
-dL
./dctL.svm
-dR
./dctR.svm
-d
./detector.svm
-a
./annotations.npy
-aR
./annoR.npy
-aL
./annoL.npy
--i
./images.npy
```

Ces paramètres reprennent les différents modèles svm et leurs paramètres.
Ensuite on lance la simulation en mode autonome sur le premier parcours.

### Algorithmes & bibliothèques
Les algorithmes primordiaux utilisé sont :
- SVM linéair & HOG

Pour pouvoir détecter des features des objets sur nos images nous avons décidé d’utiliser HOG+SVM.
L’histogramme des dégradés orientés (HOG) est un moyen efficace d’extraire des entités des couleurs de pixel pour créer un classifieur de reconnaissance d’objet. 
La représentation brut des images sous formes de tableau avec un éléments pour chaque pixel à des désavantages comme le fait que c’est coûteux en mémoire, elle contient plus d’information que nécessaire.

Le but de HOG c'est d'utiliser des vecteurs de gradients, les vecteurs de gradients peuvent servir à détecter des contours mais elles peuvent aussi être utile pour extraire des caractéristique utile d’une image.

En combinant le HOG et le SVM on à un classifieur qui détect un pattern, le HOG fournit un pattern à reconnaître sur une image et le classifieur SVM prédit si le pattern est bien sur l'image.

Le classifieur SVM peut autoriser un certain seuile classification en modifiant le paramètre C, une grande valeur du C indique qu'on autorise peut de mal classification et une petite valeur de C permet d'avoir un certain taux d'erreur.

Pour plus d'information sur HOG cliquer sur ce lien [ici](https://www.learnopencv.com/histogram-of-oriented-gradients/)
- box_selector

Cette clase utilise la librairie openCV2, elle contient des fonctions qui va permettre de sélectionner une zone sur une image et elle retourne les dimensions (largeur et longueur de la zone) et la position (le x et y) de cette zone sélectionnée.

Les bibliothèques utilisés sont :
- dlib, qui est une librairie c++ qui permet de faire le machine learning, c'est grâce à lui qu'on a pu mettre en place le SVM & HOG

- opencv2, une librairie graphique, c'est avec cette librairie qu'on va pouvoir utiliser nos images et faire du pre-processing
- numpy, c'est avec cette librairie qu'on va pouvoir sauvegarder les zones sélectionnées sous forme de matrice sur le disque et par la suite les utiliser
- argparse, cette librairie permet d'utiliser des arguments lors du lancement du programme

### Conclusion
En conclusion, notre idée de base de combiner plusieurs classifieurs svm linéaire & HOG ensemble n'est pas suffisant pour que la voiture puisse faire le parcours complet, il y a quelques problèmes d'ambiguités lorsqu'on relies les classifieurs ensemble, quelle action doit être exécutée quand les 3 classifieurs détecte quelque chose. De plus avec ce genre de modèle il n'est pas possible de l'utiliser pour d'autres parcours.

### Crédits

Pour pouvoir réaliser ce projet, nous nous sommes grandement inspirées de :
- http://www.hackevolve.com/create-your-own-object-detector/
- http://www.hackevolve.com/object-tracking/#selecting_regions
- https://www.learnopencv.com/histogram-of-oriented-gradients/
- https://medium.com/@mithi/vehicles-tracking-with-hog-and-linear-svm-c9f27eaf521a
