from django.shortcuts import render

from yahoo_fin.stock_info import tickers_nifty50


def stock_list(request):
    stocks = tickers_nifty50()
    return render(request, "stock_list.html", context={"stocks": stocks})


def stock_live_data(request):
    user_selected_stocks = request.GET.getlist("stockpicker")
    return render(
        request,
        "stock_tracker.html",
        context={"user_selected_stocks": user_selected_stocks},
    )
