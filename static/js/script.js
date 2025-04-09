// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    // Car selection filters
    const brandFilter = document.getElementById('brand-filter');
    if (brandFilter) {
        brandFilter.addEventListener('change', function() {
            const selectedBrand = this.value;
            if (selectedBrand) {
                window.location.href = `/cars/${selectedBrand}`;
            }
        });
    }

    // Car search functionality
    const searchForm = document.getElementById('car-search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchTerm = document.getElementById('search-term').value.trim();
            if (searchTerm) {
                window.location.href = `/search?term=${encodeURIComponent(searchTerm)}`;
            }
        });
    }

    // Price range slider
    const priceRange = document.getElementById('price-range');
    const priceOutput = document.getElementById('price-value');
    if (priceRange && priceOutput) {
        priceOutput.textContent = `$${priceRange.value}`;
        priceRange.addEventListener('input', function() {
            priceOutput.textContent = `$${this.value}`;
        });
    }

    // Booking date picker
    const datePicker = document.getElementById('booking-date');
    if (datePicker) {
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        datePicker.setAttribute('min', today);
    }

    // Payment form validation
    const paymentForm = document.getElementById('payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            const cardNumber = document.getElementById('card-number').value;
            const cardCvv = document.getElementById('card-cvv').value;
            const cardExpiry = document.getElementById('card-expiry').value;
            
            let isValid = true;
            
            // Simple validation
            if (!/^\d{16}$/.test(cardNumber)) {
                showError('card-number', 'Please enter a valid 16-digit card number');
                isValid = false;
            } else {
                clearError('card-number');
            }
            
            if (!/^\d{3,4}$/.test(cardCvv)) {
                showError('card-cvv', 'Please enter a valid CVV code');
                isValid = false;
            } else {
                clearError('card-cvv');
            }
            
            if (!/^\d{2}\/\d{2}$/.test(cardExpiry)) {
                showError('card-expiry', 'Please enter a valid expiry date (MM/YY)');
                isValid = false;
            } else {
                clearError('card-expiry');
            }
            
            if (!isValid) {
                e.preventDefault();
            } else {
                // Show loading indicator
                document.getElementById('payment-processing').classList.remove('d-none');
            }
        });
    }

    // Booking cancellation confirmation
    const cancelButtons = document.querySelectorAll('.cancel-booking-btn');
    cancelButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to cancel this booking?')) {
                e.preventDefault();
            }
        });
    });

    // Car details modal
    const carDetailsButtons = document.querySelectorAll('.view-details-btn');
    carDetailsButtons.forEach(button => {
        button.addEventListener('click', function() {
            const carId = this.getAttribute('data-car-id');
            fetchCarDetails(carId);
        });
    });

    // Admin dashboard charts
    initializeAdminCharts();
});

// Helper functions
function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorElement = document.getElementById(`${fieldId}-error`);
    
    field.classList.add('is-invalid');
    if (errorElement) {
        errorElement.textContent = message;
    } else {
        const div = document.createElement('div');
        div.id = `${fieldId}-error`;
        div.className = 'invalid-feedback';
        div.textContent = message;
        field.parentNode.appendChild(div);
    }
}

function clearError(fieldId) {
    const field = document.getElementById(fieldId);
    const errorElement = document.getElementById(`${fieldId}-error`);
    
    field.classList.remove('is-invalid');
    if (errorElement) {
        errorElement.textContent = '';
    }
}

function fetchCarDetails(carId) {
    fetch(`/api/cars/${carId}`)
        .then(response => response.json())
        .then(data => {
            const modal = new bootstrap.Modal(document.getElementById('carDetailsModal'));
            document.getElementById('modalCarTitle').textContent = `${data.brand} ${data.model}`;
            document.getElementById('modalCarSpecs').innerHTML = `
                <p><strong>Engine:</strong> ${data.cc}cc</p>
                <p><strong>Power:</strong> ${data.bhp} BHP</p>
                <p><strong>Torque:</strong> ${data.torque}</p>
                <p><strong>Top Speed:</strong> ${data.top_speed} km/h</p>
                <p><strong>Mileage:</strong> ${data.mileage} km/l</p>
                <p><strong>Price:</strong> $${data.price}</p>
            `;
            document.getElementById('bookNowBtn').href = `/book/${carId}`;
            modal.show();
        })
        .catch(error => {
            console.error('Error fetching car details:', error);
        });
}

function initializeAdminCharts() {
    const bookingTrendsChart = document.getElementById('bookingTrendsChart');
    if (bookingTrendsChart) {
        fetch('/api/admin/booking-trends')
            .then(response => response.json())
            .then(data => {
                new Chart(bookingTrendsChart, {
                    type: 'line',
                    data: {
                        labels: data.months,
                        datasets: [{
                            label: 'Number of Bookings',
                            data: data.counts,
                            borderColor: 'rgba(75, 192, 192, 1)',
                            tension: 0.1,
                            fill: false
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            });
    }

    const brandDistributionChart = document.getElementById('brandDistributionChart');
    if (brandDistributionChart) {
        fetch('/api/admin/brand-distribution')
            .then(response => response.json())
            .then(data => {
                new Chart(brandDistributionChart, {
                    type: 'pie',
                    data: {
                        labels: data.brands,
                        datasets: [{
                            data: data.counts,
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.7)',
                                'rgba(54, 162, 235, 0.7)',
                                'rgba(255, 206, 86, 0.7)',
                                'rgba(75, 192, 192, 0.7)',
                                'rgba(153, 102, 255, 0.7)',
                                'rgba(255, 159, 64, 0.7)',
                                'rgba(199, 199, 199, 0.7)'
                            ]
                        }]
                    },
                    options: {
                        responsive: true
                    }
                });
            });
    }
}

// Car filtering functionality
function filterCars() {
    const minPrice = document.getElementById('min-price').value;
    const maxPrice = document.getElementById('max-price').value;
    const transmission = document.getElementById('transmission').value;
    
    const carCards = document.querySelectorAll('.car-card');
    
    carCards.forEach(card => {
        const price = parseInt(card.getAttribute('data-price'));
        const cardTransmission = card.getAttribute('data-transmission');
        
        let showCard = true;
        
        if (minPrice && price < parseInt(minPrice)) {
            showCard = false;
        }
        
        if (maxPrice && price > parseInt(maxPrice)) {
            showCard = false;
        }
        
        if (transmission && transmission !== 'all' && cardTransmission !== transmission) {
            showCard = false;
        }
        
        card.style.display = showCard ? 'block' : 'none';
    });
}

// Countdown timer for special offers
function startCountdown(endTime, displayElement) {
    const countdownTimer = setInterval(function() {
        const now = new Date().getTime();
        const distance = new Date(endTime).getTime() - now;
        
        if (distance < 0) {
            clearInterval(countdownTimer);
            displayElement.textContent = "Offer expired!";
            return;
        }
        
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        displayElement.textContent = `${days}d ${hours}h ${minutes}m ${seconds}s`;
    }, 1000);
}
