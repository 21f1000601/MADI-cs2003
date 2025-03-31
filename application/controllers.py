#App Routes
from flask import Flask, render_template,request, jsonify
from flask import current_app as app
from flask import flash, redirect, url_for
from .models import *
from sqlalchemy import func, or_
from datetime import datetime
import sqlite3
import json 
import os
from werkzeug.utils import secure_filename

# Define the upload folder
UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = {'jpg'}

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check if a file is allowed based on its extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS






@app.route("/")
def index(): 
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register(): 
    success_message = None
    error_message = None
    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("password")
        fullname = request.form.get("fullname")
        address = request.form.get("address")
        phonenumber = request.form.get("phonenumber")
        
        pin = request.form.get("pincode")
        print(email, pwd, fullname, address, phonenumber, pin)
        try:
            # Attempt to create and add the new customer to the database
            new_customer = Customer(email=email, password=pwd, fullname=fullname, phone_number=phonenumber, pincode=pin, address=address)
            db.session.add(new_customer)
            db.session.commit()

            # Set success message if everything went fine
            success_message = "Registration successful! Please login now"
            flash("Status updated successfully", "success")  # Add a success message

        except Exception as e:
            # Set error message if something went wrong
            error_message = f"An error occurred: Please try again... "
    return render_template("register.html", success_message=success_message, error_message=error_message)


@app.route("/service-signup", methods=["POST", "GET"])
def  service_signup():  
    success_message = None
    error_message = None
    categories = db.session.query(Service.category_name).distinct().all()
    enumerated_categories = list(enumerate(categories, start=1)) 
    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("password")
        fullname = request.form.get("fullname")
        address = request.form.get("address")
        phonenumber = request.form.get("phonenumber")
        experience = request.form.get("experience")
        service_type = request.form.get("category_name")

        pin = request.form.get("pincode")
        print(email, pwd, fullname, address, phonenumber, pin)
        # file=request.files["file_upload"]
        # url=""
        # if file.filename:
        #     file_name=secure_filename(file.filename) #Verification of the file is done
        #     url='./uploaded_files/'+vname+"_"+file_name
        #     file.save(url)

        try:
            # Attempt to create and add the new customer to the database
            new_prof = ServiceProfessional(email=email, password=pwd, fullname=fullname, phone_number=phonenumber, address=address,experience=experience, service_type=service_type)
            db.session.add(new_prof)
            db.session.commit()

            # Set success message if everything went fine
            success_message = "Registration successful! Please login now"
        except Exception as e:
            # Set error message if something went wrong
            error_message = f"An error occurred: Please try again..."
            print(e)
    return render_template("service-signup.html", success_message=success_message, error_message=error_message, categories=enumerated_categories)


@app.route("/login", methods=["GET", "POST"])
def login():   
    error_message=None
                                                 #LOGIN MANAGEMENT
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("password")

        # Admin login verfication
        admin = Admin.query.filter_by(admin_id=uname).first()
        if admin and admin.password == pwd: 
            return redirect(url_for('admin_login',id=uname))

        # Professional login verfication
        professional = ServiceProfessional.query.filter_by(email=uname).first()
        if professional and professional.password == pwd:
            # serv = Service.query.filter_by(service_id=professional.service_type).first()
            return redirect(url_for('prof_login',id=professional.professional_id))

        # Customer login verfication
        customer = Customer.query.filter_by(email=uname).first()
        if customer and customer.password == pwd:
            return redirect(url_for('customer_login',id=customer.customer_id))

    
        else:
            error_message = f"Invalid credentials: Please try again..."

    return render_template("login.html",error_message=error_message)

