from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import io
import json
from django.http import HttpResponse, JsonResponse
# from weasyprint import HTML
import tempfile
from datetime import datetime
import jdatetime
import base64
from django.contrib.staticfiles import finders
import os
from django.conf import settings

# New
from django.contrib.auth.decorators import login_required
from io import BytesIO
from myapp.models import Sales, Customer, Shipments
import traceback
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.core.serializers import serialize


@csrf_exempt
def invoice_page(request):
    return render(request, 'invoice.html')


# @csrf_exempt
# def havaleh(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
            
#             # Convert the current UTC time to Jalali
#             current_time = datetime(2025, 5, 8, 13, 23, 21)  # Your provided timestamp
#             jalali_datetime = jdatetime.datetime.fromgregorian(datetime=current_time)
#             persian_date = jalali_datetime.strftime('%Y/%m/%d')  # Format as YYYY/MM/DD in Persian
            
#             # Calculate total weight
#             total_weight = 0
#             for item in data.get('items', []):
#                 try:
#                     total_weight += float(item.get('weight', 0))
#                 except (ValueError, TypeError):
#                     pass

#             context = {
#                 'date': persian_date,  # Use the Persian date here
#                 'serial': data.get('serial', ''),
#                 'items': data.get('items', []),
#                 'total_weight': f"{total_weight:,.0f}",
#                 'note': data.get('note', ''),
#             }

#             # Generate HTML
#             html_string = render_to_string('havaleh.html', context)
            
#             # Create PDF using WeasyPrint with base_url for static files
#             html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
#             pdf = html.write_pdf()
            
#             # Return the PDF
#             response = HttpResponse(pdf, content_type='application/pdf')
#             response['Content-Disposition'] = f'attachment; filename=havaleh_{data.get("serial", "")}.pdf'
#             return response

#         except Exception as e:
#             print(f"Error: {str(e)}")  # For debugging
#             return JsonResponse({
#                 'error': f'Server Error: {str(e)}',
#                 'status': 'error'
#             }, status=500)


