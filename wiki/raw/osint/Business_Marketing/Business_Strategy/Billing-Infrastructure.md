---
tags: [business, billing, payment-gateway, stripe, python]
---
### Infrastructure de facturation

#### a. Choisir une plateforme de paiement
Utilisez des plateformes de paiement comme Stripe, PayPal, ou Square pour traiter les paiements.

#### b. Intégrer un système de facturation
- **Stripe** : 
  - Installez la bibliothèque Stripe : `pip install stripe`
  - Configurez votre application pour gérer les paiements récurrents ou les paiements à l'utilisation.

Voici un exemple d'intégration basique avec Stripe en Python :

```python
import stripe

stripe.api_key = 'votre_cle_api_stripe'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Subscription',
                },
                'unit_amount': 1000,
            },
            'quantity': 1,
        }],
        mode='subscription',
        success_url='https://votre_site.com/success.html',
        cancel_url='https://votre_site.com/cancel.html',
    )
    return jsonify(id=session.id)
```