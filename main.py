import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class StockData:
    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol

    def get_stock_data(self):
        url = f"https://www.google.com/finance/quote/{self.stock_symbol}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        stock_price = soup.find('div', class_='YMlKec fxKbKc').text

        return stock_price


class PortfolioTracker:
    def __init__(self, stocks, initial_investment):
        self.stocks = stocks
        self.initial_investment = initial_investment
        self.portfolio_returns = pd.DataFrame()

    def track_portfolio(self):
        for stock in self.stocks:
            stock_price = float(stock.get_stock_data().replace('$', '').replace(',', ''))
            stock_volume = self.get_stock_volume(stock.stock_symbol)
            # Calculate portfolio returns
            portfolio_value = stock_price * stock_volume
            self.portfolio_returns[stock.stock_symbol] = [portfolio_value]

        # Calculate total portfolio value
        self.portfolio_returns['Total Portfolio Value'] = self.portfolio_returns.sum(axis=1)

        return self.portfolio_returns

    def visualize_returns(self):
        plt.plot(self.portfolio_returns.index, self.portfolio_returns['Total Portfolio Value'])
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.title('Portfolio Returns')
        plt.show()

    def get_stock_volume(self, stock_symbol):
        # Retrieve stock volume data
        # Placeholder implementation
        return 1000


class NotificationSystem:
    def __init__(self, email_address, email_password):
        self.email_address = email_address
        self.email_password = email_password

    def send_email_notification(self, recipient_email, subject, message):
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email_address, self.email_password)
        server.send_message(msg)
        server.quit()

    def send_sms_notification(self, phone_number, message):
        # Send SMS notification using messaging API
        # Placeholder implementation
        pass


# Example usage
stock_symbols = ['AAPL', 'GOOG', 'MSFT']
stocks = [StockData(symbol) for symbol in stock_symbols]
portfolio_tracker = PortfolioTracker(stocks, 100000)
portfolio_returns = portfolio_tracker.track_portfolio()
portfolio_tracker.visualize_returns()

notification_system = NotificationSystem('your_email@gmail.com', 'email_password')
notification_system.send_email_notification('recipient_email@gmail.com', 'Stock Market Update',
                                             'Your portfolio has performed well.')
notification_system.send_sms_notification('phone_number', 'Your portfolio has performed well.')