@csrf_exempt
def havaleh(request):
    """Generate a PDF for the havaleh (delivery form)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is supported'}, status=405)
    
    try:
        # Parse the JSON data from the request
        data = json.loads(request.body)
        
        # Get all the form data
        date = data.get('date', '')
        serial = data.get('serial', '')
        items = data.get('items', [])
        note = data.get('note', '')
        invoice_id = data.get('invoice_id')
        driver_name = data.get('driver_name', '')  # Get driver name
        plate_number = data.get('plate_number', '')  # Get plate number
        
        # Process date using PersianDateText if available
        persian_date = date
        try:
            # Import here to avoid circular imports
            from invoice.utils import PersianDateText
            
            # Parse date if it's in format like "1403/03/15"
            if date and '/' in date:
                date_parts = date.split('/')
                if len(date_parts) == 3:
                    persian_date_obj = PersianDateText(date_parts)
                    persian_date = persian_date_obj.to_text()
        except Exception as e:
            print(f"Error processing Persian date: {e}")
            # Continue with original date
        
        # Calculate total weight and convert weights to Persian text
        total_weight = 0
        processed_items = []
        
        for item in items:
            weight = float(item.get('weight', 0))
            total_weight += weight
            
            # Create a copy of the item with Persian weight
            item_copy = item.copy()
            
            # Format weight with commas
            weight_persian = f"{weight:,.0f}"
            item_copy['weight_persian'] = weight_persian
            
            processed_items.append(item_copy)
        
        # Format total weight with Persian numerals
        total_weight_persian = f"{total_weight:,.0f}"
        
        # Prepare context for template
        context = {
            'date': date,
            'persian_date': persian_date,
            'serial': serial,
            'items': processed_items,
            'note': note,
            'total_weight': f"{total_weight:,.0f}",
            'total_weight_persian': total_weight_persian,
            'driver_name': driver_name,  # Add driver name to context
            'plate_number': plate_number  # Add plate number to context
        }
        
        # If invoice_id is provided, update the related Invoice record
        if invoice_id:
            try:
                # Import Invoice model here to avoid circular imports
                from invoice.models import Invoice
                
                # Find the invoice
                invoice = Invoice.objects.get(id=invoice_id)
                
                # Mark as havaleh generated
                invoice.havaleh_generated = True
                invoice.havaleh_date = timezone.now()
                invoice.havaleh_serial = serial
                invoice.save()
                
                # Log in comments field of the sale
                sale = invoice.sale
                havaleh_info = f"Havaleh created on {timezone.now()} with serial: {serial}"
                if sale.comments:
                    sale.comments += f"\n{havaleh_info}"
                else:
                    sale.comments = havaleh_info
                sale.save(update_fields=['comments'])
                
            except Exception as e:
                print(f"Error updating Invoice record: {e}")
                # Continue to generate PDF
        
        # Render the HTML template
        html_string = render_to_string('havaleh.html', context)
        
        # Create PDF with WeasyPrint
        html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
        
        # Create a BytesIO object to store the PDF
        pdf_file = BytesIO()
        
        # Write the PDF to the BytesIO object
        html.write_pdf(pdf_file)
        
        # Get the value of the BytesIO object
        pdf_file.seek(0)
        pdf_content = pdf_file.getvalue()
        
        # Create HTTP response with PDF
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="havaleh_{serial}.pdf"'
        response['Content-Length'] = len(pdf_content)
        
        return response
        
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def havaleh_pdf(request):
    """Generate a PDF for the havaleh (delivery form)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is supported'}, status=405)
    
    try:
        # Parse the JSON data from the request
        data = json.loads(request.body)
        
        # Get all the form data
        date = data.get('date', '')
        serial = data.get('serial', '')
        items = data.get('items', [])
        note = data.get('note', '')
        invoice_id = data.get('invoice_id')
        
        # Process date using PersianDateText if available
        persian_date = date
        try:
            # Import here to avoid circular imports
            from invoice.utils import PersianDateText
            
            # Parse date if it's in format like "1403/03/15"
            if date and '/' in date:
                date_parts = date.split('/')
                if len(date_parts) == 3:
                    persian_date_obj = PersianDateText(date_parts)
                    persian_date = persian_date_obj.to_text()
        except Exception as e:
            print(f"Error processing Persian date: {e}")
            # Continue with original date
        
        # Calculate total weight and convert weights to Persian text
        total_weight = 0
        processed_items = []
        
        for item in items:
            weight = float(item.get('weight', 0))
            total_weight += weight
            
            # Create a copy of the item with Persian weight
            item_copy = item.copy()
            
            # Format weight with commas
            weight_persian = f"{weight:,.0f}"
            item_copy['weight_persian'] = weight_persian
            
            processed_items.append(item_copy)
        
        # Format total weight with Persian numerals
        total_weight_persian = f"{total_weight:,.0f}"
        
        # Prepare context for template
        context = {
            'date': date,
            'persian_date': persian_date,
            'serial': serial,
            'items': processed_items,
            'note': note,
            'total_weight': f"{total_weight:,.0f}",
            'total_weight_persian': total_weight_persian
        }
        
        # If invoice_id is provided, update the related Invoice record
        if invoice_id:
            try:
                # Import Invoice model here to avoid circular imports
                from invoice.models import Invoice
                
                # Find the invoice
                invoice = Invoice.objects.get(id=invoice_id)
                
                # Mark as havaleh generated
                invoice.havaleh_generated = True
                invoice.havaleh_date = timezone.now()
                invoice.havaleh_serial = serial
                invoice.save()
                
                # Log in comments field of the sale
                sale = invoice.sale
                havaleh_info = f"Havaleh created on {timezone.now()} with serial: {serial}"
                if sale.comments:
                    sale.comments += f"\n{havaleh_info}"
                else:
                    sale.comments = havaleh_info
                sale.save(update_fields=['comments'])
                
            except Exception as e:
                print(f"Error updating Invoice record: {e}")
                # Continue to generate PDF
        
        # Render the HTML template
        html_string = render_to_string('havaleh.html', context)
        
        # Create PDF with WeasyPrint - using basic settings compatible with all versions
        html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
        pdf_file = html.write_pdf(presentational_hints=True)
        
        # Create HTTP response with PDF
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="havaleh_{serial}.pdf"'
        
        return response
        
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def havaleh(request):
    """Render the havaleh page which will load the latest pending invoice"""
    return render(request, 'havaleh_page.html')

@csrf_exempt
def sales_order(request):
    """Render the sales order page which will fetch and show the latest pending invoice"""
    # Just render the template, the Vue component will handle the data loading
    return render(request, 'SalesOrder.html')


