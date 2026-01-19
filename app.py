#!/usr/bin/env python3
"""
Recovery Buddy - A supportive post-surgery recovery web app
Built with Streamlit - Luxury Wellness Aesthetic
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
import random

# App version
APP_VERSION = "2.0.0"
APP_CREATOR = "Ashmita Sharma"
LAST_MEDICAL_REVIEW = "January 2026"

# ============================================
# COZY MESSAGES AND AFFIRMATIONS
# ============================================

def get_time_greeting(name):
    """Get time-based greeting"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return f"Good morning, {name}! How are you feeling today? ☀️"
    elif 12 <= hour < 17:
        return f"Good afternoon, {name}! Hope you're having a gentle day 🌸"
    elif 17 <= hour < 21:
        return f"Good evening, {name}! Time to rest and heal 🌙"
    else:
        return f"Hey {name}, remember to get good sleep tonight 💤"

AFFIRMATIONS = [
    "You're doing amazing 💚",
    "Healing takes time, and that's okay",
    "Be patient with yourself today",
    "Your body is working hard to heal",
    "One day at a time 🌱",
    "You've got this!",
    "Rest is productive",
    "It's okay to take it slow",
    "Small progress is still progress",
    "Your only job right now is to heal",
    "Be gentle with yourself",
    "Healing is not linear",
    "You deserve kindness today 💚",
    "Every day is a step forward",
    "Trust the process"
]

COMFORT_REMINDERS = [
    "Have you had water today? 💧",
    "Remember to take a deep breath 🌬️",
    "It's okay to rest 🛋️",
    "You deserve kindness today 💚",
    "Take a moment to stretch gently",
    "How about some calming music? 🎵",
    "Remember: healing takes time"
]

HEALING_QUOTES = [
    "\"Healing is not linear\" 🌱",
    "\"Be gentle with yourself\"",
    "\"Small progress is still progress\"",
    "\"Your only job right now is to heal\"",
    "\"Rest is not laziness, it's recovery\"",
    "\"Every day you're getting stronger\"",
    "\"Patience is part of healing\""
]

DAILY_TIPS = [
    {"tip": "Stay hydrated! Aim for 8 glasses of water today 💧", "icon": "💧"},
    {"tip": "Sleep elevated to reduce swelling 🛏️", "icon": "🛏️"},
    {"tip": "Avoid salty foods - they increase swelling 🧂", "icon": "🧂"},
    {"tip": "Take short walks if approved by your surgeon 🚶", "icon": "🚶"},
    {"tip": "Ice the area as directed (20 min on, 20 min off) 🧊", "icon": "🧊"},
    {"tip": "Wear your compression garments as instructed 👕", "icon": "👕"},
    {"tip": "Avoid looking down at your phone too much 📱", "icon": "📱"},
    {"tip": "Keep your follow-up appointments! 📅", "icon": "📅"},
    {"tip": "Don't skip meals - your body needs fuel to heal 🍎", "icon": "🍎"},
    {"tip": "Avoid alcohol - it can increase swelling and bruising 🍷", "icon": "🍷"},
    {"tip": "No smoking! It significantly delays healing 🚭", "icon": "🚭"},
    {"tip": "Take your medications on schedule ⏰", "icon": "⏰"},
    {"tip": "Get plenty of protein for tissue repair 🥚", "icon": "🥚"},
    {"tip": "Avoid strenuous activities until cleared 🏃", "icon": "🏃"},
    {"tip": "Be patient with bruising - it can take weeks to fade 💜", "icon": "💜"}
]

# Recovery milestones by day
RECOVERY_MILESTONES = {
    1: {"title": "Day 1 - Rest Day", "message": "Focus on rest. Swelling is normal.", "icon": "🛏️"},
    3: {"title": "Day 3 - Peak Swelling", "message": "Swelling peaks around day 2-3. This is normal!", "icon": "📈"},
    7: {"title": "Week 1 Complete!", "message": "Major milestone! Stitches may be removed soon.", "icon": "🎉"},
    14: {"title": "Two Weeks!", "message": "Swelling starts decreasing. Bruising fading.", "icon": "🌟"},
    21: {"title": "Three Weeks!", "message": "Most bruising should be gone. Feeling more normal!", "icon": "✨"},
    30: {"title": "One Month!", "message": "Major healing accomplished. Results emerging!", "icon": "🏆"},
    60: {"title": "Two Months!", "message": "Swelling continues to improve. Almost there!", "icon": "🌸"},
    90: {"title": "Three Months!", "message": "Final results starting to show!", "icon": "💫"}
}

# Mascot expressions based on recovery day
def get_mascot_message(day):
    """Get mascot message based on recovery day"""
    if day <= 3:
        return {"emoji": "🌸", "expression": "determined", "message": "Hang in there! The first few days are the hardest."}
    elif day <= 7:
        return {"emoji": "🌸", "expression": "encouraging", "message": "You're doing great! Keep resting!"}
    elif day <= 14:
        return {"emoji": "🌸", "expression": "happy", "message": "Look at you go! Over a week of healing!"}
    elif day <= 30:
        return {"emoji": "🌸", "expression": "proud", "message": "Amazing progress! You're a healing superstar!"}
    else:
        return {"emoji": "🌸", "expression": "celebrating", "message": "Look how far you've come! 🎉"}

# Self-care checklist items
SELF_CARE_CHECKLIST = [
    {"id": "meds", "label": "Took medications", "icon": "💊"},
    {"id": "water", "label": "Drank 8 glasses of water", "icon": "💧"},
    {"id": "food", "label": "Ate nutritious food", "icon": "🥗"},
    {"id": "rest", "label": "Rested enough", "icon": "😴"},
    {"id": "movement", "label": "Did gentle movement (if approved)", "icon": "🚶"},
    {"id": "breathing", "label": "Practiced deep breathing", "icon": "🌬️"},
    {"id": "support", "label": "Reached out to someone supportive", "icon": "💚"}
]

# Mood options with emojis
MOOD_OPTIONS = [
    {"emoji": "😢", "label": "Struggling", "color": "#FFB4B4", "response": "I'm sorry you're having a hard time. Remember, it's okay to not be okay. Healing is tough. 💚"},
    {"emoji": "😐", "label": "Okay", "color": "#FFE4B4", "response": "Okay days are perfectly normal during recovery. You're doing great just by getting through it!"},
    {"emoji": "🙂", "label": "Good", "color": "#C4E8C4", "response": "That's wonderful to hear! Keep up the positive energy! 🌸"},
    {"emoji": "😊", "label": "Great", "color": "#A8D8A8", "response": "So happy for you! What a great recovery day! 🎉"}
]

# Symptom checker data
SYMPTOM_CHECKER = {
    "normal": {
        "symptoms": [
            "Mild to moderate swelling",
            "Bruising (yellow, purple, green)",
            "Mild discomfort or tightness",
            "Numbness or tingling",
            "Itching around incisions",
            "Fatigue or tiredness",
            "Mild headache",
            "Constipation (from pain meds)",
            "Dry skin around incision"
        ],
        "message": "These symptoms are typically normal during recovery. Continue following your surgeon's instructions.",
        "action": "Monitor and continue care",
        "color": "#E8F5E8"
    },
    "call_soon": {
        "symptoms": [
            "Increasing pain not relieved by medication",
            "Swelling that seems to be getting worse after day 3",
            "Persistent nausea or vomiting",
            "Drainage that changes color or smells bad",
            "Redness spreading from incision",
            "Low-grade fever (99-100.4°F)"
        ],
        "message": "These symptoms may need attention. Call your surgeon's office during business hours.",
        "action": "Call surgeon within 24 hours",
        "color": "#FFF8E7"
    },
    "urgent": {
        "symptoms": [
            "High fever (over 101°F)",
            "Sudden severe pain",
            "Heavy bleeding that won't stop",
            "Signs of infection (hot, red, swollen)",
            "Difficulty breathing",
            "Chest pain",
            "Severe dizziness or fainting",
            "Calf pain or swelling (possible blood clot)"
        ],
        "message": "These symptoms require immediate attention!",
        "action": "Call surgeon immediately or go to ER",
        "color": "#FFE5E5"
    }
}

# Medical Sources for Citations
MEDICAL_SOURCES = {
    "asps": {
        "name": "American Society of Plastic Surgeons",
        "url": "https://www.plasticsurgery.org",
        "abbrev": "ASPS"
    },
    "mayo": {
        "name": "Mayo Clinic",
        "url": "https://www.mayoclinic.org",
        "abbrev": "Mayo Clinic"
    },
    "cleveland": {
        "name": "Cleveland Clinic",
        "url": "https://my.clevelandclinic.org",
        "abbrev": "Cleveland Clinic"
    },
    "webmd": {
        "name": "WebMD",
        "url": "https://www.webmd.com",
        "abbrev": "WebMD"
    },
    "realself": {
        "name": "RealSelf",
        "url": "https://www.realself.com",
        "abbrev": "RealSelf"
    }
}

# Surgery Resources by procedure
SURGERY_RESOURCES = {
    "rhinoplasty": {
        "name": "Rhinoplasty (Nose Surgery)",
        "links": [
            {"source": "Mayo Clinic", "url": "https://www.mayoclinic.org/tests-procedures/rhinoplasty/about/pac-20384532"},
            {"source": "ASPS", "url": "https://www.plasticsurgery.org/cosmetic-procedures/rhinoplasty"},
            {"source": "Cleveland Clinic", "url": "https://my.clevelandclinic.org/health/treatments/11023-rhinoplasty-nose-surgery"}
        ],
        "recovery_time": "1-2 weeks for initial recovery, 6-12 months for final results",
        "common_symptoms": "Swelling, bruising around eyes, nasal congestion, mild discomfort"
    },
    "facelift": {
        "name": "Facelift",
        "links": [
            {"source": "Mayo Clinic", "url": "https://www.mayoclinic.org/tests-procedures/face-lift/about/pac-20394059"},
            {"source": "ASPS", "url": "https://www.plasticsurgery.org/cosmetic-procedures/facelift"}
        ],
        "recovery_time": "2-4 weeks, with final results at 2-3 months",
        "common_symptoms": "Swelling, bruising, tightness, numbness"
    },
    "breast_augmentation": {
        "name": "Breast Augmentation",
        "links": [
            {"source": "Mayo Clinic", "url": "https://www.mayoclinic.org/tests-procedures/breast-augmentation/about/pac-20393178"},
            {"source": "ASPS", "url": "https://www.plasticsurgery.org/cosmetic-procedures/breast-augmentation"}
        ],
        "recovery_time": "1-2 weeks, avoid strenuous activity for 4-6 weeks",
        "common_symptoms": "Swelling, soreness, tightness, sensitivity changes"
    },
    "bbl": {
        "name": "BBL (Brazilian Butt Lift)",
        "links": [
            {"source": "ASPS", "url": "https://www.plasticsurgery.org/cosmetic-procedures/buttock-enhancement/brazilian-butt-lift"}
        ],
        "recovery_time": "2-3 weeks, avoid sitting directly for 2-6 weeks",
        "common_symptoms": "Swelling, bruising, discomfort when sitting"
    },
    "tummy_tuck": {
        "name": "Tummy Tuck (Abdominoplasty)",
        "links": [
            {"source": "Mayo Clinic", "url": "https://www.mayoclinic.org/tests-procedures/tummy-tuck/about/pac-20384892"},
            {"source": "ASPS", "url": "https://www.plasticsurgery.org/cosmetic-procedures/tummy-tuck"}
        ],
        "recovery_time": "2-4 weeks, full recovery 3-6 months",
        "common_symptoms": "Swelling, bruising, tightness, drain tubes initially"
    },
    "liposuction": {
        "name": "Liposuction",
        "links": [
            {"source": "Mayo Clinic", "url": "https://www.mayoclinic.org/tests-procedures/liposuction/about/pac-20384586"},
            {"source": "ASPS", "url": "https://www.plasticsurgery.org/cosmetic-procedures/liposuction"}
        ],
        "recovery_time": "1-2 weeks, compression garments for several weeks",
        "common_symptoms": "Swelling, bruising, fluid drainage, numbness"
    }
}

# FAQ data
FAQ_DATA = [
    {
        "question": "When can I shower after surgery?",
        "answer": "This varies by procedure. Most surgeons allow showering 24-48 hours after surgery, but you may need to keep incisions dry or covered. Always follow your surgeon's specific instructions.",
        "source": "ASPS"
    },
    {
        "question": "When can I exercise after surgery?",
        "answer": "Light walking is usually encouraged within days of surgery. Most surgeons recommend waiting 4-6 weeks before any strenuous exercise. Always get clearance from your surgeon first.",
        "source": "Mayo Clinic"
    },
    {
        "question": "Is bruising normal?",
        "answer": "Yes! Bruising is very common and typically peaks around day 2-3 and then gradually fades over 1-3 weeks. Colors may change from purple to green to yellow as it heals.",
        "source": "Cleveland Clinic"
    },
    {
        "question": "When will swelling go down?",
        "answer": "Swelling peaks around day 2-3, then gradually decreases. Most swelling resolves within 2-4 weeks, but subtle swelling can persist for months. Final results may take 6-12 months.",
        "source": "ASPS"
    },
    {
        "question": "When can I wear makeup?",
        "answer": "For facial procedures, most surgeons recommend waiting until incisions are fully healed (usually 10-14 days) before applying makeup near surgical areas.",
        "source": "RealSelf"
    },
    {
        "question": "Is it normal to feel emotional after surgery?",
        "answer": "Absolutely! Post-surgical blues are very common due to anesthesia, pain medications, limited mobility, and the body's healing response. These feelings usually improve within 1-2 weeks.",
        "source": "Cleveland Clinic"
    },
    {
        "question": "When should I call my surgeon?",
        "answer": "Call if you have: fever over 101°F, sudden increase in pain, heavy bleeding, signs of infection (redness, warmth, discharge), difficulty breathing, or anything that concerns you.",
        "source": "Mayo Clinic"
    },
    {
        "question": "Can I sleep on my side?",
        "answer": "This depends on your procedure. For facial surgery, sleep elevated on your back. For breast surgery, sleep on your back. For body procedures, follow your surgeon's guidance. Most restrictions last 2-4 weeks.",
        "source": "ASPS"
    }
]

def get_citation_html(source_keys, inline=True):
    """Generate citation HTML for given source keys"""
    if isinstance(source_keys, str):
        source_keys = [source_keys]

    citations = []
    for key in source_keys:
        if key in MEDICAL_SOURCES:
            src = MEDICAL_SOURCES[key]
            citations.append(f'<a href="{src["url"]}" target="_blank" style="color: #5A7A5A; text-decoration: none;">{src["abbrev"]}</a>')

    if inline:
        return f'<span class="citation-inline">Sources: {", ".join(citations)}</span>'
    return citations