@app.route("/admin/dashboard/search", methods=["GET", "POST"])
def admin_search():
    if request.method == "POST":
        search_txt = request.form.get("query")
        search_by = request.form.get("column")
    print(search_txt)
    print(search_by)
    # Fetching all data from the database
    customers = Customer.query.all() 
    profs = ServiceProfessional.query.all() 
    servs = Service.query.all()
    reqs = ServiceRequest.query.order_by(ServiceRequest.date_of_request.desc()).all()

    # Search logic based on the selected column
    if search_by == "Services" and search_txt:
        servs = [
            service for service in servs
            if search_txt.lower() in service.service_name.lower()
        ]
        print('s')

    elif search_by == "Professionals" and search_txt:
        profs = [
            professional for professional in profs
            if search_txt.lower() in professional.fullname.lower()
        ]
        print('s2')


    elif search_by == "Customers" and search_txt:
        customers = [
            customer for customer in customers
            if search_txt.lower() in customer.fullname.lower()
        ]
    
        print(customers)

    # Returning the filtered data to the template
    # return render_template(
    #     'admindash.html',
    #     services=services,
    #     professionals=professionals,
    #     customers=customers,
    #     service_requests=service_requests
    # )
    return render_template("dash_admin.html", customers=customers, profs=profs, s=Service, sm=ServiceMap, servs=servs, reqs=reqs, p=ServiceProfessional, c=Customer)


@app.route("/admin/dashboard", methods=["GET", "POST"])              # ADMIN DASHBOARD
def admin_login(): 
    admin_id = request.args.get("id")
    status = request.args.get("status")
    if request.method=="POST":
        id=request.form.get("cust_id")
        v=request.form.get("todo")
        cust=Customer.query.filter_by(customer_id=id).first()
        if v=="block":
            cust.status=0
            db.session.commit()
            return redirect(url_for("admin_login", id=admin_id, message='customer_blocked'))
        elif v=="unblock":
            cust.status=1
            db.session.commit()
            return redirect(url_for("admin_login", id=admin_id, message='customer_unblocked'))
        elif v=="canc_req":
            c_id=request.form.get("cust_id")
            r_id=request.form.get("req_id")
            req=ServiceRequest.query.filter_by(request_id=r_id).first()
            req.service_status=-1
            db.session.commit()
            print(c_id, r_id)
            return redirect(url_for("admin_login", id=admin_id))

        

    
    categories = db.session.query(Service.category_name).distinct().all()
    enumerated_categories = list(enumerate(categories, start=1)) 
    customers = Customer.query.all() 
    profs = ServiceProfessional.query.all() 
    servs = Service.query.all()
    reqs = ServiceRequest.query.order_by(ServiceRequest.date_of_request.desc()).all()

    print(servs)
    return render_template("dash_admin.html", customers=customers, profs=profs, s=Service, sm=ServiceMap, servs=servs, reqs=reqs, p=ServiceProfessional, c=Customer,categories=enumerated_categories)



@app.route("/professional/profile", methods=["GET", "POST"])             # PROFESSIONAL DASHBOARD
def prof_profile(): 
    id = request.args.get("id")
    professional = ServiceProfessional.query.filter_by(professional_id=id).first()

    serv_cat = ServiceMap.query.filter_by(id=professional.service_type).first()

    if request.method=="POST":
        professional.fullname=request.form.get("fullname")
        professional.email=request.form.get("email")
        professional.phone_number=request.form.get("phone_number")
        professional.address=request.form.get("address")
        professional.experience=request.form.get("experience")

        db.session.commit()
    serv = Service.query.filter_by(service_id=professional.service_type).first()

    if professional.profile_status != 1:
        return render_template("dash_professional_inactive.html", prof=professional, serv_cat=serv_cat)

    return render_template("profile_professional.html", prof=professional, serv_cat=serv_cat)


@app.route("/customer/dashboard", methods=["GET", "POST"])   
def customer_login():
    id = request.args.get("id")
    print(id)
    servs = Service.query.all()
   

    success = request.args.get("success")

    # Customer login
    customer = Customer.query.filter_by(customer_id=id).first()
    reqs = ServiceRequest.query.filter(
        ServiceRequest.customer_id == customer.customer_id,
        ServiceRequest.service_status.in_([0, 1])
    ).order_by(ServiceRequest.date_of_request.desc()).all()

    return render_template("dash_customer.html", servs=servs, cust=customer,reqs=reqs,s=Service,success=success,p=ServiceProfessional)


