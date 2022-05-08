from multiprocessing import context
import re
from django.http import HttpResponse
from django.shortcuts import render
from .forms import MintForm

#nft
from thirdweb import ThirdwebSDK
from thirdweb.types.nft import NFTMetadataInput
from eth_account import Account
from dotenv import load_dotenv
from web3 import Web3
import os

load_dotenv()

PRIVATE_KEY = os.environ.get("PRIVATE_KEY")

RPC_URL = "https://polygon-rpc.com"

provider = Web3(Web3.HTTPProvider(RPC_URL))

signer = Account.from_key(PRIVATE_KEY)

sdk = ThirdwebSDK(provider, signer)
NFT_COLLECTION_ADDRESS = "ADD YOUR NFT COLLECTION ADDRESS HERE" #You can create one from thirdweb.com
nft_collection = sdk.get_nft_collection(NFT_COLLECTION_ADDRESS)

def home(request):
    context = {}
    return render(request,'home.html',context)

def issue_certificate(request):
    form = MintForm()
    context = {'form':form}
    if request.method == 'POST':
        name = request.POST.get("student_name")
        cgpa = request.POST.get("student_cgpa")
        wallet = request.POST.get("student_wallet")
        url = request.POST.get("certificate_url")

        nft_collection.mint_to(wallet,NFTMetadataInput.from_json({ 
            "name": "BE", 
            "description": "Certificate issued by ABC University", 
            "image": url,
            "properties": {'student_name':name, 'cgpa':cgpa}
        }))
    return render(request,'issue_certificate.html',context)

def verify_certificate(request):
    context = {}
    return render(request,'verify_certificate.html',context)

def apply_masters(request):
    context = {}
    return render(request,'apply_masters.html',context)

def view_certificates(request):
    nfts = request.GET.get('nfts')
    context = {'nfts':nfts}
    return render(request,'view_certificates.html',context)