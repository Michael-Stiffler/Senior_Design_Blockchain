from xrpl.wallet import Wallet
import xrpl
import json
from dotenv import load_dotenv
import os

load_dotenv()

test_wallet = Wallet(
    seed=os.getenv('XRP_WALLET'), sequence=16237283)

print(test_wallet.classic_address)

testnet_url = "https://s.altnet.rippletest.net:51234"
client = xrpl.clients.JsonRpcClient(testnet_url)

my_payment = xrpl.models.transactions.Payment(
    account=test_wallet.classic_address,
    amount=xrpl.utils.xrp_to_drops(1),
    destination="rNgcuCEW6dKcNUz1GxjLLdWjWXnVhpVuYq",
    memos=[xrpl.models.transactions.transaction.Memo(
                memo_data="687474703a2f2f6578616d706c652e636f6d2f6d656d6f2f67656e65726963")]
)

print("Payment object:", my_payment)

signed_tx = xrpl.transaction.safe_sign_and_autofill_transaction(
    my_payment, test_wallet, client)
max_ledger = signed_tx.last_ledger_sequence
tx_id = signed_tx.get_hash()
print("Signed transaction:", signed_tx)
print("Transaction cost:", xrpl.utils.drops_to_xrp(signed_tx.fee), "XRP")
print("Transaction expires after ledger:", max_ledger)
print("Identifying hash:", tx_id)

try:
    tx_response = xrpl.transaction.send_reliable_submission(signed_tx, client)
except xrpl.transaction.XRPLReliableSubmissionException as e:
    exit(f"Submit failed: {e}")

print(json.dumps(tx_response.result, indent=4, sort_keys=True))
print(f"Explorer link: https://testnet.xrpl.org/transactions/{tx_id}")
metadata = tx_response.result.get("meta", {})
if metadata.get("TransactionResult"):
    print("Result code:", metadata["TransactionResult"])
if metadata.get("delivered_amount"):
    print("XRP delivered:", xrpl.utils.drops_to_xrp(
        metadata["delivered_amount"]))