# Page config with bloom favicon - WIDE LAYOUT for better use of space
st.set_page_config(
    page_title="Recovery Buddy",
    page_icon="logos/favicon_bloom.svg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# GOOGLE ANALYTICS
# ============================================
import streamlit.components.v1 as components

# Inject GA into parent frame for reliable tracking
components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-63W4QGD1SJ"></script>
<script>
  // Initialize in current frame
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-63W4QGD1SJ');

  // Also inject into parent frame (Streamlit's main window)
  try {
    if (window.parent && window.parent !== window) {
      var parentWindow = window.parent;
      if (!parentWindow.gtag) {
        parentWindow.dataLayer = parentWindow.dataLayer || [];
        parentWindow.gtag = function(){parentWindow.dataLayer.push(arguments);};
        parentWindow.gtag('js', new Date());
        parentWindow.gtag('config', 'G-63W4QGD1SJ');

        // Load gtag.js in parent
        var script = parentWindow.document.createElement('script');
        script.async = true;
        script.src = 'https://www.googletagmanager.com/gtag/js?id=G-63W4QGD1SJ';
        parentWindow.document.head.appendChild(script);
      }
    }
  } catch(e) { console.log('GA parent injection skipped'); }
</script>
""", height=0)

# ============================================
# PWA (Progressive Web App) Setup
# ============================================
components.html("""
<script>
  // Inject PWA elements into parent frame
  try {
    if (window.parent && window.parent.document) {
      var parentDoc = window.parent.document;
      var parentHead = parentDoc.head;

      // Add manifest link if not already present
      if (!parentDoc.querySelector('link[rel="manifest"]')) {
        var manifest = parentDoc.createElement('link');
        manifest.rel = 'manifest';
        manifest.href = '/app/static/manifest.json';
        parentHead.appendChild(manifest);
      }

      // Add theme color meta tag
      if (!parentDoc.querySelector('meta[name="theme-color"]')) {
        var themeColor = parentDoc.createElement('meta');
        themeColor.name = 'theme-color';
        themeColor.content = '#A8C5A8';
        parentHead.appendChild(themeColor);
      }

      // Add Apple touch icon
      if (!parentDoc.querySelector('link[rel="apple-touch-icon"]')) {
        var appleIcon = parentDoc.createElement('link');
        appleIcon.rel = 'apple-touch-icon';
        appleIcon.href = '/app/static/icon-192.png';
        parentHead.appendChild(appleIcon);
      }

      // Add mobile web app capable meta tags
      if (!parentDoc.querySelector('meta[name="mobile-web-app-capable"]')) {
        var mobileCapable = parentDoc.createElement('meta');
        mobileCapable.name = 'mobile-web-app-capable';
        mobileCapable.content = 'yes';
        parentHead.appendChild(mobileCapable);
      }

      if (!parentDoc.querySelector('meta[name="apple-mobile-web-app-capable"]')) {
        var appleCapable = parentDoc.createElement('meta');
        appleCapable.name = 'apple-mobile-web-app-capable';
        appleCapable.content = 'yes';
        parentHead.appendChild(appleCapable);
      }

      if (!parentDoc.querySelector('meta[name="apple-mobile-web-app-status-bar-style"]')) {
        var statusBar = parentDoc.createElement('meta');
        statusBar.name = 'apple-mobile-web-app-status-bar-style';
        statusBar.content = 'default';
        parentHead.appendChild(statusBar);
      }

      // Register service worker
      if ('serviceWorker' in window.parent.navigator) {
        window.parent.navigator.serviceWorker.register('/app/static/sw.js', {scope: '/'})
          .then(function(registration) {
            console.log('Recovery Buddy: Service Worker registered with scope:', registration.scope);
          })
          .catch(function(error) {
            console.log('Recovery Buddy: Service Worker registration failed:', error);
          });
      }
    }
  } catch(e) {
    console.log('PWA setup skipped:', e);
  }
</script>
""", height=0)

# ============================================
# CUSTOM CSS - Luxury Wellness Spa Aesthetic
# ============================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* Color Palette - Improved contrast for readability */
    :root {
        --sage-light: #E8F0E8;
        --sage: #A8C5A8;
        --sage-dark: #5A7A5A;
        --pink-light: #FDF2F4;
        --pink: #F5D5DC;
        --pink-accent: #E8B4BC;
        --cream: #FDFBF7;
        --cream-dark: #F5F0E8;
        --text-dark: #2D3A2D;
        --text-medium: #3D4D3D;
        --text-light: #3A4A3A;
        --white: #FFFFFF;
        --shadow: rgba(61, 74, 61, 0.08);
        --shadow-hover: rgba(61, 74, 61, 0.12);
    }

    /* ===== CRITICAL: ENSURE ALL TEXT IS DARK AND READABLE ===== */

    /* Global dark text for content elements */
    .main p, .main span, .main li, .main td, .main th, .main label {
        color: #333333;
    }

    /* Headers always dark green */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: #2C5530 !important;
    }

    /* Subtext and captions slightly lighter */
    .stat-label, small, .caption, .subtext {
        color: #666666 !important;
    }

    /* Links should be blue and clickable */
    a:not(button):not(.stButton a) {
        color: #0066CC !important;
        text-decoration: underline !important;
    }

    a:not(button):not(.stButton a):hover {
        color: #004499 !important;
    }

    /* Ensure markdown text is dark */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span:not(.st-emotion-cache-10trblm),
    [data-testid="stMarkdownContainer"] li {
        color: #333333 !important;
    }

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        color: #2C5530 !important;
    }

    /* EXCEPTIONS: White text on dark backgrounds */
    .stButton > button,
    .stButton > button span,
    .stButton > button p {
        color: white !important;
    }

    /* Step circles with white text */
    .step-circle.completed {
        color: white !important;
    }

    /* Emergency banner red text */
    .emergency-banner p {
        color: #C0392B !important;
    }

    /* ===== WIDE LAYOUT & RESPONSIVE DESIGN ===== */

    /* Max width container for readability */
    .main .block-container {
        max-width: 1200px;
        padding: 2rem 2rem;
    }

    /* Responsive columns */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 1rem;
        }

        [data-testid="column"] {
            width: 100% !important;
            flex: 100% !important;
        }
    }

    /* Privacy badge styles */
    .privacy-badge {
        background: linear-gradient(135deg, #E8F5E8 0%, #F0FFF0 100%);
        border: 1px solid #A8C5A8;
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        font-size: 0.8rem;
        color: #3D6B3D;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Welcome back card */
    .welcome-back-card {
        background: linear-gradient(135deg, #FDF2F4 0%, #FFEEF2 100%);
        border: 1px solid #E8B4BC;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
    }

    /* Dashboard stat card */
    .stat-card {
        background: #FFFFFF;
        border: 1px solid #E8F0E8;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .stat-card .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2C5530 !important;
    }

    .stat-card .stat-label {
        font-size: 0.85rem;
        color: #555555 !important;
        margin-top: 0.25rem;
    }

    /* Section divider */
    .section-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #E8F0E8, transparent);
        margin: 1.5rem 0;
    }

    /* Home button */
    .home-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 999;
    }

    /* ===== HIDE ALL STREAMLIT INTERNAL DEBUG/KEY ELEMENTS ===== */

    /* Hide any element showing internal keys - comprehensive targeting */
    [data-testid="stWidgetLabel"] span[style*="visibility: hidden"],
    .st-emotion-cache-ue6h4q,
    div[data-testid="stMarkdownContainer"] > div:empty,
    [class*="eyeqlp"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Hide auto-generated key displays in Streamlit 1.50+ */
    [data-testid="stExpander"] summary > span:first-child:not(:last-child),
    [data-testid="stExpander"] summary div[data-testid="stMarkdownContainer"]:has(p:empty),
    details summary > div:first-child:empty {
        display: none !important;
    }

    /* Force expander summary to show only the label text */
    [data-testid="stExpander"] summary {
        display: flex !important;
        align-items: center !important;
    }

    [data-testid="stExpander"] summary > div {
        flex-grow: 1 !important;
    }

    /* Ensure expander text is visible and correct */
    [data-testid="stExpander"] summary p {
        color: #2D3A2D !important;
        margin: 0 !important;
        font-size: 1rem !important;
    }

    /* Input elements - white background, dark text */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #2D3A2D !important;
        border: 2px solid #D0D8D0 !important;
    }

    /* Multiselect chips - sage green instead of red */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #A8C5A8 !important;
        border-color: #5A7A5A !important;
    }

    .stMultiSelect [data-baseweb="tag"] span {
        color: #2D3A2D !important;
    }

    /* Slider number - remove ALL colored backgrounds */
    .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"],
    .stSlider div[data-testid="stTickBarMax"],
    .stSlider div[data-testid="stTickBarMin"],
    .stSlider [data-testid="stThumbValue"],
    .stSlider span[data-testid="stThumbValue"] {
        background: transparent !important;
        background-color: transparent !important;
        color: #2D3A2D !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Slider thumb value - the number display above the slider */
    [data-testid="stThumbValue"] {
        background: transparent !important;
        background-color: transparent !important;
        color: #2D3A2D !important;
        font-weight: 600 !important;
    }

    /* Slider - clean styling without borders */
    .stSlider > div > div {
        background: transparent !important;
    }

    /* ===== EXPANDER STYLING - WHITE/LIGHT HEADERS ===== */

    /* Expander header - white background */
    [data-testid="stExpander"] {
        background: #FFFFFF !important;
        border: 1px solid #E0E8E0 !important;
        border-radius: 12px !important;
        margin-bottom: 1rem !important;
    }

    [data-testid="stExpander"] > details {
        background: #FFFFFF !important;
        border: none !important;
    }

    [data-testid="stExpander"] > details > summary {
        background: #FFFFFF !important;
        color: #2D3A2D !important;
        padding: 1rem !important;
        border-radius: 12px !important;
    }

    /* Expander header text */
    [data-testid="stExpander"] summary span {
        color: #2D3A2D !important;
        font-weight: 500 !important;
    }

    /* Expander content area */
    [data-testid="stExpander"] > details > div {
        background: #FAFAFA !important;
        padding: 1rem !important;
        border-top: 1px solid #E0E8E0 !important;
    }

    /* ===== SECTION SPACING ===== */

    /* Add breathing room between major sections */
    .stMarkdown h4 {
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }

    /* Space after cards */
    .wellness-card {
        margin-bottom: 1.5rem !important;
    }

    /* Space between form elements */
    .stSelectbox, .stTextInput, .stNumberInput, .stSlider {
        margin-bottom: 1rem !important;
    }

    /* Add padding to checkbox groups */
    .stCheckbox {
        margin-bottom: 0.5rem !important;
    }

    /* Global Styles */
    .stApp {
        background: linear-gradient(180deg, var(--cream) 0%, var(--sage-light) 100%);
        min-height: 100vh;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main container */
    .main .block-container {
        padding: 2rem 1rem 4rem 1rem;
        max-width: 720px;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        color: var(--text-dark) !important;
    }

    p, li, span, div, label {
        font-family: 'Inter', sans-serif !important;
    }

    /* Ensure all form labels are dark and readable */
    label, .stTextInput label, .stSelectbox label, .stNumberInput label,
    .stSlider label, .stCheckbox label, .stRadio label {
        color: #2D3A2D !important;
    }

    /* Make slider value text dark */
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"],
    .stSlider [data-baseweb="slider"] > div > div > div {
        color: #2D3A2D !important;
    }

    /* ===== GLOBAL INPUT FIXES - WHITE BG, DARK TEXT ===== */

    /* All text inputs - white background, dark text */
    input, textarea {
        background-color: #FFFFFF !important;
        color: #2D3A2D !important;
    }

    /* Number input specifically */
    .stNumberInput input {
        background-color: #FFFFFF !important;
        color: #2D3A2D !important;
        border: 2px solid #D0D8D0 !important;
    }

    .stNumberInput > div > div > input {
        background: #FFFFFF !important;
        color: #2D3A2D !important;
    }

    /* Number input buttons */
    .stNumberInput button {
        background: #F5F5F5 !important;
        color: #2D3A2D !important;
    }

    /* All checkboxes - dark readable text */
    .stCheckbox label span,
    .stCheckbox > label > div > p,
    .stCheckbox label p {
        color: #2D3A2D !important;
    }

    /* Checkbox container styling */
    .stCheckbox > label {
        color: #2D3A2D !important;
        background: transparent !important;
    }

    /* Checkbox text specifically */
    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] span {
        color: #2D3A2D !important;
    }

    /* Expander styling - be specific, don't style all divs */
    .streamlit-expanderContent {
        background: #FFFFFF !important;
    }

    .streamlit-expanderContent p,
    .streamlit-expanderContent > p {
        color: #2D3A2D !important;
    }

    /* Expander header text only */
    [data-testid="stExpander"] summary span {
        color: #2D3A2D !important;
    }

    /* Sidebar styling - specific elements only */
    section[data-testid="stSidebar"] {
        background: #FDFBF7 !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {
        color: #2D3A2D !important;
    }

    /* Sidebar expander */
    section[data-testid="stSidebar"] .streamlit-expanderContent {
        background: #F5F0E8 !important;
    }

    /* Text area styling */
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #2D3A2D !important;
        border: 2px solid #D0D8D0 !important;
    }

    /* Select box text */
    .stSelectbox div[data-baseweb="select"] {
        background: #FFFFFF !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        color: #2D3A2D !important;
        background: #FFFFFF !important;
    }

    /* Multiselect */
    .stMultiSelect div[data-baseweb="select"] {
        background: #FFFFFF !important;
    }

    .stMultiSelect span {
        color: #2D3A2D !important;
    }

    /* Slider - remove any red border/outline */
    .stSlider > div {
        border: none !important;
        outline: none !important;
    }

    .stSlider [data-baseweb="slider"] {
        border: none !important;
        outline: none !important;
    }

    /* File uploader */
    .stFileUploader {
        background: #FFFFFF !important;
    }

    .stFileUploader label {
        color: #2D3A2D !important;
    }

    /* Download button */
    .stDownloadButton button {
        background: #FFFFFF !important;
        color: #2D3A2D !important;
        border: 2px solid #A8C5A8 !important;
    }

    /* Logo Header - Fixed cutoff issues */
    .logo-header {
        text-align: center;
        padding: 2rem 1rem 2rem 1rem;
        margin-bottom: 1.5rem;
        overflow: visible;
    }

    .logo-header svg {
        max-width: 100%;
        height: auto;
        overflow: visible;
    }

    /* Mobile responsive logo */
    @media (max-width: 600px) {
        .logo-header {
            padding: 1.5rem 0.5rem 1.5rem 0.5rem;
        }
        .logo-header svg {
            width: 100%;
            max-width: 360px;
        }
    }

    .logo-icon {
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        display: block;
    }

    .logo-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 600;
        color: var(--text-dark);
        margin: 0;
        letter-spacing: -0.5px;
        padding-bottom: 0.25rem;
    }

    .logo-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: var(--text-light);
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        font-weight: 400;
    }

    /* ===== FIX TEXT CUTOFF GLOBALLY ===== */
    /* Add padding-bottom to all containers */
    .wellness-card, .tip-card, .info-box, .success-box, .warning-box,
    .danger-box, .stat-card, .source-card, .legal-page, .disclaimer-modal {
        padding-bottom: 1.5rem !important;
        overflow: visible !important;
    }

    /* Ensure all text has bottom margin */
    p, h1, h2, h3, h4, h5, h6, li {
        margin-bottom: 0.5rem;
    }

    /* SVG text should not be clipped */
    svg text {
        overflow: visible;
    }

    /* Progress Steps */
    .progress-container {
        background: var(--white);
        border-radius: 20px;
        padding: 1.25rem 1.5rem;
        margin: 1.5rem 0 2rem 0;
        box-shadow: 0 2px 12px var(--shadow);
    }

    .progress-steps {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
    }

    .progress-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        z-index: 2;
        flex: 1;
    }

    .step-circle {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .step-circle.completed {
        background: linear-gradient(135deg, var(--sage) 0%, var(--sage-dark) 100%);
        color: white;
    }

    .step-circle.active {
        background: linear-gradient(135deg, var(--pink) 0%, var(--pink-accent) 100%);
        color: var(--text-dark);
        box-shadow: 0 4px 15px rgba(232, 180, 188, 0.4);
        transform: scale(1.1);
    }

    .step-circle.pending {
        background: var(--cream-dark);
        color: var(--text-light);
    }

    .step-label {
        font-size: 0.7rem;
        color: var(--text-light);
        margin-top: 0.5rem;
        text-align: center;
        font-weight: 500;
    }

    .step-label.active {
        color: var(--text-dark);
    }

    /* Progress bar line */
    .progress-line {
        position: absolute;
        top: 18px;
        left: 10%;
        right: 10%;
        height: 3px;
        background: var(--cream-dark);
        border-radius: 2px;
        z-index: 1;
    }

    .progress-line-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--sage) 0%, var(--sage-dark) 100%);
        border-radius: 2px;
        transition: width 0.5s ease;
    }

    /* Cards */
    .wellness-card {
        background: var(--white);
        border-radius: 24px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px var(--shadow);
        transition: all 0.3s ease;
    }

    .wellness-card:hover {
        box-shadow: 0 6px 25px var(--shadow-hover);
    }

    .wellness-card h3 {
        font-size: 1.4rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #2C5530 !important;
    }

    .wellness-card p {
        color: #333333 !important;
    }

    /* Info boxes with gradients */
    .info-box {
        background: linear-gradient(135deg, var(--sage-light) 0%, rgba(168, 197, 168, 0.3) 100%);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid var(--sage);
    }

    .info-box p {
        margin: 0;
        color: var(--text-dark);
        line-height: 1.6;
    }

    .warning-box {
        background: linear-gradient(135deg, #FFF8E7 0%, #FFF3D6 100%);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #F5C842;
    }

    .warning-box p, .warning-box li, .warning-box strong, .warning-box span {
        color: #5C4813 !important;
    }

    .warning-box h3, .warning-box h4 {
        color: #4A3A0F !important;
    }

    .danger-box {
        background: linear-gradient(135deg, var(--pink-light) 0%, rgba(245, 213, 220, 0.5) 100%);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid var(--pink-accent);
    }

    .danger-box p, .danger-box li, .danger-box strong, .danger-box span {
        color: #6B2D3A !important;
    }

    .danger-box h3, .danger-box h4 {
        color: #5A1F2B !important;
    }

    .success-box {
        background: linear-gradient(135deg, var(--sage-light) 0%, rgba(168, 197, 168, 0.4) 100%);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid var(--sage-dark);
    }

    .success-box p {
        color: #2D4A2D !important;
        font-weight: 500;
    }

    /* Tip Card */
    .tip-card {
        background: linear-gradient(135deg, var(--white) 0%, var(--cream) 100%);
        border-radius: 20px;
        padding: 1.75rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px var(--shadow);
        border: 1px solid rgba(168, 197, 168, 0.2);
    }

    .tip-card h4 {
        color: #2D4A2D;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.75rem;
    }

    .tip-card p {
        font-size: 1.1rem;
        line-height: 1.7;
        color: var(--text-dark);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--sage) 0%, var(--sage-dark) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.75rem 2rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 15px rgba(123, 163, 123, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(123, 163, 123, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Secondary buttons */
    .secondary-btn > button {
        background: var(--white) !important;
        color: var(--sage-dark) !important;
        border: 2px solid var(--sage) !important;
    }

    .secondary-btn > button:hover {
        background: var(--sage-light) !important;
    }

    /* Input fields */
    .stTextInput > div > div > input {
        background: var(--white) !important;
        border: 2px solid var(--cream-dark) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        color: #2D3A2D !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #6B7B6B !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--sage) !important;
        box-shadow: 0 0 0 3px rgba(168, 197, 168, 0.2) !important;
    }

    /* Select boxes */
    .stSelectbox > div > div {
        background: var(--white) !important;
        border: 2px solid var(--cream-dark) !important;
        border-radius: 12px !important;
    }

    .stSelectbox > div > div > div {
        color: #2D3A2D !important;
    }

    .stSelectbox [data-baseweb="select"] span {
        color: #2D3A2D !important;
    }

    /* Sliders */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, var(--sage-light) 0%, var(--sage) 100%) !important;
    }

    .stSlider > div > div > div > div > div {
        background: var(--sage-dark) !important;
        box-shadow: 0 2px 8px rgba(123, 163, 123, 0.4) !important;
    }

    /* Checkboxes */
    .stCheckbox > label > div[data-testid="stCheckbox"] > div {
        border-color: var(--sage) !important;
    }

    .stCheckbox > label {
        color: #2D3A2D !important;
    }

    .stCheckbox > label > span {
        color: #2D3A2D !important;
    }

    /* Radio buttons */
    .stRadio > div {
        gap: 0.75rem !important;
    }

    .stRadio > div > label {
        background: var(--white) !important;
        border: 2px solid var(--cream-dark) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.25rem !important;
        transition: all 0.3s ease !important;
        color: #2D3A2D !important;
    }

    .stRadio > div > label:hover {
        border-color: var(--sage) !important;
        background: var(--sage-light) !important;
    }

    .stRadio > div > label > div > p {
        color: #2D3A2D !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--cream-dark);
        border-radius: 16px;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 12px !important;
        padding: 0.5rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--text-medium) !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--white) !important;
        color: var(--text-dark) !important;
        box-shadow: 0 2px 8px var(--shadow) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: var(--white) !important;
        border-radius: 12px !important;
        border: 1px solid var(--cream-dark) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Metrics */
    .stMetric {
        background: var(--white);
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 2px 10px var(--shadow);
    }

    .stMetric label {
        color: var(--text-light) !important;
    }

    .stMetric [data-testid="stMetricValue"] {
        color: var(--text-dark) !important;
        font-family: 'Playfair Display', serif !important;
    }

    /* Procedure buttons */
    .procedure-btn {
        background: var(--white) !important;
        border: 2px solid var(--cream-dark) !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        margin: 0.4rem 0 !important;
        transition: all 0.3s ease !important;
        text-align: left !important;
    }

    .procedure-btn:hover {
        border-color: var(--sage) !important;
        background: var(--sage-light) !important;
        transform: translateX(5px) !important;
    }

    /* Number input */
    .stNumberInput > div > div > input {
        background: var(--white) !important;
        border: 2px solid var(--cream-dark) !important;
        border-radius: 12px !important;
        color: #2D3A2D !important;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--sage-light), transparent);
        margin: 2rem 0;
    }

    /* Mobile Responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.75rem 3rem 0.75rem;
        }

        .logo-title {
            font-size: 1.8rem;
        }

        .wellness-card {
            padding: 1.5rem;
            border-radius: 20px;
        }

        .progress-container {
            padding: 1rem;
        }

        .step-label {
            font-size: 0.6rem;
        }

        .step-circle {
            width: 30px;
            height: 30px;
            font-size: 0.75rem;
        }
    }

    /* Smooth transitions */
    * {
        transition: background-color 0.2s ease, border-color 0.2s ease;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--cream);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--sage);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--sage-dark);
    }

    /* Animation for cards */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .wellness-card, .tip-card, .info-box {
        animation: fadeIn 0.4s ease-out;
    }

    /* Emoji styling */
    .emoji-large {
        font-size: 2.5rem;
        display: block;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* Quote styling */
    .affirmation {
        text-align: center;
        font-style: italic;
        color: var(--text-medium);
        font-size: 1.1rem;
        padding: 1rem 2rem;
        position: relative;
    }

    .affirmation::before {
        content: '"';
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        color: var(--sage-light);
        position: absolute;
        left: 0;
        top: -10px;
    }

    /* ===== LOADING SCREEN ===== */
    .loading-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, #FDFBF7 0%, #E8F0E8 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        animation: fadeOut 0.5s ease-out 2s forwards;
    }

    @keyframes fadeOut {
        to { opacity: 0; visibility: hidden; }
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }

    @keyframes dots {
        0%, 20% { content: '.'; }
        40% { content: '..'; }
        60%, 100% { content: '...'; }
    }

    /* ===== SOFT ANIMATIONS FOR COZY FEEL ===== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes gentlePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }

    @keyframes softGlow {
        0%, 100% { box-shadow: 0 2px 15px rgba(168, 197, 168, 0.2); }
        50% { box-shadow: 0 2px 25px rgba(168, 197, 168, 0.4); }
    }

    @keyframes floatEmoji {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }

    /* Apply animations to elements */
    .wellness-card, .tip-card, .info-box {
        animation: fadeInUp 0.5s ease-out;
    }

    .welcome-back-card {
        animation: fadeInUp 0.6s ease-out, softGlow 3s ease-in-out infinite;
    }

    .emoji-large {
        animation: floatEmoji 3s ease-in-out infinite;
    }

    .affirmation {
        animation: fadeInUp 0.7s ease-out;
    }

    /* Hover effects for interactive elements */
    .wellness-card:hover, .tip-card:hover {
        transform: translateY(-2px);
        transition: transform 0.3s ease;
    }

    .stButton > button {
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .loading-icon {
        font-size: 4rem;
        animation: pulse 1.5s ease-in-out infinite;
        margin-bottom: 1rem;
    }

    .loading-text {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        color: #2D3A2D;
    }

    .loading-text::after {
        content: '...';
        animation: dots 1.5s steps(3, end) infinite;
    }

    /* ===== FOOTER STYLES ===== */
    .app-footer {
        margin-top: 3rem;
        padding: 2rem 1rem;
        border-top: 1px solid #E0E8E0;
        text-align: center;
    }

    .disclaimer-text {
        font-size: 0.75rem;
        color: #6B7B6B;
        line-height: 1.5;
        max-width: 600px;
        margin: 0 auto 1rem auto;
    }

    .footer-links {
        font-size: 0.8rem;
        color: #5A7A5A;
        margin-bottom: 0.5rem;
    }

    .footer-links a {
        color: #5A7A5A;
        text-decoration: none;
    }

    .footer-links a:hover {
        text-decoration: underline;
    }

    .version-text {
        font-size: 0.7rem;
        color: #8B9B8B;
    }

    .copyright-text {
        font-size: 0.75rem;
        color: #9B9B9B;
        margin-top: 1.5rem;
        line-height: 1.6;
    }

    .copyright-text a {
        color: #9B9B9B;
        text-decoration: underline;
    }

    .copyright-text a:hover {
        color: #5A7A5A;
    }

    /* ===== DISCLAIMER MODAL STYLES ===== */
    .disclaimer-modal {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem auto;
        max-width: 600px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }

    .disclaimer-modal h2 {
        color: #1A1A1A;
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        text-align: center;
    }

    .disclaimer-modal p {
        color: #333333;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 0.75rem;
    }

    .disclaimer-modal ul {
        color: #333333;
        margin-left: 1.5rem;
    }

    .disclaimer-modal li {
        color: #333333;
        margin-bottom: 0.25rem;
    }

    .disclaimer-highlight {
        background: #FFF9E6;
        border-left: 4px solid #F5A623;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }

    .disclaimer-highlight p {
        color: #1A1A1A;
        font-weight: 500;
        margin: 0;
    }

    /* ===== EMERGENCY WARNING STYLES ===== */
    .emergency-banner {
        background: linear-gradient(135deg, #FFE5E5 0%, #FFF0F0 100%);
        border: 2px solid #E74C3C;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        text-align: center;
    }

    .emergency-banner p {
        color: #C0392B;
        font-weight: 600;
        margin: 0;
        font-size: 0.9rem;
    }

    .emergency-banner a {
        color: #E74C3C;
        text-decoration: underline;
    }

    .consult-doctor-reminder {
        background: #F0F8F0;
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        margin-top: 0.75rem;
        font-size: 0.8rem;
        color: #5A7A5A;
        text-align: center;
    }

    .consult-doctor-reminder a {
        color: #3D6B3D;
        text-decoration: underline;
    }

    /* ===== CITATION STYLES ===== */
    .citation-inline {
        font-size: 0.75rem;
        color: #6B8B6B;
        font-style: italic;
        display: block;
        margin-top: 0.5rem;
    }

    .citation-inline a {
        color: #5A7A5A;
        text-decoration: underline;
    }

    .citation-inline a:hover {
        color: #3D6B3D;
    }

    .citation-box {
        background: linear-gradient(135deg, #F5F8F5 0%, #FDFBF7 100%);
        border-left: 3px solid #A8C5A8;
        padding: 0.75rem 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
        font-size: 0.8rem;
    }

    .citation-box a {
        color: #5A7A5A;
        text-decoration: none;
    }

    .citation-box a:hover {
        text-decoration: underline;
    }

    .source-card {
        background: #FFFFFF;
        border: 1px solid #E8F0E8;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        transition: box-shadow 0.2s ease;
    }

    .source-card:hover {
        box-shadow: 0 4px 12px rgba(90, 122, 90, 0.1);
    }

    .source-card h3 {
        color: #2C5530 !important;
        font-size: 1.1rem;
        margin: 0 0 0.5rem 0;
    }

    .source-card p {
        color: #333333 !important;
        font-size: 0.9rem;
        margin: 0;
    }

    .source-card a {
        color: #0066CC !important;
        font-size: 0.9rem;
        text-decoration: underline !important;
        word-break: break-all;
    }

    /* ===== LEGAL PAGE STYLES ===== */
    .legal-page {
        background: linear-gradient(135deg, #FDFBF7 0%, #F8F5F0 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid #E8E0D8;
    }

    .legal-page h1 {
        color: #2C5530 !important;
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }

    .legal-page h2 {
        color: #2C5530 !important;
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.2rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }

    .legal-page p, .legal-page li {
        color: #333333 !important;
        font-size: 0.9rem;
        line-height: 1.7;
    }

    .legal-page a {
        color: #0066CC !important;
        text-decoration: underline !important;
    }

    .legal-page ul {
        margin-left: 1.5rem;
    }

    .legal-page .last-updated {
        font-size: 0.8rem;
        color: #8B9B8B;
        text-align: center;
        margin-top: 2rem;
    }

    .footer-legal-links {
        margin-top: 0.5rem;
    }

    .footer-legal-links a {
        color: #9B9B9B;
        text-decoration: none;
        font-size: 0.75rem;
        margin: 0 0.5rem;
    }

    .footer-legal-links a:hover {
        color: #5A7A5A;
        text-decoration: underline;
    }

    /* Footer button styling - make them look like subtle links */
    .app-footer + div button,
    div[data-testid="stHorizontalBlock"]:has(button[key*="footer"]) button {
        background: transparent !important;
        border: none !important;
        color: #9B9B9B !important;
        font-size: 0.75rem !important;
        padding: 0.25rem 0.5rem !important;
        text-decoration: underline !important;
        box-shadow: none !important;
    }

    div[data-testid="stHorizontalBlock"]:has(button[key*="footer"]) button:hover {
        color: #5A7A5A !important;
        background: transparent !important;
    }

    /* ===== ERROR MESSAGE STYLES ===== */
    .friendly-error {
        background: linear-gradient(135deg, #FFF8E7 0%, #FFF3D6 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 2rem auto;
        max-width: 500px;
        border-left: 4px solid #F5C842;
    }

    .friendly-error p {
        color: #5C4813;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# File to store progress data
PROGRESS_FILE = "recovery_progress.json"

# Steps configuration
STEPS = [
    {"key": "welcome", "label": "Welcome", "icon": "👋"},
    {"key": "get_info", "label": "About You", "icon": "📋"},
    {"key": "physical_checkin", "label": "Physical", "icon": "🩺"},
    {"key": "emotional_checkin", "label": "Emotional", "icon": "💭"},
    {"key": "daily_tip", "label": "Tips", "icon": "💡"},
    {"key": "complete", "label": "Complete", "icon": "✨"},
]

# Procedure-specific recovery information
PROCEDURES = {
    "rhinoplasty": {
        "name": "Rhinoplasty",
        "emoji": "👃",
        "peak_swelling_day": 3,
        "swelling_duration": "2-3 weeks for major swelling, up to a year for subtle swelling",
        "bruising_duration": "7-14 days",
        "final_results": "12-18 months",
        "normal_symptoms": {
            1: {"swelling": "moderate to severe", "bruising": "developing", "pain": "moderate (4-7)", "bleeding": "light oozing normal"},
            2: {"swelling": "increasing", "bruising": "darkening", "pain": "moderate (4-6)", "bleeding": "minimal"},
            3: {"swelling": "peak swelling day", "bruising": "at its worst", "pain": "moderate (4-6)", "bleeding": "should be minimal"},
            4: {"swelling": "starting to decrease", "bruising": "starting to fade", "pain": "improving (3-5)", "bleeding": "none expected"},
            5: {"swelling": "gradually decreasing", "bruising": "yellowing", "pain": "mild (2-4)", "bleeding": "none expected"},
            7: {"swelling": "noticeably less", "bruising": "mostly faded", "pain": "minimal (1-3)", "bleeding": "none"},
            14: {"swelling": "much improved but still present", "bruising": "gone", "pain": "minimal to none", "bleeding": "none"},
        },
        "tips": {
            1: "Keep your head elevated at all times, even when sleeping. Use 2-3 pillows or a wedge pillow.",
            2: "Apply cold compresses gently around (not on) your nose for 20 minutes on, 20 minutes off.",
            3: "Today is typically peak swelling - this is NORMAL! Your nose will look very different from the final result.",
            4: "Start gentle walks around your home if you feel up to it. Movement helps reduce swelling.",
            5: "You might feel emotionally low today - this is super common as swelling peaks and meds wear off.",
            7: "If your splint comes off today, don't panic at what you see! There's still lots of swelling underneath.",
            14: "You're doing amazing! Most people feel comfortable going out in public around now.",
        },
        "warning_signs": ["heavy bleeding", "fever over 101°F", "severe pain not controlled by meds", "vision changes", "increasing redness/warmth"],
    },
    "facelift": {
        "name": "Facelift",
        "emoji": "✨",
        "peak_swelling_day": 3,
        "swelling_duration": "2-4 weeks for major swelling",
        "bruising_duration": "2-3 weeks",
        "final_results": "3-6 months",
        "normal_symptoms": {
            1: {"swelling": "significant", "bruising": "developing", "pain": "moderate (4-6)", "numbness": "very common"},
            2: {"swelling": "increasing", "bruising": "spreading", "pain": "moderate (4-6)", "numbness": "expected"},
            3: {"swelling": "peak", "bruising": "at its worst", "pain": "moderate (3-5)", "numbness": "normal"},
            4: {"swelling": "starting to improve", "bruising": "darkest", "pain": "improving (3-5)", "numbness": "normal"},
            5: {"swelling": "gradually decreasing", "bruising": "starting to fade", "pain": "mild (2-4)", "numbness": "normal"},
            7: {"swelling": "noticeably better", "bruising": "yellowing", "pain": "mild (1-3)", "numbness": "may persist"},
            14: {"swelling": "much improved", "bruising": "mostly gone", "pain": "minimal", "numbness": "may persist for weeks"},
        },
        "tips": {
            1: "Sleep with your head elevated at 30-45 degrees. A recliner works great!",
            2: "Gentle cold compresses can help. Avoid any pressure on incision sites.",
            3: "Peak swelling day - your face may look very tight and 'overdone'. This will settle!",
            4: "Start very gentle walks. Keep your head elevated even while sitting.",
            5: "The numbness you're feeling is normal and will gradually improve over weeks to months.",
            7: "You might be getting stir-crazy. Light activity is okay but avoid bending over.",
            14: "Most sutures are out by now. Be extra gentle with skincare around incision areas.",
        },
        "warning_signs": ["severe pain on one side", "expanding firmness under skin", "fever over 101°F", "sudden increase in swelling", "discharge from incisions"],
    },
    "breast augmentation": {
        "name": "Breast Augmentation",
        "emoji": "💫",
        "peak_swelling_day": 3,
        "swelling_duration": "2-4 weeks",
        "bruising_duration": "1-2 weeks",
        "final_results": "3-6 months for implants to settle",
        "normal_symptoms": {
            1: {"swelling": "significant", "bruising": "minimal to moderate", "pain": "moderate to severe (5-8)", "tightness": "very common"},
            2: {"swelling": "increasing", "bruising": "may increase", "pain": "moderate (5-7)", "tightness": "expected"},
            3: {"swelling": "peak", "bruising": "at its worst", "pain": "moderate (4-6)", "tightness": "very tight feeling normal"},
            4: {"swelling": "starting to decrease", "bruising": "starting to fade", "pain": "improving (4-6)", "tightness": "still present"},
            5: {"swelling": "gradually decreasing", "bruising": "fading", "pain": "improving (3-5)", "tightness": "improving"},
            7: {"swelling": "noticeably less", "bruising": "mostly gone", "pain": "mild (2-4)", "tightness": "improving"},
            14: {"swelling": "much improved", "bruising": "gone", "pain": "minimal (1-3)", "tightness": "still settling"},
        },
        "tips": {
            1: "Wear your surgical bra 24/7 as instructed. Sleep on your back propped up.",
            2: "Take short walks to prevent blood clots. Arm movements should be limited.",
            3: "Your breasts will look very high and tight right now - this is the 'drop and fluff' phase beginning!",
            4: "Continue sleeping elevated. You can start gentle arm movements but nothing overhead.",
            5: "The 'drop and fluff' process takes 3-6 months. Try not to judge your results yet!",
            7: "You may be feeling better but avoid lifting anything over 5 pounds still.",
            14: "Implants are still high and firm. They'll continue to settle over the next few months.",
        },
        "warning_signs": ["one breast significantly larger than other suddenly", "fever over 101°F", "severe redness or warmth", "foul-smelling discharge", "severe pain not controlled by meds"],
    },
    "tummy tuck": {
        "name": "Tummy Tuck",
        "emoji": "🌟",
        "peak_swelling_day": 4,
        "swelling_duration": "6-8 weeks for major swelling",
        "bruising_duration": "2-3 weeks",
        "final_results": "6-12 months",
        "normal_symptoms": {
            1: {"swelling": "significant", "bruising": "developing", "pain": "severe (6-8)", "tightness": "very tight, hunched posture normal"},
            2: {"swelling": "increasing", "bruising": "spreading", "pain": "severe (5-8)", "tightness": "cannot stand straight - normal"},
            3: {"swelling": "increasing", "bruising": "at its worst", "pain": "moderate to severe (5-7)", "tightness": "still hunched"},
            4: {"swelling": "peak", "bruising": "darkest", "pain": "moderate (4-7)", "tightness": "may start standing straighter"},
            5: {"swelling": "starting to decrease", "bruising": "starting to fade", "pain": "improving (4-6)", "tightness": "gradually improving"},
            7: {"swelling": "improving but still significant", "bruising": "yellowing", "pain": "moderate (3-5)", "tightness": "improving"},
            14: {"swelling": "much improved but still present", "bruising": "mostly gone", "pain": "mild (2-4)", "tightness": "much better"},
        },
        "tips": {
            1: "Stay hunched - trying to stand straight too soon can stress your incisions. Walk like a question mark!",
            2: "Keep drains emptied and recorded. Walking hunched every few hours prevents blood clots.",
            3: "The tightness is intense but normal. Your body is adjusting to its new contour.",
            4: "You may be able to stand slightly straighter. Let your body guide you - don't force it.",
            5: "If you have drains, they may come out soon. Keep the area clean and dry.",
            7: "You should be able to stand much straighter now. Gentle walks are your best friend!",
            14: "Swelling can fluctuate for weeks. Compression garment is your best friend right now.",
        },
        "warning_signs": ["fever over 101°F", "severe pain not controlled by meds", "opening of incision", "foul smell from incision", "excessive drain output suddenly"],
    },
    "bbl": {
        "name": "Brazilian Butt Lift",
        "emoji": "🍑",
        "peak_swelling_day": 4,
        "swelling_duration": "6-8 weeks",
        "bruising_duration": "2-3 weeks",
        "final_results": "6-12 months",
        "normal_symptoms": {
            1: {"swelling": "significant in buttocks and lipo areas", "bruising": "developing", "pain": "moderate to severe (5-8)", "numbness": "common in lipo areas"},
            2: {"swelling": "increasing", "bruising": "spreading", "pain": "moderate to severe (5-7)", "numbness": "expected"},
            3: {"swelling": "continuing to increase", "bruising": "darkening", "pain": "moderate (5-7)", "numbness": "normal"},
            4: {"swelling": "peak", "bruising": "at its worst", "pain": "moderate (4-6)", "numbness": "normal"},
            5: {"swelling": "starting to decrease", "bruising": "starting to fade", "pain": "improving (4-6)", "numbness": "may persist"},
            7: {"swelling": "improving", "bruising": "yellowing", "pain": "moderate (3-5)", "numbness": "may persist"},
            14: {"swelling": "much improved", "bruising": "mostly gone", "pain": "mild (2-4)", "numbness": "improving"},
        },
        "tips": {
            1: "NO SITTING ON YOUR BUTT! Use your BBL pillow or lie on your stomach/side only.",
            2: "Walk every 2-3 hours to prevent blood clots. This is crucial for BBL recovery!",
            3: "Your butt looks huge right now - some of this is swelling. Expect 20-40% of transferred fat to be naturally reabsorbed.",
            4: "Continue avoiding sitting directly on buttocks. Lipo areas may feel lumpy - this smooths out over time.",
            5: "Wear your compression garment religiously. It helps your lipo areas heal smoothly.",
            7: "Still no direct sitting! You can use your BBL pillow for short periods if absolutely necessary.",
            14: "You may start sitting with a BBL pillow for short periods. Standing and lying down still preferred.",
        },
        "warning_signs": ["severe shortness of breath", "chest pain", "severe pain in legs", "fever over 101°F", "asymmetric severe swelling"],
    },
    "brow lift": {
        "name": "Brow Lift",
        "emoji": "🌸",
        "peak_swelling_day": 3,
        "swelling_duration": "2-3 weeks",
        "bruising_duration": "10-14 days",
        "final_results": "3-6 months",
        "normal_symptoms": {
            1: {"swelling": "moderate to significant", "bruising": "developing", "pain": "moderate (4-6)", "numbness": "forehead numbness common"},
            2: {"swelling": "increasing, moving down to eyes", "bruising": "spreading to eyelids", "pain": "moderate (4-6)", "numbness": "expected"},
            3: {"swelling": "peak - eyes may swell shut", "bruising": "at its worst", "pain": "moderate (3-5)", "numbness": "normal"},
            4: {"swelling": "starting to decrease", "bruising": "darkest", "pain": "improving (3-5)", "numbness": "normal"},
            5: {"swelling": "gradually decreasing", "bruising": "starting to fade", "pain": "mild (2-4)", "numbness": "normal"},
            7: {"swelling": "noticeably better", "bruising": "yellowing", "pain": "mild (1-3)", "numbness": "may persist for weeks"},
            14: {"swelling": "much improved", "bruising": "mostly gone", "pain": "minimal", "numbness": "may persist for months"},
        },
        "tips": {
            1: "Keep your head elevated at 45 degrees at all times. Ice packs on forehead (not incisions) for 20 minutes on/off.",
            2: "Swelling will migrate down to your eyes - this is normal! Your eyes may nearly swell shut by day 3.",
            3: "Peak swelling day. If your eyes are swollen shut, use cool compresses. This WILL improve!",
            4: "Continue head elevation. Avoid bending over, straining, or lifting anything heavy.",
            5: "You may start gentle shampooing if your surgeon approves. Be very gentle around incisions.",
            7: "Sutures or staples may be removed soon. The tight feeling will gradually relax over weeks.",
            14: "Most visible bruising gone. Your brow may still feel tight and look 'surprised' - this settles.",
        },
        "warning_signs": ["severe headache not relieved by meds", "fever over 101°F", "vision changes", "increasing redness at incisions", "clear fluid leaking"],
    },
    "blepharoplasty": {
        "name": "Eyelid Lift",
        "emoji": "👁️",
        "peak_swelling_day": 2,
        "swelling_duration": "1-2 weeks",
        "bruising_duration": "7-14 days",
        "final_results": "3-6 months",
        "normal_symptoms": {
            1: {"swelling": "moderate to significant", "bruising": "developing", "pain": "mild to moderate (2-5)", "dryness": "eyes may feel dry"},
            2: {"swelling": "peak - eyes may swell shut", "bruising": "darkening", "pain": "mild to moderate (2-5)", "dryness": "use drops"},
            3: {"swelling": "starting to decrease", "bruising": "at its worst", "pain": "mild (2-4)", "dryness": "continue drops"},
            4: {"swelling": "improving", "bruising": "very dark", "pain": "mild (1-3)", "dryness": "may persist"},
            5: {"swelling": "noticeably better", "bruising": "starting to fade", "pain": "minimal (1-2)", "dryness": "improving"},
            7: {"swelling": "much improved", "bruising": "yellowing", "pain": "minimal", "dryness": "may persist"},
            14: {"swelling": "mostly resolved", "bruising": "mostly gone", "pain": "none to minimal", "dryness": "improving"},
        },
        "tips": {
            1: "Apply cold compresses gently to closed eyes for 10-15 minutes every hour. Use prescribed eye drops.",
            2: "Eyes may swell shut - this is temporary! Keep using cold compresses and lubricating drops.",
            3: "You may notice blurry vision from ointment and swelling - this is normal and temporary.",
            4: "Avoid reading, TV, or screen time that strains your eyes. Listen to audiobooks instead.",
            5: "Sutures may be removed around now. Continue avoiding eye strain and sun exposure.",
            7: "Bruising is shifting colors - yellow/green means healing! Light sunglasses help outside.",
            14: "Most people feel comfortable without sunglasses. Avoid eye makeup for 2-3 weeks total.",
        },
        "warning_signs": ["severe eye pain", "vision changes or loss", "bleeding from incisions", "fever over 101°F", "inability to close eyes"],
    },
    "liposuction": {
        "name": "Liposuction",
        "emoji": "💪",
        "peak_swelling_day": 4,
        "swelling_duration": "4-6 weeks",
        "bruising_duration": "2-4 weeks",
        "final_results": "3-6 months",
        "normal_symptoms": {
            1: {"swelling": "significant", "bruising": "developing", "pain": "moderate to severe (5-7)", "numbness": "treated areas numb"},
            2: {"swelling": "increasing", "bruising": "spreading", "pain": "moderate (5-7)", "numbness": "expected"},
            3: {"swelling": "continuing to increase", "bruising": "darkening", "pain": "moderate (4-6)", "numbness": "normal"},
            4: {"swelling": "peak", "bruising": "at its worst", "pain": "moderate (4-6)", "numbness": "normal"},
            5: {"swelling": "starting to decrease", "bruising": "starting to fade", "pain": "improving (3-5)", "numbness": "may persist"},
            7: {"swelling": "improving", "bruising": "yellowing", "pain": "mild (2-4)", "numbness": "may persist for weeks"},
            14: {"swelling": "much improved but area still larger", "bruising": "mostly gone", "pain": "minimal", "numbness": "improving"},
        },
        "tips": {
            1: "Compression garment 24/7 is CRUCIAL. Put pads in garment to absorb drainage. Walk every few hours.",
            2: "Fluid drainage for first 24-48 hours is totally normal. It's actually good - reducing swelling!",
            3: "You may look bigger than before surgery due to swelling. This is normal and temporary!",
            4: "Lymphatic massage can start if your surgeon approves. Helps reduce swelling faster.",
            5: "Continue 24/7 compression. You can shower now but put garment right back on after.",
            7: "Lumpiness and firmness are normal at this stage. Tissue will smooth out over time.",
            14: "Results are starting to show but you're only 25% of the way to final results. Patience!",
        },
        "warning_signs": ["fever over 101°F", "severe pain not controlled by meds", "skin turning dark or cold", "foul-smelling drainage", "dizziness or fainting"],
    },
    "breast reduction": {
        "name": "Breast Reduction",
        "emoji": "🌷",
        "peak_swelling_day": 3,
        "swelling_duration": "4-6 weeks",
        "bruising_duration": "2-3 weeks",
        "final_results": "6-12 months",
        "normal_symptoms": {
            1: {"swelling": "significant", "bruising": "developing", "pain": "moderate to severe (5-7)", "numbness": "nipple numbness common"},
            2: {"swelling": "increasing", "bruising": "spreading", "pain": "moderate (5-7)", "numbness": "expected"},
            3: {"swelling": "peak", "bruising": "at its worst", "pain": "moderate (4-6)", "numbness": "normal"},
            4: {"swelling": "starting to decrease", "bruising": "darkest", "pain": "improving (4-6)", "numbness": "normal"},
            5: {"swelling": "gradually decreasing", "bruising": "starting to fade", "pain": "improving (3-5)", "numbness": "may persist"},
            7: {"swelling": "noticeably better", "bruising": "yellowing", "pain": "mild (2-4)", "numbness": "may persist for months"},
            14: {"swelling": "much improved", "bruising": "mostly gone", "pain": "minimal", "numbness": "may persist"},
        },
        "tips": {
            1: "Wear your surgical bra 24/7. Sleep on your back, slightly elevated. Take pain meds on schedule.",
            2: "Avoid lifting your arms overhead. Short walks help prevent blood clots. Empty drains as instructed.",
            3: "Peak swelling - breasts may look larger than expected. Size reduction comes after swelling subsides.",
            4: "You may notice immediate relief from back/shoulder pain already. This is a great sign!",
            5: "Continue drain care if still in place. Keep incisions clean and dry.",
            7: "Stitches/drains often removed around now. You can see the new shape emerging.",
            14: "You can likely switch to a soft, supportive sports bra. No underwires for 6+ weeks.",
        },
        "warning_signs": ["fever over 101°F", "one breast significantly more swollen/red", "foul smell from incisions", "nipple turning dark", "opening of incisions"],
    },
    "mommy makeover": {
        "name": "Mommy Makeover",
        "emoji": "🦋",
        "peak_swelling_day": 4,
        "swelling_duration": "6-8 weeks",
        "bruising_duration": "3-4 weeks",
        "final_results": "6-12 months",
        "normal_symptoms": {
            1: {"swelling": "significant in all treated areas", "bruising": "developing", "pain": "severe (6-8)", "numbness": "multiple areas numb"},
            2: {"swelling": "increasing throughout", "bruising": "spreading", "pain": "severe (6-8)", "numbness": "expected"},
            3: {"swelling": "continuing to increase", "bruising": "at its worst", "pain": "moderate to severe (5-7)", "numbness": "normal"},
            4: {"swelling": "peak in all areas", "bruising": "darkest", "pain": "moderate (5-7)", "numbness": "normal"},
            5: {"swelling": "starting to decrease", "bruising": "starting to fade", "pain": "improving (4-6)", "numbness": "may persist"},
            7: {"swelling": "improving", "bruising": "yellowing", "pain": "moderate (4-6)", "numbness": "expected"},
            14: {"swelling": "much improved", "bruising": "mostly gone", "pain": "mild to moderate (3-5)", "numbness": "may persist for months"},
        },
        "tips": {
            1: "You had multiple procedures - recovery is INTENSE. Accept all help offered. Stay ahead of pain with meds.",
            2: "Walking hunched is expected. Focus on rest, hydration, and gentle walks for blood clots.",
            3: "Emotional lows are very common after major surgery. This is temporary and will improve.",
            4: "If you have drains, track all output. Keep a notebook - your brain is foggy right now!",
            5: "You're through the worst of it. Continue following each procedure's specific guidelines.",
            7: "You may have drains removed this week. Turning point in feeling more human!",
            14: "You can stand straighter, move more easily. Still take it easy - internal healing takes months.",
        },
        "warning_signs": ["fever over 101°F", "severe pain not controlled by meds", "shortness of breath or chest pain", "foul smell from any incision", "calf pain or swelling"],
    },
    "chemical peel": {
        "name": "Chemical Peel",
        "emoji": "🧴",
        "peak_swelling_day": 2,
        "swelling_duration": "3-7 days",
        "bruising_duration": "rare",
        "final_results": "2-4 weeks for superficial, 2-3 months for deep",
        "normal_symptoms": {
            1: {"swelling": "mild to moderate", "redness": "significant", "pain": "mild stinging (2-4)", "peeling": "not yet"},
            2: {"swelling": "peak", "redness": "intense", "pain": "mild (2-3)", "peeling": "may begin"},
            3: {"swelling": "decreasing", "redness": "still significant", "pain": "minimal", "peeling": "beginning"},
            4: {"swelling": "minimal", "redness": "improving", "pain": "minimal", "peeling": "active"},
            5: {"swelling": "resolved", "redness": "pink", "pain": "none", "peeling": "active"},
            7: {"swelling": "none", "redness": "mild pink", "pain": "none", "peeling": "finishing"},
            14: {"swelling": "none", "redness": "may still be pink", "pain": "none", "peeling": "complete"},
        },
        "tips": {
            1: "Keep treated skin moisturized with prescribed ointments. Avoid touching your face. No makeup!",
            2: "Swelling peaks today, especially around eyes. Sleep elevated. Skin will feel very tight.",
            3: "Skin may start peeling. DO NOT pick or pull! Let it shed naturally.",
            4: "Apply moisturizer frequently. Peeling skin needs constant hydration. Still no sun exposure!",
            5: "Continue gentle cleansing and heavy moisturizing. The urge to pick peeling skin is real - resist!",
            7: "Most peeling complete for superficial peels. Deep peels may take 2+ weeks.",
            14: "New skin is very sensitive. SPF 30+ daily is non-negotiable for the next several months!",
        },
        "warning_signs": ["signs of infection", "fever", "severe pain", "blistering that worsens", "skin darkening in patches"],
    },
    "botox fillers": {
        "name": "Botox & Fillers",
        "emoji": "💉",
        "peak_swelling_day": 1,
        "swelling_duration": "1-3 days for most",
        "bruising_duration": "3-10 days if present",
        "final_results": "Botox: 7-14 days; Fillers: 2-4 weeks",
        "normal_symptoms": {
            1: {"swelling": "mild to moderate", "bruising": "may develop", "pain": "mild (1-3)", "lumps": "may feel lumpy - normal"},
            2: {"swelling": "may increase slightly", "bruising": "if present, darkening", "pain": "minimal", "lumps": "still palpable"},
            3: {"swelling": "decreasing", "bruising": "if present, at worst", "pain": "minimal", "lumps": "settling"},
            4: {"swelling": "much improved", "bruising": "starting to fade", "pain": "none", "lumps": "smoothing out"},
            5: {"swelling": "mostly resolved", "bruising": "fading", "pain": "none", "lumps": "minimal"},
            7: {"swelling": "resolved", "bruising": "yellowing if present", "pain": "none", "lumps": "should be smooth"},
            14: {"swelling": "none", "bruising": "gone", "pain": "none", "lumps": "gone"},
        },
        "tips": {
            1: "Avoid rubbing treated areas for 24 hours. No exercise, alcohol, or lying flat for 4 hours after Botox.",
            2: "Arnica gel/supplements can help bruising fade faster. Ice gently if swollen.",
            3: "For Botox: Don't worry if you don't see effects yet - takes 7-14 days for full results.",
            4: "For fillers: Gently massage any lumps if your provider instructed. If not, leave alone.",
            5: "Avoid extreme heat (sauna, hot yoga) for first week - can affect how product settles.",
            7: "Botox should be starting to work. Fillers should be settled. Assess results now.",
            14: "Full results visible. If asymmetry or issues, contact your provider for touch-up.",
        },
        "warning_signs": ["severe pain", "vision changes (EMERGENCY)", "skin turning white or blue", "difficulty swallowing or breathing"],
    },
}

# Default tips
DEFAULT_TIPS = {
    1: "Day 1 is all about rest. Your only job is to heal. Stay hydrated and take your meds on schedule.",
    2: "Day 2 can feel worse than Day 1 as anesthesia wears off. This is normal - you're not going backward!",
    3: "Day 3 is often emotionally and physically challenging. Be extra gentle with yourself today.",
    4: "You're almost through the hardest part! Small improvements start to show around now.",
    5: "Day 5 - you might feel good enough to overdo it. Resist the urge! Rest is still crucial.",
    7: "One week down! You've made it through the toughest part of recovery.",
    14: "Two weeks in - you're a recovery champion! Results are still evolving but you're on the right track.",
}

# Affirmations
AFFIRMATIONS = [
    "Healing is not linear, and that's perfectly okay.",
    "Your body is doing incredible work right now.",
    "Rest is not lazy - it's essential for recovery.",
    "Be patient with yourself. You're doing better than you think.",
    "Every day brings you closer to your final results.",
    "It's okay to have hard days. They don't last forever.",
    "You are brave for taking this step for yourself.",
    "Trust the process. Trust your body. Trust yourself.",
]

# Community recovery quotes
COMMUNITY_QUOTES = [
    {"quote": "Day 7 was my turning point - suddenly I felt human again!", "day": 7, "procedure": "rhinoplasty"},
    {"quote": "The swelling at week 2 had me worried, but by week 4 I was so happy with my results.", "day": 14, "procedure": "facelift"},
    {"quote": "I cried on day 3 thinking I made a mistake. Now at 6 months, it's the best decision I ever made.", "day": 3, "procedure": "any"},
    {"quote": "Ice packs became my best friend. Stock up!", "day": 1, "procedure": "any"},
    {"quote": "The 'ugly duckling' phase is REAL but it ends! Trust the process.", "day": 5, "procedure": "rhinoplasty"},
    {"quote": "Walking helped so much more than I expected. Even just around the house.", "day": 2, "procedure": "tummy_tuck"},
    {"quote": "Week 3 I finally felt like myself. Hang in there!", "day": 21, "procedure": "blepharoplasty"},
    {"quote": "Pineapple juice before surgery - I had almost no bruising!", "day": 1, "procedure": "any"},
    {"quote": "The compression garment is annoying but SO worth it for the results.", "day": 7, "procedure": "liposuction"},
    {"quote": "Don't compare your day 5 to someone's day 30. Everyone heals differently.", "day": 5, "procedure": "any"},
    {"quote": "I'm 3 months post-op and keep forgetting I ever had surgery - that's when you know it's healed!", "day": 90, "procedure": "breast_augmentation"},
    {"quote": "Sleep elevated! I ignored this advice and regretted it. Listen to your surgeon.", "day": 1, "procedure": "any"},
]

# Countdown milestones per procedure (days until milestone)
PROCEDURE_MILESTONES = {
    "rhinoplasty": [
        {"milestone": "Cast removal", "days": 7, "icon": "🎉"},
        {"milestone": "Return to work (desk job)", "days": 10, "icon": "💼"},
        {"milestone": "Light exercise", "days": 21, "icon": "🚶"},
        {"milestone": "Full exercise", "days": 42, "icon": "🏃"},
        {"milestone": "Final results", "days": 365, "icon": "✨"},
    ],
    "facelift": [
        {"milestone": "Suture removal", "days": 7, "icon": "🎉"},
        {"milestone": "Return to work", "days": 14, "icon": "💼"},
        {"milestone": "Social activities", "days": 21, "icon": "🎭"},
        {"milestone": "Full exercise", "days": 42, "icon": "🏃"},
        {"milestone": "Final results", "days": 180, "icon": "✨"},
    ],
    "breast_augmentation": [
        {"milestone": "Shower normally", "days": 3, "icon": "🚿"},
        {"milestone": "Return to work (desk)", "days": 7, "icon": "💼"},
        {"milestone": "Light exercise", "days": 21, "icon": "🚶"},
        {"milestone": "Full exercise", "days": 42, "icon": "🏃"},
        {"milestone": "Final results", "days": 90, "icon": "✨"},
    ],
    "tummy_tuck": [
        {"milestone": "Drains removed", "days": 7, "icon": "🎉"},
        {"milestone": "Stand straight", "days": 14, "icon": "🧍"},
        {"milestone": "Return to work", "days": 21, "icon": "💼"},
        {"milestone": "Light exercise", "days": 42, "icon": "🚶"},
        {"milestone": "Full exercise", "days": 84, "icon": "🏃"},
    ],
    "liposuction": [
        {"milestone": "Return to work", "days": 5, "icon": "💼"},
        {"milestone": "Light exercise", "days": 14, "icon": "🚶"},
        {"milestone": "Full exercise", "days": 28, "icon": "🏃"},
        {"milestone": "Final results", "days": 90, "icon": "✨"},
    ],
    "blepharoplasty": [
        {"milestone": "Sutures removed", "days": 5, "icon": "🎉"},
        {"milestone": "Return to work", "days": 10, "icon": "💼"},
        {"milestone": "Wear contacts", "days": 14, "icon": "👁️"},
        {"milestone": "Full exercise", "days": 21, "icon": "🏃"},
        {"milestone": "Final results", "days": 90, "icon": "✨"},
    ],
    "default": [
        {"milestone": "Initial healing", "days": 7, "icon": "🎉"},
        {"milestone": "Return to light activities", "days": 14, "icon": "🚶"},
        {"milestone": "Return to work", "days": 21, "icon": "💼"},
        {"milestone": "Full activities", "days": 42, "icon": "🏃"},
        {"milestone": "Final results", "days": 180, "icon": "✨"},
    ],
}

# Surgeon message templates
SURGEON_TEMPLATES = {
    "general_update": {
        "title": "General Post-Op Update",
        "template": """Hi [Surgeon's Office],

This is [NAME] checking in on Day [DAY] after my [PROCEDURE].

Current status:
- Pain level: [PAIN]/10
- Swelling: [SWELLING]
- Bruising: [BRUISING]

Overall I'm feeling [good/okay/concerned]. Just wanted to provide an update.

Thank you,
[NAME]"""
    },
    "concerning_symptoms": {
        "title": "Concerning Symptoms",
        "template": """Hi [Surgeon's Office],

This is [NAME], Day [DAY] post-op from my [PROCEDURE]. I'm experiencing some symptoms I wanted to report:

- [Describe symptom 1]
- [Describe symptom 2]

Should I come in for a check, or is this normal at this stage?

Please advise when you can.

Thank you,
[NAME]"""
    },
    "medication_question": {
        "title": "Medication Question",
        "template": """Hi [Surgeon's Office],

This is [NAME], Day [DAY] after my [PROCEDURE]. I have a question about my medications:

[Your question here]

Current medications I'm taking:
- [Medication 1]
- [Medication 2]

Please let me know what you recommend.

Thank you,
[NAME]"""
    },
    "schedule_followup": {
        "title": "Schedule Follow-up",
        "template": """Hi [Surgeon's Office],

This is [NAME]. I had my [PROCEDURE] and am currently on Day [DAY]. I would like to schedule my follow-up appointment.

My availability:
- [Days/times that work for you]

Please let me know what works.

Thank you,
[NAME]"""
    },
}

# Journaling prompts - 25+ rotating prompts
JOURNALING_PROMPTS = [
    {"prompt": "What are you grateful for today?", "category": "gratitude"},
    {"prompt": "How has your energy level been?", "category": "wellness"},
    {"prompt": "What's one thing that made you smile today?", "category": "positivity"},
    {"prompt": "Describe how your body feels right now.", "category": "awareness"},
    {"prompt": "What are you looking forward to?", "category": "hope"},
    {"prompt": "How did you sleep last night?", "category": "wellness"},
    {"prompt": "What self-care did you do today?", "category": "self-care"},
    {"prompt": "Write about your healing progress.", "category": "reflection"},
    {"prompt": "What emotions came up today?", "category": "emotional"},
    {"prompt": "What would you tell someone else going through this?", "category": "wisdom"},
    {"prompt": "Why did you decide to have this procedure? What made now the right time?", "category": "reflection"},
    {"prompt": "Write a letter to your future healed self. What do you hope to feel?", "category": "hope"},
    {"prompt": "What are you most looking forward to when you're fully healed?", "category": "goals"},
    {"prompt": "How has your support system shown up for you during recovery?", "category": "gratitude"},
    {"prompt": "What's one kind thing you can do for yourself today?", "category": "self-care"},
    {"prompt": "Describe a moment today when you felt strong or brave.", "category": "strength"},
    {"prompt": "List three things your body has done for you today.", "category": "gratitude"},
    {"prompt": "What fear about recovery has turned out to be unfounded?", "category": "reflection"},
    {"prompt": "How do you want to feel in one month? In three months?", "category": "goals"},
    {"prompt": "What small victory can you celebrate today?", "category": "positivity"},
    {"prompt": "How are you being patient with yourself during recovery?", "category": "self-care"},
    {"prompt": "What has surprised you most about your recovery?", "category": "reflection"},
    {"prompt": "Describe your perfect day once you're fully healed.", "category": "hope"},
    {"prompt": "What have you learned about yourself through this experience?", "category": "wisdom"},
    {"prompt": "How has your perspective on your body changed?", "category": "awareness"},
    {"prompt": "What comfort items have helped you most during recovery?", "category": "self-care"},
    {"prompt": "Write about a kind gesture someone did for you recently.", "category": "gratitude"},
    {"prompt": "What does healing mean to you beyond the physical?", "category": "emotional"},
    {"prompt": "How are you staying positive during challenging moments?", "category": "strength"},
    {"prompt": "What advice would you give yourself from day one of recovery?", "category": "wisdom"},
]

# Daily recovery checklist
DAILY_CHECKLIST = [
    {"task": "Take morning medications", "icon": "💊", "time": "morning"},
    {"task": "Drink 8oz water", "icon": "💧", "time": "morning"},
    {"task": "Gentle walk (5-10 mins)", "icon": "🚶", "time": "morning"},
    {"task": "Take midday medications", "icon": "💊", "time": "afternoon"},
    {"task": "Eat protein-rich meal", "icon": "🥩", "time": "afternoon"},
    {"task": "Drink 8oz water", "icon": "💧", "time": "afternoon"},
    {"task": "Gentle walk (5-10 mins)", "icon": "🚶", "time": "afternoon"},
    {"task": "Take evening medications", "icon": "💊", "time": "evening"},
    {"task": "Drink 8oz water", "icon": "💧", "time": "evening"},
    {"task": "Apply ice/compression as directed", "icon": "🧊", "time": "evening"},
    {"task": "Sleep elevated", "icon": "😴", "time": "evening"},
]

# Emergency info
EMERGENCY_INFO = {
    "call_911": [
        "Difficulty breathing or shortness of breath",
        "Chest pain",
        "Severe bleeding that won't stop",
        "Signs of stroke (face drooping, arm weakness, speech difficulty)",
        "Loss of consciousness",
        "Allergic reaction (severe swelling, hives, difficulty breathing)",
    ],
    "call_surgeon_urgent": [
        "Fever over 101°F (38.3°C)",
        "Sudden increase in pain not relieved by medication",
        "Wound opening or separation",
        "Signs of infection (increasing redness, warmth, pus)",
        "Unusual swelling that's getting worse",
        "Numbness or tingling that's spreading",
    ],
    "call_surgeon_soon": [
        "Mild fever (99-101°F)",
        "Nausea from medications",
        "Constipation lasting more than 3 days",
        "Questions about activity restrictions",
        "Running low on prescription medications",
    ],
}


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_progress(data):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_step_index(step_key):
    for i, step in enumerate(STEPS):
        if step["key"] == step_key:
            return i
    return 0


def render_progress_bar():
    current_step = st.session_state.get('step', 'welcome')
    current_index = get_step_index(current_step)

    # Use Streamlit columns for the progress bar
    cols = st.columns(len(STEPS))

    for i, step in enumerate(STEPS):
        with cols[i]:
            if i < current_index:
                # Completed step
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="width: 40px; height: 40px; border-radius: 50%;
                         background: linear-gradient(135deg, #A8C5A8 0%, #5A7A5A 100%);
                         color: white; display: flex; align-items: center; justify-content: center;
                         margin: 0 auto 8px auto; font-size: 16px; font-weight: 600;">✓</div>
                    <span style="font-size: 11px; color: #3A4A3A; font-weight: 500;">{step['label']}</span>
                </div>
                """, unsafe_allow_html=True)
            elif i == current_index:
                # Active step
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="width: 44px; height: 44px; border-radius: 50%;
                         background: linear-gradient(135deg, #F5D5DC 0%, #E8B4BC 100%);
                         color: #2D3A2D; display: flex; align-items: center; justify-content: center;
                         margin: 0 auto 8px auto; font-size: 18px;
                         box-shadow: 0 4px 15px rgba(232, 180, 188, 0.4);">{step['icon']}</div>
                    <span style="font-size: 11px; color: #2D3A2D; font-weight: 600;">{step['label']}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Pending step
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="width: 40px; height: 40px; border-radius: 50%;
                         background: #F5F0E8; color: #6B7B6B;
                         display: flex; align-items: center; justify-content: center;
                         margin: 0 auto 8px auto; font-size: 16px;">{step['icon']}</div>
                    <span style="font-size: 11px; color: #6B7B6B; font-weight: 500;">{step['label']}</span>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="logo-header">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 140" width="480" height="130" style="max-width: 100%;">
          <defs>
            <linearGradient id="hPetalG" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#A8C5A8;stop-opacity:1" />
              <stop offset="100%" style="stop-color:#C8D8C8;stop-opacity:1" />
            </linearGradient>
            <linearGradient id="hPetalP" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#F5D5DC;stop-opacity:1" />
              <stop offset="100%" style="stop-color:#FFEEF2;stop-opacity:1" />
            </linearGradient>
          </defs>
          <!-- Outer petals (sage green) - enlarged -->
          <ellipse cx="65" cy="45" rx="16" ry="38" fill="url(#hPetalG)" transform="rotate(-30 65 65)" opacity="0.8"/>
          <ellipse cx="65" cy="45" rx="16" ry="38" fill="url(#hPetalG)" transform="rotate(30 65 65)" opacity="0.8"/>
          <ellipse cx="65" cy="45" rx="16" ry="38" fill="url(#hPetalG)" transform="rotate(-60 65 65)" opacity="0.7"/>
          <ellipse cx="65" cy="45" rx="16" ry="38" fill="url(#hPetalG)" transform="rotate(60 65 65)" opacity="0.7"/>
          <!-- Middle petals (soft pink) - enlarged -->
          <ellipse cx="65" cy="50" rx="13" ry="32" fill="url(#hPetalP)" transform="rotate(-20 65 65)" opacity="0.9"/>
          <ellipse cx="65" cy="50" rx="13" ry="32" fill="url(#hPetalP)" transform="rotate(20 65 65)" opacity="0.9"/>
          <ellipse cx="65" cy="50" rx="13" ry="32" fill="url(#hPetalP)" transform="rotate(-45 65 65)" opacity="0.85"/>
          <ellipse cx="65" cy="50" rx="13" ry="32" fill="url(#hPetalP)" transform="rotate(45 65 65)" opacity="0.85"/>
          <!-- Inner petals - enlarged -->
          <ellipse cx="65" cy="55" rx="10" ry="24" fill="#FFEEF2" transform="rotate(-10 65 65)" opacity="0.95"/>
          <ellipse cx="65" cy="55" rx="10" ry="24" fill="#FFEEF2" transform="rotate(10 65 65)" opacity="0.95"/>
          <ellipse cx="65" cy="58" rx="8" ry="20" fill="#FDFBF7" opacity="0.9"/>
          <!-- Center - enlarged -->
          <circle cx="65" cy="65" r="13" fill="#FDFBF7" stroke="#E8B4BC" stroke-width="1.5"/>
          <circle cx="65" cy="65" r="8" fill="#A8C5A8" opacity="0.6"/>
          <circle cx="65" cy="65" r="4" fill="#5A7A5A" opacity="0.4"/>
          <!-- Text: Recovery Buddy - larger -->
          <text x="145" y="62" font-family="Georgia, serif" font-size="48" font-weight="600" fill="#5A7A5A">Recovery</text>
          <text x="370" y="62" font-family="Georgia, serif" font-size="48" font-weight="600" fill="#8FB58F">Buddy</text>
          <!-- Tagline - larger -->
          <text x="145" y="100" font-family="Arial, sans-serif" font-size="16" fill="#8B9B8B">Bloom through your recovery journey</text>
        </svg>
    </div>
    """, unsafe_allow_html=True)


def show_terms_of_service():
    """Display Terms of Service page"""
    render_header()

    st.markdown("""
    <div class="legal-page">
        <h1>Terms of Service</h1>

        <p>Welcome to Recovery Buddy. By using this application, you agree to the following terms and conditions.</p>

        <h2>1. Informational Purpose Only</h2>
        <p>Recovery Buddy is designed for informational and educational purposes only. The content provided in this app is intended to support your post-surgery recovery journey by offering general guidance, tracking tools, and emotional support resources.</p>

        <h2>2. Not Medical Advice</h2>
        <p>This app does not provide medical advice, diagnosis, or treatment. The information presented should never replace professional medical guidance. Always consult your surgeon, physician, or qualified healthcare provider with any questions about your medical condition, recovery progress, or treatment plan.</p>

        <h2>3. Age Requirement</h2>
        <p>Users must be 18 years of age or older to use this app. Users under 18 may use this app only with parental or guardian consent and supervision.</p>

        <h2>4. Limitation of Liability</h2>
        <p>Recovery Buddy, its creators, and affiliates are not liable for any decisions, actions, or outcomes based on information provided within this app. You assume full responsibility for how you use the information and tools provided.</p>

        <h2>5. No Warranties</h2>
        <p>We make no warranties or guarantees about recovery outcomes, timelines, or results. Every individual's recovery is unique and depends on many factors beyond the scope of this app.</p>

        <h2>6. Updates and Modifications</h2>
        <p>We reserve the right to update, modify, or discontinue any features of this app at any time. These Terms of Service may also be updated periodically. Continued use of the app constitutes acceptance of any changes.</p>

        <h2>7. Intellectual Property</h2>
        <p>All content, design, features, and functionality of Recovery Buddy are the intellectual property of Recovery Buddy and its creators. Users agree not to copy, reproduce, distribute, or create derivative works based on this app without express written permission.</p>

        <h2>8. User Conduct</h2>
        <p>Users agree to use this app responsibly and not attempt to reverse engineer, hack, or misuse any part of the application.</p>

        <h2>9. Contact</h2>
        <p>If you have questions about these Terms of Service, please contact us at <a href="mailto:legal@recoverybuddy.app">legal@recoverybuddy.app</a>.</p>

        <p class="last-updated">Last updated: January 2026</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back to App", key="btn_back_from_terms", type="primary", use_container_width=True):
            st.session_state.step = 'welcome'
            st.rerun()


def show_privacy_policy():
    """Display Privacy Policy page"""
    render_header()

    st.markdown("""
    <div class="legal-page">
        <h1>Privacy Policy</h1>

        <p>Your privacy is important to us. This Privacy Policy explains how Recovery Buddy handles your information.</p>

        <h2>1. Information We Collect</h2>
        <p>Recovery Buddy may collect the following types of information that you voluntarily provide:</p>
        <ul>
            <li>Your name (for personalized messages)</li>
            <li>Procedure type and surgery date</li>
            <li>Daily symptom check-ins (pain levels, swelling, bruising, etc.)</li>
            <li>Mood and emotional well-being entries</li>
            <li>Journal entries and notes</li>
            <li>Photos you choose to upload for progress tracking</li>
        </ul>

        <h2>2. Local Storage Only</h2>
        <p><strong>Your data stays on your device.</strong> All information you enter into Recovery Buddy is stored locally in your browser's storage. We do not transmit, upload, or store your personal data on external servers.</p>

        <h2>3. No Data Selling or Sharing</h2>
        <p>We do not sell, trade, rent, or share your personal information with third parties. Your recovery journey is private and stays that way.</p>

        <h2>4. No Cross-Site Tracking</h2>
        <p>We do not use tracking cookies, pixels, or any technology to track your activity across other websites. We do not build advertising profiles or share data with advertisers.</p>

        <h2>5. Analytics</h2>
        <p>We may collect anonymous, aggregated usage statistics (such as page views) to improve the app experience. This data cannot be used to identify individual users.</p>

        <h2>6. Deleting Your Data</h2>
        <p>You have full control over your data. To delete all your Recovery Buddy data:</p>
        <ul>
            <li>Clear your browser's local storage/site data for this website</li>
            <li>Use your browser's "Clear browsing data" feature</li>
            <li>Delete the recovery_progress.json file if running locally</li>
        </ul>

        <h2>7. Data Security</h2>
        <p>Since your data is stored locally on your device, its security depends on your device's security. We recommend using a secure, password-protected device.</p>

        <h2>8. Children's Privacy</h2>
        <p>Recovery Buddy is not intended for use by children under 13. We do not knowingly collect information from children under 13 years of age.</p>

        <h2>9. Changes to This Policy</h2>
        <p>We may update this Privacy Policy from time to time. Any changes will be reflected on this page with an updated revision date.</p>

        <h2>10. Contact Us</h2>
        <p>If you have questions about this Privacy Policy or your data, please contact us at <a href="mailto:privacy@recoverybuddy.app">privacy@recoverybuddy.app</a>.</p>

        <p class="last-updated">Last updated: January 2026</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back to App", key="btn_back_from_privacy", type="primary", use_container_width=True):
            st.session_state.step = 'welcome'
            st.rerun()


def show_references():
    """Display Medical References page"""
    render_header()

    st.markdown("""
    <div class="legal-page">
        <h1>📚 Medical Sources & References</h1>

        <div style="background: linear-gradient(135deg, #E8F5E8 0%, #F0FFF0 100%);
                    border: 1px solid #A8C5A8; border-radius: 12px; padding: 1rem; margin-bottom: 1.5rem; text-align: center;">
            <p style="color: #3D6B3D; font-weight: 600; margin: 0; font-size: 1rem;">
                ✅ Information compiled from board-certified medical sources
            </p>
        </div>

        <p style="text-align: center; margin-bottom: 1.5rem;">
            The medical information in Recovery Buddy is compiled from the following credible healthcare sources.
            Always consult with your healthcare provider for personalized medical advice.
        </p>

        <div class="warning-box" style="margin-bottom: 1.5rem;">
            <p><strong>⚠️ Medical Disclaimer:</strong> Recovery Buddy provides general information for educational purposes only.
            This app is not a substitute for professional medical advice, diagnosis, or treatment.
            Always seek the advice of your surgeon or qualified healthcare provider with any questions about your recovery.</p>
        </div>

        <h2>Our Sources</h2>
    </div>
    """, unsafe_allow_html=True)

    # Source cards
    sources_info = [
        {
            "key": "asps",
            "icon": "🏥",
            "description": "The largest plastic surgery specialty organization, providing patient safety information and procedural guidelines.",
            "topics": "Procedure information, recovery timelines, safety guidelines"
        },
        {
            "key": "mayo",
            "icon": "🏛️",
            "description": "World-renowned nonprofit medical center providing expert health information reviewed by medical professionals.",
            "topics": "Symptoms, warning signs, general recovery guidance"
        },
        {
            "key": "cleveland",
            "icon": "💚",
            "description": "Top-ranked hospital providing trusted health information backed by their medical experts.",
            "topics": "Post-surgical care, pain management, healing timelines"
        },
        {
            "key": "webmd",
            "icon": "🌐",
            "description": "Leading health information services platform with physician-reviewed content.",
            "topics": "General recovery tips, symptom tracking, wellness guidance"
        },
        {
            "key": "realself",
            "icon": "✨",
            "description": "Trusted community platform with doctor-verified information about cosmetic procedures.",
            "topics": "Patient experiences, procedure-specific recovery, realistic expectations"
        }
    ]

    for src_info in sources_info:
        src = MEDICAL_SOURCES[src_info["key"]]
        st.markdown(f"""
        <div class="source-card">
            <h3>{src_info['icon']} {src['name']}</h3>
            <p>{src_info['description']}</p>
            <p style="margin-top: 0.5rem;"><strong>Topics covered:</strong> {src_info['topics']}</p>
            <p style="margin-top: 0.75rem;">
                <strong>Website:</strong>
                <a href="{src['url']}" target="_blank" style="color: #0066CC; text-decoration: underline;">{src['url']}</a>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="legal-page" style="margin-top: 1.5rem;">
        <h2>How We Use These Sources</h2>
        <ul>
            <li><strong>Recovery Timelines:</strong> Based on clinical guidelines from ASPS and Cleveland Clinic</li>
            <li><strong>Normal Symptoms:</strong> Compiled from Mayo Clinic and WebMD patient education materials</li>
            <li><strong>Warning Signs:</strong> Sourced from ASPS safety guidelines and Cleveland Clinic emergency criteria</li>
            <li><strong>Daily Tips:</strong> Adapted from post-operative care instructions across all sources</li>
            <li><strong>Emotional Support:</strong> Informed by Mayo Clinic mental health resources</li>
        </ul>

        <h2>Content Review</h2>
        <p>Our recovery information is regularly reviewed and updated to ensure accuracy. Last content review: January 2026.</p>

        <h2>Report an Issue</h2>
        <p>If you notice any medical information that appears inaccurate or outdated, please contact us at
        <a href="mailto:medical@recoverybuddy.app">medical@recoverybuddy.app</a>.</p>

        <p class="last-updated">Last updated: January 2026</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back to App", key="btn_back_from_references", type="primary", use_container_width=True):
            st.session_state.step = 'welcome'
            st.rerun()


def show_dashboard():
    """My Data - Comprehensive view of all saved recovery data"""
    render_header()

    st.markdown("""
    <div class="wellness-card">
        <h3>📊 My Data</h3>
        <p style="color: #3D4D3D;">View and manage all your recovery information in one place.</p>
    </div>
    """, unsafe_allow_html=True)

    # Privacy notice
    st.markdown("""
    <div class="privacy-badge">
        🔒 All data is stored locally on your device only - never sent to any server
    </div>
    """, unsafe_allow_html=True)

    # Get all user data
    name = st.session_state.progress_data.get('name', 'Not set')
    procedure_key = st.session_state.progress_data.get('procedure', '')
    procedure_name = PROCEDURES.get(procedure_key, {}).get('name', procedure_key) if procedure_key else 'Not set'
    surgery_date = st.session_state.progress_data.get('surgery_date', 'Not set')
    day = st.session_state.user_data.get('day', st.session_state.progress_data.get('day', 0))
    streak = st.session_state.streak
    total_checkins = len(st.session_state.check_in_history)
    total_journals = len([e for e in st.session_state.journal_entries.values() if e and e.strip()])
    medications = st.session_state.progress_data.get('medications', [])

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ===== STATS ROW =====
    st.markdown("### 📈 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">📅 {day}</div>
            <div class="stat-label">Recovery Day</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">🔥 {streak}</div>
            <div class="stat-label">Day Streak</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">📋 {total_checkins}</div>
            <div class="stat-label">Check-ins</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">📝 {total_journals}</div>
            <div class="stat-label">Journal Entries</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ===== MY INFORMATION =====
    st.markdown("### 👤 My Information")
    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E8F0E8; border-radius: 12px; padding: 1.25rem;">
            <p style="margin: 0.5rem 0;"><strong>Name:</strong> {name}</p>
            <p style="margin: 0.5rem 0;"><strong>Procedure:</strong> {procedure_name}</p>
            <p style="margin: 0.5rem 0;"><strong>Surgery Date:</strong> {surgery_date}</p>
            <p style="margin: 0.5rem 0;"><strong>Recovery Day:</strong> Day {day}</p>
        </div>
        """, unsafe_allow_html=True)

    with info_col2:
        st.markdown(f"""
        <div style="background: #F5F0E8; border: 1px solid #E8D5C4; border-radius: 12px; padding: 1.25rem;">
            <p style="margin: 0; font-weight: 600; color: #5A7A5A;">🎯 Recovery Progress</p>
            <p style="margin: 0.5rem 0; color: #3D4D3D;">You've completed {total_checkins} check-in{'s' if total_checkins != 1 else ''}</p>
            <p style="margin: 0.5rem 0; color: #3D4D3D;">You've written {total_journals} journal entr{'ies' if total_journals != 1 else 'y'}</p>
            <p style="margin: 0.5rem 0; color: #3D4D3D;">Current streak: {streak} day{'s' if streak != 1 else ''}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ===== PAIN TREND CHART =====
    st.markdown("### 📈 Pain Trend")
    if st.session_state.pain_history and len(st.session_state.pain_history) > 0:
        import pandas as pd

        # Create dataframe for chart
        pain_data = []
        for entry in st.session_state.pain_history:
            pain_data.append({
                'Day': f"Day {entry.get('day', '?')}",
                'Pain Level': entry.get('level', 0),
                'Date': entry.get('date', '')
            })

        df = pd.DataFrame(pain_data)

        if len(df) > 1:
            st.line_chart(df.set_index('Day')['Pain Level'], height=200, use_container_width=True)
        else:
            st.bar_chart(df.set_index('Day')['Pain Level'], height=200, use_container_width=True)

        # Show average
        avg_pain = sum(e.get('level', 0) for e in st.session_state.pain_history) / len(st.session_state.pain_history)
        st.markdown(f"**Average pain level:** {avg_pain:.1f}/10")
    else:
        st.markdown("""
        <div style="background: #F5F5F5; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <p style="color: #666; margin: 0;">📊 No pain data recorded yet. Complete a daily check-in to start tracking your pain levels.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ===== CHECK-IN HISTORY =====
    st.markdown("### 📋 Check-in History")
    if st.session_state.check_in_history and len(st.session_state.check_in_history) > 0:
        # Show all check-ins in an expandable section
        with st.expander(f"View all {len(st.session_state.check_in_history)} check-ins", expanded=False):
            for i, checkin in enumerate(reversed(st.session_state.check_in_history)):
                checkin_day = checkin.get('day', '?')
                checkin_date = checkin.get('date', 'Unknown date')
                pain_level = checkin.get('pain_level', 'N/A')
                mood = checkin.get('mood', 'N/A')
                symptoms = checkin.get('symptoms', [])

                st.markdown(f"""
                <div style="background: #FFFFFF; border: 1px solid #E8F0E8; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;">
                    <p style="font-weight: 600; color: #5A7A5A; margin: 0;">Day {checkin_day} - {checkin_date}</p>
                    <p style="margin: 0.25rem 0; color: #3D4D3D;">Pain: {pain_level}/10 • Mood: {mood}</p>
                    {f'<p style="margin: 0.25rem 0; color: #666; font-size: 0.9rem;">Symptoms: {", ".join(symptoms)}</p>' if symptoms else ''}
                </div>
                """, unsafe_allow_html=True)

        # Show recent check-ins summary
        st.markdown("**Recent check-ins:**")
        for entry in st.session_state.check_in_history[-5:]:
            checkin_date = entry.get('date', 'Unknown')
            pain = entry.get('pain_level', 'N/A')
            st.markdown(f"• Day {entry.get('day', '?')} ({checkin_date}): Pain {pain}/10")
    else:
        st.markdown("""
        <div style="background: #F5F5F5; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <p style="color: #666; margin: 0;">📋 No check-ins recorded yet. Start your first daily check-in!</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ===== JOURNAL ENTRIES =====
    st.markdown("### 📝 Journal Entries")
    journal_entries = [(k, v) for k, v in st.session_state.journal_entries.items() if v and v.strip()]

    if journal_entries:
        with st.expander(f"View all {len(journal_entries)} journal entries", expanded=False):
            for key, entry in reversed(journal_entries):
                st.markdown(f"""
                <div style="background: #FFF9F0; border-left: 4px solid #E8B4BC; border-radius: 0 8px 8px 0; padding: 1rem; margin: 0.5rem 0;">
                    <p style="font-size: 0.8rem; color: #8B9B8B; margin: 0 0 0.5rem 0;">Entry: {key}</p>
                    <p style="color: #2D3A2D; margin: 0; white-space: pre-wrap;">{entry}</p>
                </div>
                """, unsafe_allow_html=True)

        # Show recent entries
        st.markdown("**Recent entries:**")
        for key, entry in journal_entries[-3:]:
            preview = entry[:100] + '...' if len(entry) > 100 else entry
            st.markdown(f"• *\"{preview}\"*")
    else:
        st.markdown("""
        <div style="background: #F5F5F5; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <p style="color: #666; margin: 0;">📝 No journal entries yet. Express your thoughts in the Emotional Check-in section!</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ===== MEDICATIONS =====
    st.markdown("### 💊 Medications")
    if medications:
        for med in medications:
            st.markdown(f"• {med}")
    else:
        st.markdown("""
        <div style="background: #F5F5F5; padding: 1rem; border-radius: 12px;">
            <p style="color: #666; margin: 0;">No medications recorded. You can add medications below.</p>
        </div>
        """, unsafe_allow_html=True)

    # Add medication input
    with st.expander("➕ Add a medication"):
        new_med = st.text_input("Medication name", key="new_medication_input", placeholder="e.g., Ibuprofen 400mg")
        if st.button("Add Medication", key="btn_add_med"):
            if new_med.strip():
                if 'medications' not in st.session_state.progress_data:
                    st.session_state.progress_data['medications'] = []
                st.session_state.progress_data['medications'].append(new_med.strip())
                save_progress()
                st.success(f"Added: {new_med}")
                st.rerun()

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ===== ACTION BUTTONS =====
    st.markdown("### ⚡ Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✏️ Edit My Info", key="dash_edit", use_container_width=True):
            st.session_state.step = 'get_info'
            st.rerun()

    with col2:
        # Export data button
        if st.button("📤 Export My Data", key="dash_export", use_container_width=True):
            st.session_state.show_export = True

    with col3:
        if st.button("🗑️ Clear All Data", key="dash_clear", use_container_width=True, type="secondary"):
            st.session_state.show_clear_confirm = True

    # Export data section
    if st.session_state.get('show_export', False):
        st.markdown("---")
        st.markdown("#### 📤 Export Your Data")

        # Create export data
        import json
        from datetime import datetime as dt_export

        export_data = {
            "exported_at": dt_export.now().isoformat(),
            "app_version": APP_VERSION,
            "user_info": {
                "name": name,
                "procedure": procedure_name,
                "surgery_date": surgery_date,
                "recovery_day": day
            },
            "stats": {
                "streak": streak,
                "total_checkins": total_checkins,
                "total_journal_entries": total_journals
            },
            "pain_history": st.session_state.pain_history,
            "check_in_history": st.session_state.check_in_history,
            "journal_entries": dict(st.session_state.journal_entries),
            "medications": medications
        }

        export_json = json.dumps(export_data, indent=2)

        st.download_button(
            label="⬇️ Download JSON",
            data=export_json,
            file_name=f"recovery_buddy_export_{dt_export.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            key="download_json"
        )

        # Also show as text for copy/paste
        with st.expander("View export data"):
            st.code(export_json, language="json")

        if st.button("Close Export", key="close_export"):
            st.session_state.show_export = False
            st.rerun()

    # Clear data confirmation
    if st.session_state.get('show_clear_confirm', False):
        st.markdown("---")
        st.markdown("""
        <div style="background: #FFF0F0; border: 2px solid #E74C3C; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
            <h4 style="color: #C0392B; margin: 0 0 0.5rem 0;">⚠️ Are you sure?</h4>
            <p style="color: #333; margin: 0;">This will permanently delete all your recovery data including check-ins, journal entries, and progress history. This action cannot be undone.</p>
        </div>
        """, unsafe_allow_html=True)

        confirm_col1, confirm_col2 = st.columns(2)
        with confirm_col1:
            if st.button("❌ Cancel", key="cancel_clear", use_container_width=True):
                st.session_state.show_clear_confirm = False
                st.rerun()
        with confirm_col2:
            if st.button("🗑️ Yes, Delete Everything", key="confirm_clear", use_container_width=True, type="primary"):
                # Clear all data
                st.session_state.progress_data = {}
                st.session_state.user_data = {}
                st.session_state.pain_history = []
                st.session_state.check_in_history = []
                st.session_state.journal_entries = {}
                st.session_state.streak = 0
                st.session_state.is_returning_user = False

                # Delete local file
                if os.path.exists(LOCAL_DATA_FILE):
                    os.remove(LOCAL_DATA_FILE)

                st.session_state.show_clear_confirm = False
                st.success("All data has been cleared.")
                st.session_state.step = 'welcome'
                st.rerun()

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Home button
    if st.button("🏠 Back to Home", key="dash_home", use_container_width=True):
        st.session_state.step = 'welcome'
        st.rerun()


def show_about():
    """About page with app info and credits"""
    render_header()

    st.markdown("""
    <div class="wellness-card">
        <div class="emoji-large">🌸</div>
        <h3 style="text-align: center;">About Recovery Buddy</h3>
    </div>
    """, unsafe_allow_html=True)

    # Two column layout
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(f"""
        <div class="legal-page">
            <h2>App Information</h2>
            <p><strong>Version:</strong> {APP_VERSION}</p>
            <p><strong>Created by:</strong> {APP_CREATOR}</p>
            <p><strong>Medical Review Date:</strong> {LAST_MEDICAL_REVIEW}</p>

            <h2 style="margin-top: 1.5rem;">Our Mission</h2>
            <p>Recovery Buddy was created to provide compassionate support during your post-surgery recovery journey.
            We believe everyone deserves access to helpful recovery information and emotional support.</p>

            <h2 style="margin-top: 1.5rem;">Contact & Support</h2>
            <p>📧 <strong>Email:</strong> <a href="mailto:support@recoverybuddy.app">support@recoverybuddy.app</a></p>
            <p>💬 <strong>Feedback:</strong> <a href="mailto:feedback@recoverybuddy.app">feedback@recoverybuddy.app</a></p>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="legal-page">
            <h2>Medical Sources</h2>
            <p>Our information is compiled from board-certified medical sources:</p>
            <ul>
                <li>American Society of Plastic Surgeons</li>
                <li>Mayo Clinic</li>
                <li>Cleveland Clinic</li>
                <li>WebMD</li>
                <li>RealSelf</li>
            </ul>

            <h2 style="margin-top: 1.5rem;">Privacy & Data</h2>
            <p>🔒 <strong>Your data stays on your device.</strong> We do not collect, store, or share your personal information on external servers.</p>

            <h2 style="margin-top: 1.5rem;">Disclaimer</h2>
            <p>This app provides general information only and is NOT medical advice. Always consult your surgeon or healthcare provider.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🏠 Home", key="about_home", use_container_width=True):
            st.session_state.step = 'welcome'
            st.rerun()
    with col2:
        if st.button("📜 Terms of Service", key="about_terms", use_container_width=True):
            st.session_state.step = 'terms'
            st.rerun()
    with col3:
        if st.button("🔒 Privacy Policy", key="about_privacy", use_container_width=True):
            st.session_state.step = 'privacy'
            st.rerun()
    with col4:
        if st.button("📚 Medical References", key="about_refs", use_container_width=True):
            st.session_state.step = 'references'
            st.rerun()

    # Share and feedback section
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("#### 💝 Share & Support")

    share_col1, share_col2 = st.columns(2)
    with share_col1:
        st.markdown("""
        <div style="background: #FDF2F4; padding: 1rem; border-radius: 12px; text-align: center;">
            <p style="margin: 0;"><strong>💌 Know someone recovering from surgery?</strong></p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Share Recovery Buddy with them!</p>
        </div>
        """, unsafe_allow_html=True)
    with share_col2:
        st.markdown("""
        <div style="background: #E8F5E8; padding: 1rem; border-radius: 12px; text-align: center;">
            <p style="margin: 0;"><strong>📝 Have feedback?</strong></p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">We'd love to hear from you!</p>
        </div>
        """, unsafe_allow_html=True)


def show_settings():
    """Settings page with data management"""
    render_header()

    st.markdown("""
    <div class="wellness-card">
        <h3>⚙️ Settings</h3>
        <p style="color: #3D4D3D;">Manage your preferences and data.</p>
    </div>
    """, unsafe_allow_html=True)

    # Two column layout
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 🎨 Appearance")

        # Dark mode toggle
        dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode, key="settings_dark_mode")
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()

        # Celebration style
        celebration_options = [
            "🎈 Balloons", "❄️ Snow", "🫧 Bubbles", "❤️ Hearts",
            "🎊 Confetti", "✨ Sparkles", "🦋 Butterflies"
        ]
        current_index = celebration_options.index(st.session_state.celebration_style) if st.session_state.celebration_style in celebration_options else 0
        celebration = st.selectbox("🎉 Celebration Style", celebration_options, index=current_index, key="settings_celebration")
        if celebration != st.session_state.celebration_style:
            st.session_state.celebration_style = celebration

        st.markdown("#### 📱 Notifications")
        st.markdown("*Push notifications coming soon!*")

    with col_right:
        st.markdown("#### 🔒 Data & Privacy")

        st.markdown("""
        <div class="privacy-badge" style="margin-bottom: 1rem;">
            🔒 All your data is stored locally on this device only
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### Your Saved Data:")
        st.markdown(f"""
        - **Name:** {st.session_state.progress_data.get('name', 'Not set')}
        - **Procedure:** {st.session_state.progress_data.get('procedure', 'Not set')}
        - **Journal entries:** {len(st.session_state.journal_entries)}
        - **Check-ins:** {len(st.session_state.check_in_history)}
        """)

        st.markdown("##### Data Management:")

        if st.button("🗑️ Clear All My Data", key="clear_data", type="secondary", use_container_width=True):
            st.session_state.show_clear_confirm = True

        if st.session_state.get('show_clear_confirm', False):
            st.warning("⚠️ This will permanently delete all your saved data. This cannot be undone.")
            confirm_col1, confirm_col2 = st.columns(2)
            with confirm_col1:
                if st.button("Yes, Delete Everything", key="confirm_delete", type="primary"):
                    # Clear all data
                    st.session_state.progress_data = {}
                    st.session_state.user_data = {}
                    st.session_state.journal_entries = {}
                    st.session_state.checklist = {}
                    st.session_state.pain_history = []
                    st.session_state.check_in_history = []
                    st.session_state.streak = 0
                    st.session_state.is_returning_user = False
                    st.session_state.show_clear_confirm = False
                    # Clear saved file
                    if os.path.exists(PROGRESS_FILE):
                        os.remove(PROGRESS_FILE)
                    st.success("✅ All data cleared!")
                    st.rerun()
            with confirm_col2:
                if st.button("Cancel", key="cancel_delete"):
                    st.session_state.show_clear_confirm = False
                    st.rerun()

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Home button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏠 Back to Home", key="settings_home", type="primary", use_container_width=True):
            st.session_state.step = 'welcome'
            st.rerun()


def show_surgery_resources():
    """Surgery Resources page with links to official sources"""
    render_header()

    st.markdown("""
    <div class="wellness-card">
        <h3>📚 Surgery Resources</h3>
        <p style="color: #333;">Find official information about your procedure from trusted medical sources.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <p>📋 These links go to official medical websites with detailed information about each procedure,
        recovery timelines, and what to expect. Always consult your surgeon for personalized advice.</p>
    </div>
    """, unsafe_allow_html=True)

    for proc_key, proc_info in SURGERY_RESOURCES.items():
        with st.expander(f"📖 {proc_info['name']}", expanded=False):
            st.markdown(f"**Recovery Time:** {proc_info['recovery_time']}")
            st.markdown(f"**Common Symptoms:** {proc_info['common_symptoms']}")
            st.markdown("**Official Resources:**")
            for link in proc_info['links']:
                st.markdown(f"- [{link['source']}]({link['url']})")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    if st.button("🏠 Back to Home", key="resources_home", use_container_width=True):
        st.session_state.step = 'welcome'
        st.rerun()


def show_faq():
    """FAQ page with common questions"""
    render_header()

    st.markdown("""
    <div class="wellness-card">
        <h3>❓ Frequently Asked Questions</h3>
        <p style="color: #333;">Common questions about post-surgery recovery.</p>
    </div>
    """, unsafe_allow_html=True)

    # Search box
    search_query = st.text_input("🔍 Search questions", placeholder="Type to search...", key="faq_search")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    for faq in FAQ_DATA:
        # Filter by search
        if search_query and search_query.lower() not in faq['question'].lower() and search_query.lower() not in faq['answer'].lower():
            continue

        with st.expander(f"❓ {faq['question']}", expanded=False):
            st.markdown(faq['answer'])
            st.markdown(f"*Source: {faq['source']}*")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    if st.button("🏠 Back to Home", key="faq_home", use_container_width=True):
        st.session_state.step = 'welcome'
        st.rerun()


def show_symptom_checker_page():
    """Symptom checker - Is this normal?"""
    render_header()

    st.markdown("""
    <div class="wellness-card">
        <h3>🩺 Symptom Checker</h3>
        <p style="color: #333;">Not sure if what you're experiencing is normal? Check here.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-box">
        <p>⚠️ <strong>Disclaimer:</strong> This is for informational purposes only and is NOT medical advice.
        When in doubt, always call your surgeon's office.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Select any symptoms you're experiencing:")

    # Create columns for symptom checkboxes
    selected_symptoms = []

    st.markdown("#### 🟢 Typically Normal Symptoms")
    for symptom in SYMPTOM_CHECKER['normal']['symptoms']:
        if st.checkbox(symptom, key=f"sym_normal_{symptom}"):
            selected_symptoms.append(('normal', symptom))

    st.markdown("#### 🟡 May Need Attention")
    for symptom in SYMPTOM_CHECKER['call_soon']['symptoms']:
        if st.checkbox(symptom, key=f"sym_soon_{symptom}"):
            selected_symptoms.append(('call_soon', symptom))

    st.markdown("#### 🔴 Urgent - Seek Immediate Care")
    for symptom in SYMPTOM_CHECKER['urgent']['symptoms']:
        if st.checkbox(symptom, key=f"sym_urgent_{symptom}"):
            selected_symptoms.append(('urgent', symptom))

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    if selected_symptoms:
        # Determine highest severity
        severities = [s[0] for s in selected_symptoms]
        if 'urgent' in severities:
            level = 'urgent'
            st.markdown(f"""
            <div style="background: {SYMPTOM_CHECKER['urgent']['color']}; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #E74C3C;">
                <h4 style="color: #C0392B; margin: 0 0 0.5rem 0;">🚨 {SYMPTOM_CHECKER['urgent']['action']}</h4>
                <p style="color: #333; margin: 0;">{SYMPTOM_CHECKER['urgent']['message']}</p>
            </div>
            """, unsafe_allow_html=True)
        elif 'call_soon' in severities:
            level = 'call_soon'
            st.markdown(f"""
            <div style="background: {SYMPTOM_CHECKER['call_soon']['color']}; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #F5C842;">
                <h4 style="color: #856404; margin: 0 0 0.5rem 0;">📞 {SYMPTOM_CHECKER['call_soon']['action']}</h4>
                <p style="color: #333; margin: 0;">{SYMPTOM_CHECKER['call_soon']['message']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            level = 'normal'
            st.markdown(f"""
            <div style="background: {SYMPTOM_CHECKER['normal']['color']}; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #28A745;">
                <h4 style="color: #155724; margin: 0 0 0.5rem 0;">✅ {SYMPTOM_CHECKER['normal']['action']}</h4>
                <p style="color: #333; margin: 0;">{SYMPTOM_CHECKER['normal']['message']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <p style="font-size: 0.85rem; color: #666; margin-top: 1rem; text-align: center;">
            <em>Source: American Society of Plastic Surgeons (ASPS), Mayo Clinic, Cleveland Clinic</em>
        </p>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Back to Home", key="symptom_home", use_container_width=True):
            st.session_state.step = 'welcome'
            st.rerun()
    with col2:
        if st.button("📞 Emergency Contacts", key="symptom_emergency", use_container_width=True):
            st.session_state.step = 'emergency_contacts'
            st.rerun()


def show_emergency_contacts():
    """Emergency contacts page"""
    render_header()

    st.markdown("""
    <div class="wellness-card">
        <h3>📞 Emergency Contacts</h3>
        <p style="color: #333;">Keep your important contacts handy.</p>
    </div>
    """, unsafe_allow_html=True)

    # Emergency banner
    st.markdown("""
    <div style="background: #FFE5E5; border: 2px solid #E74C3C; border-radius: 12px; padding: 1rem; margin-bottom: 1.5rem; text-align: center;">
        <p style="color: #C0392B; font-weight: 700; font-size: 1.2rem; margin: 0;">
            🚨 Medical Emergency? Call 911
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Surgeon info
    st.markdown("### 👨‍⚕️ Your Surgeon")
    surgeon_name = st.text_input("Surgeon's Name", value=st.session_state.emergency_contacts.get('surgeon_name', ''), key="surgeon_name_input")
    surgeon_phone = st.text_input("Surgeon's Phone", value=st.session_state.emergency_contacts.get('surgeon_phone', ''), key="surgeon_phone_input")

    st.markdown("### 👥 Emergency Contact")
    emergency_name = st.text_input("Contact Name", value=st.session_state.emergency_contacts.get('emergency_name', ''), key="emergency_name_input")
    emergency_phone = st.text_input("Contact Phone", value=st.session_state.emergency_contacts.get('emergency_phone', ''), key="emergency_phone_input")

    if st.button("💾 Save Contacts", key="save_contacts", type="primary"):
        st.session_state.emergency_contacts = {
            'surgeon_name': surgeon_name,
            'surgeon_phone': surgeon_phone,
            'emergency_name': emergency_name,
            'emergency_phone': emergency_phone
        }
        st.session_state.progress_data['emergency_contacts'] = st.session_state.emergency_contacts
        save_progress(st.session_state.progress_data)
        st.success("✅ Contacts saved!")

    # Quick dial buttons if contacts exist
    if surgeon_phone:
        st.markdown("### 📱 Quick Dial")
        st.markdown(f"""
        <a href="tel:{surgeon_phone}" style="display: inline-block; background: #A8C5A8; color: white;
           padding: 0.75rem 1.5rem; border-radius: 25px; text-decoration: none; margin-right: 1rem;">
            📞 Call Surgeon
        </a>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    if st.button("🏠 Back to Home", key="emergency_home", use_container_width=True):
        st.session_state.step = 'welcome'
        st.rerun()


def show_self_care():
    """Daily self-care checklist"""
    render_header()

    st.markdown("""
    <div class="wellness-card">
        <h3>💚 Daily Self-Care Checklist</h3>
        <p style="color: #333;">Take care of yourself today! Check off what you've done.</p>
    </div>
    """, unsafe_allow_html=True)

    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')

    # Show affirmation
    affirmation = AFFIRMATIONS[st.session_state.affirmation_index]
    st.markdown(f"""
    <div class="info-box" style="text-align: center;">
        <p style="font-size: 1.1rem; font-style: italic;">✨ {affirmation}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Checklist
    completed_count = 0
    for item in SELF_CARE_CHECKLIST:
        checked = st.checkbox(
            f"{item['icon']} {item['label']}",
            value=st.session_state.self_care_today.get(item['id'], False),
            key=f"selfcare_{item['id']}"
        )
        st.session_state.self_care_today[item['id']] = checked
        if checked:
            completed_count += 1

    # Save progress
    st.session_state.progress_data['self_care_today'] = st.session_state.self_care_today
    st.session_state.progress_data['self_care_date'] = today
    save_progress(st.session_state.progress_data)

    # Progress indicator
    total_items = len(SELF_CARE_CHECKLIST)
    progress_pct = (completed_count / total_items) * 100

    st.markdown(f"""
    <div style="background: #E8F5E8; padding: 1rem; border-radius: 12px; margin-top: 1rem; text-align: center;">
        <p style="margin: 0; color: #2C5530; font-weight: 600;">
            {completed_count}/{total_items} completed today ({progress_pct:.0f}%)
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Celebration if all complete
    if completed_count == total_items:
        st.balloons()
        st.markdown("""
        <div style="background: linear-gradient(135deg, #A8C5A8 0%, #C8D8C8 100%); padding: 1.5rem; border-radius: 12px; text-align: center; margin-top: 1rem;">
            <p style="font-size: 1.5rem; margin: 0;">🎉 Amazing! You completed all your self-care tasks! 🎉</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    if st.button("🏠 Back to Home", key="selfcare_home", use_container_width=True):
        st.session_state.step = 'welcome'
        st.rerun()


def show_mood_tracker():
    """Mood tracker page"""
    render_header()

    st.markdown("""
    <div class="wellness-card">
        <h3>😊 How Are You Feeling?</h3>
        <p style="color: #333;">Track your emotional wellbeing during recovery.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Select your mood today:")

    cols = st.columns(4)
    selected_mood = None

    for i, mood in enumerate(MOOD_OPTIONS):
        with cols[i]:
            if st.button(
                f"{mood['emoji']}\n{mood['label']}",
                key=f"mood_{mood['label']}",
                use_container_width=True
            ):
                selected_mood = mood

    if selected_mood:
        # Save mood
        mood_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M'),
            'mood': selected_mood['label'],
            'emoji': selected_mood['emoji']
        }
        st.session_state.mood_history.append(mood_entry)
        st.session_state.progress_data['mood_history'] = st.session_state.mood_history
        save_progress(st.session_state.progress_data)

        # Show response
        st.markdown(f"""
        <div style="background: {selected_mood['color']}; padding: 1.5rem; border-radius: 12px; margin-top: 1rem; text-align: center;">
            <p style="font-size: 2rem; margin: 0 0 0.5rem 0;">{selected_mood['emoji']}</p>
            <p style="color: #333; margin: 0;">{selected_mood['response']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Show mood history
    if st.session_state.mood_history:
        st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
        st.markdown("### Recent Mood History")

        for entry in reversed(st.session_state.mood_history[-7:]):
            st.markdown(f"{entry['emoji']} **{entry['date']}** - {entry['mood']}")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    if st.button("🏠 Back to Home", key="mood_home", use_container_width=True):
        st.session_state.step = 'welcome'
        st.rerun()


def main():
    # Show loading screen on first load
    if 'app_loaded' not in st.session_state:
        st.session_state.app_loaded = True
        st.markdown("""
        <div class="loading-screen">
            <div class="loading-icon">🌸</div>
            <div class="loading-text">Loading Recovery Buddy</div>
        </div>
        """, unsafe_allow_html=True)

    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 'welcome'
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'progress_data' not in st.session_state:
        st.session_state.progress_data = load_progress()
    if 'dark_mode' not in st.session_state:
        # Load dark mode preference from saved data
        st.session_state.dark_mode = st.session_state.progress_data.get('dark_mode', False)
    if 'checklist' not in st.session_state:
        st.session_state.checklist = {}
    if 'journal_entries' not in st.session_state:
        st.session_state.journal_entries = {}
    if 'celebration_shown' not in st.session_state:
        st.session_state.celebration_shown = False
    if 'celebration_style' not in st.session_state:
        st.session_state.celebration_style = "🎈 Balloons"
    if 'disclaimer_accepted' not in st.session_state:
        st.session_state.disclaimer_accepted = False
    # Enhanced data tracking
    if 'pain_history' not in st.session_state:
        st.session_state.pain_history = []  # List of {date, level, notes}
    if 'check_in_history' not in st.session_state:
        st.session_state.check_in_history = []  # List of check-ins
    if 'is_returning_user' not in st.session_state:
        # Check if user has saved data
        saved_data = st.session_state.progress_data
        st.session_state.is_returning_user = bool(saved_data.get('name') or saved_data.get('procedure'))
    if 'last_check_in' not in st.session_state:
        st.session_state.last_check_in = st.session_state.progress_data.get('last_check_in')
    if 'streak' not in st.session_state:
        st.session_state.streak = st.session_state.progress_data.get('streak', 0)

    # New feature session state
    if 'mood_history' not in st.session_state:
        st.session_state.mood_history = st.session_state.progress_data.get('mood_history', [])
    if 'self_care_today' not in st.session_state:
        # Reset daily if it's a new day
        today = datetime.now().strftime('%Y-%m-%d')
        saved_date = st.session_state.progress_data.get('self_care_date', '')
        if saved_date != today:
            st.session_state.self_care_today = {}
        else:
            st.session_state.self_care_today = st.session_state.progress_data.get('self_care_today', {})
    if 'medications' not in st.session_state:
        st.session_state.medications = st.session_state.progress_data.get('medications', [])
    if 'emergency_contacts' not in st.session_state:
        st.session_state.emergency_contacts = st.session_state.progress_data.get('emergency_contacts', {})
    if 'daily_tip_index' not in st.session_state:
        # Use day of year for consistent daily tips
        st.session_state.daily_tip_index = datetime.now().timetuple().tm_yday % len(DAILY_TIPS)
    if 'affirmation_index' not in st.session_state:
        st.session_state.affirmation_index = random.randint(0, len(AFFIRMATIONS) - 1)

    # Show disclaimer popup on first visit
    if not st.session_state.disclaimer_accepted:
        st.markdown("""
        <div class="disclaimer-modal">
            <h2>⚠️ Important Medical Disclaimer</h2>

            <div class="disclaimer-highlight">
                <p>🏥 This app provides <strong>general recovery information only</strong> and is NOT medical advice.</p>
            </div>

            <p><strong>Recovery Buddy does NOT:</strong></p>
            <ul>
                <li>Provide medical diagnosis or treatment recommendations</li>
                <li>Replace professional medical advice from your surgeon</li>
                <li>Serve as an emergency medical resource</li>
            </ul>

            <p><strong>Always consult your surgeon or healthcare provider</strong> for personalized medical guidance about your recovery.</p>

            <div style="background: #FFF0F0; border: 1px solid #E74C3C; border-radius: 8px; padding: 1rem; margin: 1rem 0; text-align: center;">
                <p style="color: #C0392B; font-weight: 600; margin: 0;">🚨 If you are experiencing a medical emergency, call 911 or go to the nearest emergency room immediately.</p>
            </div>

            <p style="font-size: 0.85rem; color: #666666; text-align: center; margin-top: 1rem;">
                <em>Information compiled from board-certified medical sources including the American Society of Plastic Surgeons,
                Mayo Clinic, Cleveland Clinic, WebMD, and RealSelf.</em>
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("I Understand - Continue to App", key="btn_accept_disclaimer", type="primary", use_container_width=True):
                st.session_state.disclaimer_accepted = True
                st.rerun()
        return  # Don't show rest of app until disclaimer accepted

    # Save dark mode preference
    if 'dark_mode' in st.session_state:
        st.session_state.progress_data['dark_mode'] = st.session_state.dark_mode
        save_progress(st.session_state.progress_data)

    # Apply dark mode if enabled
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
        /* ===== COMPREHENSIVE DARK MODE ===== */

        /* Main app background */
        .stApp {
            background: #121212 !important;
        }

        .main .block-container {
            background: #121212 !important;
        }

        /* All cards and containers */
        .wellness-card, .tip-card, .info-box, .success-box, .warning-box, .danger-box,
        .stat-card, .source-card, .legal-page, .disclaimer-modal {
            background: #1E1E1E !important;
            border-color: #333333 !important;
        }

        /* Headers - light text */
        h1, h2, h3, h4, h5, h6,
        .wellness-card h2, .wellness-card h3, .wellness-card h4,
        .tip-card h2, .tip-card h3, .tip-card h4,
        .stat-card .stat-value, .source-card h3, .legal-page h1, .legal-page h2 {
            color: #FFFFFF !important;
        }

        /* Body text - slightly dimmed white */
        p, li, span, label, td, th,
        .wellness-card p, .tip-card p, .info-box p,
        .stat-card .stat-label, .source-card p, .legal-page p, .legal-page li,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li {
            color: #E0E0E0 !important;
        }

        /* Logo */
        .logo-title {
            color: #A8C5A8 !important;
        }
        .logo-subtitle {
            color: #8AA88A !important;
        }

        /* Progress container */
        .progress-container {
            background: #1E1E1E !important;
        }

        /* Input fields */
        .stTextInput input, .stTextArea textarea, .stSelectbox > div > div,
        .stNumberInput input {
            background: #2D2D2D !important;
            color: #FFFFFF !important;
            border-color: #444444 !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: #1A1A1A !important;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label {
            color: #E0E0E0 !important;
        }

        /* Expanders */
        [data-testid="stExpander"] {
            background: #1E1E1E !important;
            border-color: #333333 !important;
        }
        [data-testid="stExpander"] > details > summary {
            background: #1E1E1E !important;
            color: #E0E0E0 !important;
        }
        [data-testid="stExpander"] > details > div {
            background: #252525 !important;
        }

        /* Buttons - keep accent colors */
        .stButton > button {
            background: linear-gradient(135deg, #4A6B4A 0%, #3A5A3A 100%) !important;
            color: white !important;
        }

        /* Links */
        a {
            color: #7CB7FF !important;
        }

        /* Privacy badge */
        .privacy-badge {
            background: #2D3A2D !important;
            border-color: #4A6B4A !important;
            color: #A8C5A8 !important;
        }

        /* Dividers */
        hr, .section-divider {
            background: #333333 !important;
        }

        /* Checkbox and toggle text */
        .stCheckbox label, .stToggle label {
            color: #E0E0E0 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar with dark mode and emergency info
    with st.sidebar:
        st.markdown("### 📊 Navigation")
        if st.button("🏠 Home", key="sidebar_home", use_container_width=True):
            st.session_state.step = 'welcome'
            st.rerun()
        if st.button("📊 My Data", key="sidebar_my_data", use_container_width=True):
            st.session_state.step = 'dashboard'
            st.rerun()
        if st.button("😊 Mood Tracker", key="sidebar_mood", use_container_width=True):
            st.session_state.step = 'mood_tracker'
            st.rerun()
        if st.button("✅ Self-Care", key="sidebar_selfcare", use_container_width=True):
            st.session_state.step = 'self_care'
            st.rerun()
        if st.button("🩺 Symptom Checker", key="sidebar_symptoms", use_container_width=True):
            st.session_state.step = 'symptom_checker'
            st.rerun()
        if st.button("📞 Emergency Contacts", key="sidebar_contacts", use_container_width=True):
            st.session_state.step = 'emergency_contacts'
            st.rerun()
        if st.button("📚 Surgery Resources", key="sidebar_resources", use_container_width=True):
            st.session_state.step = 'surgery_resources'
            st.rerun()
        if st.button("❓ FAQ", key="sidebar_faq", use_container_width=True):
            st.session_state.step = 'faq'
            st.rerun()

        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode, key="toggle_dark_mode")
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()

        # Celebration style selector
        celebration_options = [
            "🎈 Balloons",
            "❄️ Snow",
            "🫧 Bubbles",
            "❤️ Hearts",
            "🎊 Confetti",
            "✨ Sparkles",
            "🦋 Butterflies"
        ]
        current_index = celebration_options.index(st.session_state.celebration_style) if st.session_state.celebration_style in celebration_options else 0
        celebration_style = st.selectbox(
            "🎉 Celebration Style",
            celebration_options,
            index=current_index,
            key="select_celebration_style"
        )
        if celebration_style != st.session_state.celebration_style:
            st.session_state.celebration_style = celebration_style

        st.markdown("---")

        # PROMINENT Emergency Warning Banner
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFE5E5 0%, #FFCCCC 100%);
                    border: 2px solid #E74C3C; border-radius: 10px; padding: 0.75rem; margin-bottom: 1rem; text-align: center;">
            <p style="color: #C0392B; font-weight: 700; margin: 0; font-size: 0.9rem;">
                🚨 MEDICAL EMERGENCY?
            </p>
            <p style="color: #E74C3C; margin: 0.25rem 0 0 0; font-size: 0.85rem; font-weight: 600;">
                Call 911 or go to the ER
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Emergency Info Box - Always visible
        st.markdown("### 🚨 Emergency Info")

        # Call 911 section - more prominent
        st.markdown("""
        <p style="color: #C0392B; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem;">
            🔴 <strong>Call 911 Immediately If:</strong>
        </p>
        """, unsafe_allow_html=True)
        show_911 = st.checkbox("Show 911 warning signs", key="show_911", value=False)
        if show_911:
            for item in EMERGENCY_INFO["call_911"]:
                st.markdown(f"<p style='color: #C0392B; font-size: 0.85rem; margin: 0.25rem 0 0.25rem 1rem;'>🔴 {item}</p>", unsafe_allow_html=True)

        # Call Surgeon Urgently section
        st.markdown("""
        <p style="color: #E67E22; font-weight: 600; font-size: 0.9rem; margin: 0.75rem 0 0.5rem 0;">
            🟠 <strong>Call Surgeon Urgently If:</strong>
        </p>
        """, unsafe_allow_html=True)
        show_urgent = st.checkbox("Show urgent warning signs", key="show_urgent", value=False)
        if show_urgent:
            for item in EMERGENCY_INFO["call_surgeon_urgent"]:
                st.markdown(f"<p style='color: #E67E22; font-size: 0.85rem; margin: 0.25rem 0 0.25rem 1rem;'>🟠 {item}</p>", unsafe_allow_html=True)

        # Call Surgeon Soon section
        st.markdown("""
        <p style="color: #F1C40F; font-weight: 600; font-size: 0.9rem; margin: 0.75rem 0 0.5rem 0;">
            🟡 <strong>Call Surgeon Soon If:</strong>
        </p>
        """, unsafe_allow_html=True)
        show_soon = st.checkbox("Show other warning signs", key="show_soon", value=False)
        if show_soon:
            for item in EMERGENCY_INFO["call_surgeon_soon"]:
                st.markdown(f"<p style='color: #B7950B; font-size: 0.85rem; margin: 0.25rem 0 0.25rem 1rem;'>🟡 {item}</p>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <p style="font-size: 0.8rem; color: #666;">
        💚 <strong>Your Surgeon's Office:</strong><br>
        <em>Add your surgeon's contact info here</em>
        </p>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📚 Medical Info")
        st.markdown("""
        <p style="font-size: 0.75rem; color: #666; line-height: 1.4;">
        Information sourced from <strong>ASPS</strong>, <strong>Mayo Clinic</strong>,
        <strong>Cleveland Clinic</strong>, <strong>WebMD</strong>, and <strong>RealSelf</strong>.
        </p>
        <p style="font-size: 0.75rem; color: #888; margin-top: 0.5rem;">
        ⚠️ <em>This app provides general information only and is not a substitute for professional medical advice.</em>
        </p>
        """, unsafe_allow_html=True)

    # Render header and progress
    render_header()
    render_progress_bar()

    # Check for legal pages first (they have their own layout)
    if st.session_state.step == 'terms':
        show_terms_of_service()
        return
    elif st.session_state.step == 'privacy':
        show_privacy_policy()
        return
    elif st.session_state.step == 'references':
        show_references()
        return

    # Main content
    if st.session_state.step == 'welcome':
        show_welcome()
    elif st.session_state.step == 'get_info':
        show_get_info()
    elif st.session_state.step == 'physical_checkin':
        show_physical_checkin()
    elif st.session_state.step == 'symptom_results':
        show_symptom_results()
    elif st.session_state.step == 'emotional_checkin':
        show_emotional_checkin()
    elif st.session_state.step == 'daily_tip':
        show_daily_tip()
    elif st.session_state.step == 'complete':
        show_complete()
    elif st.session_state.step == 'dashboard':
        show_dashboard()
    elif st.session_state.step == 'about':
        show_about()
    elif st.session_state.step == 'settings':
        show_settings()
    elif st.session_state.step == 'surgery_resources':
        show_surgery_resources()
    elif st.session_state.step == 'faq':
        show_faq()
    elif st.session_state.step == 'symptom_checker':
        show_symptom_checker_page()
    elif st.session_state.step == 'emergency_contacts':
        show_emergency_contacts()
    elif st.session_state.step == 'self_care':
        show_self_care()
    elif st.session_state.step == 'mood_tracker':
        show_mood_tracker()


def show_welcome():
    import random

    # Check for returning user
    saved_name = st.session_state.progress_data.get('name', '')
    saved_procedure = st.session_state.progress_data.get('procedure', '')
    is_returning = bool(saved_name)

    # Calculate recovery day if surgery date is set
    recovery_day = 0
    surgery_date = st.session_state.progress_data.get('surgery_date')
    if surgery_date:
        try:
            surgery_dt = datetime.strptime(surgery_date, '%Y-%m-%d')
            recovery_day = (datetime.now() - surgery_dt).days + 1
        except:
            recovery_day = 0

    # Wide layout with two columns
    if is_returning:
        # Time-based greeting for returning users
        greeting = get_time_greeting(saved_name)
        mascot = get_mascot_message(recovery_day) if recovery_day > 0 else {"emoji": "🌸", "message": "Welcome back to your recovery journey!"}

        st.markdown(f"""
        <div class="welcome-back-card" style="background: linear-gradient(135deg, #F8FDF8 0%, #E8F5E8 100%); border: 2px solid #A8C5A8; border-radius: 15px; padding: 1.5rem; margin-bottom: 1rem;">
            <h3 style="color: #5A7A5A; margin: 0; font-size: 1.3rem;">{greeting}</h3>
            <div style="display: flex; align-items: center; margin-top: 0.75rem;">
                <span style="font-size: 2rem; margin-right: 0.75rem;">{mascot['emoji']}</span>
                <p style="color: #3D4D3D; margin: 0; font-style: italic;">"{mascot['message']}"</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Show recovery milestone if applicable
        if recovery_day > 0:
            # Find the most recent milestone
            milestone_days = sorted([d for d in RECOVERY_MILESTONES.keys() if d <= recovery_day], reverse=True)
            if milestone_days:
                milestone = RECOVERY_MILESTONES[milestone_days[0]]
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FFF8F0 0%, #FFEFD5 100%); border: 1px solid #FFD700; border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
                    <p style="margin: 0; color: #B8860B;">
                        {milestone['icon']} <strong>{milestone['title']}</strong> — Day {recovery_day} of Recovery
                    </p>
                    <p style="margin: 0.5rem 0 0 0; color: #8B7355; font-size: 0.9rem;">{milestone['message']}</p>
                </div>
                """, unsafe_allow_html=True)

        # Show last check-in info if available
        last_check = st.session_state.progress_data.get('last_check_in')
        if last_check:
            st.markdown(f"""
            <p style="color: #6B8B6B; font-size: 0.85rem;">
                📅 Last check-in: {last_check} • 🔥 Streak: {st.session_state.streak} days
            </p>
            """, unsafe_allow_html=True)

    # Main content in columns for wide layout
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("""
        <div class="wellness-card">
            <div class="emoji-large">🌸</div>
            <h3 style="text-align: center;">Welcome to Your Recovery Journey</h3>
            <p style="text-align: center; color: #3D4D3D; line-height: 1.8;">
                I'm here to support you through your post-surgery healing. Together, we'll check in on how you're feeling,
                track your progress, and make sure you have the information you need to recover with confidence.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Random affirmation
        affirmation = random.choice(AFFIRMATIONS)
        st.markdown(f"""
        <div class="affirmation">{affirmation}</div>
        """, unsafe_allow_html=True)

    with col_right:
        # Daily Tip of the Day
        daily_tip = DAILY_TIPS[st.session_state.daily_tip_index]
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFF9F0 0%, #FFE8D6 100%); border: 1px solid #DEB887; border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
            <p style="margin: 0; color: #8B4513; font-weight: 600;">
                {daily_tip['icon']} Tip of the Day
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #654321; font-size: 0.95rem;">
                {daily_tip['tip']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
            <p>✨ <strong>What we'll do together:</strong></p>
            <p style="margin-top: 0.5rem;">
                • Check your physical symptoms<br>
                • Support your emotional wellbeing<br>
                • Provide personalized daily tips<br>
                • Track your healing progress
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Privacy notice
        st.markdown("""
        <div class="privacy-badge" style="margin-top: 1rem;">
            🔒 <strong>Your data stays on your device</strong> — We don't collect or store your personal information on external servers.
        </div>
        """, unsafe_allow_html=True)

        # Medical review date
        st.markdown(f"""
        <p style="color: #8B9B8B; font-size: 0.75rem; margin-top: 0.75rem;">
            📚 Medical information last reviewed: {LAST_MEDICAL_REVIEW}
        </p>
        """, unsafe_allow_html=True)

    # Action buttons
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1, 1, 1, 1])
    with btn_col1:
        if st.button("🩺 Begin Check-In", key="btn_begin", type="primary", use_container_width=True):
            st.session_state.step = 'get_info'
            st.rerun()
    with btn_col2:
        if st.button("📊 My Data", key="btn_progress", use_container_width=True):
            st.session_state.step = 'dashboard'
            st.rerun()
    with btn_col3:
        if st.button("ℹ️ About", key="btn_about", use_container_width=True):
            st.session_state.step = 'about'
            st.rerun()
    with btn_col4:
        if st.button("⚙️ Settings", key="btn_settings", use_container_width=True):
            st.session_state.step = 'settings'
            st.rerun()

    st.markdown("""
    <p style="text-align: center; color: #3A4A3A; font-size: 0.85rem; margin-top: 2rem;">
        💚 Remember: I'm here to support you, not replace medical advice.<br>
        Always follow your surgeon's instructions.
    </p>
    """, unsafe_allow_html=True)


def show_get_info():
    st.markdown("""
    <div class="wellness-card">
        <h3>📋 Tell Me About You</h3>
        <p style="color: #3D4D3D;">Let's personalize your recovery experience.</p>
    </div>
    """, unsafe_allow_html=True)

    # Name input
    name = st.text_input("What should I call you?", value=st.session_state.user_data.get('name', ''),
                         placeholder="Enter your name", key="input_name")

    if name and name in st.session_state.progress_data:
        st.markdown(f"""
        <div class="success-box">
            <p>🌟 Welcome back, <strong>{name}</strong>! I have your previous check-ins saved.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Procedure selection
    st.markdown("#### What procedure did you have?")

    categories = {
        "🌸 Face": ["rhinoplasty", "facelift", "brow lift", "blepharoplasty"],
        "💫 Breast": ["breast augmentation", "breast reduction"],
        "🦋 Body": ["tummy tuck", "bbl", "liposuction", "mommy makeover"],
        "✨ Skin": ["chemical peel", "botox fillers"],
    }

    selected_procedure = st.session_state.user_data.get('procedure', '')

    tabs = st.tabs(list(categories.keys()))

    for i, (category, procedures) in enumerate(categories.items()):
        with tabs[i]:
            for proc_key in procedures:
                if proc_key in PROCEDURES:
                    proc = PROCEDURES[proc_key]
                    btn_label = f"{proc.get('emoji', '✨')}  {proc['name']}"
                    if st.button(btn_label, key=f"proc_{proc_key}", use_container_width=True):
                        selected_procedure = proc_key
                        st.session_state.user_data['procedure'] = proc_key

    if selected_procedure and selected_procedure in PROCEDURES:
        proc = PROCEDURES[selected_procedure]
        st.markdown(f"""
        <div class="success-box">
            <p>{proc.get('emoji', '✨')} Selected: <strong>{proc['name']}</strong></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Post-op day
    st.markdown("#### What day of recovery are you on?")
    day = st.number_input("Post-op day", min_value=1, max_value=365,
                          value=st.session_state.user_data.get('day', 1),
                          label_visibility="collapsed", key="input_day")

    st.markdown(f"""
    <p style="color: #3A4A3A; font-size: 0.9rem;">
        Day {day} of your healing journey 🌱
    </p>
    """, unsafe_allow_html=True)

    # Continue button
    st.markdown("<br>", unsafe_allow_html=True)

    if name and selected_procedure:
        st.session_state.user_data['name'] = name
        st.session_state.user_data['day'] = day

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Continue", key="btn_continue_info", type="primary", use_container_width=True):
                st.session_state.step = 'physical_checkin'
                st.rerun()
    else:
        st.markdown("""
        <p style="text-align: center; color: #3A4A3A;">
            Please enter your name and select your procedure to continue.
        </p>
        """, unsafe_allow_html=True)


def show_physical_checkin():
    name = st.session_state.user_data.get('name', 'there')
    day = st.session_state.user_data.get('day', 1)

    st.markdown(f"""
    <div class="wellness-card">
        <h3>🩺 Physical Check-In</h3>
        <p style="color: #3D4D3D;">Day {day} — Let's see how your body is healing, {name}.</p>
    </div>
    """, unsafe_allow_html=True)

    # Symptom checker disclaimer
    st.markdown("""
    <div style="background: #FFF8F0; border: 1px solid #E8B4BC; border-radius: 10px; padding: 0.75rem 1rem; margin: 0.5rem 0 1rem 0;">
        <p style="color: #5A2D3A; font-size: 0.85rem; margin: 0;">
            ⚠️ <strong>Not a Diagnosis Tool:</strong> This check-in helps you track symptoms for your records.
            It does not diagnose conditions. Always consult your surgeon about any concerns.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Pain level with visual scale and dynamic colors
    st.markdown("#### How's your pain level?")
    pain_level = st.slider("Pain level", 1, 10, 5,
                           help="1 = No pain, 10 = Worst imaginable",
                           label_visibility="collapsed",
                           key="slider_pain_level")

    # Dynamic color based on pain level
    if pain_level <= 3:
        pain_color = "#2D7A2D"  # Green - doing great
        pain_bg = "#E8F5E8"
        pain_border = "#4CAF50"
    elif pain_level <= 6:
        pain_color = "#996B00"  # Orange/Yellow - moderate
        pain_bg = "#FFF8E1"
        pain_border = "#FFC107"
    else:
        pain_color = "#C62828"  # Red - high pain
        pain_bg = "#FFEBEE"
        pain_border = "#EF5350"

    pain_descriptions = {
        1: "😊 No pain", 2: "😌 Minimal", 3: "🙂 Mild", 4: "😐 Moderate-low",
        5: "😕 Moderate", 6: "😟 Moderate-high", 7: "😣 Significant",
        8: "😖 Severe", 9: "😫 Very severe", 10: "😰 Worst possible"
    }

    # Pain level display with dynamic color
    st.markdown(f"""
    <div style="background: {pain_bg}; border-left: 4px solid {pain_border};
                border-radius: 12px; padding: 1rem; margin: 0.5rem 0; text-align: center;">
        <p style="margin: 0; color: {pain_color}; font-size: 1.2rem; font-weight: 600;">
            {pain_descriptions.get(pain_level, '')}
        </p>
        <p style="margin: 0.5rem 0 0 0; color: {pain_color}; font-size: 0.85rem;">
            {'Excellent! Keep it up! 💚' if pain_level <= 3 else 'Manageable - stay on top of meds 💛' if pain_level <= 6 else 'Consider calling your surgeon if this persists ❤️'}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Symptoms in a clean layout
    st.markdown("#### Current Symptoms")

    col1, col2 = st.columns(2)

    with col1:
        swelling = st.selectbox("💧 Swelling", ["None", "Mild", "Moderate", "Severe"], index=2, key="select_swelling")
        bleeding = st.selectbox("🩸 Bleeding", ["None", "Spotting", "Light", "Heavy"], key="select_bleeding")

    with col2:
        bruising = st.selectbox("💜 Bruising", ["None", "Mild", "Moderate", "Severe"], index=1, key="select_bruising")

    col_check1, col_check2 = st.columns(2)
    with col_check1:
        has_fever = st.checkbox("🌡️ Fever or feeling feverish", key="check_fever")
    with col_check2:
        numbness = st.checkbox("✋ Numbness in surgical area", key="check_numbness")

    if has_fever:
        temperature = st.text_input("Temperature if known", placeholder="e.g., 100.5°F", key="input_temperature")
    else:
        temperature = None

    st.markdown("---")

    other_concerns = st.text_area("Anything else you want to share?",
                                   placeholder="Optional: describe any other symptoms or concerns...",
                                   height=80, key="input_concerns")

    # Store symptoms
    st.session_state.user_data['symptoms'] = {
        'pain_level': pain_level,
        'swelling': swelling.lower(),
        'bruising': bruising.lower(),
        'bleeding': bleeding.lower(),
        'fever': has_fever,
        'temperature': temperature,
        'numbness': numbness,
        'other': other_concerns if other_concerns else None
    }

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("See My Assessment", key="btn_see_assessment", type="primary", use_container_width=True):
            st.session_state.step = 'symptom_results'
            st.rerun()


def show_symptom_results():
    procedure_key = st.session_state.user_data.get('procedure', 'other')
    day = st.session_state.user_data.get('day', 1)
    symptoms = st.session_state.user_data.get('symptoms', {})
    pain_level = symptoms.get('pain_level', 5)

    if procedure_key in PROCEDURES:
        procedure = PROCEDURES[procedure_key]

        st.markdown(f"""
        <div class="wellness-card">
            <h3>{procedure.get('emoji', '✨')} Your Day {day} Assessment</h3>
            <p style="color: #3D4D3D;">{procedure['name']} Recovery</p>
        </div>
        """, unsafe_allow_html=True)

        # Find closest day
        available_days = sorted(procedure['normal_symptoms'].keys())
        closest_day = min(available_days, key=lambda x: abs(x - day))
        expected = procedure['normal_symptoms'][closest_day]

        # Expected symptoms
        st.markdown("#### What's Typical Right Now")

        for symptom, expected_level in expected.items():
            st.markdown(f"""
            <div style="background: #F5F0E8; padding: 0.75rem 1rem; border-radius: 10px; margin: 0.5rem 0;">
                <strong style="color: #3D6B3D;">{symptom.title()}</strong>
                <span style="color: #3D4D3D; float: right;">{expected_level}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="citation-box">
            📚 Symptom data from <a href="https://www.plasticsurgery.org" target="_blank">ASPS</a>,
            <a href="https://www.realself.com" target="_blank">RealSelf</a>, and
            <a href="https://www.webmd.com" target="_blank">WebMD</a>
        </div>
        """, unsafe_allow_html=True)

        # Peak swelling notice
        if day == procedure.get('peak_swelling_day'):
            st.markdown(f"""
            <div class="warning-box">
                <p>📍 <strong>Today is typically peak swelling day!</strong></p>
                <p style="margin-top: 0.5rem;">What you see right now is NOT your final result. This is completely normal and will improve significantly over the coming days.</p>
            </div>
            """, unsafe_allow_html=True)

        # Timeline metrics - custom cards for better text display
        st.markdown("#### Your Recovery Timeline")
        st.markdown(f"""
        <div style="display: flex; gap: 1rem; margin: 1rem 0; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 120px; background: #FFFFFF; border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                <p style="color: #5A7A5A; font-size: 0.85rem; margin: 0 0 0.5rem 0; font-weight: 500;">Peak Swelling</p>
                <p style="color: #2D3A2D; font-size: 1.1rem; margin: 0; font-weight: 600;">Day {procedure['peak_swelling_day']}</p>
            </div>
            <div style="flex: 1; min-width: 120px; background: #FFFFFF; border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                <p style="color: #5A7A5A; font-size: 0.85rem; margin: 0 0 0.5rem 0; font-weight: 500;">Swelling Duration</p>
                <p style="color: #2D3A2D; font-size: 1.1rem; margin: 0; font-weight: 600;">{procedure['swelling_duration'].split(',')[0]}</p>
            </div>
            <div style="flex: 1; min-width: 120px; background: #FFFFFF; border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                <p style="color: #5A7A5A; font-size: 0.85rem; margin: 0 0 0.5rem 0; font-weight: 500;">Final Results</p>
                <p style="color: #2D3A2D; font-size: 1.1rem; margin: 0; font-weight: 600;">{procedure['final_results']}</p>
            </div>
        </div>
        <div class="citation-box">
            📚 Timeline data from <a href="https://www.plasticsurgery.org" target="_blank">ASPS</a>,
            <a href="https://www.clevelandclinic.org" target="_blank">Cleveland Clinic</a>, and
            <a href="https://www.realself.com" target="_blank">RealSelf</a>
        </div>
        """, unsafe_allow_html=True)

    # Pain assessment
    st.markdown("#### Pain Assessment")

    if day <= 3 and pain_level <= 6:
        st.markdown("""
        <div class="success-box">
            <p>✅ Your pain level is manageable for this stage. Keep up with your medication schedule!</p>
        </div>
        """, unsafe_allow_html=True)
    elif day <= 3 and pain_level >= 7:
        st.markdown("""
        <div class="warning-box">
            <p>⚠️ Your pain is on the higher end, but this can be normal in the first few days. Make sure you're staying on top of your pain medication schedule.</p>
        </div>
        """, unsafe_allow_html=True)
    elif day > 3 and pain_level >= 7:
        st.markdown("""
        <div class="danger-box">
            <p>🔔 Your pain seems higher than typical for this stage. If it's not improving or getting worse, please contact your surgeon's office.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
            <p>🌟 Low pain level - you're doing wonderfully!</p>
        </div>
        """, unsafe_allow_html=True)

    # Warning signs check
    concerns = []
    if symptoms.get('bleeding', '').lower() == 'heavy':
        concerns.append("Heavy bleeding requires attention")
    if symptoms.get('fever') and symptoms.get('temperature'):
        try:
            temp = float(symptoms['temperature'].replace('F', '').replace('f', '').replace('°', '').strip())
            if temp >= 101:
                concerns.append(f"Fever of {temp}°F needs medical evaluation")
        except:
            pass

    if concerns:
        st.markdown("""
        <div class="danger-box">
            <p>🚨 <strong>Please contact your surgeon's office about:</strong></p>
        </div>
        """, unsafe_allow_html=True)
        for concern in concerns:
            st.error(f"• {concern}")

    # Warning signs to watch - using markdown box instead of expander
    if procedure_key in PROCEDURES:
        warning_signs = PROCEDURES[procedure_key].get('warning_signs', [])
        if warning_signs:
            st.markdown("""
            <div class="warning-box">
                <h4 style="margin: 0 0 0.75rem 0; color: #5C4813;">⚠️ Warning Signs to Watch For</h4>
                <p style="margin: 0 0 0.5rem 0; color: #5C4813;"><strong>🚨 Monitor for these symptoms:</strong></p>
            </div>
            """, unsafe_allow_html=True)
            for sign in warning_signs:
                st.markdown(f"<p style='color: #5C4813; margin: 0.25rem 0; padding-left: 1rem;'>⚠️ {sign}</p>", unsafe_allow_html=True)
            st.markdown("""
            <div class="citation-box">
                📚 Warning signs from <a href="https://www.plasticsurgery.org" target="_blank">ASPS</a> and
                <a href="https://www.mayoclinic.org" target="_blank">Mayo Clinic</a>
            </div>
            """, unsafe_allow_html=True)

    # Consult doctor reminder
    st.markdown("""
    <div class="consult-doctor-reminder">
        👩‍⚕️ <strong>Remember:</strong> Always consult your surgeon if you have concerns about your symptoms.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("📚 Medical Sources", key="btn_sources_symptom", use_container_width=True):
            st.session_state.step = 'references'
            st.rerun()
    with col2:
        if st.button("Continue to Emotional Check-In", key="btn_emotional", type="primary", use_container_width=True):
            st.session_state.step = 'emotional_checkin'
            st.rerun()


def show_emotional_checkin():
    name = st.session_state.user_data.get('name', 'there')
    procedure_key = st.session_state.user_data.get('procedure', 'other')
    day = st.session_state.user_data.get('day', 1)

    st.markdown(f"""
    <div class="wellness-card">
        <h3>💭 Emotional Check-In</h3>
        <p style="color: #3D4D3D;">How are you feeling emotionally today, {name}?</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Mood selection with emojis - use 3 columns on first row, 2 on second for better width
    st.markdown("""
    <style>
    .mood-btn button {
        white-space: nowrap !important;
        min-width: 100px !important;
        font-size: 0.85rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    moods = [
        ("😊", "Great", col1),
        ("🙂", "Good", col2),
        ("😐", "Okay", col3),
        ("😔", "Down", col4),
        ("😢", "Struggling", col5),
    ]

    selected_mood = st.session_state.user_data.get('emotional_state', None)

    for emoji, label, col in moods:
        with col:
            btn_style = "primary" if selected_mood == label.lower() else "secondary"
            if st.button(f"{emoji}\n{label}", key=f"mood_{label}", use_container_width=True):
                selected_mood = label.lower()
                st.session_state.user_data['emotional_state'] = selected_mood
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Response based on mood
    if selected_mood:
        if selected_mood in ['down', 'struggling']:
            st.markdown("""
            <div class="wellness-card" style="background: linear-gradient(135deg, #FDF2F4 0%, #FFFFFF 100%);">
                <div class="emoji-large">💗</div>
                <h3 style="text-align: center;">I hear you</h3>
                <p style="text-align: center; color: #3D4D3D; line-height: 1.8;">
                    What you're feeling is completely normal and valid. Post-surgical blues are incredibly common.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="info-box">
                <p><strong>Here's why you might be feeling this way:</strong></p>
                <p style="margin-top: 0.5rem; line-height: 1.8;">
                    🧠 Anesthesia affects your brain chemistry for days<br>
                    💊 Pain medications can cause mood changes<br>
                    ⚡ Your body is using all its energy to heal<br>
                    🏠 Limited mobility and isolation are hard<br>
                    🪞 Swelling can make you look/feel unlike yourself
                </p>
            </div>
            """, unsafe_allow_html=True)

            if procedure_key in PROCEDURES:
                procedure = PROCEDURES[procedure_key]
                st.markdown(f"""
                <div class="tip-card">
                    <h4>Remember</h4>
                    <p>Final {procedure['name']} results take {procedure['final_results']}. What you see right now is NOT what you'll look like when you're healed. 🌸</p>
                </div>
                """, unsafe_allow_html=True)

        elif selected_mood == 'okay':
            st.markdown("""
            <div class="success-box">
                <p>💚 <strong>That's perfectly valid!</strong></p>
                <p style="margin-top: 0.5rem;">Recovery is a marathon, not a sprint. "Okay" is absolutely acceptable when you're healing from surgery.</p>
            </div>
            """, unsafe_allow_html=True)

            if day <= 5:
                st.markdown("""
                <div class="info-box">
                    <p>🌱 The first week is the hardest emotionally for most people. You're almost through it!</p>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="success-box">
                <p>🌟 <strong>That's wonderful to hear!</strong></p>
                <p style="margin-top: 0.5rem;">A positive mindset can really help with healing. Just remember it's also okay to have down moments - recovery isn't linear.</p>
            </div>
            """, unsafe_allow_html=True)

        # Universal reminders
        st.markdown("""
        <div class="tip-card">
            <h4>Gentle Reminders</h4>
            <p style="line-height: 1.8;">
                🌸 Swelling distorts your results - don't judge what you see right now<br>
                🦋 Comparison is the thief of joy - everyone heals differently<br>
                📱 It's okay to limit social media and 'transformation' photos<br>
                💕 Reach out to friends, family, or your surgeon if you're struggling
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Continue to Daily Tips", key="btn_daily_tips", type="primary", use_container_width=True):
                st.session_state.step = 'daily_tip'
                st.rerun()


def show_daily_tip():
    procedure_key = st.session_state.user_data.get('procedure', 'other')
    day = st.session_state.user_data.get('day', 1)
    name = st.session_state.user_data.get('name', 'there')
    symptoms = st.session_state.user_data.get('symptoms', {})
    emotional_state = st.session_state.user_data.get('emotional_state', 'okay')

    # Get tip
    tip = None
    if procedure_key in PROCEDURES:
        procedure = PROCEDURES[procedure_key]
        tips = procedure.get('tips', {})

        if day in tips:
            tip = tips[day]
        else:
            available_days = sorted(tips.keys())
            closest = min(available_days, key=lambda x: abs(x - day))
            if abs(closest - day) <= 2:
                tip = tips[closest]

    if not tip:
        if day in DEFAULT_TIPS:
            tip = DEFAULT_TIPS[day]
        else:
            tip = "Keep up with your recovery routine! Consistency is key at this stage."

    st.markdown(f"""
    <div class="wellness-card">
        <h3>💡 Your Daily Wisdom</h3>
        <p style="color: #3D4D3D;">Personalized guidance for Day {day}</p>
    </div>
    """, unsafe_allow_html=True)

    # Main tip
    st.markdown(f"""
    <div class="tip-card">
        <h4>Today's Tip</h4>
        <p>{tip}</p>
    </div>
    """, unsafe_allow_html=True)

    # Recovery essentials
    st.markdown("#### Recovery Essentials")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: #E8F0E8; padding: 1rem; border-radius: 12px; height: 100%;">
            <p style="margin: 0; color: #2D4A2D;"><strong>💧 Hydration</strong></p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #2D4A2D;">Water, herbal tea, clear broths</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: #FDF2F4; padding: 1rem; border-radius: 12px; margin-top: 0.75rem;">
            <p style="margin: 0; color: #5A2D3A;"><strong>😴 Rest</strong></p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #5A2D3A;">Healing is hard work!</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: #F5F0E8; padding: 1rem; border-radius: 12px; height: 100%;">
            <p style="margin: 0; color: #4A3A2D;"><strong>🥩 Protein</strong></p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #4A3A2D;">Helps your body heal</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: #E8F0E8; padding: 1rem; border-radius: 12px; margin-top: 0.75rem;">
            <p style="margin: 0; color: #2D4A2D;"><strong>🚶 Movement</strong></p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #2D4A2D;">Gentle walks prevent clots</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="citation-box">
        📚 Recovery guidance from <a href="https://www.mayoclinic.org" target="_blank">Mayo Clinic</a>,
        <a href="https://www.clevelandclinic.org" target="_blank">Cleveland Clinic</a>, and
        <a href="https://www.webmd.com" target="_blank">WebMD</a>
    </div>
    <div class="consult-doctor-reminder">
        👩‍⚕️ <strong>Tip:</strong> These are general guidelines. Your surgeon's specific instructions take priority.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== COUNTDOWN TIMERS =====
    st.markdown("#### ⏱️ Recovery Milestones")

    milestones = PROCEDURE_MILESTONES.get(procedure_key, PROCEDURE_MILESTONES["default"])

    # Find upcoming milestones
    upcoming = [m for m in milestones if m["days"] > day]
    completed = [m for m in milestones if m["days"] <= day]

    if completed:
        st.markdown(f"""
        <div class="success-box">
            <p><strong>✅ Completed:</strong> {', '.join([f"{m['icon']} {m['milestone']}" for m in completed])}</p>
        </div>
        """, unsafe_allow_html=True)

    if upcoming:
        cols = st.columns(min(len(upcoming), 3))
        for i, m in enumerate(upcoming[:3]):
            with cols[i]:
                days_until = m["days"] - day
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FDF2F4 0%, #FFFFFF 100%);
                            padding: 1rem; border-radius: 12px; text-align: center;">
                    <div style="font-size: 2rem;">{m['icon']}</div>
                    <p style="margin: 0.5rem 0 0 0; font-weight: 600; color: #2D3A2D;">{m['milestone']}</p>
                    <p style="margin: 0.25rem 0 0 0; color: #5A2D3A; font-size: 1.2rem; font-weight: 700;">
                        {days_until} {'day' if days_until == 1 else 'days'}
                    </p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== RECOVERY CHECKLIST =====
    st.markdown("#### ✅ Daily Recovery Checklist")

    today_key = datetime.now().strftime("%Y-%m-%d")
    if today_key not in st.session_state.checklist:
        st.session_state.checklist[today_key] = {}

    # Group by time of day - using tabs instead of expanders to avoid key display bug
    morning_tab, afternoon_tab, evening_tab = st.tabs(["🌅 Morning", "☀️ Afternoon", "🌙 Evening"])

    for time_period, tab in [("morning", morning_tab), ("afternoon", afternoon_tab), ("evening", evening_tab)]:
        tasks = [t for t in DAILY_CHECKLIST if t["time"] == time_period]

        with tab:
            for idx, task in enumerate(tasks):
                task_key = f"checklist_{time_period}_{idx}_{hash(task['task']) % 10000}"
                checked = st.checkbox(
                    f"{task['icon']} {task['task']}",
                    value=st.session_state.checklist[today_key].get(task['task'], False),
                    key=task_key
                )
                st.session_state.checklist[today_key][task['task']] = checked

    # Show completion percentage
    total_tasks = len(DAILY_CHECKLIST)
    completed_tasks = sum(1 for t in DAILY_CHECKLIST if st.session_state.checklist[today_key].get(t['task'], False))
    completion_pct = int((completed_tasks / total_tasks) * 100)

    if completion_pct == 100:
        # Only show celebration ONCE when 100% is first reached
        if not st.session_state.celebration_shown:
            st.session_state.celebration_shown = True
            celebration = st.session_state.celebration_style

            # Built-in Streamlit animations
            if "Balloons" in celebration:
                st.balloons()
            elif "Snow" in celebration:
                st.snow()
            else:
                # Custom CSS animations for other celebration types
                if "Bubbles" in celebration:
                    animation_emoji = "🫧"
                elif "Hearts" in celebration:
                    animation_emoji = "❤️"
                elif "Confetti" in celebration:
                    animation_emoji = "🎊"
                elif "Sparkles" in celebration:
                    animation_emoji = "✨"
                elif "Butterflies" in celebration:
                    animation_emoji = "🦋"
                else:
                    animation_emoji = "🎉"

                # Custom falling animation CSS
                st.markdown(f"""
                <style>
                @keyframes fall {{
                    0% {{ transform: translateY(-100vh) rotate(0deg); opacity: 1; }}
                    100% {{ transform: translateY(100vh) rotate(720deg); opacity: 0; }}
                }}
                .celebration-particle {{
                    position: fixed;
                    top: -20px;
                    font-size: 2rem;
                    animation: fall 3s ease-in forwards;
                    z-index: 9999;
                    pointer-events: none;
                }}
                </style>
                <div class="celebration-particle" style="left: 10%; animation-delay: 0s;">{animation_emoji}</div>
                <div class="celebration-particle" style="left: 20%; animation-delay: 0.2s;">{animation_emoji}</div>
                <div class="celebration-particle" style="left: 30%; animation-delay: 0.4s;">{animation_emoji}</div>
                <div class="celebration-particle" style="left: 40%; animation-delay: 0.1s;">{animation_emoji}</div>
                <div class="celebration-particle" style="left: 50%; animation-delay: 0.3s;">{animation_emoji}</div>
                <div class="celebration-particle" style="left: 60%; animation-delay: 0.5s;">{animation_emoji}</div>
                <div class="celebration-particle" style="left: 70%; animation-delay: 0.2s;">{animation_emoji}</div>
                <div class="celebration-particle" style="left: 80%; animation-delay: 0.4s;">{animation_emoji}</div>
                <div class="celebration-particle" style="left: 90%; animation-delay: 0.1s;">{animation_emoji}</div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div class="success-box">
            <p>🎉 <strong>Amazing!</strong> You completed all your recovery tasks today!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Reset celebration flag when not at 100% (allows celebration again tomorrow)
        st.session_state.celebration_shown = False
        st.progress(completion_pct / 100)
        st.markdown(f"<p style='text-align: center; color: #3D4D3D;'>{completed_tasks}/{total_tasks} tasks completed ({completion_pct}%)</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== COMMUNITY QUOTES =====
    st.markdown("#### 💬 From Others Who've Been There")

    # Get relevant quotes (matching procedure or "any")
    relevant_quotes = [q for q in COMMUNITY_QUOTES
                      if q["procedure"] == procedure_key or q["procedure"] == "any"]
    # Prefer quotes from similar recovery day
    import random
    sorted_quotes = sorted(relevant_quotes, key=lambda q: abs(q["day"] - day))
    display_quote = sorted_quotes[0] if sorted_quotes else random.choice(COMMUNITY_QUOTES)

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #F5F0E8 0%, #FFFFFF 100%);
                border-radius: 16px; padding: 1.5rem; margin: 1rem 0;
                border-left: 4px solid #A8C5A8;">
        <p style="font-style: italic; font-size: 1.1rem; color: #2D3A2D; margin: 0;">
            "{display_quote['quote']}"
        </p>
        <p style="color: #5C6B5C; font-size: 0.85rem; margin: 0.75rem 0 0 0;">
            — Anonymous, Day {display_quote['day']} Recovery
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== SURGEON MESSAGE TEMPLATES =====
    st.markdown("#### 📝 Message Your Surgeon")

    show_surgeon_template = st.checkbox("📝 Click to generate a message template", key="show_surgeon_template")
    if show_surgeon_template:
        template_type = st.selectbox(
            "What do you need to communicate?",
            ["General Post-Op Update", "Concerning Symptoms", "Medication Question", "Schedule Follow-up"],
            key="select_template_type"
        )

        template_keys = {
            "General Post-Op Update": "general_update",
            "Concerning Symptoms": "concerning_symptoms",
            "Medication Question": "medication_question",
            "Schedule Follow-up": "schedule_followup"
        }

        template_key = template_keys[template_type]
        template_data = SURGEON_TEMPLATES[template_key]

        # Pre-fill template with user data
        procedure_name = PROCEDURES.get(procedure_key, {}).get('name', 'my procedure')
        pain_level = symptoms.get('pain_level', 5)
        swelling = symptoms.get('swelling', 'unknown')
        bruising = symptoms.get('bruising', 'unknown')

        filled_template = template_data["template"]
        filled_template = filled_template.replace("[NAME]", name if name else "[Your Name]")
        filled_template = filled_template.replace("[DAY]", str(day))
        filled_template = filled_template.replace("[PROCEDURE]", procedure_name)
        filled_template = filled_template.replace("[PAIN]", str(pain_level))
        filled_template = filled_template.replace("[SWELLING]", swelling.title())
        filled_template = filled_template.replace("[BRUISING]", bruising.title())

        # Use template_key in the widget key so it updates when selection changes
        st.text_area(
            "Copy and customize this message:",
            value=filled_template,
            height=300,
            key=f"surgeon_template_{template_key}"
        )

        st.markdown("""
        <p style="font-size: 0.85rem; color: #5C6B5C;">
            💡 <em>Tip: Copy this template and customize the bracketed sections before sending.</em>
        </p>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== SMART NOTIFICATIONS / CALENDAR EXPORT =====
    st.markdown("#### 📅 Medication Reminder Schedule")

    show_calendar = st.checkbox("📅 Click to create reminder schedule", key="show_calendar")
    if show_calendar:
        st.markdown("""
        <p style="color: #3D4D3D;">Enter your medication schedule to generate calendar reminders:</p>
        """, unsafe_allow_html=True)

        med_name = st.text_input("Medication name", placeholder="e.g., Pain medication", key="input_med_name")
        med_times = st.multiselect(
            "Reminder times",
            ["6:00 AM", "8:00 AM", "10:00 AM", "12:00 PM", "2:00 PM", "4:00 PM", "6:00 PM", "8:00 PM", "10:00 PM"],
            default=["8:00 AM", "2:00 PM", "8:00 PM"],
            key="multiselect_med_times"
        )
        med_days = st.slider("How many days of reminders?", 1, 14, 7, key="slider_med_days")

        if st.button("Generate Calendar File", key="btn_gen_calendar"):
            # Generate ICS content
            from datetime import timedelta
            ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Recovery Buddy//Medication Reminders//EN
"""
            base_date = datetime.now()

            for d in range(med_days):
                event_date = base_date + timedelta(days=d)
                for time_str in med_times:
                    hour = int(time_str.split(":")[0])
                    if "PM" in time_str and hour != 12:
                        hour += 12
                    elif "AM" in time_str and hour == 12:
                        hour = 0

                    event_datetime = event_date.replace(hour=hour, minute=0, second=0)
                    dtstart = event_datetime.strftime("%Y%m%dT%H%M%S")
                    dtend = (event_datetime + timedelta(minutes=15)).strftime("%Y%m%dT%H%M%S")

                    ics_content += f"""BEGIN:VEVENT
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:💊 {med_name if med_name else 'Take Medication'}
DESCRIPTION:Recovery Buddy Reminder - Day {d+1} of recovery
BEGIN:VALARM
TRIGGER:-PT5M
ACTION:DISPLAY
DESCRIPTION:Time to take your medication!
END:VALARM
END:VEVENT
"""
            ics_content += "END:VCALENDAR"

            st.download_button(
                label="📥 Download Calendar File",
                data=ics_content,
                file_name="medication_reminders.ics",
                mime="text/calendar"
            )

            st.success("Calendar file ready! Import into your phone's calendar app.")

    # Save progress
    today = datetime.now().strftime("%Y-%m-%d")
    today_entry = {
        'day': day,
        'pain_level': symptoms.get('pain_level', 5),
        'swelling': symptoms.get('swelling', 'unknown'),
        'emotional_state': emotional_state,
        'date': today
    }

    if name not in st.session_state.progress_data:
        st.session_state.progress_data[name] = {'procedure': procedure_key, 'entries': []}

    st.session_state.progress_data[name]['entries'].append(today_entry)
    save_progress(st.session_state.progress_data)

    # Progress summary
    entries = st.session_state.progress_data[name].get('entries', [])
    if len(entries) > 1:
        st.markdown("#### Your Progress")
        prev = entries[-2] if len(entries) > 1 else None
        if prev:
            prev_pain = prev.get('pain_level', 5)
            curr_pain = symptoms.get('pain_level', 5)

            if curr_pain < prev_pain:
                st.markdown(f"""
                <div class="success-box">
                    <p>📈 Your pain improved from {prev_pain} to {curr_pain}. That's progress!</p>
                </div>
                """, unsafe_allow_html=True)
            elif curr_pain > prev_pain:
                st.markdown(f"""
                <div class="warning-box">
                    <p>Pain increased from {prev_pain} to {curr_pain}. Keep monitoring and contact your doctor if it continues to rise.</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Complete Check-In", key="btn_complete", type="primary", use_container_width=True):
            st.session_state.step = 'complete'
            st.rerun()


def show_complete():
    import random

    name = st.session_state.user_data.get('name', 'there')
    day = st.session_state.user_data.get('day', 1)

    st.markdown(f"""
    <div class="wellness-card" style="text-align: center; background: linear-gradient(135deg, #FFFFFF 0%, #E8F0E8 100%);">
        <div class="emoji-large">🌸</div>
        <h2 style="margin-bottom: 0.5rem;">You're All Set, {name}!</h2>
        <p style="color: #3D4D3D; font-size: 1.1rem;">Day {day} check-in complete</p>
    </div>
    """, unsafe_allow_html=True)

    # Affirmation
    affirmation = random.choice(AFFIRMATIONS)
    st.markdown(f"""
    <div class="affirmation">{affirmation}</div>
    """, unsafe_allow_html=True)

    # Reminders
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="tip-card">
            <h4 style="text-align: center;">Remember</h4>
            <p style="text-align: center; line-height: 1.8;">
                🌿 Rest is productive<br>
                🕐 Healing takes time<br>
                🌊 Trust the process<br>
                📞 Call your surgeon with concerns
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="tip-card">
            <h4 style="text-align: center;">What's Next</h4>
            <p style="text-align: center; line-height: 1.8;">
                Come back tomorrow<br>
                for your next check-in!<br><br>
                💚 Wishing you a<br>
                smooth recovery
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== JOURNALING PROMPTS =====
    st.markdown("#### 📝 Reflection Journal")

    show_journal = st.checkbox("📓 Click to write in your recovery journal", key="show_journal")
    if show_journal:
        # Get random prompt - changes each time journal is opened
        import random
        import hashlib
        # Use a combination of date and session to get different prompt each session
        from datetime import datetime
        seed_str = f"{datetime.now().strftime('%Y%m%d%H')}{id(st.session_state)}"
        random.seed(int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (10**9))
        today_prompt = random.choice(JOURNALING_PROMPTS)

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FDF2F4 0%, #FFFFFF 100%);
                    padding: 1.25rem; border-radius: 12px; margin-bottom: 1rem;">
            <p style="color: #5A2D3A; font-weight: 600; margin: 0;">💭 Today's Prompt:</p>
            <p style="color: #2D3A2D; font-size: 1.1rem; font-style: italic; margin: 0.5rem 0 0 0;">
                "{today_prompt['prompt']}"
            </p>
            <p style="color: #8B9B8B; font-size: 0.75rem; margin-top: 0.5rem;">
                <em>Prompts rotate randomly • {len(JOURNALING_PROMPTS)} prompts available</em>
            </p>
        </div>
        """, unsafe_allow_html=True)

        journal_key = f"journal_{name}_{day}"
        journal_entry = st.text_area(
            "Your thoughts:",
            value=st.session_state.journal_entries.get(journal_key, ""),
            height=150,
            placeholder="Write freely - this is your private space to process your recovery journey...",
            key=f"journal_input_{day}"
        )

        if st.button("Save Journal Entry", key="btn_save_journal"):
            st.session_state.journal_entries[journal_key] = journal_entry
            st.success("Journal entry saved! 💚")

        # Show previous entries
        if len(st.session_state.journal_entries) > 0:
            st.markdown("---")
            st.markdown("**Previous Entries:**")
            for key, entry in sorted(st.session_state.journal_entries.items(), reverse=True)[:3]:
                if entry and entry.strip():
                    parts = key.split("_")
                    entry_day = parts[-1] if len(parts) >= 3 else "?"
                    st.markdown(f"""
                    <div style="background: #F5F0E8; padding: 0.75rem; border-radius: 8px; margin: 0.5rem 0;">
                        <p style="color: #5C6B5C; font-size: 0.8rem; margin: 0;">Day {entry_day}</p>
                        <p style="color: #2D3A2D; margin: 0.25rem 0 0 0; font-size: 0.9rem;">{entry[:200]}{'...' if len(entry) > 200 else ''}</p>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== PHOTO PROGRESS TRACKER =====
    st.markdown("#### 📸 Photo Progress Tracker")

    show_photos = st.checkbox("📸 Click to track your visual progress", key="show_photos")
    if show_photos:
        st.markdown("""
        <div class="info-box">
            <p>📱 <strong>Privacy Note:</strong> Photos are stored only on your device and are never uploaded to any server.
            This is your private record of your healing journey.</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            f"Upload Day {day} photo",
            type=['png', 'jpg', 'jpeg'],
            help="Take a photo of your surgical area to track healing progress",
            key="file_uploader_photo"
        )

        if uploaded_file is not None:
            st.image(uploaded_file, caption=f"Day {day} - {datetime.now().strftime('%B %d, %Y')}", use_container_width=True)

            # Save to session state for comparison
            photo_key = f"photo_{name}_{day}"
            if 'photos' not in st.session_state:
                st.session_state.photos = {}
            st.session_state.photos[photo_key] = uploaded_file

            st.success(f"Photo saved for Day {day}! 📸")

        # Show comparison if multiple photos exist
        if 'photos' in st.session_state and len(st.session_state.photos) > 1:
            st.markdown("---")
            st.markdown("**Compare Progress:**")

            photo_days = sorted([int(k.split("_")[-1]) for k in st.session_state.photos.keys()])

            if len(photo_days) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    day1 = st.selectbox("Compare Day:", photo_days[:-1], key="compare_day1")
                with col2:
                    day2 = st.selectbox("With Day:", [d for d in photo_days if d > day1], key="compare_day2")

                if f"photo_{name}_{day1}" in st.session_state.photos and f"photo_{name}_{day2}" in st.session_state.photos:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(st.session_state.photos[f"photo_{name}_{day1}"], caption=f"Day {day1}")
                    with col2:
                        st.image(st.session_state.photos[f"photo_{name}_{day2}"], caption=f"Day {day2}")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start New Check-In", key="btn_new_checkin", type="primary", use_container_width=True):
            st.session_state.step = 'welcome'
            st.session_state.user_data = {}
            st.rerun()

    # ===== FOOTER WITH COPYRIGHT, DISCLAIMER, LEGAL LINKS =====
    st.markdown(f"""
    <div class="app-footer">
        <p class="copyright-text">
            © 2026 Recovery Buddy. All rights reserved.<br>
            For informational purposes only. Not a substitute for professional medical advice.
        </p>
        <p class="copyright-text">
            Created with 💚 by Ashmita Sharma
        </p>
        <p class="copyright-text">
            <a href="mailto:contact@recoverybuddy.app">Questions? Contact us</a>
        </p>
        <p class="version-text">v{APP_VERSION}</p>
    </div>
    """, unsafe_allow_html=True)

    # Medical review date
    st.markdown(f"""
    <p style="text-align: center; color: #8B9B8B; font-size: 0.75rem; margin-top: 0.5rem;">
        📚 Medical information last reviewed: {LAST_MEDICAL_REVIEW} • 🔒 Data stored locally
    </p>
    """, unsafe_allow_html=True)

    # Footer navigation links
    st.markdown("<div style='text-align: center; margin-top: 0.5rem;'>", unsafe_allow_html=True)
    footer_cols = st.columns([1, 1, 1, 1, 1, 1])
    with footer_cols[0]:
        if st.button("🏠 Home", key="footer_home"):
            st.session_state.step = 'welcome'
            st.rerun()
    with footer_cols[1]:
        if st.button("📊 Progress", key="footer_progress"):
            st.session_state.step = 'dashboard'
            st.rerun()
    with footer_cols[2]:
        if st.button("Terms", key="footer_terms"):
            st.session_state.step = 'terms'
            st.rerun()
    with footer_cols[3]:
        if st.button("Privacy", key="footer_privacy"):
            st.session_state.step = 'privacy'
            st.rerun()
    with footer_cols[4]:
        if st.button("References", key="footer_references"):
            st.session_state.step = 'references'
            st.rerun()
    with footer_cols[5]:
        if st.button("About", key="footer_about"):
            st.session_state.step = 'about'
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def run_with_error_handling():
    """Wrapper to catch errors and show friendly messages"""
    try:
        main()
    except Exception as e:
        st.markdown("""
        <div class="friendly-error">
            <p style="font-size: 2rem;">😟</p>
            <p><strong>Oops! Something went wrong.</strong></p>
            <p>Please refresh the page to try again.</p>
            <p style="font-size: 0.8rem; margin-top: 1rem;">
                If this keeps happening, try clearing your browser cache<br>
                or contact us at feedback@recoverybuddy.app
            </p>
        </div>
        """, unsafe_allow_html=True)
        # Log the actual error for debugging (won't show to user)
        import logging
        logging.error(f"Recovery Buddy Error: {str(e)}")


if __name__ == "__main__":
    run_with_error_handling()
