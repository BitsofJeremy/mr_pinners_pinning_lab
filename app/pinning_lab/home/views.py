
# external imports
from flask import Blueprint, render_template, request, \
    redirect, url_for, flash, jsonify
import humanize

# Local imports
from pinning_lab.utils import ada_usd

# Logging
import logging
logger = logging.getLogger(__name__)


home = Blueprint('home', __name__)
home.config = {}


@home.record
def record_params(setup_state):
  app = setup_state.app
  home.config = dict([(key, value) for (key, value) in app.config.items()])


# Basic site routes
@home.route('/', methods=['GET'])
def index():
    """ Main page """
    return render_template('index.html')


@home.route('/quote', methods=["GET"])
def quote():
    """ Endpoint to GET ADA/USD Price quote. """
    raw_quote = ada_usd()
    q = {
        "usd": f"${raw_quote['cardano']['usd']}",
        "usd_market_cap": humanize.intword(raw_quote['cardano']['usd_market_cap'], "%0.2f"),
        "usd_24h_vol": humanize.intword(raw_quote['cardano']['usd_24h_vol'], "%0.2f"),
        "usd_24h_change": f"{round(raw_quote['cardano']['usd_24h_change'], 2)}%",
    }
    return jsonify({'quote': q})
