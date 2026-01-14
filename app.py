#!/usr/bin/env python3
"""
Recovery Buddy - A supportive post-surgery recovery web app
Built with Streamlit - Luxury Wellness Aesthetic
"""

import streamlit as st
import json
import os
from datetime import datetime

# App version
APP_VERSION = "1.0"

# Page config with bloom favicon
st.set_page_config(
    page_title="Recovery Buddy",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

    /* Logo Header */
    .logo-header {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        margin-bottom: 1rem;
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
    }

    .logo-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: var(--text-light);
        margin-top: 0.5rem;
        font-weight: 400;
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

# Journaling prompts
JOURNALING_PROMPTS = [
    {"prompt": "Why did you decide to have this procedure? What made now the right time?", "category": "reflection"},
    {"prompt": "Write a letter to your future healed self. What do you hope to feel?", "category": "hope"},
    {"prompt": "What are you most looking forward to when you're fully healed?", "category": "goals"},
    {"prompt": "How has your support system shown up for you during recovery?", "category": "gratitude"},
    {"prompt": "What's one kind thing you can do for yourself today?", "category": "self-care"},
    {"prompt": "Describe a moment today when you felt strong or brave.", "category": "strength"},
    {"prompt": "What would you tell a friend going through the same recovery?", "category": "wisdom"},
    {"prompt": "List three things your body has done for you today.", "category": "gratitude"},
    {"prompt": "What fear about recovery has turned out to be unfounded?", "category": "reflection"},
    {"prompt": "How do you want to feel in one month? In three months?", "category": "goals"},
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
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" width="320" height="80" style="max-width: 100%;">
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
          <ellipse cx="50" cy="35" rx="12" ry="28" fill="url(#hPetalG)" transform="rotate(-30 50 50)" opacity="0.8"/>
          <ellipse cx="50" cy="35" rx="12" ry="28" fill="url(#hPetalG)" transform="rotate(30 50 50)" opacity="0.8"/>
          <ellipse cx="50" cy="35" rx="12" ry="28" fill="url(#hPetalG)" transform="rotate(-60 50 50)" opacity="0.7"/>
          <ellipse cx="50" cy="35" rx="12" ry="28" fill="url(#hPetalG)" transform="rotate(60 50 50)" opacity="0.7"/>
          <ellipse cx="50" cy="38" rx="10" ry="24" fill="url(#hPetalP)" transform="rotate(-20 50 50)" opacity="0.9"/>
          <ellipse cx="50" cy="38" rx="10" ry="24" fill="url(#hPetalP)" transform="rotate(20 50 50)" opacity="0.9"/>
          <ellipse cx="50" cy="38" rx="10" ry="24" fill="url(#hPetalP)" transform="rotate(-45 50 50)" opacity="0.85"/>
          <ellipse cx="50" cy="38" rx="10" ry="24" fill="url(#hPetalP)" transform="rotate(45 50 50)" opacity="0.85"/>
          <ellipse cx="50" cy="42" rx="8" ry="18" fill="#FFEEF2" transform="rotate(-10 50 50)" opacity="0.95"/>
          <ellipse cx="50" cy="42" rx="8" ry="18" fill="#FFEEF2" transform="rotate(10 50 50)" opacity="0.95"/>
          <ellipse cx="50" cy="44" rx="6" ry="15" fill="#FDFBF7" opacity="0.9"/>
          <circle cx="50" cy="50" r="10" fill="#FDFBF7" stroke="#E8B4BC" stroke-width="1"/>
          <circle cx="50" cy="50" r="6" fill="#A8C5A8" opacity="0.6"/>
          <circle cx="50" cy="50" r="3" fill="#5A7A5A" opacity="0.4"/>
          <text x="120" y="45" font-family="Georgia, serif" font-size="32" font-weight="600" fill="#5A7A5A">Recovery</text>
          <text x="280" y="45" font-family="Georgia, serif" font-size="32" font-weight="600" fill="#8FB58F">Buddy</text>
          <text x="120" y="72" font-family="Arial, sans-serif" font-size="12" fill="#8B9B8B">Bloom through your recovery journey</text>
        </svg>
    </div>
    """, unsafe_allow_html=True)


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
        st.session_state.dark_mode = False
    if 'checklist' not in st.session_state:
        st.session_state.checklist = {}
    if 'journal_entries' not in st.session_state:
        st.session_state.journal_entries = {}
    if 'celebration_shown' not in st.session_state:
        st.session_state.celebration_shown = False
    if 'celebration_style' not in st.session_state:
        st.session_state.celebration_style = "🎈 Balloons"

    # Apply dark mode if enabled
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(180deg, #1a2420 0%, #2d3a35 100%) !important;
        }
        .wellness-card, .tip-card, .info-box, .success-box, .warning-box, .danger-box {
            background: #2d3a35 !important;
            color: #E8F0E8 !important;
        }
        .wellness-card h2, .wellness-card h3, .wellness-card h4,
        .tip-card h2, .tip-card h3, .tip-card h4,
        h1, h2, h3, h4, h5, h6 {
            color: #E8F0E8 !important;
        }
        .wellness-card p, .tip-card p, .info-box p,
        p, li, span, label {
            color: #C8D8C8 !important;
        }
        .logo-title {
            color: #A8C5A8 !important;
        }
        .logo-subtitle {
            color: #8AA88A !important;
        }
        .progress-container {
            background: #2d3a35 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar with dark mode and emergency info
    with st.sidebar:
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

        # Emergency Info Box - Always visible
        st.markdown("### 🚨 Emergency Info")

        # Call 911 section
        show_911 = st.checkbox("🔴 Call 911 Immediately If:", key="show_911")
        if show_911:
            for item in EMERGENCY_INFO["call_911"]:
                st.markdown(f"&nbsp;&nbsp;&nbsp;🔴 {item}")

        # Call Surgeon Urgently section
        show_urgent = st.checkbox("🟠 Call Surgeon Urgently If:", key="show_urgent")
        if show_urgent:
            for item in EMERGENCY_INFO["call_surgeon_urgent"]:
                st.markdown(f"&nbsp;&nbsp;&nbsp;🟠 {item}")

        # Call Surgeon Soon section
        show_soon = st.checkbox("🟡 Call Surgeon Soon If:", key="show_soon")
        if show_soon:
            for item in EMERGENCY_INFO["call_surgeon_soon"]:
                st.markdown(f"&nbsp;&nbsp;&nbsp;🟡 {item}")

        st.markdown("---")
        st.markdown("""
        <p style="font-size: 0.8rem; color: #666;">
        💚 <strong>Your Surgeon's Office:</strong><br>
        <em>Add your surgeon's contact info here</em>
        </p>
        """, unsafe_allow_html=True)

    # Render header and progress
    render_header()
    render_progress_bar()

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


def show_welcome():
    import random

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

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Begin Check-In", key="btn_begin", type="primary", use_container_width=True):
            st.session_state.step = 'get_info'
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

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
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
        # Get today's prompt
        import random
        prompt_index = day % len(JOURNALING_PROMPTS)
        today_prompt = JOURNALING_PROMPTS[prompt_index]

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FDF2F4 0%, #FFFFFF 100%);
                    padding: 1.25rem; border-radius: 12px; margin-bottom: 1rem;">
            <p style="color: #5A2D3A; font-weight: 600; margin: 0;">Today's Prompt:</p>
            <p style="color: #2D3A2D; font-size: 1.1rem; font-style: italic; margin: 0.5rem 0 0 0;">
                "{today_prompt['prompt']}"
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

    # ===== FOOTER WITH COPYRIGHT, DISCLAIMER, CONTACT =====
    st.markdown(f"""
    <div class="app-footer">
        <p class="copyright-text">
            © 2026 Recovery Buddy. All rights reserved.<br>
            This app is for informational purposes only and is not a substitute for professional medical advice.
        </p>
        <p class="copyright-text">
            <a href="mailto:contact@recoverybuddy.app">Questions? Contact us</a>
        </p>
        <p class="version-text">v{APP_VERSION}</p>
    </div>
    """, unsafe_allow_html=True)


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