@app.route("/professional/dashboard", methods=["GET", "POST"])             # PROFESSIONAL DASHBOARD
def prof_login(): 
    id = request.args.get("id")
    
    print(id)
      # Professional login
    professional = ServiceProfessional.query.filter_by(professional_id=id).first()

    serv_cat = ServiceMap.query.filter_by(id=professional.service_type).first()

    potential_services = Service.query.filter_by(service_category=professional.service_type).all()

    # Extract IDs from your list of Service objects
    service_ids = [service.service_id for service in potential_services]
    print(service_ids)


    

    avail_reqs = ServiceRequest.query.filter(
        ServiceRequest.service_id.in_(service_ids),
        ServiceRequest.professional_id == None,
        ServiceRequest.service_status == 0
    ).order_by(ServiceRequest.date_of_request).all()

    
    
    

    
    
    
    my_reqs = ServiceRequest.query.filter_by(professional_id=professional.professional_id, service_status=1).order_by(ServiceRequest.date_of_request.desc()).all()
    closed_reqs = ServiceRequest.query.filter(
        ServiceRequest.professional_id == professional.professional_id,
        ServiceRequest.service_status.in_([9, -1])
    ).order_by(ServiceRequest.date_of_request.desc()).all()

    if professional.profile_status != 1:
        return render_template("dash_professional_inactive.html", prof=professional, serv_cat=serv_cat)

    return render_template("dash_professional.html", prof=professional, serv_cat=serv_cat, avail_reqs=avail_reqs, my_reqs=my_reqs, s=Service, c=Customer, closed_reqs=closed_reqs)

@app.route("/professional/my_services", methods=["GET", "POST"])             # PROFESSIONAL DASHBOARD
def prof_services(): 
    id = request.args.get("id")

    print(id)
      # Professional login
    professional = ServiceProfessional.query.filter_by(professional_id=id).first()
    serv_cat = ServiceMap.query.filter_by(id=professional.service_type).first()

    serv = Service.query.filter_by(service_id=professional.service_type).first()
    avail_reqs = ServiceRequest.query.filter_by(service_id=professional.service_type,professional_id=None, service_status=0).order_by(ServiceRequest.date_of_request).all()
    my_reqs = ServiceRequest.query.filter_by(professional_id=professional.professional_id, service_status=1).order_by(ServiceRequest.date_of_request.desc()).all()
    closed_reqs = ServiceRequest.query.filter(
        ServiceRequest.professional_id == professional.professional_id,
        ServiceRequest.service_status.in_([9, -1])
    ).order_by(ServiceRequest.date_of_request.desc()).all()

    if professional.profile_status != 1:
        return render_template("dash_professional_inactive.html", prof=professional, serv_cat=serv_cat)
    serc = ServiceRequest.query.filter_by(professional_id=professional.professional_id).order_by(ServiceRequest.date_of_request.desc())

    if request.args.get("search")=='1':
        col=request.args.get("col")
        query=request.args.get("query")
        print(col, query)

         # Apply search filter based on selected column
        if col == 'name':
            # Search by Service Name
            serc = serc.join(Service).filter(Service.service_name.ilike(f"%{query}%")).all()
        
        
        elif col == 'customer':
            # Search by Customer Name
            serc = serc.join(Customer).filter(Customer.fullname.ilike(f"%{query}%")).all()
        
        elif col == 'status':
            # Search by Status
            serc = serc.filter(ServiceRequest.service_status==query).all()
        
        
        elif col == 'rating':
            # Search by Rating
            try:
                rating_value = float(query)
                if 1 <= rating_value <= 5:
                    serc = serc.filter(ServiceRequest.rating == rating_value)
                else:
                    flash("Rating must be between 1 and 5.", "danger")
            except ValueError:
                flash("Invalid rating format. Provide a number between 1 and 5.", "danger")
        print(serc)

    return render_template("req_professional.html", prof=professional, serv=serv, avail_reqs=avail_reqs, my_reqs=my_reqs, s=Service, c=Customer, closed_reqs=closed_reqs, serc=serc)



