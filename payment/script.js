// Configuration - Replace these with your actual Stripe keys
const STRIPE_PUBLISHABLE_KEY = 'pk_live_51SXNg3JkSt0JSgSxsW7CLYsr3G0al9CckviSYweRXgp2wjj6rfEaPtNCiMivvTgWUXhujKfJ6w6lpiGmTM4WAp8n00MDXp5hNq';

// Price IDs mapping - Replace with your actual Stripe Price IDs
const PRICE_IDS = {
    'PRICE_ID_10_PACK': 'price_1SyIw5JkSt0JSgSxllTL3hfd',
    'PRICE_ID_25_PACK': 'price_1SyJ7YJkSt0JSgSxXSgvHrA0',
    'PRICE_ID_50_PACK': 'price_1SyJAUJkSt0JSgSxI4S1V0LU',
    'PRICE_ID_100_PACK': 'price_1SyJDGJkSt0JSgSxaNWrOXL0'
};

// Initialize Stripe
let stripe;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Stripe (will fail gracefully if key is placeholder)
    try {
        stripe = Stripe(STRIPE_PUBLISHABLE_KEY);
    } catch (error) {
        console.error('Stripe initialization failed. Please add your publishable key to script.js');
    }

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

// Handle checkout button click
async function handleCheckout(event) {
    const button = event.target;
    const priceIdKey = button.getAttribute('data-price-id');
    const packageName = button.getAttribute('data-package');

    // Validate Stripe is initialized
    if (!stripe) {
        alert('Payment system is not configured. Please contact support.');
        console.error('Stripe not initialized. Check your publishable key in script.js');
        return;
    }

    // Get the actual Price ID
    const priceId = PRICE_IDS[priceIdKey];

    if (!priceId || priceId.startsWith('price_YOUR_')) {
        alert('This product is not yet configured. Please contact support.');
        console.error(`Price ID not configured for ${priceIdKey}. Update PRICE_IDS in script.js`);
        return;
    }

    // Disable button and show loading state
    button.disabled = true;
    const originalText = button.textContent;
    button.textContent = 'Loading...';
    button.classList.add('loading');

    try {
        // Redirect to Stripe Checkout
        const { error } = await stripe.redirectToCheckout({
            lineItems: [{
                price: priceId,
                quantity: 1
            }],
            mode: 'payment',
            successUrl: window.location.origin + '/success.html?session_id={CHECKOUT_SESSION_ID}',
            cancelUrl: window.location.origin + '/cancel.html',
            clientReferenceId: packageName,
            // Optional: Auto-apply discount coupon
            // discounts: [{
            //     coupon: 'YOUR_COUPON_CODE_HERE'
            // }]
        });

        if (error) {
            console.error('Stripe Checkout error:', error);
            alert('Unable to process checkout. Please try again or contact support.');
        }
    } catch (error) {
        console.error('Checkout error:', error);
        alert('An error occurred. Please try again.');
    } finally {
        // Re-enable button
        button.disabled = false;
        button.textContent = originalText;
        button.classList.remove('loading');
    }
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
