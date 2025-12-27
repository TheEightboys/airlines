/**
 * Airline Recommendation System - GSAP Animations
 * Subtle, performant animations for enhanced UX
 */

// Register ScrollTrigger plugin
gsap.registerPlugin(ScrollTrigger);

// Configuration
const ANIMATION_CONFIG = {
    duration: {
        fast: 0.3,
        normal: 0.6,
        slow: 1
    },
    ease: {
        smooth: 'power2.out',
        bounce: 'back.out(1.2)',
        elastic: 'elastic.out(1, 0.5)'
    },
    stagger: 0.15
};

/**
 * Initialize all animations
 */
function initAnimations() {
    // Only animate if reduced motion is not preferred
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        // Show all elements without animation
        gsap.set('.hero-content, .hero-visual, .feature-card, .section-title, .regulation-card, .search-title, .search-subtitle, .search-box', {
            opacity: 1,
            y: 0,
            x: 0
        });
        return;
    }

    initLandingAnimations();
    initCloudAnimations();
    initScrollAnimations();
}

/**
 * Landing Page - Hero animations on page load
 */
function initLandingAnimations() {
    const landingTimeline = gsap.timeline({
        defaults: {
            ease: ANIMATION_CONFIG.ease.smooth,
            duration: ANIMATION_CONFIG.duration.normal
        }
    });

    // Hero content slide in
    landingTimeline
        .to('.hero-content', {
            opacity: 1,
            y: 0,
            duration: 0.8
        })
        .to('.hero-visual', {
            opacity: 1,
            duration: 0.6
        }, '-=0.4');

    // Plane floating animation
    gsap.to('.plane', {
        y: -15,
        duration: 2,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
    });

    // Start button pulse
    gsap.to('.start-btn', {
        boxShadow: '0 10px 40px rgba(14, 165, 233, 0.5), 0 0 60px rgba(14, 165, 233, 0.3)',
        duration: 1.5,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
    });
}

/**
 * Cloud parallax animations
 */
function initCloudAnimations() {
    gsap.to('.cloud-1', {
        x: 100,
        duration: 30,
        repeat: -1,
        yoyo: true,
        ease: 'none'
    });

    gsap.to('.cloud-2', {
        x: -80,
        duration: 25,
        repeat: -1,
        yoyo: true,
        ease: 'none'
    });

    gsap.to('.cloud-3', {
        x: 60,
        duration: 35,
        repeat: -1,
        yoyo: true,
        ease: 'none'
    });
}

/**
 * ScrollTrigger animations for section reveals
 */
function initScrollAnimations() {
    // Feature cards staggered reveal
    gsap.to('.feature-card', {
        scrollTrigger: {
            trigger: '.features',
            start: 'top 80%',
            toggleActions: 'play none none none'
        },
        opacity: 1,
        y: 0,
        duration: ANIMATION_CONFIG.duration.normal,
        stagger: ANIMATION_CONFIG.stagger,
        ease: ANIMATION_CONFIG.ease.smooth
    });

    // Regulations section title
    gsap.to('.section-title', {
        scrollTrigger: {
            trigger: '.regulations-section',
            start: 'top 80%',
            toggleActions: 'play none none none'
        },
        opacity: 1,
        duration: ANIMATION_CONFIG.duration.normal,
        ease: ANIMATION_CONFIG.ease.smooth
    });

    // Regulation cards
    gsap.to('.regulation-card', {
        scrollTrigger: {
            trigger: '.regulations-content',
            start: 'top 80%',
            toggleActions: 'play none none none'
        },
        opacity: 1,
        y: 0,
        duration: ANIMATION_CONFIG.duration.normal,
        stagger: ANIMATION_CONFIG.stagger,
        ease: ANIMATION_CONFIG.ease.smooth
    });
}

/**
 * App page search section animations
 */
