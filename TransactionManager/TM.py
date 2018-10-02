import subprocess
import json


def updateVotings(poll_addr,ind = -1):
    new_list = subprocess.check_output(['flo-cli','--testnet','listsinceblock'])
    data =  json.loads(new_list.decode())
    choices = []
    for transaction in data["transactions"]:
        if transaction["category"]=="receive" and transaction["address"]==poll_addr:
            choices.append(readUnitFromBlockchain(transaction["txid"]))
    return choices

def writeDatatoBlockchain(text,receiver,amt):
    """
    Function Name: writeDatatoBlockChain

    Function use: write the recieved Data to the Block-Chain with a specified amount amt charge
    """

    txid = subprocess.check_output(["flo-cli","--testnet", "sendtoaddress",receiver,str(amt),'""','""',"true","false","10",'UNSET',str(text)])
    txid = str(txid)
    txid = txid[2:-3]
    return txid

def readUnitFromBlockchain(txid):
    #Reads Unit Data from Block Chain
    rawtx = subprocess.check_output(["flo-cli","--testnet", "getrawtransaction", str(txid)])
    rawtx = str(rawtx)
    rawtx = rawtx[2:-3]
    tx = subprocess.check_output(["flo-cli","--testnet", "decoderawtransaction", str(rawtx)])
    content = json.loads(tx)
    text = content['floData']
    return text

def getPollAdress():
    """
    Function Name: getPollAdress

    Function use: Returns a new Wallet Adress for every poll created
    """
    new_address = subprocess.check_output(["flo-cli","--testnet","getnewaddress"])
    return new_address
