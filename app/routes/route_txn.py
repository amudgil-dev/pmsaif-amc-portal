from flask import Blueprint, render_template, request,flash,redirect, url_for
from flask_login import login_required, current_user
from app.models.models import Transaction
from app.extensions import db
from app.forms.forms import AddTransactionForm
from app.helpers.auth_helper import AuthHelper

bp_txn = Blueprint('txn', __name__)

@bp_txn.route('/transactions', methods=['GET', 'POST'])
@login_required
@AuthHelper.check_session_and_authorize
def transactions():
    search = request.args.get('search')
    txn_type = current_user.user_type
    query = Transaction.query.filter_by(user_id=current_user.id, txn_type=txn_type)
    
    if search:
        query = query.filter(Transaction.txn_amount.like(f'%{search}%'))
    
    transactions = query.all()

    # Add transaction form
    form = AddTransactionForm()
    if form.validate_on_submit():
        new_transaction = Transaction(
            user_id=current_user.id,
            txn_date=form.date.data,
            txn_amount=form.amount.data,
            txn_type=current_user.user_type
        )
        db.session.add(new_transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('txn.transactions'))

    return render_template('transactions.html', transactions=transactions, form=form)