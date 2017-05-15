"""
Grab images from OMERO based on Screen data
"""

import csv
import multiprocessing
import progressbar
import signal
import sys
import time
import requests
import json
import getpass
from argparse import ArgumentParser
from collections import OrderedDict
from omeroidr.images import Images
from omeroidr.constants import API_LOGIN, API_LOGOUT

parser = ArgumentParser(prog='OMERO screen image downloader')
parser.add_argument('-o', '--output', help='Path to the output images directory')
parser.add_argument('-d', '--data', required=False, default='omero.tab', help='Path to the data source')
parser.add_argument('-s', '--server', required=False, default='https://lincs.ohsu.edu', help='Base url for OMERO server')
parser.add_argument('-u', '--user', required=False, help='OMERO Username')
parser.add_argument('-w', '--password', required=False, help='OMERO Password')

pargs = parser.parse_args()

# initialize the progress bar
widgets = [progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(widgets=widgets)

def connect_to_omero(base_url: str, user: str, password: str):

    session = requests.Session()

    login_url = base_url + API_LOGIN
    session.get(login_url)
    token = session.cookies['csrftoken']

    if (user == None):
        user = input('OMERO Username (return for public repository): ')

    if (password == None):
        password = getpass.getpass('OMERO Password (return for public repository): ')

    # Login with username, password and server
    payload = {'username': user,
           'password': password,
           'server': 1,
           'noredirect': 1,
           'csrfmiddlewaretoken': token}
    r = session.post(login_url, data=payload, headers=dict(Referer=login_url))

    # Return session handle
    return session

def disconnect(session, base_url: str):
    logout_url = base_url + API_LOGOUT
    login_url = base_url + API_LOGIN
    r = session.post(logout_url, headers=dict(Referer=login_url))

def init_worker():
    """
    Initialise multiprocessing pool
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def download_image_callback(val):
    """
    Callback from apply_async download image method.

    :param val: Callback value
    """
    # update progress bar
    pbar.update(pbar.previous_value + 1)


def main():
    # login
    session = connect_to_omero(pargs.server, pargs.user, pargs.password)

    omero_images = Images(session, pargs.server, pargs.output)

    # open tab metadata file
    with open(pargs.data, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        # get headers
        headers = [i.strip() for i in next(csv_reader)]
        # transform into dict
        wells = list(OrderedDict(zip(headers, row)) for row in csv_reader)

    # get list of image ids from wells
    image_ids = [well['id'] for well in wells]

    print('Fetching images...')

    # using a pool of processes
    p = multiprocessing.Pool(multiprocessing.cpu_count(), init_worker)

    pbar.max_value = len(wells)
    pbar.start()
    for image_id in image_ids:
        # p.apply_async(omero_images.download_image, args=(image_id,), callback=download_image_callback)
        p.apply_async(omero_images.download_imagethumb, args=(image_id,), kwds=dict(w=150), callback=download_image_callback)

        # (self, image_id: int, w=64, z=0, t=0, explicit=False)
    try:
        # wait 10 seconds, this allows for the capture of the KeyboardInterrupt exception
        time.sleep(10)
    except KeyboardInterrupt:
        p.terminate()
        p.join()
        disconnect(session, pargs.server)
        print('exiting...')
        sys.exit(0)
    finally:
        p.close()
        p.join()
        pbar.finish()

    disconnect(session, pargs.server)
    print('Image fetch complete')

if __name__ == '__main__':
    main()