@csrf_exempt
def confirm_sales_invoice(request, sales_id=None):
    """Confirm a sales invoice by setting its status to 'Sent'"""
    print(f"confirm_sales_invoice called with sales_id: {sales_id}")
    
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method is supported'}, status=405)
    
    try:
        # If sales_id is provided in the URL
        if sales_id:
            print(f"Looking for sale with ID: {sales_id}")
            sale = Sales.objects.get(id=sales_id)
        else:
            # Try to get sales_id from request body
            try:
                data = json.loads(request.body)
                sales_id = data.get('sales_id')
                print(f"Extracted sales_id from body: {sales_id}")
                if not sales_id:
                    return JsonResponse({'status': 'error', 'message': 'No sales_id provided'}, status=400)
                sale = Sales.objects.get(id=sales_id)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON in request body'}, status=400)
        
        print(f"Found sale: {sale}, current status: {sale.invoice_status}")
        
        # Only confirm if status is 'NA'
        if sale.invoice_status == 'NA':
            print("Updating status to 'Sent'")
            sale.invoice_status = 'Sent'
            sale.save()
            print("Sale saved successfully, status now:", sale.invoice_status)
            return JsonResponse({'status': 'success'})
        else:
            print(f"Cannot confirm: status is already {sale.invoice_status}")
            return JsonResponse({'status': 'error', 'message': f'Invoice already confirmed (status: {sale.invoice_status})'}, status=400)
    
    except Sales.DoesNotExist:
        print(f"Sales record not found for ID: {sales_id}")
        return JsonResponse({'status': 'error', 'message': 'Sales record not found'}, status=404)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
def create_test_sale(request):
    """Create a test sale entry with invoice_status='NA'"""
    try:
        from myapp.models import Sales, Customer
        
        print("Attempting to create a test sale")
        
        # First check if we can create a test customer
        try:
            # Try to find an existing customer
            customer = Customer.objects.first()
            if not customer:
                # If no customer exists, create a test one
                customer = Customer(
                    customer_name="Test Customer",
                    date=timezone.now(),
                    status='Active'
                )
                customer.save()
                print(f"Created test customer with ID: {customer.id}")
        except Exception as customer_e:
            print(f"Error with customer: {customer_e}")
            customer = None
        
        # Create a simple Sale entry with minimal fields
        sale_kwargs = {
            'invoice_status': 'NA',
            'date': timezone.now(),
            'price_per_kg': 1000,
            'total_price': 50000
        }
        
        # Use customer as ForeignKey if available
        if customer:
            sale_kwargs['customer_name'] = customer
        else:
            sale_kwargs['customer_name'] = "Test Customer (String)"
        
        sale = Sales(**sale_kwargs)
        sale.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Test sale created with ID: {sale.id}',
            'sale_id': sale.id
        })
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def latest_invoice(request):
    """Get the latest invoice from the database, regardless of status"""
    try:
        from invoice.models import Invoice
        
        # Get the latest invoice by creation date
        invoice = Invoice.objects.order_by('-created_at').first()
        
        if not invoice:
            return JsonResponse({'message': 'No invoices found'}, status=404)
        
        # Get the associated sale
        sale = invoice.sale
        
        # Prepare response data
        data = {
            'id': invoice.id,
            'sale_id': sale.id,
            'date': sale.date.isoformat() if sale.date else None,
            'customer_name': str(sale.customer_name),
            'invoice_number': getattr(sale, 'invoice_number', ''),
            'year': invoice.year,
            'month': invoice.month,
            'day': invoice.day,
            'is_paid': invoice.is_paid,
            'created_at': invoice.created_at.isoformat(),
            'list_of_reels': sale.list_of_reels,
            'width': sale.width,
            'net_weight': sale.net_weight
        }
        
        return JsonResponse(data)
    
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
    

def get_next_sales_invoice(request):
    # You may want to filter by user: e.g. username=request.user.username
    sales = Sales.objects.filter(invoice_status="NA").order_by('date').first()
    if not sales:
        return JsonResponse({'error': 'No pending sales'}, status=404)
    # Serialize required fields
    data = {
        'id': sales.id,
        'customer_name': sales.customer_name,
        'license_number': sales.license_number,
        # ...add all fields you need for the invoice
        'items': [],  # If you have related items, serialize them too
    }
    return JsonResponse(data)

