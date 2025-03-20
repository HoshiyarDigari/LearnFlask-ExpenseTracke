from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from utils.categorizer import suggest_category
from models import db, Expense
import os

#flask app 
app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'expenses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

#route for home page
@app.route('/')
def index():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return render_template('index.html', current_time=current_time, expenses=expenses)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        amount = float(request.form['amount'])
        description = request.form['description']
        category = request.form['category']
        
        expense = Expense(
            amount=amount,
            description=description,
            category=category
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return redirect(url_for('index'))
    except ValueError:
        error = "Please enter a valid amount"
        expenses = Expense.query.order_by(Expense.date.desc()).all()
        return render_template('index.html', error=error, current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), expenses=expenses)

@app.route('/suggest_category', methods=['POST'])
def get_category_suggestion():
    description = request.form.get('description', '')
    if len(description) < 3:
        return jsonify({'suggestion': None})
    
    category, confidence = suggest_category(description)
    if confidence > 0.3:  # Lowered threshold from 0.5 to 0.3
        return jsonify({
            'suggestion': category,
            'confidence': round(confidence * 100, 1)
        })
    return jsonify({'suggestion': None})

if __name__ == '__main__':
    app.run(debug=True, port=8004)
    