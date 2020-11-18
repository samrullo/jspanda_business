import datetime
from application.admin.models.family_spending import FamilySpending, db
import logging
import pandas as pd
import numpy as np
from flask import flash
from flask import render_template
from flask import redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, IntegerField, FieldList, DateField


class FamilySpendingSingleItemForm(FlaskForm):
    id = IntegerField("id", render_kw={"class": "form-control"})
    date = DateField("date")
    name = StringField("name", render_kw={"class": "form-control"})
    amount = IntegerField("amount", render_kw={"class": "form-control", })
    submit = SubmitField("Update family spending", render_kw={"class": "btn btn-lg btn-dark"})


class FamilySpendingForm(FlaskForm):
    cost_names = ['date', 'mitsubishi_current_balance', 'saitama_current_balance', 'solar to receive', 'salary', 'metlife',
                  'mortgage', 'saison_lalaport_visa_saitama', 'cosmos_gasoline_visa_saitama', 'edion_visa_saitama', 'costco_old_visa_saitama',
                  'costco_new_visa_mitsubishi', 'yahoo_visa_saitama', 'rakuten_visa_mitsubishi','amazon_visa_mitsubishi', 'softbank', 'solar_panel', 'proyezd',
                  'sadik', 'samira_swimming', 'samira_russian', 'denki', 'gas', 'suv', 'timur school', 'karen school', 'jidoushazei', 'home tax']

    date = StringField("date", description="date", render_kw={"class": "form-control", "data-clear-btn": "true"})
    mitsubishi_current_balance = IntegerField("mitsubishi_current_balance", description="mitsubishi_current_balance", render_kw={"class": "form-control", })
    saitama_current_balance = IntegerField("saitama_current_balance", description="saitama_current_balance", render_kw={"class": "form-control", })
    solar_to_receive = IntegerField("solar to receive", description="solar to receive", render_kw={"class": "form-control", })
    salary = IntegerField("salary", description="salary", render_kw={"class": "form-control", })
    metlife = IntegerField("metlife", description="metlife", render_kw={"class": "form-control", })
    mortgage = IntegerField("mortgage", description="mortgage", render_kw={"class": "form-control", })
    saison_lalaport_visa_saitama = IntegerField("saison_lalaport_visa_saitama", description="saison_lalaport_visa_saitama", render_kw={"class": "form-control", })
    cosmos_gasoline_visa_saitama = IntegerField("cosmos_gasoline_visa_saitama", description="cosmos_gasoline_visa_saitama", render_kw={"class": "form-control", })
    edion_visa_saitama = IntegerField("edion_visa_saitama", description="edion_visa_saitama", render_kw={"class": "form-control", })
    costco_old_visa_saitama = IntegerField("costco_old_visa_saitama", description="costco_old_visa_saitama", render_kw={"class": "form-control", })
    costco_new_visa_mitsubishi = IntegerField("costco_new_visa_mitsubishi", description="costco_new_visa_mitsubishi", render_kw={"class": "form-control", })
    yahoo_visa_saitama = IntegerField("yahoo_visa_saitama", description="yahoo_visa_saitama", render_kw={"class": "form-control", })
    rakuten_visa_mitsubishi = IntegerField("rakuten_visa_mitsubishi", description="rakuten_visa_mitsubishi", render_kw={"class": "form-control", })
    amazon_visa_mitsubishi = IntegerField("amazon_visa_mitsubishi", description="amazon_visa_mitsubishi", render_kw={"class": "form-control", })
    softbank = IntegerField("softbank", description="softbank", render_kw={"class": "form-control", })
    solar_panel = IntegerField("solar_panel", description="solar_panel", render_kw={"class": "form-control", })
    proyezd = IntegerField("proyezd", description="proyezd", render_kw={"class": "form-control", })
    sadik = IntegerField("sadik", description="sadik", render_kw={"class": "form-control", })
    samira_swimming = IntegerField("samira_swimming", description="samira_swimming", render_kw={"class": "form-control", })
    samira_russian = IntegerField("samira_russian", description="samira_russian", render_kw={"class": "form-control", })
    denki = IntegerField("denki", description="denki", render_kw={"class": "form-control", })
    gas = IntegerField("gas", description="gas", render_kw={"class": "form-control", })
    suv = IntegerField("suv", description="suv", render_kw={"class": "form-control", })
    timur_school = IntegerField("timur school", description="timur school", render_kw={"class": "form-control", })
    karen_school = IntegerField("karen school", description="karen school", render_kw={"class": "form-control", })
    jidoushazei = IntegerField("jidoushazei", description="jidoushazei", render_kw={"class": "form-control", })
    home_tax = IntegerField("home tax", description="home tax", render_kw={"class": "form-control", })
    submit = SubmitField("Save family spending", render_kw={"class": "btn btn-lg btn-dark"})


