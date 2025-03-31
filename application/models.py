# Data Models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import CheckConstraint, LargeBinary
db = SQLAlchemy()

# Admin Table
class Admin(db.Model):
    __tablename__ = "admin"
    admin_id = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)


# Customer Table
class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer, nullable =False)
    address = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=True)  

    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='customer', lazy=True)

class ServiceMap(db.Model):
    __tablename__ = 'service_map'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)

    service_professionals = db.relationship('ServiceProfessional', backref='service_professional', lazy=True)
    service_category = db.relationship('Service', backref='service', lazy=True)

# Service Professional Table
class ServiceProfessional(db.Model):
    __tablename__ = 'service_professionals'
    professional_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Add autoincrement=True    password = db.Column(db.String, nullable=False)
    fullname = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True,nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    experience = db.Column(db.String, nullable=False)
    service_type = db.Column(db.Integer, db.ForeignKey('service_map.id'), nullable=False)
    profile_status = db.Column(db.Integer, nullable=False, default=False)  
    rating = db.Column(db.Float, nullable=False, default=0.0)
    document = db.Column(LargeBinary, nullable=True)  # Column for storing PDF data

    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='service_professional', lazy=True)



# Service Table
class Service(db.Model):
    __tablename__ = 'services'
    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String, nullable=False, unique=True)
    service_category = db.Column(db.Integer, db.ForeignKey('service_map.id'),autoincrement=True ,nullable=False)
    category_name = db.Column(db.String, nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    time_required = db.Column(db.Integer, nullable=False) 

    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='service', lazy=True)


# Service Request Table
class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    request_id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professionals.professional_id'))
    date_of_request = db.Column(db.DateTime, nullable=False)
    date_of_completion = db.Column(db.DateTime)
    service_status = db.Column(db.String, nullable=False, default=0)
    remarks = db.Column(db.String)
    rating = db.Column(db.Integer, CheckConstraint('rating BETWEEN 1 AND 5'), nullable=True)