function animateSearchSection() {
    const searchTimeline = gsap.timeline({
        defaults: {
            ease: ANIMATION_CONFIG.ease.smooth,
            duration: ANIMATION_CONFIG.duration.normal
        }
    });

    searchTimeline
        .to('.search-title', {
            opacity: 1,
            y: 0
        })
        .to('.search-subtitle', {
            opacity: 1,
            y: 0
        }, '-=0.3')
        .to('.search-box', {
            opacity: 1,
            y: 0
        }, '-=0.2');
}

/**
 * Animate airline result cards with stagger
 */
function animateResultCards() {
    gsap.fromTo('.airline-card', {
        opacity: 0,
        x: 50
    }, {
        opacity: 1,
        x: 0,
        duration: ANIMATION_CONFIG.duration.normal,
        stagger: ANIMATION_CONFIG.stagger * 1.5,
        ease: ANIMATION_CONFIG.ease.bounce
    });

    // Animate delay numbers (count up effect)
    document.querySelectorAll('.delay-value').forEach((el, index) => {
        const finalValue = parseFloat(el.textContent);
        const obj = { value: 0 };

        gsap.to(obj, {
            value: finalValue,
            duration: 1,
            delay: index * ANIMATION_CONFIG.stagger + 0.3,
            ease: 'power1.out',
            onUpdate: () => {
                el.textContent = obj.value.toFixed(2);
            }
        });
    });

    // Animate rank badges with pop effect
    gsap.fromTo('.airline-rank', {
        scale: 0
    }, {
        scale: 1,
        duration: ANIMATION_CONFIG.duration.fast,
        stagger: ANIMATION_CONFIG.stagger * 1.5,
        delay: 0.2,
        ease: ANIMATION_CONFIG.ease.elastic
    });
}

/**
 * Reset animation - cards slide out
 */
function animateResetOut() {
    return new Promise((resolve) => {
        const resetTimeline = gsap.timeline({
            onComplete: resolve
        });

        resetTimeline
            .to('.airline-card', {
                opacity: 0,
                x: -50,
                duration: ANIMATION_CONFIG.duration.fast,
                stagger: 0.08,
                ease: 'power2.in'
            })
            .to('#results', {
                opacity: 0,
                duration: ANIMATION_CONFIG.duration.fast
            }, '-=0.1');
    });
}

/**
 * Animate dropdown re-enable after reset
 */
function animateDropdownEnable() {
    gsap.fromTo('#destination-select', {
        scale: 0.95,
        borderColor: 'rgba(14, 165, 233, 0.8)'
    }, {
        scale: 1,
        borderColor: 'rgba(14, 165, 233, 0.3)',
        duration: ANIMATION_CONFIG.duration.fast,
        ease: ANIMATION_CONFIG.ease.bounce
    });
}

/**
 * Loading animation
 */
function animateLoading() {
    gsap.to('.plane-loader', {
        rotation: 10,
        duration: 0.5,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
    });
}

/**
 * Show results section with animation
 */
function animateShowResults() {
    gsap.fromTo('#results', {
        opacity: 0,
        y: 20
    }, {
        opacity: 1,
        y: 0,
        duration: ANIMATION_CONFIG.duration.normal,
        ease: ANIMATION_CONFIG.ease.smooth,
        onComplete: animateResultCards
    });
}

/**
 * Page transition animation
 */
function animatePageTransition(fromPage, toPage) {
    const timeline = gsap.timeline();

    timeline
        .to(fromPage, {
            opacity: 0,
            duration: ANIMATION_CONFIG.duration.fast,
            onComplete: () => {
                fromPage.classList.remove('active');
                toPage.classList.add('active');

                // Re-initialize animations for the new page
                if (toPage.id === 'app') {
                    animateSearchSection();
                }
            }
        })
        .fromTo(toPage, {
            opacity: 0
        }, {
            opacity: 1,
            duration: ANIMATION_CONFIG.duration.fast
        });
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', initAnimations);

// Export functions for use in app.js
window.FlightAnimations = {
    animateSearchSection,
    animateResultCards,
    animateResetOut,
    animateDropdownEnable,
    animateLoading,
    animateShowResults,
    animatePageTransition
};
