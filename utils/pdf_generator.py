"""PDF generation utilities for tickets and confirmations."""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
from typing import Dict, Any
import os

from config.settings import settings


def generate_flight_ticket(booking_data: Dict[str, Any]) -> BytesIO:
    """
    Generate flight e-ticket PDF.
    
    Args:
        booking_data: Dictionary containing flight booking information
    
    Returns:
        BytesIO object containing PDF data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a73e8'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#202124'),
        spaceAfter=12
    )
    
    # Title
    story.append(Paragraph("✈️ FLIGHT E-TICKET", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Company info
    company_info = f"""
    <para align=center>
    <b>{settings.COMPANY_NAME}</b><br/>
    {settings.COMPANY_EMAIL} | {settings.COMPANY_PHONE}
    </para>
    """
    story.append(Paragraph(company_info, styles['Normal']))
    story.append(Spacer(1, 0.3 * inch))
    
    # Booking reference
    story.append(Paragraph(f"<b>Booking Reference:</b> {booking_data.get('booking_reference', 'N/A')}", header_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Passenger information
    passenger_data = [
        ['Passenger Name', booking_data.get('passenger_name', 'N/A')],
        ['Email', booking_data.get('email', 'N/A')],
        ['Phone', booking_data.get('phone', 'N/A')],
    ]
    
    passenger_table = Table(passenger_data, colWidths=[2.5 * inch, 4 * inch])
    passenger_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f3f4')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(Paragraph("<b>Passenger Information</b>", header_style))
    story.append(passenger_table)
    story.append(Spacer(1, 0.3 * inch))
    
    # Flight details
    flight_data = booking_data.get('flight_data', {})
    flight_details = [
        ['From', flight_data.get('from_city', 'N/A')],
        ['To', flight_data.get('to_city', 'N/A')],
        ['Departure', flight_data.get('departure_time', 'N/A')],
        ['Arrival', flight_data.get('arrival_time', 'N/A')],
        ['Flight Number', flight_data.get('flight_number', 'N/A')],
        ['Airline', flight_data.get('airline', 'N/A')],
        ['Class', flight_data.get('class', 'Economy')],
    ]
    
    flight_table = Table(flight_details, colWidths=[2.5 * inch, 4 * inch])
    flight_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0fe')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(Paragraph("<b>Flight Details</b>", header_style))
    story.append(flight_table)
    story.append(Spacer(1, 0.3 * inch))
    
    # Payment information
    payment_data = [
        ['Total Amount', f"{booking_data.get('total_price', 0)} {booking_data.get('currency', 'ETB')}"],
        ['Payment Status', booking_data.get('payment_status', 'N/A')],
        ['Payment Method', booking_data.get('payment_method', 'N/A')],
        ['Booking Date', booking_data.get('booking_date', datetime.now().strftime('%Y-%m-%d %H:%M'))],
    ]
    
    payment_table = Table(payment_data, colWidths=[2.5 * inch, 4 * inch])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f3f4')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(Paragraph("<b>Payment Information</b>", header_style))
    story.append(payment_table)
    story.append(Spacer(1, 0.5 * inch))
    
    # Footer
    footer_text = """
    <para align=center>
    <b>Important Information:</b><br/>
    Please arrive at the airport at least 2 hours before departure.<br/>
    Valid ID/Passport required for check-in.<br/>
    For support, contact {email} or {phone}
    </para>
    """.format(email=settings.COMPANY_EMAIL, phone=settings.COMPANY_PHONE)
    
    story.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer


def generate_hotel_confirmation(booking_data: Dict[str, Any]) -> BytesIO:
    """
    Generate hotel booking confirmation PDF.
    
    Args:
        booking_data: Dictionary containing hotel booking information
    
    Returns:
        BytesIO object containing PDF data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a73e8'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#202124'),
        spaceAfter=12
    )
    
    # Title
    story.append(Paragraph("🏨 HOTEL BOOKING CONFIRMATION", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Company info
    company_info = f"""
    <para align=center>
    <b>{settings.COMPANY_NAME}</b><br/>
    {settings.COMPANY_EMAIL} | {settings.COMPANY_PHONE}
    </para>
    """
    story.append(Paragraph(company_info, styles['Normal']))
    story.append(Spacer(1, 0.3 * inch))
    
    # Booking reference
    story.append(Paragraph(f"<b>Confirmation Number:</b> {booking_data.get('booking_reference', 'N/A')}", header_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Guest information
    guest_data = [
        ['Guest Name', booking_data.get('guest_name', 'N/A')],
        ['Email', booking_data.get('email', 'N/A')],
        ['Phone', booking_data.get('phone', 'N/A')],
    ]
    
    guest_table = Table(guest_data, colWidths=[2.5 * inch, 4 * inch])
    guest_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f3f4')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(Paragraph("<b>Guest Information</b>", header_style))
    story.append(guest_table)
    story.append(Spacer(1, 0.3 * inch))
    
    # Hotel details
    hotel_data = booking_data.get('hotel_data', {})
    hotel_details = [
        ['Hotel Name', hotel_data.get('hotel_name', 'N/A')],
        ['Address', hotel_data.get('address', 'N/A')],
        ['City', hotel_data.get('city', 'N/A')],
        ['Check-in', hotel_data.get('checkin_date', 'N/A')],
        ['Check-out', hotel_data.get('checkout_date', 'N/A')],
        ['Room Type', hotel_data.get('room_type', 'N/A')],
        ['Number of Rooms', str(hotel_data.get('rooms', 1))],
        ['Number of Guests', str(hotel_data.get('guests', 1))],
    ]
    
    hotel_table = Table(hotel_details, colWidths=[2.5 * inch, 4 * inch])
    hotel_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0fe')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(Paragraph("<b>Hotel Details</b>", header_style))
    story.append(hotel_table)
    story.append(Spacer(1, 0.3 * inch))
    
    # Payment information
    payment_data = [
        ['Total Amount', f"{booking_data.get('total_price', 0)} {booking_data.get('currency', 'ETB')}"],
        ['Payment Status', booking_data.get('payment_status', 'N/A')],
        ['Payment Method', booking_data.get('payment_method', 'N/A')],
        ['Booking Date', booking_data.get('booking_date', datetime.now().strftime('%Y-%m-%d %H:%M'))],
    ]
    
    payment_table = Table(payment_data, colWidths=[2.5 * inch, 4 * inch])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f3f4')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(Paragraph("<b>Payment Information</b>", header_style))
    story.append(payment_table)
    story.append(Spacer(1, 0.5 * inch))
    
    # Footer
    footer_text = """
    <para align=center>
    <b>Important Information:</b><br/>
    Check-in time: 2:00 PM | Check-out time: 12:00 PM<br/>
    Valid ID required at check-in.<br/>
    For inquiries, contact {email} or {phone}
    </para>
    """.format(email=settings.COMPANY_EMAIL, phone=settings.COMPANY_PHONE)
    
    story.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer


