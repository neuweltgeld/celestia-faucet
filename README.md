# Celestia Testnet Faucet
Faucet UI for Celestia Blockspacerace where users can get 0.1 TIA test tokens.

If you want to use the tool on your own node, you should configure ```Apache2``` and ```Flask``` settings. You can use the repository at [this link](https://github.com/neuweltgeld/ubuntu-python-server) for the guide.

The project folder may look like the following:

```
celestia-faucet/
├── static/
│   ├── logo.png
│   └── styles.css
├── templates/
│   └── index.html
└── faucet.py
```

The balance in the wallet named ```wallet``` is used. 

## Planned features
. Keplr wallet integration

. Wallet balance check

. Wallet address autofill