class FamilySpendingController:
    def __init__(self):
        self.model = FamilySpending()
        self.income_cols = ['mitsubishi_current_balance', 'saitama_current_balance', 'solar to receive', 'salary']
        self.cost_cols = ['metlife', 'mortgage', 'saison_lalaport_visa_saitama', 'cosmos_gasoline_visa_saitama', 'edion_visa_saitama', 'costco_old_visa_saitama',
                          'costco_new_visa_mitsubishi', 'yahoo_visa_saitama', 'rakuten_visa_mitsubishi', 'amazon_visa_mitsubishi','softbank', 'solar_panel', 'proyezd',
                          'sadik', 'samira_swimming', 'samira_russian', 'denki', 'gas', 'suv', 'timur school', 'karen school', 'jidoushazei', 'home tax']
        self.cost_names = ['month', 'mitsubishi_current_balance', 'saitama_current_balance', 'solar to receive', 'salary', 'metlife',
                           'mortgage', 'saison_lalaport_visa_saitama', 'cosmos_gasoline_visa_saitama', 'edion_visa_saitama', 'costco_old_visa_saitama',
                           'costco_new_visa_mitsubishi', 'yahoo_visa_saitama', 'rakuten_visa_mitsubishi', 'amazon_visa_mitsubishi','softbank', 'solar_panel', 'proyezd',
                           'sadik', 'samira_swimming', 'samira_russian', 'denki', 'gas', 'suv', 'timur school', 'karen school', 'jidoushazei', 'home tax']
        self.visa_cols = ['saison_lalaport_visa_saitama', 'cosmos_gasoline_visa_saitama', 'edion_visa_saitama', 'costco_old_visa_saitama', 'costco_new_visa_mitsubishi', 'yahoo_visa_saitama', 'rakuten_visa_mitsubishi','amazon_visa_mitsubishi']
        self.saitama_items = ['saison_lalaport_visa_saitama', 'cosmos_gasoline_visa_saitama', 'edion_visa_saitama', 'costco_old_visa_saitama', 'yahoo_visa_saitama', 'mortgage', 'solar_panel', 'samira_swimming', 'timur school']
        self.mitsubishi_items = ['metlife', 'costco_new_visa_mitsubishi', 'rakuten_visa_mitsubishi', 'amazon_visa_mitsubishi','denki', 'gas', 'karen school']
        self.calculated_names = ['balance', 'saitama_liabilities', 'saitama_new_balance', 'mitsubishi_liabilities', 'mitsubishi_new_balance']

    def family_spending_main(self):
        # all_records = self.model.get_items()
        # all_df = pd.DataFrame(columns=['id', 'date', 'name', 'amount'], data=all_records)
        all_df = pd.read_sql(FamilySpending.query.statement, FamilySpending.query.session.bind)
        spending_df = pd.DataFrame()
        for adate in all_df['date'].unique():
            logging.info(f"will prepare spendings for {adate}")
            for col in self.cost_names:
                logging.info(f"set value for date {adate} column {col}")
                try:
                    spending_df.loc[adate, col] = all_df.loc[np.logical_and(all_df['date'] == adate, all_df['name'] == col), 'amount'].values[0]
                except IndexError:
                    spending_df.loc[adate, col] = 0
            spending_df.loc[adate, 'balance'] = spending_df.loc[adate, self.cost_names].sum()
            spending_df.loc[adate, 'total_visa_spending'] = spending_df.loc[adate, self.visa_cols].sum()
            spending_df.loc[adate, 'saitama_liabilities'] = spending_df.loc[adate, self.saitama_items].sum()
            spending_df.loc[adate, 'saitama_new_balance'] = spending_df.loc[adate, 'saitama_current_balance'] + spending_df.loc[adate, 'saitama_liabilities']
            spending_df.loc[adate, 'mitsubishi_liabilities'] = spending_df.loc[adate, self.mitsubishi_items].sum()
            spending_df.loc[adate, 'mitsubishi_new_balance'] = spending_df.loc[adate, 'mitsubishi_current_balance'] + spending_df.loc[adate, 'salary'] + spending_df.loc[adate, 'mitsubishi_liabilities']
        spending_df.sort_index(ascending=False, inplace=True)
        return render_template("family_spending/family_spending_main.html", spending_df=spending_df)

    def family_spending_month(self, adate):
        # all_records = self.model.get_items_by_date(adate)
        spending_df = pd.read_sql(FamilySpending.query.filter(FamilySpending.date == adate).statement, FamilySpending.query.session.bind)
        spending_df['amount'] = pd.to_numeric(spending_df['amount'])
        logging.info(f"total of {len(spending_df)} as of {adate}")
        summary = {}
        summary['balance'] = spending_df.loc[spending_df['name'].isin(self.cost_names), 'amount'].sum()
        summary['total_visa_spending'] = spending_df.loc[spending_df['name'].isin(self.visa_cols), 'amount'].sum()
        summary['saitama_liabilities'] = spending_df.loc[spending_df['name'].isin(self.saitama_items), 'amount'].sum()
        summary['saitama_new_balance'] = spending_df.loc[spending_df['name'] == 'saitama_current_balance', 'amount'].values[0] + summary['saitama_liabilities']
        summary['mitsubishi_liabilities'] = spending_df.loc[spending_df['name'].isin(self.mitsubishi_items), 'amount'].sum()
        summary['mitsubishi_new_balance'] = spending_df.loc[spending_df['name'].isin(['mitsubishi_current_balance', 'salary']), 'amount'].sum() + summary['mitsubishi_liabilities']
        return render_template("family_spending/family_spending_single_date.html", spending_df=spending_df, summary=summary, adate=adate, saitama_items=self.saitama_items, mitsubishi_items=self.mitsubishi_items)

    def add_family_spending(self):
        form = FamilySpendingForm()
        if form.validate_on_submit():
            date = form.date.data
            for field in form:
                if field.description in self.income_cols + self.cost_cols:
                    if field.description in self.cost_cols and field.data > 0:
                        field.data = field.data * -1
                    record = FamilySpending(date=date, name=field.description, amount=field.data)
                    # self.model.add_item(date, field.label, field.data)
                    db.session.add(record)
                    db.session.commit()
                    logging.info(f"added {date} {field.description} {field.data}")
            flash(f"Added family spending for {date}", "success")
            return redirect(f"/admin/family_spending_by_month/{date}")
        adate = datetime.date.today()
        # adate_records = self.model.get_items_by_date(datetime.date(adate.year, adate.month, 1))
        # spending_df = pd.DataFrame(columns=['id', 'date', 'name', 'amount'], data=adate_records)
        all_df = pd.read_sql(FamilySpending.query.statement, FamilySpending.query.session.bind)
        most_recent_date = all_df['date'].max()
        spending_df = pd.read_sql(FamilySpending.query.filter(FamilySpending.date == most_recent_date).statement, FamilySpending.query.session.bind)
        if len(spending_df) != 0:
            form.date.data = adate
            for field in form:
                if field.description in form.cost_names and field.description != 'date':
                    spending_amount_series = spending_df.loc[spending_df['name'] == field.description, 'amount']
                    if len(spending_amount_series) > 0:
                        field.data = spending_df.loc[spending_df['name'] == field.description, 'amount'].values[0]
                    else:
                        field.data = 0
            return render_template("family_spending/add_family_spending.html", form=form)
        else:
            flash(f"No records were found as of {datetime.date(adate.year, adate.month, 1)}", "danger")
            return self.family_spending_main()

    def edit_family_spending(self, id):
        form = FamilySpendingSingleItemForm()
        record = FamilySpending.query.get(id)
        if form.validate_on_submit():
            record.date = form.date.data
            record.name = form.name.data
            if record.name in self.cost_cols and form.amount.data > 0:
                record.amount = form.amount.data * -1
            else:
                record.amount = form.amount.data
            if record.name in self.income_cols:
                record.amount = form.amount.data
            db.session.commit()
            flash(f"Updated {id} to {record.date}, {record.name}, {record.amount}", "success")
            return redirect(f"/admin/family_spending_by_month/{record.date}")
        form.id.data = id
        form.date.data = record.date
        form.name.data = record.name
        form.amount.data = record.amount
        return render_template("family_spending/edit_family_spending.html", form=form)

    def remove_family_spending(self, id):
        record = FamilySpending.query.get(id)
        date = record.date
        db.session.delete(record)
        db.session.commit()
        flash(f"Removed {id} record", "success")
        return redirect(f"/admin/family_spending_by_month/{date}")
