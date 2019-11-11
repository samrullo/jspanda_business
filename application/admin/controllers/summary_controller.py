import datetime
from application.admin.models.received_money_model import ReceivedMoney, db
from application.admin.models.visa_spendings import VisaSpending
from application.admin.models.shipment_spending import ShipmentSpending
from application.admin.models.transferrals import Transferral
import logging
import pandas as pd
from flask import flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, DateField
from application.utils.utils import to_yyyymmdd


class SummaryController:
    def __init__(self):
        self.name = "summary_controller"

    def show_summary(self):
        received_money_df = pd.read_sql(ReceivedMoney.query.statement, ReceivedMoney.query.session.bind)
        visa_spendings_df = pd.read_sql(VisaSpending.query.statement, VisaSpending.query.session.bind)
        shipment_spendings_df = pd.read_sql(ShipmentSpending.query.statement, ShipmentSpending.query.session.bind)
        transferrals_df=pd.read_sql(Transferral.query.statement,Transferral.query.session.bind)
        return render_template("summary.html", title="JSPanda business Summary", total_received_money=received_money_df['amount_jpy'].sum(),
                               total_transferral=transferrals_df['amount'].sum(),
                               total_visa_spending=visa_spendings_df['amount'].sum(),
                               total_shipment_spending=shipment_spendings_df['amount'].sum())
