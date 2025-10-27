from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
from datetime import datetime
import os

MONGO_HOST ='172.31.25.157'
MONGO_PORT = 27017
DB_NAME = 'assignment6_db'
COLLECTION_NAME = 'calculations'

def get_mongo_client():
    """Create and return MongoDB client"""
    try:
        client = MongoClient(f'mongodb://{MONGO_HOST}:{MONGO_PORT}/', 
                           serverSelectionTimeoutMS=5000)
        # Test connection
        client.server_info()
        return client
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None

def process_inputs(a, b, c, d, e):
    """
    Process the five numerical inputs with logical and bitwise operations
    """
    results = {}
    
    # Store original values as list
    original_values = [a, b, c, d, e]
    results['original_values'] = original_values
    
    # Check if all inputs are numeric (already validated in form, but double-check)
    results['all_numeric'] = all(isinstance(x, (int, float)) for x in original_values)
    
    # Warn if any values are negative
    negative_values = [x for x in original_values if x < 0]
    results['has_negative'] = len(negative_values) > 0
    results['negative_values'] = negative_values
    
    # Calculate average
    average = sum(original_values) / len(original_values)
    results['average'] = round(average, 2)
    results['average_greater_than_50'] = average > 50
    
    # Count positive values
    positive_count = sum(1 for x in original_values if x > 0)
    results['positive_count'] = positive_count
    
    # Bitwise check: determine if positive count is even or odd
    # Using bitwise AND with 1: if result is 0, number is even; if 1, number is odd
    is_even = (positive_count & 1) == 0
    results['positive_count_even'] = is_even
    results['positive_count_odd'] = not is_even
    
    # Create new list with values > 10 and sort it
    values_greater_than_10 = [x for x in original_values if x > 10]
    sorted_values = sorted(values_greater_than_10)
    results['sorted_values_gt_10'] = sorted_values
    
    # Additional bitwise operations for demonstration
    results['bitwise_operations'] = {}
    for i, val in enumerate(original_values):
        if isinstance(val, int) and val >= 0:
            results['bitwise_operations'][f'value_{i+1}'] = {
                'value': val,
                'is_even': (val & 1) == 0,
                'binary': bin(val)
            }
    
    return results

def index(request):
    """Main view for input form and result display"""
    context = {
        'results': None,
        'errors': [],
        'mongo_status': 'Not connected'
    }
    
    # Check MongoDB connection
    client = get_mongo_client()
    if client:
        context['mongo_status'] = 'Connected'
        client.close()
    else:
        context['mongo_status'] = 'Disconnected'
    
    if request.method == 'POST':
        try:
            # Collect and validate inputs
            inputs = {}
            errors = []
            
            for field in ['a', 'b', 'c', 'd', 'e']:
                value = request.POST.get(field, '').strip()
                
                if not value:
                    errors.append(f"Field '{field}' is required")
                    continue
                
                try:
                    num_value = float(value)
                    inputs[field] = num_value
                except ValueError:
                    errors.append(f"Field '{field}' must be a valid number")
            
            if errors:
                context['errors'] = errors
                return render(request, 'bitwise/index.html', context)
            
            # Process the inputs
            a, b, c, d, e = inputs['a'], inputs['b'], inputs['c'], inputs['d'], inputs['e']
            results = process_inputs(a, b, c, d, e)
            
            # Save to MongoDB
            client = get_mongo_client()
            if client:
                try:
                    db = client[DB_NAME]
                    collection = db[COLLECTION_NAME]
                    
                    document = {
                        'timestamp': datetime.now(),
                        'inputs': {
                            'a': a, 'b': b, 'c': c, 'd': d, 'e': e
                        },
                        'results': results
                    }
                    
                    collection.insert_one(document)
                    results['saved_to_db'] = True
                except Exception as e:
                    results['saved_to_db'] = False
                    results['db_error'] = str(e)
                finally:
                    client.close()
            else:
                results['saved_to_db'] = False
                results['db_error'] = "Could not connect to MongoDB"
            
            context['results'] = results
            context['inputs'] = inputs
            
        except Exception as e:
            context['errors'] = [f"Processing error: {str(e)}"]
    
    return render(request, 'bitwise/index.html', context)

def view_all_entries(request):
    """View to display all saved entries from MongoDB"""
    context = {
        'entries': [],
        'error': None
    }
    
    client = get_mongo_client()
    if client:
        try:
            db = client[DB_NAME]
            collection = db[COLLECTION_NAME]
            
            # Retrieve all documents, sorted by timestamp (newest first)
            entries = list(collection.find().sort('timestamp', -1))
            
            context['entries'] = entries
            context['total_entries'] = len(entries)
            
        except Exception as e:
            context['error'] = f"Error retrieving entries: {str(e)}"
        finally:
            client.close()
    else:
        context['error'] = "Could not connect to MongoDB"
    
    return render(request, 'bitwise/view_entries.html', context)