@csrf_exempt
def confirm_sales_invoice(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sales_id = data.get('id')
        try:
            sales = Sales.objects.get(id=sales_id)
            if sales.invoice_status == "NA":
                sales.invoice_status = "Sent"
                sales.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Already confirmed.'}, status=400)
        except Sales.DoesNotExist:
            return JsonResponse({'error': 'Sales not found.'}, status=404)

def check_pending_invoice(request):

    """
    API endpoint to check if there's a pending invoice with 'NA' status.
    Returns JSON with:
    - has_pending: boolean indicating if a pending invoice exists
    - pending_id: ID of the pending invoice (if exists)
    """
    pending_invoice = Sales.objects.filter(invoice_status='NA').first()
    
    response_data = {
        'has_pending': pending_invoice is not None
    }
    
    if pending_invoice:
        response_data['pending_id'] = pending_invoice.id
    
    return JsonResponse(response_data)

@csrf_exempt
def get_last_10_sales(request):
    try:
        # Get last 10 outgoing shipments ordered by date and join with Sales and Products tables
        shipments = Shipments.objects.filter(
            shipment_type='Outgoing'
        ).select_related(
            'invoice'  # Join with Sales table through invoice field
        ).order_by('-date')[:15]
        
        sales_data = []

        for shipment in shipments:
            try:
                # Convert date to Jalali
                if isinstance(shipment.date, datetime):
                    gregorian_date = shipment.date
                    jdate = jdatetime.datetime.fromgregorian(datetime=gregorian_date)
                    formatted_date = jdate.strftime('%Y/%m/%d')
                else:
                    formatted_date = str(shipment.date)

                # Get items from list_of_reels
                items = []
                if shipment.list_of_reels:
                    try:
                        # Clean the JSON string before parsing
                        reels_str = shipment.list_of_reels.strip()
                        if reels_str.startswith('[') and reels_str.endswith(']'):
                            reels_list = json.loads(reels_str)
                            for reel in reels_list:
                                quantity = float(reel.get('quantity', 0))
                                price = float(shipment.price_per_kg or 0)
                                total = quantity * price
                                
                                # Get grammage and grade from Products table
                                from myapp.models import Products
                                product = Products.objects.filter(shipment_id=shipment.id).first()
                                gsm = product.gsm if product else None
                                grade = product.grade if product else None
                                
                                items.append({
                                    'description': reel.get('description', ''),
                                    'code': str(shipment.id),  # Use shipment ID as code
                                    'quantity': quantity,
                                    'unit': reel.get('unit', 'کیلو'),
                                    'gsm': gsm,  # Add grammage
                                    'type': grade,  # Add grade
                                    'price': price,
                                    'total': total,
                                    'net_weight': shipment.net_weight or '',
                                    'width': shipment.width or ''
                                })
                        else:
                            raise ValueError("Invalid JSON format")
                    except Exception as e:
                        # If list_of_reels is not valid JSON, use net_weight
                        quantity = float(shipment.net_weight or 0)
                        price = float(shipment.price_per_kg or 0)
                        total = quantity * price
                        
                        # Get grammage and grade from Products table
                        from myapp.models import Products
                        product = Products.objects.filter(shipment_id=shipment.id).first()
                        gsm = product.gsm if product else None
                        grade = product.grade if product else None
                        
                        items.append({
                            'description': '',  # Removed profile_name reference
                            'code': str(shipment.id),
                            'quantity': quantity,
                            'unit': 'کیلو',
                            'gsm': gsm,  # Add grammage
                            'type': grade,  # Add grade
                            'price': price,
                            'total': total,
                            'net_weight': shipment.net_weight or '',
                            'width': shipment.width or '',
                            'total_weight': quantity  # Use quantity as total_weight
                        })
                else:
                    # If no list_of_reels, use net_weight
                    quantity = float(shipment.net_weight or 0)
                    price = float(shipment.price_per_kg or 0)
                    total = quantity * price
                    
                    # Get grammage and grade from Products table
                    from myapp.models import Products
                    product = Products.objects.filter(shipment_id=shipment.id).first()
                    gsm = product.gsm if product else None
                    grade = product.grade if product else None
                    
                    items.append({
                        'description': '',  # Removed profile_name reference
                        'code': str(shipment.id),
                        'quantity': quantity,
                        'unit': 'کیلو',
                        'gsm': gsm,  # Add grammage
                        'type': grade,  # Add grade
                        'price': price,
                        'total': total,
                        'net_weight': shipment.net_weight or '',
                        'width': shipment.width or '',
                        'total_weight': quantity  # Use quantity as total_weight
                    })

                # Get invoice number from Sales table through the relationship
                from myapp.models import Sales
                sale = Sales.objects.filter(shipment=shipment).first()
                invoice_number = sale.invoice_number if sale else None

                # Calculate total weight for the shipment
                total_weight = float(shipment.net_weight or 0)

                # Calculate reel count from list_of_reels
                reel_count = 0
                if shipment.list_of_reels:
                    try:
                        # Split by comma and count non-empty strings
                        reels = [reel.strip() for reel in shipment.list_of_reels.split(',') if reel.strip()]
                        reel_count = len(reels)
                    except Exception as e:
                        print(f"Error counting reels: {str(e)}")
                        reel_count = 0

                shipment_data = {
                    'id': shipment.id,
                    'date': formatted_date,
                    'buyer_name': shipment.customer_name or '',
                    'invoice_number': invoice_number,  # Add invoice number from Sales
                    'items': items,
                    'total_amount': float(shipment.total_price or 0),
                    'total_items': len(items),
                    'total_weight': total_weight,  # Use calculated total_weight
                    'comments': shipment.comments or '',
                    'status': shipment.status or '',
                    'license_number': shipment.license_number or '',
                    'list_of_reels': shipment.list_of_reels or '',  # Add list_of_reels field
                    'reel_count': reel_count,  # Add reel count field
                }
                sales_data.append(shipment_data)
            except Exception as e:
                print(f"Error processing shipment {shipment.id}: {str(e)}")
                continue

        return JsonResponse(sales_data, safe=False)

    except Exception as e:
        print(f"Error in get_last_10_sales: {str(e)}")
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def save_buyer_info(request):
    """Save buyer information to CSV file"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is supported'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Extract buyer information
        buyer_info = {
            'buyer_name': data.get('buyer_name', ''),
            'buyer_economic_code': data.get('buyer_economic_code', ''),
            'buyer_reg': data.get('buyer_reg', ''),
            'buyer_national_id': data.get('buyer_national_id', ''),
            'buyer_postcode': data.get('buyer_postcode', ''),
            'buyer_address': data.get('buyer_address', ''),
            'buyer_phone': data.get('buyer_phone', '')
        }
        
        # Check if buyer name is provided
        if not buyer_info['buyer_name']:
            return JsonResponse({'error': 'Buyer name is required'}, status=400)
        
        # Path to CSV file
        csv_path = os.path.join(settings.BASE_DIR, 'SaleOrder.csv')
        
        # Check if file exists to determine if we need to write headers
        file_exists = os.path.isfile(csv_path)
        
        # Open file in append mode
        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            import csv
            writer = csv.DictWriter(csvfile, fieldnames=buyer_info.keys())
            
            # Write headers if file is new
            if not file_exists:
                writer.writeheader()
            
            # Write buyer information
            writer.writerow(buyer_info)
        
        return JsonResponse({'status': 'success', 'message': 'Buyer information saved successfully'})
    
    except Exception as e:
        print(f"Error saving buyer info: {str(e)}")
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_buyers_list(request):
    """Retrieve list of buyers from CSV file"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method is supported'}, status=405)
    
    try:
        # Path to CSV file
        csv_path = os.path.join(settings.BASE_DIR, 'SaleOrder.csv')
        
        # Check if file exists
        if not os.path.isfile(csv_path):
            return JsonResponse([], safe=False)
        
        # Read CSV file
        buyers_list = []
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            import csv
            # Define the fieldnames explicitly
            fieldnames = [
                'buyer_name',
                'buyer_economic_code',
                'buyer_reg',
                'buyer_national_id',
                'buyer_postcode',
                'buyer_address',
                'buyer_phone'
            ]
            
            # Read the first line to check if it's a header
            first_line = csvfile.readline().strip()
            csvfile.seek(0)  # Reset file pointer to beginning
            
            # If first line doesn't contain our fieldnames, it's probably data
            if not any(field in first_line for field in fieldnames):
                # Read as data
                for line in csvfile:
                    values = line.strip().split(',')
                    if len(values) >= 7:  # Make sure we have enough values
                        buyer = {
                            'buyer_name': values[0],
                            'buyer_economic_code': values[1],
                            'buyer_reg': values[2],
                            'buyer_national_id': values[3],
                            'buyer_postcode': values[4],
                            'buyer_address': values[5],
                            'buyer_phone': values[6]
                        }
                        buyers_list.append(buyer)
            else:
                # Read as CSV with headers
                reader = csv.DictReader(csvfile, fieldnames=fieldnames)
                for row in reader:
                    buyers_list.append(row)
        
        # print(f"Found {len(buyers_list)} buyers in CSV file")
        return JsonResponse(buyers_list, safe=False)
    
    except Exception as e:
        print(f"Error reading buyers list: {str(e)}")
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)