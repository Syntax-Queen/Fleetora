# Fleetora
This project is a full-scale logistics and delivery platform designed to operate at the level of modern on-demand delivery apps like Uber Eats, DoorDash, or Glovo. It supports a three-sided marketplace — Restaurants/Vendors, Customers, and Riders — with real-time operations, automated dispatching, and a complete order-to-delivery workflow.

The application is built with a demanding architecture optimized for speed, reliability, and scalability, supporting real-time communication, dynamic pricing, and continuous order tracking.

Core Features
1. Real-Time Driver Tracking

Drivers are tracked live through GPS, allowing customers and restaurants to see:

Driver’s live location

Movement updates

Pick-up and delivery progress

2. ETA Predictions

The platform calculates estimated arrival times using:

Driver speed

Distance

Traffic patterns

Delay factors

3. Dispatch Algorithm

The system automatically assigns riders based on:

Distance to restaurant

Rider availability

Rider pricing

Historical reliability

Delivery load balancing

4. Multi-step Order States

Every order moves through a lifecycle:

Created

Confirmed

Preparing

Rider Assigned

Picked Up

On The Way

Delivered

Rated

All states update live for customers, restaurants, and riders.

5. Payment Workflow

Complete payment lifecycle including:

Customer → Restaurant

Restaurant → Rider

Rider earnings breakdown

Automatic deduction logic

In-app confirmation for all parties

6. Secure Messaging & Calls

Each role gets:

Real-time chat

Secure, temporary phone-share system

Communication between restaurant ↔ customer ↔ rider

7. Highly Demanding Architecture

This project covers advanced system behavior:

WebSockets / Real-time communication

Complex routing logic

High availability and fast response design patterns

Modular role-based dashboards and experiences

Role-Based Flows

The platform has unique interfaces and operations for the three core roles.

Restaurant / Vendor Features

Sign up

Login

Delete account

Edit name / password reset

Post food items

Edit food posts

Delete food posts

View customer orders

Chat with customers and riders

Accept payments from customers

Deduct rider payment

View available riders nearby with prices

Confirm orders

Update customer when rider arrives for pickup

Connect rider to customer with one click

Rate riders

Customer Features

Sign up

Login

Delete account

Edit name / password reset

Search for menu items

Place orders

Choose delivery mode:

Rider picks up from restaurant

Restaurant handles rider selection

Chat with restaurant / rider

Real-time rider tracking

Make payment

See order movement stages

Receive notifications when order is picked and on the way

Rate restaurants

Rider Features

Sign up

Login

Delete account

Edit name / password reset

Browse available orders (from restaurants and customers)

Accept customer or restaurant delivery orders

Input delivery charge

Receive customer details for communication

Confirm pickup

Update status (On The Way → Delivered)

Receive payments

Rate customers

Real-time communication with restaurant or customer

System Architecture Overview

Although the backend/frontend stack isn’t specified yet, the system is designed to support:

Microservice or modular monolith structure

WebSocket server for real-time tracking and chat

Order service handling state transitions

Payment service with verification and ledger logic

Rider dispatch service with price and distance calculations

Authentication service for all roles

Database models for restaurants, customers, riders, menus, orders, payments

Project Goal

To deliver a robust, production-grade logistics platform capable of supporting:

Food delivery

Courier services

Vendor-to-customer logistics

Multi-role real-time interactions

The system is engineered to be scalable and extendable, making it suitable for startups, academic demonstrations, and large product prototypes.

