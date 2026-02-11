// Payment Links - Get these from Stripe Dashboard → Products → Create Payment Link
const PAYMENT_LINKS = {
    'PRICE_ID_10_PACK': 'https://buy.stripe.com/bJe3cw1eXdRRe1O2Y2ebu04',
    'PRICE_ID_25_PACK': 'https://buy.stripe.com/3cIeVeg9RbJJ9LycyCebu03',
    'PRICE_ID_50_PACK': 'https://buy.stripe.com/9B65kE3n59BBf5SgOSebu02',
    'PRICE_ID_100_PACK': 'https://buy.stripe.com/00w5kEe1JbJJ5vi56aebu01'
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize countdown timer
    initCountdown();

    // Add click handlers to all CTA buttons
    const buttons = document.querySelectorAll('.cta-button');
    buttons.forEach(button => {
        button.addEventListener('click', handleCheckout);
    });
});

// Countdown Timer to February 28, 2026 11:59 PM
function initCountdown() {
    const countdownElement = document.getElementById('countdown');
    const endDate = new Date('February 28, 2026 23:59:59').getTime();

    function updateCountdown() {
        const now = new Date().getTime();
        const distance = endDate - now;

        if (distance < 0) {
            countdownElement.innerHTML = '<span style="color: #e25950;">Offer Expired</span>';
            return;
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.getElementById('days').textContent = String(days).padStart(2, '0');
        document.getElementById('hours').textContent = String(hours).padStart(2, '0');
        document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
        document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
    }

    updateCountdown();
    setInterval(updateCountdown, 1000);
}

// Handle checkout button click - Redirect to Stripe Payment Link
function handleCheckout(event) {
    const button = event.target;
    const priceIdKey = button.getAttribute('data-price-id');
    
    // Get the payment link
    const paymentLink = PAYMENT_LINKS[priceIdKey];
    
    if (!paymentLink || paymentLink.includes('YOUR_')) {
        alert('This product is not yet configured. Please contact support.');
        console.error(`Payment link not configured for ${priceIdKey}`);
        return;
    }
    
    // Track the click
    const packageName = button.getAttribute('data-package');
    trackEvent('checkout_initiated', { package: packageName });
    
    // Redirect to Stripe Payment Link
    window.location.href = paymentLink;
}

// Optional: Track analytics events
function trackEvent(eventName, eventData) {
    // Add your analytics tracking here (Google Analytics, Plausible, etc.)
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, eventData);
    }
    
    if (typeof plausible !== 'undefined') {
        plausible(eventName, { props: eventData });
    }
    
    console.log('Event:', eventName, eventData);
}

// Track button clicks
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.cta-button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const packageName = this.getAttribute('data-package');
            trackEvent('checkout_initiated', {
                package: packageName
            });
        });
    });
});
