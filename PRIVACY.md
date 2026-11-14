# Politique de confidentialité – vStream

**Dernière mise à jour : 14 novembre 2026**

## 1. Présentation

vStream est une extension open source destinée au lecteur multimédia Kodi. Elle permet aux utilisateurs d'accéder à différentes fonctionnalités de recherche, de consultation et de gestion de contenus multimédias.

La présente politique décrit les données susceptibles d'être utilisées ou stockées lors de l'utilisation de vStream, notamment dans le cadre de son intégration avec des services tiers tels que Trakt.

## 2. Collecte des données personnelles

vStream ne demande pas la création d'un compte utilisateur propre au projet.

vStream ne possède aucun serveur centralisé destiné à collecter, stocker ou traiter les données personnelles des utilisateurs.

L'extension n'intègre aucun système de télémétrie, de statistiques d'utilisation ou de suivi du comportement des utilisateurs.

Aucune donnée d'utilisation n'est collectée ou transmise à l'équipe de développement à des fins statistiques.

## 3. Intégration avec Trakt

vStream propose une intégration avec Trakt permettant notamment :

- L'authentification du compte Trakt de l'utilisateur.
- La consultation et la gestion des listes personnelles.
- La récupération et la synchronisation de l'historique de visionnage.
- La synchronisation de la progression de lecture des films et épisodes.
- Le signalement des débuts, progressions et fins de lecture (scrobbling).

L'authentification utilise le mécanisme OAuth de Trakt avec PKCE.

Lorsque l'utilisateur connecte son compte, vStream utilise les jetons d'accès (access token) et de renouvellement (refresh token) fournis par Trakt pour effectuer les opérations autorisées par l'utilisateur.

Ces jetons sont stockés localement dans le profil Kodi de l'utilisateur. Ils ne sont pas transmis à un serveur centralisé géré par le projet vStream.

Les communications avec Trakt sont effectuées directement entre l'installation Kodi de l'utilisateur et les services de Trakt, au moyen de son API officielle.

Les données échangées avec Trakt sont soumises à la politique de confidentialité de ce service :

https://trakt.tv/privacy

## 4. Stockage local des données

Les paramètres de configuration, les préférences et les informations nécessaires au fonctionnement de vStream sont susceptibles d'être stockés localement dans l'environnement Kodi de l'utilisateur.

Les informations d'authentification Trakt, notamment les jetons OAuth, sont conservées dans le profil local Kodi afin de permettre la connexion et la synchronisation du compte.

Ces informations restent sous le contrôle de l'utilisateur et de son environnement Kodi.

## 5. Services tiers

Certaines fonctionnalités de vStream peuvent communiquer avec des services et des sites Internet externes.

Ces communications peuvent entraîner la transmission d'informations techniques nécessaires au fonctionnement des requêtes, notamment l'adresse IP de l'utilisateur, les en-têtes HTTP et les informations propres aux services concernés.

Ces services tiers disposent de leurs propres conditions d'utilisation et politiques de confidentialité.

vStream ne contrôle pas les pratiques de confidentialité de ces services externes.

## 6. Partage et transmission des données

vStream ne vend, ne loue et ne commercialise aucune donnée personnelle.

Les informations associées au compte Trakt sont transmises directement à Trakt dans le cadre des fonctionnalités demandées par l'utilisateur et des autorisations accordées lors de l'authentification.

Aucune donnée personnelle n'est centralisée ou collectée par un serveur exploité par le projet vStream.

## 7. Déconnexion et suppression des données

L'utilisateur peut déconnecter son compte Trakt depuis les fonctionnalités prévues dans vStream.

La suppression des données locales de configuration de l'extension ou la désinstallation de vStream permet de supprimer les informations locales associées, sous réserve des éventuelles sauvegardes de Kodi.

L'utilisateur peut également révoquer les autorisations accordées à vStream depuis les paramètres de son compte Trakt.

La suppression des données éventuellement conservées par Trakt reste soumise aux procédures propres à ce service.

## 8. Sécurité

Les informations d'authentification Trakt sont conservées localement dans le profil Kodi de l'utilisateur.

La sécurité de ces informations dépend également de la protection de l'installation Kodi, du système d'exploitation et du périphérique utilisés.

L'utilisateur est responsable de la sécurité de son environnement informatique.

## 9. Évolution de cette politique

Cette politique de confidentialité peut être mise à jour afin de tenir compte des évolutions de vStream, de ses fonctionnalités et des services tiers intégrés.

La version la plus récente est publiée sur le dépôt officiel du projet.

## 10. Contact

Pour toute question concernant cette politique de confidentialité ou le fonctionnement de vStream, les utilisateurs peuvent contacter l'équipe du projet via le dépôt GitHub officiel :

https://github.com/Kodi-vStream/venom-xbmc-addons

## 11. Informations relatives à Trakt

vStream utilise Trakt mais n'est ni approuvé ni certifié par Trakt.

vStream uses Trakt but is not endorsed or certified by Trakt.
