import pprint

import shopify
from flask import (
    Blueprint, render_template, current_app, request, redirect, session,
    url_for)

from .models import Shop
from .decorators import shopify_auth_required
from ..extensions import db


shopify_bp = Blueprint('shopify_bp', __name__, url_prefix='/shopify')

@shopify_bp.route('/')
@shopify_auth_required
def index():
    """ Render the index page of our application.

    """

    return render_template('shopify_bp/index.html')

@shopify_bp.route('/install')
def install():
    """ Redirect user to permission authorization page.

    """

    shop_url = request.args.get("shop")

    shopify.Session.setup(
        api_key=current_app.config['SHOPIFY_API_KEY'], 
        secret=current_app.config['SHOPIFY_SHARED_SECRET'])

    session = shopify.Session(shop_url)

    scope=[
        "write_products", "read_products", "read_script_tags", 
        "write_script_tags"]
    redirect_uri = url_for("shopify_bp.finalize", _external=True)
    print redirect_uri
    permission_url = session.create_permission_url(
        scope, redirect_uri)

    return render_template(
        'shopify_bp/install.html', permission_url=permission_url)

@shopify_bp.route('/finalize')
def finalize():
    """ Generate shop token and store the shop information.
    
    """
    
    shop_url = request.args.get("shop")
    shopify.Session.setup(
        api_key=current_app.config['SHOPIFY_API_KEY'], 
        secret=current_app.config['SHOPIFY_SHARED_SECRET'])
    shopify_session = shopify.Session(shop_url)

    token = shopify_session.request_token(request.args)

    shop = Shop(shop=shop_url, token=token)
    db.session.add(shop)
    db.session.commit()

    session['shopify_url'] = shop_url
    session['shopify_token'] = token
    session['shopify_id'] = shop.id


    return redirect(url_for('shopify_bp.index'))