#!/usr/bin/env python3
"""
Recovery Buddy - A supportive post-surgery recovery chatbot
"""

import json
import os
from datetime import datetime

# File to store progress data
PROGRESS_FILE = "recovery_progress.json"

# Procedure-specific recovery information
PROCEDURES = {
    "rhinoplasty": {
        "name": "Rhinoplasty",
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
        "warning_signs": ["heavy bleeding", "fever over 101F", "severe pain not controlled by meds", "vision changes", "increasing redness/warmth"],
    },
    "facelift": {
        "name": "Facelift",
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
        "warning_signs": ["severe pain on one side", "expanding firmness under skin", "fever over 101F", "sudden increase in swelling", "discharge from incisions"],
    },
    "breast augmentation": {
        "name": "Breast Augmentation",
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
            3: "Your breasts will look very high and tight right now - this is the 'bolt-on' phase. They WILL drop and soften!",
            4: "Continue sleeping elevated. You can start gentle arm movements but nothing overhead.",
            5: "The 'drop and fluff' process takes 3-6 months. Try not to judge your results yet!",
            7: "You may be feeling better but avoid lifting anything over 5 pounds still.",
            14: "Implants are still high and firm. They'll continue to settle over the next few months.",
        },
        "warning_signs": ["one breast significantly larger than other suddenly", "fever over 101F", "severe redness or warmth", "foul-smelling discharge", "severe pain not controlled by meds"],
    },
    "tummy tuck": {
        "name": "Tummy Tuck",
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
        "warning_signs": ["fever over 101F", "severe pain not controlled by meds", "opening of incision", "foul smell from incision", "excessive drain output suddenly"],
    },
    "bbl": {
        "name": "Brazilian Butt Lift (BBL)",
        "peak_swelling_day": 4,
        "swelling_duration": "6-8 weeks",
        "bruising_duration": "2-3 weeks",
        "final_results": "6-12 months (some fat reabsorption normal)",
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
        "warning_signs": ["severe shortness of breath", "chest pain", "severe pain in legs", "fever over 101F", "asymmetric severe swelling"],
    },
    # HEAD/FACE PROCEDURES
    "brow lift": {
        "name": "Brow/Forehead Lift",
        "peak_swelling_day": 3,
        "swelling_duration": "2-3 weeks for major swelling",
        "bruising_duration": "10-14 days",
        "final_results": "3-6 months",
        "normal_symptoms": {
            1: {"swelling": "moderate to significant", "bruising": "developing around eyes/forehead", "pain": "moderate (4-6)", "numbness": "forehead numbness common", "tightness": "significant"},
            2: {"swelling": "increasing, moving down to eyes", "bruising": "spreading to eyelids", "pain": "moderate (4-6)", "numbness": "expected", "tightness": "very tight feeling"},
            3: {"swelling": "peak - eyes may swell shut", "bruising": "at its worst", "pain": "moderate (3-5)", "numbness": "normal", "tightness": "intense"},
            4: {"swelling": "starting to decrease", "bruising": "darkest, spreading", "pain": "improving (3-5)", "numbness": "normal", "tightness": "still present"},
            5: {"swelling": "gradually decreasing", "bruising": "starting to fade", "pain": "mild (2-4)", "numbness": "normal", "tightness": "improving"},
            7: {"swelling": "noticeably better", "bruising": "yellowing", "pain": "mild (1-3)", "numbness": "may persist for weeks", "tightness": "improving"},
            14: {"swelling": "much improved", "bruising": "mostly gone", "pain": "minimal", "numbness": "may persist for months", "tightness": "much better"},
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
        "warning_signs": ["severe headache not relieved by meds", "fever over 101F", "vision changes", "increasing redness/warmth at incisions", "clear fluid leaking from incisions"],
    },
    "blepharoplasty": {
        "name": "Eyelid Lift (Blepharoplasty)",
        "peak_swelling_day": 2,
        "swelling_duration": "1-2 weeks for major swelling",
        "bruising_duration": "7-14 days",
        "final_results": "3-6 months",
        "normal_symptoms": {
            1: {"swelling": "moderate to significant", "bruising": "developing", "pain": "mild to moderate (2-5)", "dryness": "eyes may feel dry/gritty", "tearing": "excessive tearing common"},
            2: {"swelling": "peak - eyes may swell shut", "bruising": "darkening", "pain": "mild to moderate (2-5)", "dryness": "use lubricating drops", "tearing": "may continue"},
            3: {"swelling": "starting to decrease", "bruising": "at its worst", "pain": "mild (2-4)", "dryness": "continue drops", "tearing": "improving"},
            4: {"swelling": "improving", "bruising": "very dark", "pain": "mild (1-3)", "dryness": "may persist", "tearing": "normalizing"},
            5: {"swelling": "noticeably better", "bruising": "starting to fade", "pain": "minimal (1-2)", "dryness": "improving", "tearing": "normal"},
            7: {"swelling": "much improved", "bruising": "yellowing", "pain": "minimal", "dryness": "may persist", "tearing": "normal"},
            14: {"swelling": "mostly resolved", "bruising": "mostly gone", "pain": "none to minimal", "dryness": "improving", "tearing": "normal"},
        },
        "tips": {
            1: "Apply cold compresses gently to closed eyes for 10-15 minutes every hour. Use prescribed eye drops/ointment.",
            2: "Eyes may swell shut - this is temporary! Keep using cold compresses and lubricating drops.",
            3: "You may notice blurry vision from ointment and swelling - this is normal and temporary.",
            4: "Avoid reading, TV, or screen time that strains your eyes. Listen to audiobooks/podcasts instead.",
            5: "Sutures may be removed around now. Continue avoiding eye strain and sun exposure.",
            7: "Bruising is shifting colors - yellow/green means healing! Light sunglasses help when going outside.",
            14: "Most people feel comfortable without sunglasses. Avoid eye makeup for 2-3 weeks total.",
        },
        "warning_signs": ["severe eye pain", "vision changes or loss", "bleeding from incisions", "fever over 101F", "increasing redness or discharge", "inability to close eyes completely"],
    },
    "otoplasty": {
        "name": "Ear Pinning (Otoplasty)",
        "peak_swelling_day": 3,
        "swelling_duration": "2-3 weeks",
        "bruising_duration": "1-2 weeks",
        "final_results": "3-6 months",
        "normal_symptoms": {
            1: {"swelling": "moderate", "bruising": "minimal to mild", "pain": "moderate (4-6)", "numbness": "ears feel numb", "throbbing": "common"},
            2: {"swelling": "increasing", "bruising": "may develop", "pain": "moderate (4-6)", "numbness": "expected", "throbbing": "may continue"},
            3: {"swelling": "peak", "bruising": "if present, at worst", "pain": "moderate (3-5)", "numbness": "normal", "throbbing": "improving"},
            4: {"swelling": "starting to decrease", "bruising": "starting to fade", "pain": "improving (3-5)", "numbness": "normal", "throbbing": "less frequent"},
            5: {"swelling": "gradually decreasing", "bruising": "fading", "pain": "mild (2-4)", "numbness": "may persist", "throbbing": "occasional"},
            7: {"swelling": "noticeably less", "bruising": "mostly gone", "pain": "mild (1-3)", "numbness": "may persist", "throbbing": "rare"},
            14: {"swelling": "much improved", "bruising": "gone", "pain": "minimal", "numbness": "may persist for weeks", "throbbing": "none"},
        },
        "tips": {
            1: "Wear your headband/dressing exactly as instructed - it's crucial for results! Sleep on your back only.",
            2: "The pressure from the bandage may feel uncomfortable but is necessary. Take pain meds as needed.",
            3: "DO NOT touch, adjust, or remove your bandages. Ears are delicate right now.",
            4: "Continue sleeping on your back. A travel pillow can help keep you from rolling onto your ears.",
            5: "Bandages may be changed or removed at your follow-up. Ears will look very swollen - this is normal!",
            7: "Switch to sleeping headband at night as directed. Continue avoiding contact sports or rough activities.",
            14: "Ears are still healing internally. Continue wearing headband at night for 4-6 weeks total.",
        },
        "warning_signs": ["severe pain in one ear", "fever over 101F", "foul smell from bandages", "dark discoloration of ear", "blood soaking through bandages", "increasing redness/warmth"],
    },
    "facial implants": {
        "name": "Chin/Cheek/Jaw Reshaping (Facial Implants)",
        "peak_swelling_day": 3,
        "swelling_duration": "3-4 weeks for major swelling, subtle swelling up to 3 months",
        "bruising_duration": "1-2 weeks",
        "final_results": "3-6 months",
        "normal_symptoms": {
            1: {"swelling": "significant", "bruising": "developing", "pain": "moderate to severe (5-7)", "numbness": "common in implant area", "tightness": "significant"},
            2: {"swelling": "increasing", "bruising": "spreading", "pain": "moderate (5-7)", "numbness": "expected", "tightness": "very tight"},
            3: {"swelling": "peak", "bruising": "at its worst", "pain": "moderate (4-6)", "numbness": "normal", "tightness": "intense"},
            4: {"swelling": "starting to improve", "bruising": "darkest", "pain": "improving (4-6)", "numbness": "normal", "tightness": "still present"},
            5: {"swelling": "gradually decreasing", "bruising": "starting to fade", "pain": "improving (3-5)", "numbness": "may persist", "tightness": "improving"},
            7: {"swelling": "noticeably better but still significant", "bruising": "yellowing", "pain": "mild (2-4)", "numbness": "may persist for weeks", "tightness": "improving"},
            14: {"swelling": "much improved", "bruising": "mostly gone", "pain": "minimal", "numbness": "may persist for months", "tightness": "much better"},
        },
        "tips": {
            1: "Soft foods or liquid diet as directed. Avoid excessive chewing or talking. Sleep elevated.",
            2: "Ice packs applied externally (20 on/20 off) help with swelling. Continue soft diet.",
            3: "Your face will look very swollen and different - this is NOT your final result!",
            4: "If you had chin implant, avoid touching or putting pressure on your chin. No resting chin on hands.",
            5: "You may transition to softer solid foods. Continue avoiding hard or chewy foods.",
            7: "Implants are still settling. Asymmetry at this stage is normal and will improve.",
            14: "Swelling is improving but implants take 3+ months to fully settle into final position.",
        },
        "warning_signs": ["implant feels like it's shifting", "severe asymmetric swelling", "fever over 101F", "increasing pain after day 5", "difficulty opening mouth", "numbness getting worse rather than better"],
    },
    "lip augmentation": {
        "name": "Lip Augmentation (Surgical)",
        "peak_swelling_day": 2,
        "swelling_duration": "1-2 weeks for major swelling",
        "bruising_duration": "5-10 days",
        "final_results": "2-4 weeks for surgical; fillers settle in 2 weeks",
        "normal_symptoms": {
            1: {"swelling": "significant - lips very large", "bruising": "developing", "pain": "moderate (4-6)", "numbness": "common", "tightness": "lips feel huge"},
            2: {"swelling": "peak - lips extremely swollen", "bruising": "at its worst", "pain": "moderate (4-6)", "numbness": "expected", "tightness": "very tight"},
            3: {"swelling": "starting to decrease", "bruising": "dark", "pain": "improving (3-5)", "numbness": "normal", "tightness": "still significant"},
            4: {"swelling": "improving", "bruising": "starting to fade", "pain": "mild (2-4)", "numbness": "may persist", "tightness": "improving"},
            5: {"swelling": "noticeably better", "bruising": "yellowing", "pain": "mild (1-3)", "numbness": "improving", "tightness": "better"},
            7: {"swelling": "much improved", "bruising": "mostly gone", "pain": "minimal", "numbness": "may persist", "tightness": "minimal"},
            14: {"swelling": "mostly resolved", "bruising": "gone", "pain": "none", "numbness": "should be resolved", "tightness": "none"},
        },
        "tips": {
            1: "Ice is your best friend! Apply gently to lips (with barrier) for 10 minutes every hour. Stay hydrated.",
            2: "Your lips look MUCH bigger than they will be - expect 50%+ of this swelling to go down. Avoid salty foods.",
            3: "Drink through a straw if comfortable. Avoid hot foods/drinks. Soft, cool foods are best.",
            4: "Keep lips moisturized with plain Vaseline or Aquaphor. Avoid lipstick or lip products with fragrance.",
            5: "You can see your results emerging as swelling decreases. Continue gentle care.",
            7: "Most major swelling gone. Avoid kissing or pressure on lips for another week.",
            14: "Final results are visible. Lips may still feel slightly firm - this softens over next few weeks.",
        },
        "warning_signs": ["severe asymmetry", "hard lumps that don't improve", "fever over 101F", "white or dark discoloration of lip tissue", "increasing pain after day 3", "signs of infection at incision sites"],
    },
    # BREAST PROCEDURES
    "breast reduction": {
        "name": "Breast Reduction",
        "peak_swelling_day": 3,
        "swelling_duration": "4-6 weeks for major swelling",
        "bruising_duration": "2-3 weeks",
        "final_results": "6-12 months for final shape",
        "normal_symptoms": {
            1: {"swelling": "significant", "bruising": "developing", "pain": "moderate to severe (5-7)", "numbness": "nipple numbness common", "tightness": "very tight"},
            2: {"swelling": "increasing", "bruising": "spreading", "pain": "moderate (5-7)", "numbness": "expected", "tightness": "significant"},
            3: {"swelling": "peak", "bruising": "at its worst", "pain": "moderate (4-6)", "numbness": "normal", "tightness": "intense"},
            4: {"swelling": "starting to decrease", "bruising": "darkest", "pain": "improving (4-6)", "numbness": "normal", "tightness": "still present"},
            5: {"swelling": "gradually decreasing", "bruising": "starting to fade", "pain": "improving (3-5)", "numbness": "may persist", "tightness": "improving"},
            7: {"swelling": "noticeably better", "bruising": "yellowing", "pain": "mild (2-4)", "numbness": "may persist for months", "tightness": "improving"},
            14: {"swelling": "much improved but breasts still swollen", "bruising": "mostly gone", "pain": "minimal", "numbness": "may persist", "tightness": "much better"},
        },
        "tips": {
            1: "Wear your surgical bra 24/7. Sleep on your back, slightly elevated. Take pain meds on schedule.",
            2: "Avoid lifting your arms overhead. Short walks help prevent blood clots. Empty drains as instructed.",
            3: "Peak swelling - your breasts may look larger than expected. Significant size reduction comes after swelling subsides.",
            4: "You may notice the immediate relief from back/shoulder pain already. This is a great sign!",
            5: "Continue drain care if still in place. Keep incisions clean and dry.",
            7: "Stitches/drains often removed around now. Breasts will be swollen but you can see the new shape emerging.",
            14: "You can likely switch to a soft, supportive sports bra. No underwires for 6+ weeks.",
        },
        "warning_signs": ["fever over 101F", "one breast significantly more swollen/red than other", "foul smell from incisions", "nipple turning dark color", "opening of incisions", "severe pain not controlled by meds"],
    },
    "breast lift": {
        "name": "Breast Lift (Mastopexy)",
        "peak_swelling_day": 3,
        "swelling_duration": "3-4 weeks for major swelling",
        "bruising_duration": "2-3 weeks",
        "final_results": "6-12 months for final shape",
        "normal_symptoms": {
            1: {"swelling": "significant", "bruising": "developing", "pain": "moderate (4-6)", "numbness": "nipple area may be numb", "tightness": "significant"},
            2: {"swelling": "increasing", "bruising": "spreading", "pain": "moderate (4-6)", "numbness": "expected", "tightness": "very tight"},
            3: {"swelling": "peak", "bruising": "at its worst", "pain": "moderate (4-6)", "numbness": "normal", "tightness": "intense"},
            4: {"swelling": "starting to improve", "bruising": "darkest", "pain": "improving (3-5)", "numbness": "normal", "tightness": "still present"},
            5: {"swelling": "gradually decreasing", "bruising": "starting to fade", "pain": "improving (3-5)", "numbness": "may persist", "tightness": "improving"},
            7: {"swelling": "noticeably better", "bruising": "yellowing", "pain": "mild (2-4)", "numbness": "may persist", "tightness": "improving"},
            14: {"swelling": "much improved", "bruising": "mostly gone", "pain": "minimal", "numbness": "may persist for weeks", "tightness": "much better"},
        },
        "tips": {
            1: "Surgical bra 24/7 is crucial! Sleep on your back with slight elevation. Limit arm movements.",
            2: "Your breasts will look 'high' and swollen. They will settle into a more natural position.",
            3: "Peak swelling day. Incisions may look red and raised - this is normal healing.",
            4: "Gentle walking helps circulation. No lifting anything heavier than a coffee cup.",
            5: "You may feel pulling or twinges as nerves reconnect - good sign of healing!",
            7: "Tape or strips on incisions may start peeling. Follow surgeon's instructions on removal.",
            14: "Shape is emerging but will continue to evolve. Scars will be red but will fade over 12-18 months.",
        },
        "warning_signs": ["fever over 101F", "increasing redness/warmth around incisions", "foul-smelling discharge", "nipple turning dark color", "sudden increase in pain", "opening of incision line"],
    },
    "breast reconstruction": {
        "name": "Breast Reconstruction",
        "peak_swelling_day": 4,
        "swelling_duration": "6-8 weeks for major swelling",
        "bruising_duration": "2-4 weeks",
        "final_results": "6-18 months depending on type",
        "normal_symptoms": {
            1: {"swelling": "significant", "bruising": "developing", "pain": "moderate to severe (5-8)", "numbness": "extensive numbness normal", "tightness": "very tight"},
            2: {"swelling": "increasing", "bruising": "spreading", "pain": "moderate to severe (5-7)", "numbness": "expected", "tightness": "significant"},
            3: {"swelling": "continuing to increase", "bruising": "at its worst", "pain": "moderate (5-7)", "numbness": "normal", "tightness": "intense"},
            4: {"swelling": "peak", "bruising": "darkest", "pain": "moderate (4-6)", "numbness": "normal", "tightness": "very tight"},
            5: {"swelling": "starting to decrease", "bruising": "starting to fade", "pain": "improving (4-6)", "numbness": "may persist for months", "tightness": "still present"},
            7: {"swelling": "improving but still significant", "bruising": "yellowing", "pain": "moderate (3-5)", "numbness": "expected", "tightness": "improving"},
            14: {"swelling": "much improved", "bruising": "mostly gone", "pain": "mild (2-4)", "numbness": "may persist long-term", "tightness": "improving"},
        },
        "tips": {
            1: "This is major surgery - rest is essential. Surgical bra 24/7. Drain care as instructed.",
            2: "If you had flap surgery, avoid pressure on donor site too. Pillows everywhere for positioning!",
            3: "You've been through so much. Be incredibly gentle with yourself physically AND emotionally.",
            4: "Check drains regularly and record output. This info is important for your surgeon.",
            5: "Light walking is good but listen to your body. This recovery takes longer than cosmetic procedures.",
            7: "Drains may come out this week. Reconstructed breast will look different from final result.",
            14: "Healing well! If you're having tissue expander fills, expect ongoing appointments. Patience is key.",
        },
        "warning_signs": ["fever over 101F", "sudden increase in pain", "flap area turning dark/cool", "excessive drain output", "foul-smelling discharge", "hardness in reconstructed area", "redness spreading from incisions"],
    },
    "gynecomastia": {
        "name": "Gynecomastia Surgery (Male Breast Reduction)",
        "peak_swelling_day": 3,
        "swelling_duration": "3-4 weeks for major swelling",
        "bruising_duration": "2-3 weeks",
        "final_results": "3-6 months",
        "normal_symptoms": {
            1: {"swelling": "significant", "bruising": "developing", "pain": "moderate (4-6)", "numbness": "nipple numbness common", "tightness": "chest feels tight"},
            2: {"swelling": "increasing", "bruising": "spreading", "pain": "moderate (4-6)", "numbness": "expected", "tightness": "significant"},
            3: {"swelling": "peak", "bruising": "at its worst", "pain": "moderate (4-6)", "numbness": "normal", "tightness": "intense"},
            4: {"swelling": "starting to decrease", "bruising": "darkest", "pain": "improving (3-5)", "numbness": "normal", "tightness": "still present"},
            5: {"swelling": "gradually decreasing", "bruising": "starting to fade", "pain": "improving (3-5)", "numbness": "may persist", "tightness": "improving"},
            7: {"swelling": "noticeably better", "bruising": "yellowing", "pain": "mild (2-4)", "numbness": "may persist for weeks", "tightness": "improving"},
            14: {"swelling": "much improved", "bruising": "mostly gone", "pain": "minimal", "numbness": "may persist", "tightness": "much better"},
        },
        "tips": {
            1: "Wear compression vest 24/7 as instructed. Sleep on your back, slightly elevated.",
            2: "Ice can help with swelling. Apply over compression garment, 20 minutes on/off.",
            3: "Chest will look swollen and possibly lumpy. This is temporary - not your final result!",
            4: "Light walking is encouraged. Avoid any arm movements that engage chest muscles.",
            5: "Continue compression vest religiously. This helps skin retract and prevents fluid buildup.",
            7: "You may be anxious to see results but swelling masks the final outcome. Be patient!",
            14: "Many men return to desk jobs around now. Continue avoiding chest exercises for 4-6 weeks total.",
        },
        "warning_signs": ["fever over 101F", "significant asymmetry in swelling", "fluid buildup under skin", "hardness that doesn't improve", "nipple turning dark color", "increasing pain after day 5"],
    },
    # BODY PROCEDURES
    "liposuction": {
        "name": "Liposuction",
        "peak_swelling_day": 4,
        "swelling_duration": "4-6 weeks for major swelling, subtle swelling up to 6 months",
        "bruising_duration": "2-4 weeks",
        "final_results": "3-6 months",
        "normal_symptoms": {
            1: {"swelling": "significant", "bruising": "developing", "pain": "moderate to severe (5-7)", "numbness": "treated areas numb", "fluid": "drainage from incisions normal"},
            2: {"swelling": "increasing", "bruising": "spreading", "pain": "moderate (5-7)", "numbness": "expected", "fluid": "continued drainage normal"},
            3: {"swelling": "continuing to increase", "bruising": "darkening", "pain": "moderate (4-6)", "numbness": "normal", "fluid": "decreasing"},
            4: {"swelling": "peak", "bruising": "at its worst", "pain": "moderate (4-6)", "numbness": "normal", "fluid": "minimal"},
            5: {"swelling": "starting to decrease", "bruising": "starting to fade", "pain": "improving (3-5)", "numbness": "may persist", "fluid": "minimal to none"},
            7: {"swelling": "improving but still significant", "bruising": "yellowing", "pain": "mild (2-4)", "numbness": "may persist for weeks", "fluid": "none"},
            14: {"swelling": "much improved but area still larger than final", "bruising": "mostly gone", "pain": "minimal", "numbness": "improving", "fluid": "none"},
        },
        "tips": {
            1: "Compression garment 24/7 is CRUCIAL. Put pads in garment to absorb drainage. Walk every few hours.",
            2: "Fluid drainage for first 24-48 hours is totally normal. It's actually good - reducing swelling!",
            3: "You may look bigger than before surgery due to swelling. This is normal and temporary!",
            4: "Lymphatic massage can start if your surgeon approves. Helps move fluid and reduce swelling faster.",
            5: "Continue 24/7 compression. You can shower now but put garment right back on after.",
            7: "Lumpiness and firmness are normal at this stage. Tissue is healing and will smooth out.",
            14: "Results are starting to show but you're only about 25% of the way to final results. Patience!",
        },
        "warning_signs": ["fever over 101F", "severe pain not controlled by meds", "skin turning dark or cold", "foul-smelling drainage", "hard painful lump", "increasing redness/warmth", "dizziness or fainting"],
    },
    "brachioplasty": {
        "name": "Arm Lift (Brachioplasty)",
        "peak_swelling_day": 3,
        "swelling_duration": "3-4 weeks for major swelling",
        "bruising_duration": "2-3 weeks",
        "final_results": "3-6 months for scars to mature",
        "normal_symptoms": {
            1: {"swelling": "significant in arms and hands", "bruising": "developing", "pain": "moderate (4-6)", "numbness": "inner arm numbness common", "tightness": "arms feel tight"},
            2: {"swelling": "increasing", "bruising": "spreading", "pain": "moderate (4-6)", "numbness": "expected", "tightness": "very tight"},
            3: {"swelling": "peak - hands may swell too", "bruising": "at its worst", "pain": "moderate (4-6)", "numbness": "normal", "tightness": "intense"},
            4: {"swelling": "starting to decrease", "bruising": "darkest", "pain": "improving (3-5)", "numbness": "normal", "tightness": "still present"},
            5: {"swelling": "gradually decreasing", "bruising": "starting to fade", "pain": "improving (3-5)", "numbness": "may persist", "tightness": "improving"},
            7: {"swelling": "noticeably better", "bruising": "yellowing", "pain": "mild (2-4)", "numbness": "may persist for weeks", "tightness": "improving"},
            14: {"swelling": "much improved", "bruising": "mostly gone", "pain": "minimal", "numbness": "may persist for months", "tightness": "much better"},
        },
        "tips": {
            1: "Keep arms elevated when possible. Wear compression sleeves as instructed. Limit arm movements.",
            2: "Your hands may swell - this is fluid tracking down. Elevate and wiggle fingers often.",
            3: "Arms will feel very tight. You won't be able to fully straighten them yet - this improves.",
            4: "Gentle finger and wrist movements are good. Avoid lifting anything or reaching overhead.",
            5: "You may start to extend arms more. Listen to your body - don't force full extension.",
            7: "Drains out, sutures may be removed. Scars will be visible but will fade significantly.",
            14: "Range of motion improving. Continue avoiding lifting. Scars are red but will mature to lighter color.",
        },
        "warning_signs": ["fever over 101F", "one arm significantly more swollen than other", "hand numbness/tingling that's severe", "incisions opening", "foul smell from incisions", "dark discoloration of skin"],
    },
    "thigh lift": {
        "name": "Thigh Lift",
        "peak_swelling_day": 4,
        "swelling_duration": "4-6 weeks for major swelling",
        "bruising_duration": "2-4 weeks",
        "final_results": "6-12 months for scars to mature",
        "normal_symptoms": {
            1: {"swelling": "significant in thighs and groin", "bruising": "developing", "pain": "moderate to severe (5-7)", "numbness": "inner thigh numbness common", "tightness": "legs feel very tight"},
            2: {"swelling": "increasing", "bruising": "spreading", "pain": "moderate (5-7)", "numbness": "expected", "tightness": "significant"},
            3: {"swelling": "continuing to increase", "bruising": "at its worst", "pain": "moderate (5-7)", "numbness": "normal", "tightness": "intense"},
            4: {"swelling": "peak", "bruising": "darkest", "pain": "moderate (4-6)", "numbness": "normal", "tightness": "very tight"},
            5: {"swelling": "starting to decrease", "bruising": "starting to fade", "pain": "improving (4-6)", "numbness": "may persist", "tightness": "still present"},
            7: {"swelling": "improving but still significant", "bruising": "yellowing", "pain": "moderate (3-5)", "numbness": "may persist for weeks", "tightness": "improving"},
            14: {"swelling": "much improved", "bruising": "mostly gone", "pain": "mild (2-4)", "numbness": "may persist for months", "tightness": "much better"},
        },
        "tips": {
            1: "Compression garment 24/7. Sleep with legs slightly elevated and pillow between knees.",
            2: "Walking is difficult but important! Short, slow walks every few hours to prevent blood clots.",
            3: "Sitting may be uncomfortable. Use a donut pillow and avoid direct pressure on incisions.",
            4: "Incisions in groin area need to be kept dry. Extra careful hygiene important.",
            5: "Drainage and some oozing normal first week. Keep incision areas clean.",
            7: "You may be able to sit more comfortably. Continue wearing compression garment.",
            14: "Mobility much better. Swelling fluctuates - worse at end of day, better in morning. Normal!",
        },
        "warning_signs": ["fever over 101F", "severe leg pain or swelling (could be blood clot)", "incisions opening", "foul smell from groin incisions", "one leg significantly more swollen", "increasing redness spreading from incisions"],
    },
    "mommy makeover": {
        "name": "Mommy Makeover",
        "peak_swelling_day": 4,
        "swelling_duration": "6-8 weeks for major swelling",
        "bruising_duration": "3-4 weeks",
        "final_results": "6-12 months",
        "normal_symptoms": {
            1: {"swelling": "significant in all treated areas", "bruising": "developing", "pain": "severe (6-8)", "numbness": "multiple areas numb", "tightness": "cannot stand straight"},
            2: {"swelling": "increasing throughout", "bruising": "spreading", "pain": "severe (6-8)", "numbness": "expected", "tightness": "very hunched"},
            3: {"swelling": "continuing to increase", "bruising": "at its worst", "pain": "moderate to severe (5-7)", "numbness": "normal", "tightness": "intense"},
            4: {"swelling": "peak in all areas", "bruising": "darkest", "pain": "moderate (5-7)", "numbness": "normal", "tightness": "still significant"},
            5: {"swelling": "starting to decrease", "bruising": "starting to fade", "pain": "improving (4-6)", "numbness": "may persist", "tightness": "gradually improving"},
            7: {"swelling": "improving", "bruising": "yellowing", "pain": "moderate (4-6)", "numbness": "expected", "tightness": "improving"},
            14: {"swelling": "much improved but still present", "bruising": "mostly gone", "pain": "mild to moderate (3-5)", "numbness": "may persist for months", "tightness": "much better"},
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
        "warning_signs": ["fever over 101F", "severe pain not controlled by meds", "shortness of breath or chest pain (EMERGENCY)", "one area significantly more swollen", "foul smell from any incision", "dark discoloration of skin", "calf pain or swelling (blood clot risk)"],
    },
    # SKIN/NON-SURGICAL PROCEDURES
    "chemical peel": {
        "name": "Chemical Peel",
        "peak_swelling_day": 2,
        "swelling_duration": "3-7 days depending on peel depth",
        "bruising_duration": "rare, 0-5 days if present",
        "final_results": "2-4 weeks for superficial, 2-3 months for deep peels",
        "normal_symptoms": {
            1: {"swelling": "mild to moderate", "redness": "significant - skin is red/pink", "pain": "mild stinging/burning (2-4)", "tightness": "skin feels tight", "peeling": "not yet"},
            2: {"swelling": "peak for most peels", "redness": "intense", "pain": "mild (2-3)", "tightness": "very tight", "peeling": "may begin"},
            3: {"swelling": "decreasing", "redness": "still significant", "pain": "minimal (1-2)", "tightness": "tight", "peeling": "beginning"},
            4: {"swelling": "minimal", "redness": "improving", "pain": "minimal", "tightness": "moderate", "peeling": "active peeling"},
            5: {"swelling": "resolved", "redness": "pink", "pain": "none", "tightness": "less tight", "peeling": "active peeling"},
            7: {"swelling": "none", "redness": "mild pink", "pain": "none", "tightness": "minimal", "peeling": "finishing"},
            14: {"swelling": "none", "redness": "may still be pink", "pain": "none", "tightness": "none", "peeling": "complete for most"},
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
        "warning_signs": ["signs of infection (increasing redness, pus)", "fever", "severe pain", "blistering that worsens", "skin darkening in patches", "no peeling after 7 days (deep peels)"],
    },
    "laser resurfacing": {
        "name": "Laser Resurfacing",
        "peak_swelling_day": 2,
        "swelling_duration": "5-7 days for major swelling",
        "bruising_duration": "rare",
        "final_results": "3-6 months for full collagen remodeling",
        "normal_symptoms": {
            1: {"swelling": "moderate to significant", "redness": "intense - like severe sunburn", "pain": "moderate burning (4-6)", "oozing": "skin may ooze/weep", "tightness": "very tight"},
            2: {"swelling": "peak - eyes may swell", "redness": "intense", "pain": "moderate (4-5)", "oozing": "continuing", "tightness": "intense"},
            3: {"swelling": "starting to decrease", "redness": "still intense", "pain": "improving (3-4)", "oozing": "decreasing", "tightness": "very tight"},
            4: {"swelling": "improving", "redness": "still significant", "pain": "mild (2-3)", "oozing": "minimal", "tightness": "tight"},
            5: {"swelling": "much better", "redness": "pink to red", "pain": "minimal (1-2)", "oozing": "none", "tightness": "moderate"},
            7: {"swelling": "mostly resolved", "redness": "pink", "pain": "minimal", "oozing": "none", "tightness": "mild"},
            14: {"swelling": "none", "redness": "may still be pink - can last weeks", "pain": "none", "oozing": "none", "tightness": "minimal"},
        },
        "tips": {
            1: "Keep skin moist with prescribed ointment at ALL times. Skin should never feel dry. Sleep elevated.",
            2: "Eyes often swell significantly. Cool compresses on forehead (not treated skin) can help.",
            3: "Skin will ooze and crust - this is normal! Keep applying ointment. Crusting is part of healing.",
            4: "Gentle soaking with cool water then reapplying ointment helps with tight feeling.",
            5: "You may transition from ointment to gentle moisturizer as instructed. Skin still very delicate.",
            7: "Most people are through the 'social downtime' but redness persists. Mineral makeup can help camouflage.",
            14: "Redness may last weeks to months. It fades gradually. SPF is absolutely essential - new skin burns easily!",
        },
        "warning_signs": ["signs of infection (yellow/green discharge, increasing pain)", "fever", "cold sore outbreak (can be serious)", "severe swelling that doesn't improve", "darkening or whitening of treated skin"],
    },
    "botox fillers": {
        "name": "Botox/Fillers",
        "peak_swelling_day": 1,
        "swelling_duration": "1-3 days for most, up to 2 weeks for lip filler",
        "bruising_duration": "3-10 days if present",
        "final_results": "Botox: 7-14 days; Fillers: 2-4 weeks",
        "normal_symptoms": {
            1: {"swelling": "mild to moderate at injection sites", "bruising": "may develop", "pain": "mild (1-3)", "tenderness": "injection sites tender", "lumps": "may feel lumpy - normal"},
            2: {"swelling": "may increase slightly", "bruising": "if present, darkening", "pain": "minimal (1-2)", "tenderness": "still tender", "lumps": "still palpable"},
            3: {"swelling": "decreasing", "bruising": "if present, at worst", "pain": "minimal", "tenderness": "improving", "lumps": "settling"},
            4: {"swelling": "much improved", "bruising": "starting to fade", "pain": "none", "tenderness": "minimal", "lumps": "smoothing out"},
            5: {"swelling": "mostly resolved", "bruising": "fading", "pain": "none", "tenderness": "minimal", "lumps": "minimal"},
            7: {"swelling": "resolved", "bruising": "yellowing if present", "pain": "none", "tenderness": "none", "lumps": "should be smooth"},
            14: {"swelling": "none", "bruising": "gone", "pain": "none", "tenderness": "none", "lumps": "gone - if persist, see provider"},
        },
        "tips": {
            1: "Avoid rubbing or massaging treated areas for 24 hours. No strenuous exercise, alcohol, or lying flat for 4 hours after Botox.",
            2: "Arnica gel/supplements can help bruising fade faster. Ice gently if swollen.",
            3: "For Botox: Don't worry if you don't see effects yet - takes 7-14 days for full results.",
            4: "For fillers: Gently massage any lumps if your provider instructed. If not, leave alone.",
            5: "Avoid extreme heat (sauna, hot yoga) for first week - can affect how product settles.",
            7: "Botox should be starting to work. Fillers should be settled. Assess results now.",
            14: "Full results visible. If asymmetry or issues, contact your provider for touch-up assessment.",
        },
        "warning_signs": ["severe pain", "vision changes (EMERGENCY)", "skin turning white or blue", "signs of infection", "severe asymmetry", "difficulty swallowing or breathing (rare, EMERGENCY)", "skin breakdown at injection site"],
    },
    "scar revision": {
        "name": "Scar Revision",
        "peak_swelling_day": 2,
        "swelling_duration": "1-2 weeks",
        "bruising_duration": "1-2 weeks if present",
        "final_results": "12-18 months for scar to fully mature",
        "normal_symptoms": {
            1: {"swelling": "moderate around incision", "bruising": "may develop", "pain": "mild to moderate (3-5)", "redness": "incision site red", "tightness": "site feels tight"},
            2: {"swelling": "peak", "bruising": "if present, developing", "pain": "mild (2-4)", "redness": "expected", "tightness": "tight"},
            3: {"swelling": "starting to decrease", "bruising": "if present, at worst", "pain": "mild (2-3)", "redness": "normal", "tightness": "still present"},
            4: {"swelling": "improving", "bruising": "starting to fade", "pain": "minimal (1-2)", "redness": "still present", "tightness": "improving"},
            5: {"swelling": "much better", "bruising": "fading", "pain": "minimal", "redness": "normal part of healing", "tightness": "improving"},
            7: {"swelling": "mostly resolved", "bruising": "mostly gone", "pain": "minimal to none", "redness": "will persist for weeks", "tightness": "minimal"},
            14: {"swelling": "resolved", "bruising": "gone", "pain": "none", "redness": "still red - normal", "tightness": "minimal"},
        },
        "tips": {
            1: "Keep incision clean and dry. Follow wound care instructions precisely. No stretching the area.",
            2: "New scar will look WORSE before it looks better. This is totally normal with scar revision.",
            3: "Avoid any tension or movement that pulls on the healing incision.",
            4: "Keep area protected from sun - new scars darken easily and permanently.",
            5: "Sutures may be removed around now. Steri-strips or tape often applied after.",
            7: "Begin silicone gel/sheets if your surgeon recommends. This helps scar heal flatter.",
            14: "Scar will be red and possibly raised. It takes 12-18 months for final appearance!",
        },
        "warning_signs": ["signs of infection (increasing redness, warmth, pus)", "fever", "incision opening", "severe pain", "dark discoloration", "raised bumps along incision (may indicate keloid forming)"],
    },
}

# Default tips for days not specifically listed
DEFAULT_TIPS = {
    1: "Day 1 is all about rest. Your only job is to heal. Stay hydrated and take your meds on schedule.",
    2: "Day 2 can feel worse than Day 1 as anesthesia wears off. This is normal - you're not going backward!",
    3: "Day 3 is often emotionally and physically challenging. Be extra gentle with yourself today.",
    4: "You're almost through the hardest part! Small improvements start to show around now.",
    5: "Day 5 - you might feel good enough to overdo it. Resist the urge! Rest is still crucial.",
    7: "One week down! You've made it through the toughest part of recovery.",
    14: "Two weeks in - you're a recovery warrior! Results are still evolving but you're on the right track.",
}


def load_progress():
    """Load previous progress data if it exists."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_progress(data):
    """Save progress data to file."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def print_slow(text, pause=False):
    """Print text with formatting."""
    print(f"\n{text}")
    if pause:
        input("\n(Press Enter to continue...)")


def get_input(prompt):
    """Get user input with a friendly prompt."""
    print(f"\n{prompt}")
    return input("> ").strip()


def get_numeric_input(prompt, min_val, max_val):
    """Get numeric input within a range."""
    while True:
        response = get_input(prompt)
        try:
            value = int(response)
            if min_val <= value <= max_val:
                return value
            print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print(f"Please enter a number between {min_val} and {max_val}.")


def get_yes_no(prompt):
    """Get yes/no input."""
    while True:
        response = get_input(prompt).lower()
        if response in ['yes', 'y', 'yeah', 'yep', 'yup']:
            return True
        if response in ['no', 'n', 'nope', 'nah']:
            return False
        print("Please answer yes or no.")


def select_procedure():
    """Let user select their procedure."""
    print("\n" + "=" * 50)
    print("What procedure did you have?")
    print("=" * 50)

    procedures_list = list(PROCEDURES.keys())
    for i, proc in enumerate(procedures_list, 1):
        print(f"  {i}. {PROCEDURES[proc]['name']}")
    print(f"  {len(procedures_list) + 1}. Other")

    while True:
        choice = get_input("Enter the number of your procedure:")
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(procedures_list):
                return procedures_list[choice_num - 1]
            elif choice_num == len(procedures_list) + 1:
                return "other"
            print("Please enter a valid number.")
        except ValueError:
            # Check if they typed the procedure name
            choice_lower = choice.lower()
            for proc_key in procedures_list:
                if choice_lower in proc_key or choice_lower in PROCEDURES[proc_key]['name'].lower():
                    return proc_key
            print("Please enter a valid number or procedure name.")


def check_symptoms(procedure_key, day):
    """Ask about and evaluate symptoms."""
    print("\n" + "=" * 50)
    print("SYMPTOM CHECK")
    print("=" * 50)

    symptoms = {}
    concerns = []

    # Swelling
    print_slow("Let's check on your symptoms...")
    swelling = get_input("How would you rate your swelling? (none / mild / moderate / severe)")
    symptoms['swelling'] = swelling.lower()

    # Bruising
    bruising = get_input("How about bruising? (none / mild / moderate / severe)")
    symptoms['bruising'] = bruising.lower()

    # Bleeding
    bleeding = get_input("Any bleeding? (none / spotting / light / heavy)")
    symptoms['bleeding'] = bleeding.lower()
    if bleeding.lower() == 'heavy':
        concerns.append("Heavy bleeding is concerning")

    # Fever
    has_fever = get_yes_no("Do you have a fever or feel feverish?")
    symptoms['fever'] = has_fever
    if has_fever:
        temp = get_input("What's your temperature if you've checked? (or type 'unsure')")
        symptoms['temperature'] = temp
        if temp != 'unsure':
            try:
                temp_val = float(temp.replace('F', '').replace('f', '').strip())
                if temp_val >= 101:
                    concerns.append(f"Fever of {temp_val}F needs medical attention")
            except ValueError:
                pass

    # Numbness
    numbness = get_yes_no("Are you experiencing numbness in the surgical area?")
    symptoms['numbness'] = numbness

    # Additional concerns
    unusual = get_input("Anything else unusual or concerning you? (describe or type 'no')")
    if unusual.lower() not in ['no', 'n', 'none', 'nope']:
        symptoms['other'] = unusual

    return symptoms, concerns


def give_symptom_feedback(procedure_key, day, symptoms, pain_level):
    """Provide feedback on symptoms based on procedure and day."""
    print("\n" + "=" * 50)
    print("HOW YOU'RE DOING")
    print("=" * 50)

    if procedure_key == "other":
        print_slow("Since I don't have specific info about your procedure, here's general guidance:")
        print_slow(f"- Day {day} typically involves some swelling and discomfort")
        print_slow("- Your symptoms sound within the range of normal post-surgical recovery")
        print_slow("- Always trust your instincts - if something feels wrong, call your surgeon!")
        return

    procedure = PROCEDURES[procedure_key]

    # Find the closest day we have data for
    available_days = sorted(procedure['normal_symptoms'].keys())
    closest_day = min(available_days, key=lambda x: abs(x - day))
    expected = procedure['normal_symptoms'][closest_day]

    print_slow(f"For {procedure['name']} on day {day}, here's what's typical:")

    for symptom, expected_level in expected.items():
        print(f"  - {symptom.title()}: {expected_level}")

    # Pain assessment
    if day <= 3 and pain_level <= 6:
        print_slow("Your pain level sounds manageable for this stage - that's good!")
    elif day <= 3 and pain_level >= 7:
        print_slow("Your pain level is on the higher end but can be normal for the first few days. "
                   "Make sure you're staying on top of your pain medication schedule.")
    elif day > 3 and pain_level >= 7:
        print_slow("Your pain seems higher than typical for this stage. If it's not improving "
                   "or is getting worse, please contact your surgeon's office.")
    elif pain_level <= 3:
        print_slow("Low pain level - you're doing great!")

    # Swelling assessment
    if procedure.get('peak_swelling_day') and day == procedure['peak_swelling_day']:
        print_slow(f"Today is typically PEAK SWELLING day for {procedure['name']}. "
                   "What you're seeing is NOT your final result!")


def check_warning_signs(procedure_key, symptoms, concerns):
    """Check for warning signs that need medical attention."""
    print("\n" + "=" * 50)
    print("IMPORTANT HEALTH CHECK")
    print("=" * 50)

    urgent_warnings = []

    # Add any concerns already identified
    urgent_warnings.extend(concerns)

    # Check for universal warning signs
    if symptoms.get('bleeding', '').lower() == 'heavy':
        urgent_warnings.append("Heavy bleeding")

    if symptoms.get('fever') and symptoms.get('temperature', 'unsure') != 'unsure':
        try:
            temp = float(symptoms['temperature'].replace('F', '').replace('f', '').strip())
            if temp >= 101:
                urgent_warnings.append(f"Fever of {temp}F")
        except ValueError:
            pass

    # Check procedure-specific warnings
    if procedure_key != "other" and procedure_key in PROCEDURES:
        procedure = PROCEDURES[procedure_key]
        print_slow("Please watch out for these warning signs specific to your procedure:")
        for sign in procedure.get('warning_signs', []):
            print(f"  - {sign}")

    if urgent_warnings:
        print("\n" + "!" * 50)
        print("PLEASE CONTACT YOUR SURGEON'S OFFICE ABOUT:")
        print("!" * 50)
        for warning in urgent_warnings:
            print(f"  >>> {warning}")
        print("\nIt's always better to call and have it be nothing than to wait and have it be something!")
        print("Your surgeon's office expects these calls - that's what they're there for.")
    else:
        print_slow("Based on what you've shared, your symptoms sound within normal range. "
                   "But always trust your gut - if something feels off, call your doctor!")


def emotional_checkin(name, procedure_key, day):
    """Check in on emotional wellbeing."""
    print("\n" + "=" * 50)
    print("EMOTIONAL CHECK-IN")
    print("=" * 50)

    print_slow(f"Okay {name}, let's talk about how you're doing emotionally...")

    feeling = get_input("How are you feeling mentally/emotionally today? "
                        "(great / good / okay / down / struggling)")

    feeling_lower = feeling.lower()

    print_slow("Thank you for sharing that with me.")

    if feeling_lower in ['down', 'struggling', 'sad', 'depressed', 'anxious', 'worried', 'bad', 'terrible']:
        print_slow("I hear you, and I want you to know that what you're feeling is SO NORMAL.")
        print_slow("Post-surgical blues are incredibly common and there are real reasons for it:")
        print_slow("  - Anesthesia affects your brain chemistry for days")
        print_slow("  - Pain medications can cause mood changes")
        print_slow("  - Your body is using all its energy to heal")
        print_slow("  - Limited mobility and isolation are hard!")
        print_slow("  - Swelling can make you look/feel unlike yourself")

        if procedure_key != "other" and procedure_key in PROCEDURES:
            procedure = PROCEDURES[procedure_key]
            print_slow(f"\nRemember: Final {procedure['name']} results take {procedure['final_results']}.")
            print_slow("What you see right now is NOT what you'll look like when you're healed!")

        print_slow("\nBe gentle with yourself. You just had SURGERY. It's okay to rest, cry, or feel frustrated.")
        print_slow("These feelings will pass as you heal.")

    elif feeling_lower in ['okay', 'fine', 'alright', 'meh']:
        print_slow("That's totally valid! Recovery is a marathon, not a sprint.")
        print_slow("'Okay' is perfectly acceptable when you're healing from surgery.")

        if day <= 5:
            print_slow("The first week is the hardest emotionally for most people. You're almost through it!")

    else:  # good, great, etc.
        print_slow("That's wonderful to hear! A positive mindset can really help with healing.")
        print_slow("Just remember it's also okay to have down moments - recovery isn't linear.")

    # Universal reminders
    print_slow("\nA few reminders:")
    print_slow("  - Swelling distorts your results - try not to judge what you see right now")
    print_slow("  - Comparison is the thief of joy - everyone heals differently")
    print_slow("  - It's okay to limit social media and 'transformation' photos right now")
    print_slow("  - Reach out to friends, family, or your surgeon if you're struggling")

    return feeling_lower


def medication_reminder(name):
    """Check in on medications."""
    print("\n" + "=" * 50)
    print("MEDICATION CHECK")
    print("=" * 50)

    print_slow(f"Let's make sure you're staying on top of your meds, {name}...")

    taking_meds = get_yes_no("Are you currently taking any prescribed medications?")

    if not taking_meds:
        print_slow("Okay! If your doctor prescribed anything, make sure to follow their instructions.")
        return

    meds = get_input("What medications are you taking? (e.g., antibiotics, pain meds, anti-nausea)")

    taken_today = get_yes_no("Have you taken all your scheduled doses today?")

    if taken_today:
        print_slow("Great job staying on schedule! This is so important for your recovery.")
    else:
        print_slow("Try to get back on schedule as soon as you can!")
        print_slow("Setting phone alarms for each dose can really help.")

    print_slow("\nMedication tips:")
    print_slow("  - Take pain meds BEFORE pain gets severe - staying ahead of it is key")
    print_slow("  - Antibiotics should be completed even if you feel better")
    print_slow("  - Take meds with food if they upset your stomach")
    print_slow("  - Stay hydrated! Water helps your body process medications")
    print_slow("  - Stool softeners are your friend if you're on pain meds!")

    pain_med_concern = get_yes_no("Do you have any concerns about your pain management?")

    if pain_med_concern:
        print_slow("Please reach out to your surgeon's office about your pain management concerns.")
        print_slow("They may be able to adjust your medications or dosage.")
        print_slow("You shouldn't have to suffer - effective pain control helps you heal better!")


def give_daily_tip(procedure_key, day):
    """Give a helpful tip for the day."""
    print("\n" + "=" * 50)
    print("YOUR TIP FOR TODAY")
    print("=" * 50)

    tip = None

    if procedure_key != "other" and procedure_key in PROCEDURES:
        procedure = PROCEDURES[procedure_key]
        tips = procedure.get('tips', {})

        # Find exact day or closest day
        if day in tips:
            tip = tips[day]
        else:
            available_days = sorted(tips.keys())
            closest = min(available_days, key=lambda x: abs(x - day))
            if abs(closest - day) <= 2:  # Only use if within 2 days
                tip = tips[closest]

    if not tip:
        # Use default tips
        if day in DEFAULT_TIPS:
            tip = DEFAULT_TIPS[day]
        elif day < 7:
            tip = DEFAULT_TIPS[min(DEFAULT_TIPS.keys(), key=lambda x: abs(x - day) if x < 7 else float('inf'))]
        else:
            tip = "Keep up with your recovery routine! Consistency is key at this stage."

    print_slow(f"Day {day} Tip: {tip}")

    # Add general tips
    print_slow("\nGeneral reminders:")
    print_slow("  - Stay hydrated (water, herbal tea, clear broths)")
    print_slow("  - Eat protein to help your body heal")
    print_slow("  - Rest is productive - healing is hard work!")
    print_slow("  - Short, gentle walks help prevent blood clots")


def track_progress(name, procedure_key, day, pain_level, symptoms, emotional_state, progress_data):
    """Track and compare progress."""
    print("\n" + "=" * 50)
    print("PROGRESS TRACKING")
    print("=" * 50)

    today = datetime.now().strftime("%Y-%m-%d")

    # Create today's entry
    today_entry = {
        'day': day,
        'pain_level': pain_level,
        'swelling': symptoms.get('swelling', 'unknown'),
        'emotional_state': emotional_state,
        'date': today
    }

    # Initialize user data if needed
    if name not in progress_data:
        progress_data[name] = {
            'procedure': procedure_key,
            'entries': []
        }

    # Check for previous entry
    entries = progress_data[name].get('entries', [])
    previous_entry = entries[-1] if entries else None

    print_slow(f"Today's Summary for {name}:")
    print(f"  - Post-op Day: {day}")
    print(f"  - Pain Level: {pain_level}/10")
    print(f"  - Swelling: {symptoms.get('swelling', 'not reported')}")
    print(f"  - Emotional State: {emotional_state}")

    # Compare to yesterday
    if previous_entry:
        print_slow("\nComparing to your last check-in:")

        # Pain comparison
        prev_pain = previous_entry.get('pain_level', 0)
        if pain_level < prev_pain:
            print_slow(f"  Your pain went from {prev_pain} to {pain_level} - that's progress!")
        elif pain_level > prev_pain:
            print_slow(f"  Your pain increased from {prev_pain} to {pain_level}. "
                       "Keep an eye on this and call your doctor if it continues to rise.")
        else:
            print_slow(f"  Your pain is stable at {pain_level}.")

        # Celebrate progress
        prev_day = previous_entry.get('day', 0)
        if day > prev_day:
            print_slow(f"\n  You've made it from day {prev_day} to day {day}! Every day is progress.")
    else:
        print_slow("\nThis is your first check-in! I'll track your progress from here.")

    # Add today's entry
    entries.append(today_entry)
    progress_data[name]['entries'] = entries

    # Save progress
    save_progress(progress_data)

    # Encouragement
    print_slow("\nRemember: Recovery isn't linear. Some days are harder than others.")
    print_slow("You're doing amazing just by taking it day by day!")


def answer_questions():
    """Answer any questions the user might have."""
    print("\n" + "=" * 50)
    print("QUESTIONS?")
    print("=" * 50)

    has_questions = get_yes_no("Do you have any questions about your recovery?")

    if has_questions:
        question = get_input("What would you like to know?")

        print_slow("\nThank you for asking! While I can provide general information, "
                   "please remember that your surgeon's office is the best resource for "
                   "specific questions about YOUR recovery.")

        question_lower = question.lower()

        # Try to give helpful responses to common questions
        if any(word in question_lower for word in ['shower', 'bath', 'wash']):
            print_slow("\nAbout bathing: Most surgeons allow gentle showering 24-48 hours after surgery, "
                       "but NO baths, pools, or submerging incisions for several weeks. "
                       "Check your specific post-op instructions!")

        elif any(word in question_lower for word in ['exercise', 'workout', 'gym', 'lift']):
            print_slow("\nAbout exercise: Light walking is usually encouraged immediately, "
                       "but strenuous exercise typically needs to wait 4-6 weeks. "
                       "Your surgeon will clear you when it's safe.")

        elif any(word in question_lower for word in ['eat', 'food', 'diet']):
            print_slow("\nAbout diet: Focus on protein for healing, stay hydrated, "
                       "and eat fiber to prevent constipation from pain meds. "
                       "Some surgeons recommend limiting sodium to reduce swelling.")

        elif any(word in question_lower for word in ['sleep', 'sleeping', 'bed']):
            print_slow("\nAbout sleeping: Most procedures require elevated sleeping for the first week or more. "
                       "A wedge pillow or recliner can be really helpful. "
                       "Your specific procedure may have additional requirements.")

        elif any(word in question_lower for word in ['scar', 'scarring']):
            print_slow("\nAbout scarring: Scars take 12-18 months to fully mature. "
                       "They'll look worse before they look better! "
                       "Ask your surgeon about silicone sheets/gel after incisions are fully closed.")

        elif any(word in question_lower for word in ['swelling', 'swollen']):
            print_slow("\nAbout swelling: It's totally normal and can take weeks to months to fully resolve. "
                       "Stay hydrated, limit sodium, wear compression if prescribed, "
                       "and be patient - this is the hardest part!")

        else:
            print_slow("\nFor specific medical questions, please contact your surgeon's office. "
                       "They know your case and can give you personalized guidance.")

        # Ask if they have more questions
        return answer_questions()  # Recursive call for more questions

    else:
        print_slow("No problem! I'm here whenever you need support.")


def main():
    """Main chatbot flow."""
    # Load existing progress data
    progress_data = load_progress()

    # Welcome message
    print("\n" + "=" * 60)
    print("   Welcome to RECOVERY BUDDY")
    print("   Your Post-Surgery Support Companion")
    print("=" * 60)

    print_slow("Hi there! I'm Recovery Buddy, and I'm here to support you "
               "through your post-surgery recovery journey.")
    print_slow("I'll check in on how you're doing physically and emotionally, "
               "give you tips, and help track your progress.")
    print_slow("Remember: I'm not a replacement for medical advice - "
               "always follow your surgeon's instructions and call them with concerns!")

    # Get name
    name = get_input("First, what's your name?")
    print_slow(f"Nice to meet you, {name}! Let's see how you're doing today.")

    # Check if returning user
    if name in progress_data:
        print_slow(f"Welcome back, {name}! I have your previous check-ins saved.")

    # Get procedure
    procedure_key = select_procedure()

    if procedure_key == "other":
        other_procedure = get_input("What procedure did you have?")
        print_slow(f"Thanks! I don't have specific info about {other_procedure}, "
                   "but I'll give you general recovery guidance.")
    else:
        print_slow(f"Got it - {PROCEDURES[procedure_key]['name']}. "
                   "I'll tailor my feedback to your specific procedure!")

    # Get post-op day
    day = get_numeric_input("What day post-surgery are you on? (1, 2, 3, etc.)", 1, 365)
    print_slow(f"Day {day} - you're doing great making it this far!")

    # Get pain level
    print("\n" + "=" * 50)
    print("PHYSICAL CHECK-IN")
    print("=" * 50)
    pain_level = get_numeric_input("On a scale of 1-10, what's your pain level right now?\n"
                                    "(1 = no pain, 10 = worst pain imaginable)", 1, 10)

    # Check symptoms
    symptoms, concerns = check_symptoms(procedure_key, day)

    # Give feedback
    give_symptom_feedback(procedure_key, day, symptoms, pain_level)

    # Check warning signs
    check_warning_signs(procedure_key, symptoms, concerns)

    # Emotional check-in
    emotional_state = emotional_checkin(name, procedure_key, day)

    # Medication reminder
    medication_reminder(name)

    # Daily tip
    give_daily_tip(procedure_key, day)

    # Track progress
    track_progress(name, procedure_key, day, pain_level, symptoms, emotional_state, progress_data)

    # Questions
    answer_questions()

    # Closing
    print("\n" + "=" * 60)
    print("   Thank you for checking in with Recovery Buddy!")
    print("=" * 60)
    print_slow(f"Take care of yourself, {name}. You're doing amazing!")
    print_slow("Remember:")
    print("  - Rest is productive")
    print("  - Healing takes time")
    print("  - Trust the process")
    print("  - Call your surgeon if anything concerns you")
    print_slow("\nCome back tomorrow and let me know how you're doing!")
    print_slow("Wishing you a smooth recovery!")
    print("\n")


if __name__ == "__main__":
    main()
