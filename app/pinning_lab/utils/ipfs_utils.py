# pinning_lab/utils/ipfs_utils.py
import argparse
import os
import requests
import sys

# Logging
import logging
logger = logging.getLogger(__name__)

# Basic functionality for IPFS
# provided by Blockfrost for pinning

# Options:
# python ipfs_utils.py --create_ipfs image.png
# python ipfs_utils.py --pin_ipfs QmbdnAH65b7QhY2G5r1AHhEdytsBUY4oiU29cpUQtMRCHW
# python ipfs_utils.py --remove_ipfs QmbdnAH65b7QhY2G5r1AHhEdytsBUY4oiU29cpUQtMRCHW
# python ipfs_utils.py --check_ipfs QmbdnAH65b7QhY2G5r1AHhEdytsBUY4oiU29cpUQtMRCHW

BLOCKFROST_IPFS = os.getenv('BLOCKFROST_IPFS')


def create_ipfs(image):
    """ Uploads image to Blockfrost """
    ipfs_create_url = "https://ipfs.blockfrost.io/api/v0/ipfs/add"
    files = {'file': image}
    headers = {"project_id": f"{BLOCKFROST_IPFS}"}
    res = requests.post(ipfs_create_url,  files=files, headers=headers)
    res.raise_for_status()
    if res.status_code == 200:
        logger.info("Uploaded image to Blockfrost")
        logger.info(res.json())
        return res.json()
    else:
        logger.error("Something failed here? Upload to blockfrost failed")
        return False


def pin_ipfs(ipfs_hash):
    """ Pins IPFS hash in Account """
    ipfs_pin_url = f"https://ipfs.blockfrost.io/api/v0/ipfs/pin/add/{ipfs_hash}"
    headers = {"project_id": f"{BLOCKFROST_IPFS}"}
    res = requests.post(ipfs_pin_url, headers=headers)
    res.raise_for_status()
    if res.status_code == 200:
        logger.info("Pinned on Blockfrost")
        logger.info(res.json())
        return True
    else:
        logger.error("Something failed here? Pin failed")
        return False


def remove_ipfs(ipfs_hash):
    """ Removes pin from IPFS hash in Blockfrost """
    ipfs_remove_url = f"https://ipfs.blockfrost.io/api/v0/ipfs/pin/remove/{ipfs_hash}"
    headers = {"project_id": f"{BLOCKFROST_IPFS}"}
    res = requests.post(ipfs_remove_url, headers=headers)
    res.raise_for_status()
    if res.status_code == 200:
        logger.info("Removing pin worked")
        logger.info(res.json())
        return True
    else:
        logger.error("Something failed here? Remove Pin failed")
        return False


def check_ipfs(ipfs_hash):
    """ Check to see if the ipfs hash is accessible via
    ipfs.io and cloudflare """
    # TODO Add Celery later for speed up?
    ipfs_gateways = [
        f"https://gateway.ipfs.io/ipfs/{ipfs_hash}",
        f"https://cloudflare-ipfs.com/ipfs/{ipfs_hash}"
    ]

    ipfs_status = []
    for gateway in ipfs_gateways:
        res = requests.get(gateway)
        logger.info(res.status_code)
        if res.status_code == 200:
            ipfs_status.append(True)
        else:
            ipfs_status.append(False)
    logger.info(f"Availability:  {ipfs_status}")
    return True


def main(**kwargs):
    if kwargs.get('create_ipfs'):
        print(kwargs.get('create_ipfs'))
        res = create_ipfs(image=kwargs.get('create_ipfs'))
        if res:
            print('Created IPFS Hash')

    elif kwargs.get('pin_ipfs'):
        print(kwargs.get('pin_ipfs'))
        res = pin_ipfs(ipfs_hash=kwargs.get('pin_ipfs'))
        if res:
            print('Pin IPFS Hash')

    elif kwargs.get('remove_ipfs'):
        print(kwargs.get('remove_ipfs'))
        res = remove_ipfs(ipfs_hash=kwargs.get('remove_ipfs'))
        if res:
            print('Remove IPFS Hash')

    elif kwargs.get('check_ipfs'):
        print(kwargs.get('check_ipfs'))
        res = check_ipfs(ipfs_hash=kwargs.get('check_ipfs'))
        if res:
            print('Check IPFS Hash')
    else:
        print('Fail')

    return print('FIN')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--create_ipfs',
        help='Create the IPFS hash',
        required=False
    )

    parser.add_argument(
        '--pin_ipfs',
        help='Create the IPFS pin',
        required=False
    )

    parser.add_argument(
        '--remove_ipfs',
        help='Remove the IPFS hash pin',
        required=False
    )

    parser.add_argument(
        '--check_ipfs',
        help='Check the IPFS hash',
        required=False
    )
    args = parser.parse_args()

    # Convert the argparse.Namespace to a dictionary: vars(args)
    arg_dict = vars(args)
    # pass dictionary to main
    main(**arg_dict)
    sys.exit(0)