@app.route("/professional/search", methods=["POST"])             # PROFESSIONAL DASHBOARD
def prof_search(): 
    id = request.args.get("id")
    col = request.form.get("column")
    query = request.form.get("query")
    professional = ServiceProfessional.query.filter_by(professional_id=id).first()
    serv_cat = ServiceMap.query.filter_by(id=professional.service_type).first()

    if professional.profile_status != 1:
        return render_template("dash_professional_inactive.html", prof=professional,serv_cat=serv_cat)

    return redirect(url_for('prof_services', id=id, search=1, col=col, query=query))



@app.route("/customer/search", methods=["POST"])             # PROFESSIONAL DASHBOARD
def cust_search(): 
    id = request.args.get("id")
    col = request.form.get("column")
    query = request.form.get("query")
    professional = ServiceProfessional.query.filter_by(professional_id=id).first()

    if professional.profile_status != 1:
        return render_template("dash_professional_inactive.html", prof=professional)

    return redirect(url_for('req_customer', id=id, search=1, col=col, query=query))

@app.route("/customer/my_requests", methods=["GET", "POST"])   
def req_customer():
    id = request.args.get("id")
    print(id)
    servs = Service.query.all()
    success = request.args.get("success")

    # Customer login
    customer = Customer.query.filter_by(customer_id=id).first()
    open_reqs = ServiceRequest.query.filter(
        ServiceRequest.customer_id == customer.customer_id,
        ServiceRequest.service_status.in_([0, 1])
    ).order_by(ServiceRequest.date_of_request.desc()).all()
    closed_reqs = ServiceRequest.query.filter(
        ServiceRequest.customer_id == customer.customer_id,
        ServiceRequest.service_status.in_([-1, 9])
    ).order_by(ServiceRequest.date_of_request.desc()).all()

    serc = ServiceRequest.query.filter_by(customer_id=id).order_by(ServiceRequest.date_of_request.desc())


    if request.args.get("search")=='1':
        col=request.args.get("col")
        query=request.args.get("query")
        print(col, query)

         # Apply search filter based on selected column
        if col == 'name':
            # Search by Service Name
            serc = serc.join(Service).filter(Service.service_name.ilike(f"%{query}%")).all()
        
        
        elif col == 'professional':
            # Search by Customer Name
            serc = serc.join(ServiceProfessional).filter(ServiceProfessional.fullname.ilike(f"%{query}%")).all()
        
        elif col == 'status':
            # Search by Status
            serc = serc.filter(ServiceRequest.service_status==query).all()
        
        
        print(serc)


    return render_template("req_customer.html", servs=servs, cust=customer,open_reqs=open_reqs,closed_reqs=closed_reqs,s=Service,success=success,p=ServiceProfessional, serc=serc)

@app.route("/customer/profile", methods=["GET", "POST"])             # CUSTOMER DASHBOARD
def customer_profile(): 

    id = request.args.get("id")
    print(id)
    servs = Service.query.all()
    success = request.args.get("success")

    # Customer login
    customer = Customer.query.filter_by(customer_id=id).first()


    if request.method=="POST":
        customer.fullname=request.form.get("fullname")
        customer.email=request.form.get("email")
        customer.phone_number=request.form.get("phone_number")
        customer.address=request.form.get("address")
        customer.pincode=request.form.get("pincode")
        db.session.commit()

    reqs = ServiceRequest.query.filter_by(customer_id=customer.customer_id).order_by(ServiceRequest.date_of_request.desc()).all()

    return render_template("profile_cust.html", servs=servs, cust=customer,reqs=reqs,s=Service,success=success,p=ServiceProfessional)



