/**
 * Airline Recommendation System - Main Application
 * Handles API calls, UI updates, and user interactions
 */

// Configuration
const API_BASE = '';  // Same origin

// State
let currentDestination = null;
let isLoading = false;

/**
 * Initialize the application
 */
async function initApp() {
    await loadDestinations();
    setupEventListeners();
}

/**
 * Load destinations from API and populate dropdown
 */
async function loadDestinations() {
    try {
        const response = await fetch(`${API_BASE}/api/destinations`);
        const data = await response.json();

        if (data.success) {
            const select = document.getElementById('destination-select');

            // Clear existing options except the first one
            select.innerHTML = '<option value="">-- בחר יעד --</option>';

            // Add destinations sorted alphabetically
            data.destinations.sort().forEach(dest => {
                const option = document.createElement('option');
                option.value = dest;
                option.textContent = dest;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading destinations:', error);
        showError('שגיאה בטעינת היעדים. אנא רענן את הדף.');
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.dataset.page;
            navigateToPage(page);
        });
    });

    // Destination select change
    const select = document.getElementById('destination-select');
    select.addEventListener('change', () => {
        updateSearchButton();
    });

    // Enter key on select triggers search
    select.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && select.value) {
            searchAirlines();
        }
    });
}

/**
 * Navigate to a specific page
 */
function navigateToPage(pageName) {
    const pages = document.querySelectorAll('.page');
    const navLinks = document.querySelectorAll('.nav-link');

    // Update nav links
    navLinks.forEach(link => {
        link.classList.toggle('active', link.dataset.page === pageName);
    });

    // Get current and target pages
    const currentPage = document.querySelector('.page.active');
    const targetPage = document.getElementById(pageName);

    if (currentPage && targetPage && currentPage !== targetPage) {
        // Use GSAP animation if available
        if (window.FlightAnimations) {
            window.FlightAnimations.animatePageTransition(currentPage, targetPage);
        } else {
            currentPage.classList.remove('active');
            targetPage.classList.add('active');
        }
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Navigate to app page (called from landing page button)
 */
function navigateToApp() {
    navigateToPage('app');
}

/**
 * Update search button state
 */
function updateSearchButton() {
    const select = document.getElementById('destination-select');
    const btn = document.getElementById('search-btn');
    btn.disabled = !select.value || isLoading;
}

/**
 * Search for airline recommendations
 */
async function searchAirlines() {
    const select = document.getElementById('destination-select');
    const destination = select.value;

    if (!destination || isLoading) return;

    currentDestination = destination;
    isLoading = true;
    updateSearchButton();

    // Show loading state
    hideElement('results');
    hideElement('no-results');
    showElement('loading');

    if (window.FlightAnimations) {
        window.FlightAnimations.animateLoading();
    }

    try {
        const response = await fetch(`${API_BASE}/api/recommend/${encodeURIComponent(destination)}`);
        const data = await response.json();

        // Hide loading
        hideElement('loading');

        if (data.success) {
            displayResults(data);
        } else {
            showNoResults(data.error || 'לא נמצאו תוצאות');
        }
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        hideElement('loading');
        showNoResults('שגיאה בחיבור לשרת. אנא נסה שוב.');
    }

    isLoading = false;
    updateSearchButton();
}

/**
 * Display recommendation results
 */
function displayResults(data) {
    // Update header
    document.querySelector('.destination-name').textContent = data.destination;
    document.getElementById('results-message').textContent = data.message;

    // Build airline cards
    const cardsContainer = document.getElementById('airline-cards');
    cardsContainer.innerHTML = '';

    data.airlines.forEach((airline, index) => {
        const card = createAirlineCard(airline, index + 1);
        cardsContainer.appendChild(card);
    });

    // Show results section
    showElement('results');

    // Animate with GSAP
    if (window.FlightAnimations) {
        window.FlightAnimations.animateShowResults();
    }

    // Disable dropdown and search, show reset button
    document.getElementById('destination-select').disabled = true;
    document.getElementById('search-btn').classList.add('hidden');
    showElement('reset-btn');
}

/**
 * Create an airline card element
 */
function createAirlineCard(airline, rank) {
    const card = document.createElement('div');
    card.className = `airline-card rank-${rank}`;

    card.innerHTML = `
        <div class="airline-rank">${rank}</div>
        <div class="airline-info">
            <div class="airline-name">${airline.name}</div>
            <div class="airline-delay">
                <span class="delay-value">${airline.delay.toFixed(2)}</span>
                <span class="delay-unit">דקות עיכוב ממוצע</span>
            </div>
        </div>
        <div class="airline-logo">
            <span class="airline-logo-placeholder">✈️</span>
        </div>
    `;

    // Try to load actual logo
    const logoPlaceholder = card.querySelector('.airline-logo');
    const img = new Image();
    img.src = airline.logo;
    img.alt = airline.name;
    img.onload = () => {
        logoPlaceholder.innerHTML = '';
        logoPlaceholder.appendChild(img);
    };
    // Keep placeholder if logo fails to load

    return card;
}

/**
 * Show no results state
 */
function showNoResults(message) {
    document.getElementById('no-results-message').textContent = message;
    showElement('no-results');
}

/**
 * Reset search to initial state
 */
async function resetSearch() {
    // Animate out if GSAP available
    if (window.FlightAnimations) {
        await window.FlightAnimations.animateResetOut();
    }

    // Hide results
    hideElement('results');
    hideElement('no-results');

    // Reset dropdown
    const select = document.getElementById('destination-select');
    select.value = '';
    select.disabled = false;

    // Hide reset button, show search button
    hideElement('reset-btn');
    document.getElementById('search-btn').classList.remove('hidden');
    updateSearchButton();

    // Animate dropdown
    if (window.FlightAnimations) {
        window.FlightAnimations.animateDropdownEnable();
    }

    // Focus dropdown
    select.focus();

    currentDestination = null;
}

/**
 * Show an error message
 */
function showError(message) {
    showNoResults(message);
}

/**
 * Utility: Show element
 */
function showElement(id) {
    document.getElementById(id).classList.remove('hidden');
}

/**
 * Utility: Hide element
 */
function hideElement(id) {
    document.getElementById(id).classList.add('hidden');
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', initApp);
