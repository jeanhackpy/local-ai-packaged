---
tags: [blockchain, smart-contract, erc20, audit, openzeppelin, solidity]
---
### Audit du contrat Ethereum ERC20

Le contrat Ethereum fourni est une implémentation standard du token ERC20, basé sur les contrats OpenZeppelin. Voici une explication claire des modifications et des commentaires du développeur.

#### Structure du Contrat

- **Pragma et SPDX License Identifier** : 
  ```solidity
  // SPDX-License-Identifier: MIT
  pragma solidity ^0.8.20;
  ```
  Utilisation de la version 0.8.20 du compilateur Solidity et spécification de la licence MIT.

- **Imports** : 
  ```solidity
  import {IERC20} from "./IERC20.sol";
  import {IERC20Metadata} from "./extensions/IERC20Metadata.sol";
  import {Context} from "../../utils/Context.sol";
  import {IERC20Errors} from "../../interfaces/draft-IERC6093.sol";
  ```
  Importation des interfaces et classes nécessaires à partir des bibliothèques OpenZeppelin, y compris des interfaces pour les erreurs personnalisées.

#### Implémentation du Contrat

- **Commentaires et Documentation** :
  ```solidity
  /**
   * @dev Implementation of the {IERC20} interface.
   * This implementation is agnostic to the way tokens are created. This means
   * that a supply mechanism has to be added in a derived contract using {_mint}.
   * ...
   */
  ```
  Explications détaillées sur la structure du contrat et des recommandations pour la gestion de l'approvisionnement des tokens.

- **Variables Privées** :
  ```solidity
  mapping(address account => uint256) private _balances;
  mapping(address account => mapping(address spender => uint256)) private _allowances;
  uint256 private _totalSupply;
  string private _name;
  string private _symbol;
  ```
  Variables pour gérer les soldes, les allocations, l'offre totale, le nom et le symbole des tokens.

- **Constructeur** :
  ```solidity
  constructor(string memory name_, string memory symbol_) {
      _name = name_;
      _symbol = symbol_;
  }
  ```
  Initialisation des valeurs de nom et de symbole des tokens, immuables après la construction.

- **Fonctions Publiques et Externes** :
  - `name()`, `symbol()`, `decimals()`, `totalSupply()`, `balanceOf()`, `transfer()`, `allowance()`, `approve()`, `transferFrom()`.
  - Ces fonctions suivent les spécifications de l'ERC20 et fournissent les fonctionnalités nécessaires pour interagir avec les tokens.

#### Modifications et Commentaires Clés du Développeur

1. **Généralisation des Rejets d'Erreurs** :
   - Utilisation des erreurs personnalisées avec `revert` au lieu de retourner `false` pour des échecs.
   - Exemple :
     ```solidity
     if (from == address(0)) {
         revert ERC20InvalidSender(address(0));
     }
     ```

2. **Gestion des Événements `Approval`** :
   - Emission de l'événement `Approval` lors des appels à `transferFrom`.
   - Commentaire : Cela permet aux applications de reconstruire les allocations en écoutant ces événements.

3. **Optimisation des Fonctions Internes** :
   - Utilisation des fonctions `_transfer`, `_update`, `_mint`, `_burn`, `_approve`, `_spendAllowance` pour la gestion des transferts et des allocations.
   - Exemple :
     ```solidity
     function _update(address from, address to, uint256 value) internal virtual {
         ...
         emit Transfer(from, to, value);
     }
   ```
   - Les vérifications et mises à jour des soldes sont faites avec des `unchecked` pour éviter des coûts de gaz inutiles tout en garantissant qu'aucun débordement n'est possible.

4. **Gestion de l'Allocation Infinie** :
   - Cas particulier pour `approve` avec la valeur maximale `uint256` considérée comme une allocation infinie et non mise à jour dans `transferFrom`.
   - Exemple :
     ```solidity
     if (currentAllowance != type(uint256).max) {
         ...
     }
     ```