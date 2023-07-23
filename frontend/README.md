# Frontend

Ce projet Angular fait partie d'une application possédant un Frontend et un Backend. 

Ce projet est codé en anglais, pourtant l'interface elle-même est en espagnol puisque ce projet était un projet développé pour une entreprise qui parle uniquement en espagnol. 

## Architecture du projet 

Ce projet communique avec le Backend pour récolter information en aide d'un service Angular. 

Le nom de ce service est backend-service.

Complémentairement, le service data permet le transfert d'information entre divers 'components', ce service est nécessaire puisque @Input n'est pas utilisable dans des 'components' qui implémentent la fonction de routage. 
Pourtant, l'utilisation de ce service est considéré une mauvaise technique. 

C'est pour cela que l'utilisation d'Angular material fut une alternative pour remplacer le transfert de données par des 'pop-ups'.

Ce projet possède 3 types de 'components' :
<ul>
  <li>
    Des 'components' permettant de calculer le score d'un audio
  </li>
  <li>
    Des 'components' permettant de calculer les embeddings d'un audio
  </li>
  <li>
    Des pop-ups
  </li>
</ul>

Ce projet utilise les fonctionnalités de routage d'Angular 

## Déployer le projet sur Stackblitz

Stackblitz est un environnement de déploiement online. 

Il permet le déploiement d'un projet Angular depuis Github. 
Pour le faire, il faudra acceder dans le link suivant : 
https://stackblitz.com/github/Henrei3/openaiProductividad/tree/main/frontend

Ce projet Angular utilise un version axios différente de celle par default sur Stackblitz.
Pour que le projet se déploie correctement, il suffit uniquement de changer la librairie axios à la version correcte. 

Pour faire cela, vous devrez écrire: <code>axios@0.27.2</code> sur la barre dépendance, comme montré ci-dessous : 

<img width="279" alt="image" src="https://github.com/Henrei3/openaiProductividad/assets/95311577/00495960-a010-45f5-8a31-610592d814a5">


