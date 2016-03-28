from functools import wraps

import shopify
from flask import session, redirect, url_for, request, current_app

from .models import Shop
from ..extensions import db

def shopify_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "shopify_token" not in session:
            shop_url = request.args.get('shop')
            shopify.Session.setup(
                api_key=current_app.config['SHOPIFY_API_KEY'], 
                secret=current_app.config['SHOPIFY_SHARED_SECRET'])
            try:
                shopify_session = \
                    shopify.Session.validate_params(request.args)
            except Exception as ex:
                return redirect(url_for('shopify_bp.install', **request.args))
            
            try:
                shop = Shop.query.filter_by(shop=shop_url).one()
            except Exception as ex:
                return redirect(url_for('shopify_bp.install', **request.args))

            session['shopify_token'] = shop.token
            session['shopify_url'] = shop_url
            session['shopify_id'] = shop.id

        else:
            try:
                shop = Shop.query.filter_by(shop=session['shopify_url']).one()
            except Exception as ex:
                session.pop("shopify_token")
                session.pop("shopify_url")
                session.pop("shopify_id")
                return redirect(url_for('shopify_bp.install', **request.args))

        return f(*args, **kwargs)
    
    return decorated_function