import os
from . import mortgage_app_bp
from flask import render_template,current_app
from flask import send_file

@mortgage_app_bp.route("/")
def mortgage_app():    
    return render_template("mortgage_index.html")


from bokeh.plotting import figure
from bokeh.embed import components

@mortgage_app_bp.route('/plot')
def plot():
    # Create a Bokeh plot
    p = figure(outer_width=400, outer_height=400)
    p.vbar(x=[1, 2, 3], width=0.5, bottom=0,
           top=[1.2, 2.5, 3.7], color="firebrick")

    # Generate the HTML and JavaScript for the plot
    script, div = components(p)

    # Render the template
    return render_template("bokeh_plot.html", title="Simple Bokeh plot", script=script, div=div)

def calc_smm(a, t, y):
    y=y/100
    smm = a * (y / 12) * (1 + y / 12) ** (t * 12) / ((1 + y / 12) ** (t * 12) - 1)
    return smm


def get_principal_interest_paydowns(borrowed_amount, borrowed_time, smm, ir_pct):
    ir=ir_pct/100
    ir_monthly=ir/12
    prin_paydowns=[]
    ir_paydowns = []
    paid_down_principal=0
    for i in range(borrowed_time*12):
        remaining_debt = borrowed_amount - paid_down_principal
        ir_paydown = remaining_debt*ir_monthly
        prin_paydown=smm-ir_paydown
        paid_down_principal+=prin_paydown
        ir_paydowns.append(ir_paydown)
        prin_paydowns.append(prin_paydown)        
    return prin_paydowns,ir_paydowns


from .forms import MortgageForm

@mortgage_app_bp.route("/plot/paydowns",methods=["GET","POST"])
def plot_paydowns():
    form = MortgageForm()
    if form.validate_on_submit():
        borrowed_amount=form.borrowed_amount.data
        borrowing_time = form.borrowing_time.data
        interest_rate=form.interest_rate.data
        smm = calc_smm(borrowed_amount,borrowing_time,interest_rate)
        prin_paydowns, ir_paydowns = get_principal_interest_paydowns(borrowed_amount,borrowing_time,smm,interest_rate)
        from bokeh.plotting import figure

        # Create a Bokeh plot
        p = figure(outer_width=1200, outer_height=1200,width=1200)

        # Data for the bar plot
        x = list(range(1,borrowing_time*12+1))
        top1 = prin_paydowns
        top2 = ir_paydowns

        # Add the first set of bars to the plot
        p.vbar(x=x, width=0.4, bottom=0, top=top1, color="firebrick")

        # Shift the x values for the second set of bars
        x2 = [x_val + 0.4 for x_val in x]

        # Add the second set of bars to the plot
        p.vbar(x=x2, width=0.4, bottom=0, top=top2, color="navy")

        # Generate the HTML and JavaScript for the plot
        script, div = components(p)
        return render_template("bokeh_plot.html", title="Simple Bokeh plot", script=script, div=div)
    return render_template("generic_form.html",title="Mortgage", form=form)