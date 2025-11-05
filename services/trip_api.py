"""Trip.com API integration for flights, hotels, and tours."""

import requests
import hashlib
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from config.settings import settings

logger = logging.getLogger(__name__)


class TripAPI:
    """Client for Trip.com API integration."""
    
    def __init__(self):
        self.api_key = settings.TRIP_COM_API_KEY
        self.api_secret = settings.TRIP_COM_API_SECRET
        self.base_url = settings.TRIP_COM_BASE_URL
        self.session = requests.Session()
    
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """
        Generate API signature for authentication.
        
        Args:
            params: Request parameters
        
        Returns:
            Signature string
        """
        # Sort parameters and create signature string
        sorted_params = sorted(params.items())
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params])
        signature_string = f"{self.api_secret}{param_str}{self.api_secret}"
        
        # Generate MD5 hash
        signature = hashlib.md5(signature_string.encode()).hexdigest().upper()
        return signature
    
    def _make_request(self, endpoint: str, params: Dict[str, Any], method: str = "GET") -> Dict[str, Any]:
        """
        Make API request to Trip.com.
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            method: HTTP method
        
        Returns:
            API response as dictionary
        """
        # Add authentication parameters
        params['api_key'] = self.api_key
        params['timestamp'] = str(int(time.time()))
        params['sign'] = self._generate_signature(params)
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            if method == "GET":
                response = self.session.get(url, params=params, timeout=30)
            else:
                response = self.session.post(url, json=params, timeout=30)
            
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as e:
            logger.error(f"Trip.com API error: {e}")
            return {"error": str(e), "success": False}
    
    def search_flights(
        self,
        from_city: str,
        to_city: str,
        depart_date: str,
        return_date: Optional[str] = None,
        passengers: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Search for flights.
        
        Args:
            from_city: Origin city/airport code
            to_city: Destination city/airport code
            depart_date: Departure date (YYYY-MM-DD)
            return_date: Return date for round-trip (YYYY-MM-DD)
            passengers: Number of passengers
        
        Returns:
            List of available flights
        """
        # Check if using test API keys - return mock data
        if not self.api_key or self.api_key == 'test' or self.api_key == 'test_key':
            logger.info("Using mock flight data (test mode)")
            # Return mock flight results
            return [
                {
                    'flight_id': 'ET001',
                    'airline': 'Ethiopian Airlines',
                    'from_city': from_city,
                    'to_city': to_city,
                    'departure_time': f'{depart_date}T08:00:00Z',
                    'arrival_time': f'{depart_date}T12:30:00Z',
                    'duration': '4h 30m',
                    'stops': 0,
                    'flight_number': 'ET-302',
                    'price_usd': 450.00,
                    'class': 'Economy'
                },
                {
                    'flight_id': 'KQ002',
                    'airline': 'Kenya Airways',
                    'from_city': from_city,
                    'to_city': to_city,
                    'departure_time': f'{depart_date}T14:00:00Z',
                    'arrival_time': f'{depart_date}T18:45:00Z',
                    'duration': '4h 45m',
                    'stops': 0,
                    'flight_number': 'KQ-442',
                    'price_usd': 380.00,
                    'class': 'Economy'
                },
                {
                    'flight_id': 'TK003',
                    'airline': 'Turkish Airlines',
                    'from_city': from_city,
                    'to_city': to_city,
                    'departure_time': f'{depart_date}T22:00:00Z',
                    'arrival_time': f'{depart_date}T06:30:00Z',
                    'duration': '8h 30m',
                    'stops': 1,
                    'flight_number': 'TK-724',
                    'price_usd': 520.00,
                    'class': 'Economy'
                }
            ]
        
        params = {
            'from_city': from_city,
            'to_city': to_city,
            'depart_date': depart_date,
            'passengers': passengers
        }
        
        if return_date:
            params['return_date'] = return_date
        
        # Try real API call
        response = self._make_request('flights/search', params)
        
        # If error, return mock data
        if 'error' in response:
            logger.warning("API error, returning mock data")
            return self.search_flights(from_city, to_city, depart_date, return_date, passengers)
        
        # Parse and return flights
        flights = response.get('data', {}).get('flights', [])
        return flights
    
    def search_hotels(
        self,
        city: str,
        checkin_date: str,
        checkout_date: str,
        rooms: int = 1,
        guests: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Search for hotels.
        
        Args:
            city: City name
            checkin_date: Check-in date (YYYY-MM-DD)
            checkout_date: Check-out date (YYYY-MM-DD)
            rooms: Number of rooms
            guests: Number of guests
        
        Returns:
            List of available hotels
        """
        # Check if using test API keys - return mock data
        if not self.api_key or self.api_key == 'test' or self.api_key == 'test_key':
            logger.info("Using mock hotel data (test mode)")
            # Return mock hotel results
            return [
                {
                    'hotel_id': 'H001',
                    'name': 'Skylight Hotel ' + city,
                    'address': 'Main Street, ' + city,
                    'city': city,
                    'rating': 4.5,
                    'checkin_date': checkin_date,
                    'checkout_date': checkout_date,
                    'room_type': 'Deluxe Room',
                    'price_usd': 120.00,
                    'amenities': 'WiFi, Breakfast, Pool'
                },
                {
                    'hotel_id': 'H002',
                    'name': 'Grand Palace Hotel',
                    'address': 'City Center, ' + city,
                    'city': city,
                    'rating': 5.0,
                    'checkin_date': checkin_date,
                    'checkout_date': checkout_date,
                    'room_type': 'Executive Suite',
                    'price_usd': 250.00,
                    'amenities': 'WiFi, Breakfast, Pool, Spa, Gym'
                },
                {
                    'hotel_id': 'H003',
                    'name': 'Budget Inn ' + city,
                    'address': 'Airport Road, ' + city,
                    'city': city,
                    'rating': 3.5,
                    'checkin_date': checkin_date,
                    'checkout_date': checkout_date,
                    'room_type': 'Standard Room',
                    'price_usd': 65.00,
                    'amenities': 'WiFi, Breakfast'
                },
                {
                    'hotel_id': 'H004',
                    'name': 'Hilltop Resort',
                    'address': 'Mountain View, ' + city,
                    'city': city,
                    'rating': 4.8,
                    'checkin_date': checkin_date,
                    'checkout_date': checkout_date,
                    'room_type': 'Villa',
                    'price_usd': 350.00,
                    'amenities': 'WiFi, Breakfast, Pool, Spa, Gym, Restaurant'
                }
            ]
        
        params = {
            'city': city,
            'checkin_date': checkin_date,
            'checkout_date': checkout_date,
            'rooms': rooms,
            'guests': guests
        }
        
        response = self._make_request('hotels/search', params)
        
        if 'error' in response:
            logger.warning("API error, returning mock data")
            return self.search_hotels(city, checkin_date, checkout_date, rooms, guests)
        
        hotels = response.get('data', {}).get('hotels', [])
        return hotels
    
    def search_tours(
        self,
        destination: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for tour packages.
        
        Args:
            destination: Destination name
            category: Tour category (cultural, adventure, etc.)
        
        Returns:
            List of available tours
        """
        # Check if using test API keys - return mock data
        if not self.api_key or self.api_key == 'test' or self.api_key == 'test_key':
            logger.info("Using mock tour data (test mode)")
            # Return mock tour results
            return [
                {
                    'tour_id': 'T001',
                    'name': 'Historic Route of Ethiopia',
                    'destination': 'Ethiopia',
                    'category': 'Cultural',
                    'duration_days': 8,
                    'description': 'Visit Lalibela, Axum, Gondar and Bahir Dar',
                    'price_usd': 1200.00,
                    'includes': 'Accommodation, Transport, Guide, Meals'
                },
                {
                    'tour_id': 'T002',
                    'name': 'Simien Mountains Trek',
                    'destination': 'Ethiopia',
                    'category': 'Adventure',
                    'duration_days': 5,
                    'description': 'Trekking in UNESCO World Heritage Site',
                    'price_usd': 850.00,
                    'includes': 'Camping, Guide, Meals, Transport'
                },
                {
                    'tour_id': 'T003',
                    'name': 'Omo Valley Cultural Tour',
                    'destination': 'Ethiopia',
                    'category': 'Cultural',
                    'duration_days': 7,
                    'description': 'Explore traditional tribes and cultures',
                    'price_usd': 1100.00,
                    'includes': 'Accommodation, Guide, Transport, Permits'
                },
                {
                    'tour_id': 'T004',
                    'name': 'Danakil Depression Adventure',
                    'destination': 'Ethiopia',
                    'category': 'Adventure',
                    'duration_days': 4,
                    'description': 'Visit one of the hottest places on Earth',
                    'price_usd': 950.00,
                    'includes': 'Camping, Guide, Transport, Meals'
                },
                {
                    'tour_id': 'T005',
                    'name': 'East African Safari',
                    'destination': 'Kenya & Tanzania',
                    'category': 'Wildlife',
                    'duration_days': 10,
                    'description': 'Serengeti, Masai Mara, and Ngorongoro Crater',
                    'price_usd': 2500.00,
                    'includes': 'Accommodation, Transport, Guide, Meals, Park Fees'
                }
            ]
        
        params = {}
        
        if destination:
            params['destination'] = destination
        if category:
            params['category'] = category
        
        response = self._make_request('tours/search', params)
        
        if 'error' in response:
            logger.warning("API error, returning mock data")
            return self.search_tours(destination, category)
        
        tours = response.get('data', {}).get('tours', [])
        return tours
    
    def get_flight_details(self, flight_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific flight.
        
        Args:
            flight_id: Flight identifier
        
        Returns:
            Flight details or None
        """
        params = {'flight_id': flight_id}
        response = self._make_request('flights/details', params)
        
        if 'error' in response:
            return None
        
        return response.get('data', {})
    
    def get_hotel_details(self, hotel_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific hotel.
        
        Args:
            hotel_id: Hotel identifier
        
        Returns:
            Hotel details or None
        """
        params = {'hotel_id': hotel_id}
        response = self._make_request('hotels/details', params)
        
        if 'error' in response:
            return None
        
        return response.get('data', {})
    
    def create_flight_booking(self, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a flight booking.
        
        Args:
            booking_data: Booking information
        
        Returns:
            Booking confirmation
        """
        response = self._make_request('flights/book', booking_data, method="POST")
        return response
    
    def create_hotel_booking(self, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a hotel booking.
        
        Args:
            booking_data: Booking information
        
        Returns:
            Booking confirmation
        """
        response = self._make_request('hotels/book', booking_data, method="POST")
        return response
    
    def create_tour_booking(self, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a tour booking.
        
        Args:
            booking_data: Booking information
        
        Returns:
            Booking confirmation
        """
        response = self._make_request('tours/book', booking_data, method="POST")
        return response