@app.route("/add_service", methods=["POST", "PUT"])
def add_service():
    if request.method == "POST":
        # Get form data
        serv_name = request.form.get("service_name")
        cat = request.form.get("category_name")
        price = request.form.get("base_price")
        desc = request.form.get("description")
        time = request.form.get("time-required")
        file = request.files.get("image_file")  # File input field name
        
        if(file):
            print("File Found")

        # Validate and save the uploaded file
        if file and allowed_file(file.filename):
            # Use the service name as the file name
            filename = f"{serv_name}.jpg"  # Append .jpg extension
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        else:
            return redirect(url_for('admin_login', message='file_upload_error'))

        try:
            if cat!='-1':
                print(cat)
                cat_id = ServiceMap.query.filter_by(name=cat).first().id

                new_service = Service(service_name=serv_name, category_name=cat,service_category=cat_id, base_price=price, description=desc, time_required=time)
            else:
                
                cat = request.form.get("new_category")
                new_cat = ServiceMap(name=cat)
                db.session.add(new_cat)
                cat_id = ServiceMap.query.filter_by(name=cat).first().id
                # print(cat_id)
                new_service = Service(service_name=serv_name, category_name=cat,service_category=cat_id, base_price=price, description=desc, time_required=time)
            db.session.add(new_service)
                        
            db.session.commit()
            
            return redirect(url_for('admin_login', message='service_creation_success'))
        except Exception as e:
            print(e)
            return redirect(url_for('admin_login', message='service_creation_error'))
        

@app.route("/update_service", methods=["POST", "PUT"])
def update_service():
    if request.method == "POST":
        # Get form data
        serv_name = request.form.get("service_name")
        serv_id = request.form.get("service_id")
        cat = request.form.get("category")
        price = request.form.get("base_price")
        desc = request.form.get("description")
        time = request.form.get("time-required")
        file = request.files.get("image_file")  # File input field name

        print(request.files)
        if(file):
            print("File FOund")

        # Validate and save the uploaded file
        if file and allowed_file(file.filename):
            # Use the service name as the file name
            filename = f"{serv_name}.jpg"  # Append .jpg extension
            print(filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
       

        try:
            service = Service.query.filter_by(service_id=serv_id).first()
            service.service_name=serv_name
            service.service_category=cat
            service.base_price=price
            service.description=desc
            service.time_required=time
            db.session.commit()
            
            return redirect(url_for('admin_login', message='service_updation_success'))
        except Exception as e:
            return redirect(url_for('admin_login', message='service_updation_error'))


@app.route("/update_status", methods=["PUT"])
def update_status():
    data_json = request.get_json()
    print(data_json)
    if not data_json:
        return jsonify({'error': 'Invalid or missing data'}), 400



    if data_json.get('type')=="status_prof":
        professional_id = data_json.get('professional_id')
        new_status = data_json.get('new_status')
        professional = ServiceProfessional.query.filter_by(professional_id=professional_id).first()
        
        professional.profile_status = new_status
        db.session.commit()
        if new_status == 9:
        # Return a JSON response to indicate success
            return jsonify({'message': 'Profile status updated successfully.... Person Blocked'}), 200
        elif new_status == 1:
            return jsonify({'message': 'Profile status updated successfully.... Person Unblocked'}), 200
        


    elif  data_json.get('type')=="del_service":
        try:
            serv_id = data_json.get('service_id')
            serv = Service.query.filter_by(service_id=serv_id).first()
            cat = ServiceMap.query.filter_by(name=serv.category_name).first()



            # count = db.session.query(func.count(func.distinct(Service.category_name))).scalar() + 1
            cat_count = Service.query.filter_by(category_name=serv.category_name).count()
            print("no",cat_count)
            print("1",cat)
            image_filename = serv.service_name
            if serv:
                if image_filename:
                    file_path = os.path.join('static', 'images', image_filename)
                    
                    # Check if the file exists before trying to delete it
                    if os.path.exists(file_path):
                        os.remove(file_path)  # Delete the file
                        print(f"File {image_filename} deleted successfully.")
                    else:
                        print(f"File {image_filename} not found.")
                
                db.session.delete(serv)
                if cat_count==1:
                    db.session.delete(cat)
                #  Exception as ex:
                db.session.commit()  
                print("1",cat)

                return jsonify({'message': 'Service deleted successfully....'}), 200
        except Exception as e:
            
            return jsonify({'error': 'ERROR: Service still in use ....\nPlease make sure the{0} service is not in use'.format(e)}), 200

    return jsonify({'error': 'Professional not found'}), 404

@app.route("/customer/book_service", methods=["POST"])
def book_service():
    if request.method=="POST":

        serv_id = request.form.get("service_id")
        price = request.form.get("price")
        cust_email= request.form.get("email")
        cat = request.form.get("service_category")
        customer = Customer.query.filter_by(email=cust_email).first()
        serv = Service.query.filter_by(service_id=serv_id).first()

        print(serv_id, price, cat, cust_email)
        return render_template("book_conf.html", serv=serv, cust=customer)

        
@app.route("/customer/confirm_booking", methods=["POST"])
def conf_book():
    if request.method=="POST":
        serv_id = request.form.get("service_id")
        cust_email= request.form.get("email")
        customer = Customer.query.filter_by(email=cust_email).first()
        date=datetime.today()


        # print(serv_id, uname, cat, cust_email, date, reqs)
        try:
            new_request = ServiceRequest(service_id=serv_id, customer_id=customer.customer_id, date_of_request=date)    
            db.session.add(new_request)
            db.session.commit()
            return redirect(url_for('customer_login',id=customer.customer_id,success=1))

        except Exception as e:
            print(e)
            return redirect(url_for('customer_login',id=customer.customer_id,success=0))




        
@app.route("/update_request", methods=["PUT", "POST"])
def update_request():
    if request.method=="POST":
        req_id=request.form.get("req_id")
        cust_id=request.form.get("customer_id")
        rating=request.form.get("rating")
        remarks=request.form.get("feedback")
        req = ServiceRequest.query.filter_by(request_id=req_id).first()
        req.rating=rating
        avg_rating = db.session.query(
            func.avg(ServiceRequest.rating)
        ).filter(
            ServiceRequest.professional_id == req.professional_id  # Replace with the specific professional's ID
        ).scalar()
        professional = ServiceProfessional.query.filter_by(professional_id=req.professional_id).first()
        professional.rating=avg_rating
        req.remarks=remarks
        db.session.commit()

        # print(serv_id, rating, remarks)
        return redirect(url_for('req_customer',id=cust_id))
    data_json = request.get_json()
    # print(data_json)
    if not data_json:
        return jsonify({'error': 'Invalid or missing data'}), 400



    if data_json.get('type')=="accept_request":
        professional_id = data_json.get('professional_id')
        request_id = data_json.get('request_id')
        print(professional_id, request_id)


        try:
            req = ServiceRequest.query.filter_by(request_id=request_id).first()
            req.professional_id=professional_id
            req.service_status=1
            db.session.commit()
            return jsonify({'message': 'Service Request accepted successfully.... '}), 200

        except:
            return jsonify({'message': 'Failed, try again later.... '}), 200
        


    if data_json.get('type')=="complete_request":
            request_id = data_json.get('request_id')
            print(request_id)


            try:
                req = ServiceRequest.query.filter_by(request_id=request_id).first()
                req.service_status=9
                req.date_of_completion=datetime.today()
                db.session.commit()
                return jsonify({'message': 'Service Request Completed successfully.... '}), 200

            except:
                return jsonify({'message': 'Failed, try again later.... '}), 200
            

    if data_json.get('type')=="cancel_request":
            request_id = data_json.get('request_id')
            print( request_id)


            try:
                req = ServiceRequest.query.filter_by(request_id=request_id).first()
                req.service_status=-1
                req.date_of_completion=datetime.today()

                db.session.commit()
                return jsonify({'message': 'Service Request Cancelled successfully.... '}), 200

            except:
                return jsonify({'message': 'Failed, try again later.... '}), 200



       
    return jsonify({'error': 'Service Request not found'}), 404

        
@app.route("/submit", methods=["POST"])
def submit_review():
    rating = request.form.get('rating')
    feedback = request.form.get('feedback')
    cust = request.form.get('cust_id')
    req_id = request.form.get('req_id')

    
    try:
        req = ServiceRequest.query.filter_by(request_id=req_id).first()
        req.remarks=feedback
        req.rating=rating
        db.session.commit()
        return jsonify({'message': 'Review submitted successfully.... '}), 200

    except:
        return jsonify({'message': 'Failed, try again later.... '}), 200



