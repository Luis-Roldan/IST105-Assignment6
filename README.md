# IST105-Assignment6
## Django Web Application with Bitwise Operations and MongoDB Integration

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-success.svg)](https://www.mongodb.com/)
[![AWS EC2](https://img.shields.io/badge/AWS-EC2-orange.svg)](https://aws.amazon.com/ec2/)

A dynamic web application that performs **bitwise operations**, **logical checks**, and **statistical calculations** on user input, with data persistence in MongoDB running on a separate AWS EC2 instance.

---

## 📋 Project Overview

This application demonstrates:
- **Django web framework** for form handling and view rendering
- **Python programming** with lists, logical operations, and bitwise operations
- **MongoDB integration** for data persistence across EC2 instances
- **AWS EC2 deployment** with multi-instance architecture
- **Git version control** with proper branching strategy

---

## 🎯 Features

### Input & Validation
- ✅ Accept five numerical inputs (a, b, c, d, e)
- ✅ Real-time validation (numeric check)
- ✅ Negative value warnings
- ✅ CSRF protection

### Calculations & Operations

1. **Statistical Analysis**
   - Calculate average of all values
   - Check if average > 50
   - Count positive values

2. **Bitwise Operations** 
   - Use bitwise AND (`&`) to determine if count is even/odd
   - Binary representation of values
   - Even/odd check for each input using `(value & 1) == 0`

3. **List Operations**
   - Filter values greater than 10
   - Sort filtered list
   - Display original and processed lists

4. **Data Persistence**
   - Save all inputs and results to MongoDB
   - View historical entries with timestamps
   - Persistent storage across sessions

