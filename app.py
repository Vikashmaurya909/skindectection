import os
import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
from fpdf import FPDF
import webbrowser
from flask import Flask, render_template

import streamlit as st

from flask import Flask, render_template




# Load the model
model = tf.keras.models.load_model('cnn_model.h5', compile=False)

# Rename layers to avoid '/' issue
for layer in model.layers:
    layer._name = layer.name.replace("/", "_")

# Save the fixed model
model.save("cnn_model.h5")

# Load the fixed model
model = tf.keras.models.load_model('cnn_model.h5', compile=False)

# Define the class labels
class_labels = {
    0: "Acne",
    1: "Actinic Keratosis",
    2: "Aids",
    3: "Albinism_",
    4: "Angioedema",
    5: "Atopic Dermatitis",
    6: "Atopic dermatitis_",
    7: "Bacterial Skin Infections",
    8: "Bacterial Vaginosis (BV)",
    9: "Balanitis",
    10: "Benign Tumors",
    11: "Boils (Furuncles)",
    12: "Breast Abscess",
    13: "Bullous Disease ",
    14: "Bullous Pemphigoid",
    15: "Candidiasis (Yeast Infection)",
    16: "Cellulitis-1",
    17: "Chickenpox (Varicella)",
    18: "Chlamydia",
    19: "Contact dermatitis",
    20: "Cutaneous Anthrax",
    21: "Cutaneous Tuberculosis",
    22: "Drug Eruptions",
    23: "Drug Rash",
    24: "Ductal Carcinoma In Situ (DCIS)",
    25: "Eczema (Atopic Dermatitis)",
    26: "Eczema ",
    27: "Epidermolysis Bullosa",
    28: "Erysipelas",
    29: "Erysipeloid-2",
    30: "Exanthems and Drug Eruptions",
    31: "Fat Necrosis",
    32: "Folliculitiss",
    33: "Genital Herpes (HSV-2)",
    34: "Genital Scabies & Pubic Lice_",
    35: "Genital disease",
    36: "Gonorrhea",
    37: "Hair Diseases",
    38: "Harlequin Ichthyosis",
    39: "Head Lice (Pediculosis Capitis",
    40: "Herpes Simplex",
    41: "Hidradenitis Suppurativa",
    42: "Hives (Urticaria)",
    43: "Human Papillomavirus (HPV - Genital Warts)",
    44: "Hyperpigmentation",
    45: "Hypopigmentation",
    46: "Ichthyosis",
    47: "Impetigo",
    48: "Keratosis Pilaris",
    49: "Leishmaniasis",
    50: "Leprosy (Hansena_Ts Disease)",
    51: "Lichen Sclerosus",
    52: "Lichen disease",
    53: "Light Diseases and Disorders of Pigmentation",
    54: "Lupus (Cutaneous Lupus Erythematosus)",
    55: "Lupus and other Connective Tissue diseases",
    56: "Malignant Lesions",
    57: "Measles",
    58: "Melanoma",
    59: "Melasma",
    60: "Miliaria (Heat Rash)",
    61: "Moles",
    62: "Molluscum",
    63: "Molluscum Contagiosum",
    64: "Morphea",
    65: "Nail Disease",
    66: "Pemphigus",
    67: "Perianal Cellulitis",
    68: "Pseudomonas-Folliculitis-0018",
    69: "Psoriasis",
    70: "Psoriasis-Guttate",
    71: "Rosacea",
    72: "STDS",
    73: "Scabies (Scalp Scabies)",
    74: "Scalp Fungal Diseases",
    75: "Scleroderma",
    76: "Sebaceous Cyst",
    77: "Seborrheic dermatitis",
    78: "Shingles (Herpes Zoster)",
    79: "Staphylococcal-Folliculitis-18",
    80: "Sun damage",
    81: "Systemic Disease",
    82: "Tinea Ringworm Candidiasis and Fungal Infections",
    83: "Tinea corporis (body ringworm)",
    84: "Traction Alopecia",
    85: "Urticaria Hives",
    86: "Vaginal Melanoma",
    87: "Vascular Tumors",
    88: "Vasculitis Photos",
    89: "Vitiligo",
    90: "Warts Molluscum and other Viral Infections",
    91: "Xeroderma Pigmentosum",
    92: "Yeast Infections",
    93: "acne-keloidalis-29",
    94: "actinic keratosis",
    95: "allergic-contact-dermatitis",
    96: "alopecia-areata-22",
    97: "atypical-nevi",
    98: "basal cell cercinoma",
    99: "dermatofibroma",
    100: "dissecting-cellulitis-9",
    101: "halo nevus",
    102: "herpus disease",
    103: "insect bities",
    104: "lentigo adults",
    105: "lichen-planus",
    106: "malignant-melanoma",
    107: "mila",
    108: "nevus",
    109: "phototoxic-reactions",
    110: "pigmented benign keratosis",
    111: "pityriasis-rosea",
    112: "porphyrias-51",
    113: "psoriasis-digits",
    114: "rhus-dermatitis",
    115: "scabies",
    116: "seborrheic keratosis",
    117: "seborrheic-dermatitis",
    118: "spyhilis",
    119: "squamous cell carcinoma",
    120: "trichotillomania-25",
    121: "vascular lesion"
}

# Disease details dictionary
disease_info = {
     "Acne": {
        "Symptoms": "Acne presents as pimples, blackheads, whiteheads, cysts, and nodules, commonly appearing on the face, chest, back, and shoulders. It may also cause redness, swelling, and tenderness.",
        "Causes": "Acne is caused by excess oil production, clogged hair follicles, bacteria, and hormonal changes. Factors like stress, diet, and certain medications can also contribute.",
        "Protection": "Maintain a proper skincare routine, cleanse the skin regularly, use non-comedogenic products, avoid touching the face, and follow a healthy diet.",
        "Medicines": "Topical treatments like benzoyl peroxide, salicylic acid, retinoids, and oral antibiotics (doxycycline, minocycline) are common treatments. Severe cases may require isotretinoin.",
        "Treatment": "Treatment includes topical medications, oral antibiotics, laser therapy, chemical peels, and lifestyle modifications. Severe cases might require dermatologist intervention."
    },
    "Actinic Keratosis": {
        "Symptoms": "Actinic keratosis appears as rough, scaly patches on sun-exposed areas like the face, ears, scalp, and hands. It may itch, burn, or feel tender.",
        "Causes": "Prolonged UV exposure is the primary cause. Other factors include fair skin, aging, and weakened immune systems.",
        "Protection": "Use sunscreen (SPF 30+), wear protective clothing, and limit sun exposure, especially during peak hours.",
        "Medicines": "Topical treatments like fluorouracil, imiquimod, and diclofenac gel can be used. Cryotherapy and photodynamic therapy are other options.",
        "Treatment": "Early treatment prevents progression to squamous cell carcinoma. Treatments include cryotherapy, laser therapy, chemical peels, and excision of affected skin."
    },
    "Aids": {
        "Symptoms": "Early symptoms include fever, swollen lymph nodes, sore throat, rash, and fatigue. As the disease progresses, it weakens the immune system, making the body vulnerable to infections and certain cancers.",
        "Causes": "AIDS is caused by the Human Immunodeficiency Virus (HIV), which attacks the immune system, particularly CD4 cells.",
        "Protection": "Use protection during intercourse, avoid sharing needles, and take pre-exposure prophylaxis (PrEP) if at high risk.",
        "Medicines": "Antiretroviral therapy (ART) is the primary treatment. Common drugs include tenofovir, emtricitabine, dolutegravir, and efavirenz.",
        "Treatment": "There is no cure for AIDS, but ART can help manage the virus, improve life expectancy, and prevent transmission. Regular monitoring and a healthy lifestyle are essential."
    },
     "Albinism": {
        "Symptoms": "Pale skin, light-colored eyes, vision problems, sensitivity to sunlight.",
        "Causes": "Genetic mutations affecting melanin production.",
        "Protection": "Use sunscreen, wear sunglasses, avoid direct sunlight.",
        "Medicines": "No specific cure, but eye conditions can be managed with corrective lenses.",
        "Treatment": "Regular skin checks, vision therapy, sun protection measures."
    },
    "Angioedema": {
        "Symptoms": "Swelling under the skin, usually around the eyes and lips, sometimes affecting the throat.",
        "Causes": "Allergic reactions, hereditary factors, medication side effects.",
        "Protection": "Avoid known allergens, carry an epinephrine auto-injector if prescribed.",
        "Medicines": "Antihistamines, corticosteroids, epinephrine for severe cases.",
        "Treatment": "Identify triggers, emergency care for severe reactions, long-term allergy management."
    },
    "Atopic Dermatitis": {
        "Symptoms": "Red, itchy, inflamed skin, dryness, cracking, and oozing lesions.",
        "Causes": "Genetic factors, immune system dysfunction, environmental triggers.",
        "Protection": "Moisturize regularly, avoid allergens and irritants, wear soft fabrics.",
        "Medicines": "Topical steroids, antihistamines, immune-modulating creams.",
        "Treatment": "Skin hydration, medication, phototherapy for severe cases, lifestyle adjustments."
    },
    "Bacterial Skin Infections": {
        "Symptoms": "Redness, swelling, pus-filled lesions, pain, and fever in severe cases.",
        "Causes": "Bacteria such as Staphylococcus and Streptococcus.",
        "Protection": "Maintain hygiene, avoid sharing personal items, treat cuts promptly.",
        "Medicines": "Topical and oral antibiotics like mupirocin, cephalexin.",
        "Treatment": "Cleaning wounds properly, antibiotic therapy, drainage of abscesses if needed."
    },
    "Bacterial Vaginosis (BV)": {
        "Symptoms": "Thin, gray or white vaginal discharge, fishy odor, itching, burning sensation.",
        "Causes": "Imbalance of vaginal bacteria, multiple sexual partners, douching.",
        "Protection": "Practice safe hygiene, avoid douching, use protection during intercourse.",
        "Medicines": "Metronidazole, Clindamycin (oral or topical antibiotics).",
        "Treatment": "Antibiotic therapy, probiotics, maintaining vaginal pH balance."
    },
    "Balanitis": {
        "Symptoms": "Redness, swelling, pain, itching, and white discharge under the foreskin.",
        "Causes": "Poor hygiene, fungal or bacterial infections, diabetes, irritation from soaps.",
        "Protection": "Maintain proper hygiene, avoid harsh soaps, keep the area dry.",
        "Medicines": "Antifungal creams (Clotrimazole), antibiotics for bacterial infections.",
        "Treatment": "Improved hygiene, antifungal or antibacterial treatment, circumcision in chronic cases."
    },
    "Benign Tumors": {
        "Symptoms": "Non-cancerous growths, lumps, or masses in various body tissues, usually painless.",
        "Causes": "Genetic factors, environmental triggers, hormonal imbalances.",
        "Protection": "Regular medical check-ups, healthy diet, avoid radiation exposure.",
        "Medicines": "Pain relievers if needed, medications for hormone-related tumors.",
        "Treatment": "Observation, surgical removal if symptomatic, radiation therapy in rare cases."
    },
   "Boils (Furuncles)": {
        "Symptoms": "Red, painful lump filled with pus, swelling, tenderness, may drain pus.",
        "Causes": "Bacterial infection (Staphylococcus aureus), poor hygiene, weakened immune system.",
        "Protection": "Maintain good hygiene, avoid sharing personal items, keep cuts clean.",
        "Medicines": "Antibiotics (Clindamycin for Moderate ,Fusidic Acid Cream for small), pain relievers.",
        "Treatment": "Warm compresses, drainage by a doctor if necessary, antibiotic therapy."
    },
    "Breast Abscess": {
        "Symptoms": "Painful lump in the breast, redness, warmth, fever, swelling.",
        "Causes": "Bacterial infection, clogged milk ducts, breastfeeding complications.",
        "Protection": "Proper breastfeeding techniques, good hygiene, avoiding nipple damage.",
        "Medicines": "Antibiotics (Amoxicillin, Clindamycin), pain relievers.",
        "Treatment": "Antibiotic therapy, drainage of abscess, continued breastfeeding if possible."
    },
    "Bullous Disease": {
        "Symptoms": "Blistering skin, itching, redness, fluid-filled lesions.",
        "Causes": "Autoimmune reactions, infections, genetic factors.",
        "Protection": "Avoid triggers, use gentle skincare products, stay hydrated.",
        "Medicines": "Corticosteroids, immunosuppressants, antibiotics for secondary infections.",
        "Treatment": "Medications to control the immune response, wound care, avoiding irritants."
    },
    "Bullous Pemphigoid": {
        "Symptoms": "Large, fluid-filled blisters, redness, itching, skin irritation.",
        "Causes": "Autoimmune disorder attacking skin layers, aging, certain medications.",
        "Protection": "Avoid skin trauma, manage underlying health conditions.",
        "Medicines": "Corticosteroids (Prednisone), immunosuppressants, topical treatments.",
        "Treatment": "Long-term immune suppression, wound care, lifestyle modifications."
    },
    "Candidiasis (Yeast Infection)": {
        "Symptoms": "White patches in the mouth (oral thrush), itching, burning, discharge.",
        "Causes": "Overgrowth of Candida fungus, weakened immune system, antibiotic use.",
        "Protection": "Maintain proper hygiene, avoid excessive sugar, wear breathable fabrics.",
        "Medicines": "Antifungal creams (Clotrimazole), oral antifungals (Fluconazole).",
        "Treatment": "Topical or oral antifungal therapy, probiotic supplementation."
    },
    "Cellulitis": {
        "Symptoms": "Red, swollen, warm skin, pain, fever, chills.",
        "Causes": "Bacterial infection (Streptococcus, Staphylococcus), open wounds, weak immunity.",
        "Protection": "Proper wound care, hygiene, managing diabetes or other risk factors.",
        "Medicines": "Oral or IV antibiotics (Amoxicillin, Cephalexin, Clindamycin).",
        "Treatment": "Antibiotic therapy, elevation of affected limb, pain management."
    },
   "Chickenpox (Varicella)": {
        "Symptoms": "Red, itchy rash with fluid-filled blisters, fever, fatigue, headache.",
        "Causes": "Varicella-zoster virus, highly contagious through droplets or contact.",
        "Protection": "Varicella vaccine, avoid contact with infected individuals.",
        "Medicines": "Antiviral drugs (Acyclovir) for severe cases, antihistamines for itching.",
        "Treatment": "Rest, hydration, calamine lotion, cool baths, pain relievers."
    },
    "Chlamydia": {
        "Symptoms": "Painful urination, genital discharge, pelvic pain, asymptomatic in some cases.",
        "Causes": "Sexually transmitted infection (Chlamydia trachomatis), unprotected sex.",
        "Protection": "Use condoms, regular STD testing, limit sexual partners.",
        "Medicines": "Antibiotics (Azithromycin, Doxycycline).",
        "Treatment": "Full antibiotic course, partner treatment, abstaining from sex during recovery."
    },
    "Contact Dermatitis": {
        "Symptoms": "Red, itchy, dry, or cracked skin, blisters in severe cases.",
        "Causes": "Allergic reaction (plants, cosmetics, metals) or irritants (chemicals, soaps).",
        "Protection": "Avoid known triggers, use hypoallergenic products, wear gloves.",
        "Medicines": "Topical steroids (Hydrocortisone), antihistamines for itching.",
        "Treatment": "Avoidance of irritants, cool compresses, moisturizing, medical creams."
    },
    "Cutaneous Anthrax": {
        "Symptoms": "Painless skin sore with black center, fever, swelling, flu-like symptoms.",
        "Causes": "Bacillus anthracis infection from infected animals or contaminated products.",
        "Protection": "Avoid handling infected animals, use protective clothing.",
        "Medicines": "Antibiotics (Ciprofloxacin, Doxycycline).",
        "Treatment": "Long-term antibiotic therapy, wound care, supportive care for complications."
    },
    "Cutaneous Tuberculosis": {
        "Symptoms": "Symptoms of cutaneous tuberculosis include ulcers, lesions, and thickened skin. It may also cause swelling of the lymph nodes near the affected area. In some cases, the skin may become discolored or form abscesses.",
        "Causes": "Cutaneous tuberculosis is caused by the Mycobacterium tuberculosis bacterium, which typically affects the lungs but can spread to the skin. The infection is transmitted through close contact with an infected person.",
        "Protection": "Preventing cutaneous tuberculosis involves avoiding close contact with individuals who have active tuberculosis, maintaining good hygiene, and ensuring early detection and treatment of tuberculosis in the body.",
        "Medicines": "Antibiotic treatment for tuberculosis, such as rifampin, isoniazid, and pyrazinamide, is commonly used to treat cutaneous tuberculosis.",
        "Treatment": "Treatment typically includes a course of antibiotics that may last several months, depending on the severity of the infection. In some cases, surgery may be needed to remove infected tissue."
    },
    "Drug Eruptions": {
        "Symptoms": "Drug eruptions can cause skin rashes, redness, blisters, and swelling. The rash may be itchy or painful and can appear anywhere on the body. In severe cases, it may cause peeling skin or difficulty breathing.",
        "Causes": "Drug eruptions are caused by an allergic reaction to medications or by direct irritation from drugs. Common culprits include antibiotics, anticonvulsants, and nonsteroidal anti-inflammatory drugs (NSAIDs).",
        "Protection": "To prevent drug eruptions, avoid medications known to cause allergic reactions. Always inform healthcare providers about any known drug allergies before starting a new treatment.",
        "Medicines": "Treatment involves discontinuing the offending medication and, in some cases, administering antihistamines or corticosteroids to reduce symptoms. Severe reactions may require hospitalization.",
        "Treatment": "Treatment includes stopping the medication causing the reaction and managing symptoms with antihistamines or corticosteroids. If the reaction is severe, hospitalization may be required."
    },
    "Drug Rash": {
        "Symptoms": "Drug rashes are typically red, itchy, and may develop into hives or blisters. The rash can spread to different parts of the body and cause inflammation.",
        "Causes": "Drug rashes are caused by an allergic reaction or hypersensitivity to a specific drug, such as antibiotics, painkillers, or anticonvulsants.",
        "Protection": "Prevention involves avoiding drugs that trigger allergic reactions, informing healthcare providers of any known allergies, and following prescribed doses carefully.",
        "Medicines": "Medications such as antihistamines and corticosteroids are commonly prescribed to alleviate symptoms of a drug rash.",
        "Treatment": "Discontinuing the offending medication is the primary treatment. Symptomatic treatment with antihistamines or corticosteroids may be necessary for relief."
    },
    "Ductal Carcinoma In Situ (DCIS)": {
        "Symptoms": "DCIS usually does not cause noticeable symptoms. In some cases, it may be detected through routine breast screening as a small lump or abnormal mammogram.",
        "Causes": "The exact cause of DCIS is unknown, but it occurs when abnormal cells grow inside the milk ducts of the breast. It is considered a precursor to invasive breast cancer.",
        "Protection": "While DCIS cannot always be prevented, maintaining a healthy lifestyle, avoiding excessive alcohol consumption, and regular breast screening can help with early detection.",
        "Medicines": "Treatment for DCIS may include surgery, radiation therapy, and hormone therapy to reduce the risk of recurrence or progression to invasive cancer.",
        "Treatment": "Treatment options for DCIS include surgery to remove the abnormal cells, radiation therapy, and sometimes hormone therapy. A mastectomy may be recommended in some cases."
    },
    "Eczema (Atopic Dermatitis)": {
        "Symptoms": "Symptoms of eczema include dry, itchy skin, red rashes, and sometimes blistering. The skin may also become thickened and inflamed with long-term irritation.",
        "Causes": "Eczema is caused by a combination of genetic and environmental factors, including allergies, irritants, and immune system dysfunction.",
        "Protection": "Eczema can be managed by avoiding triggers, using mild skin care products, and keeping the skin moisturized.",
        "Medicines": "Topical corticosteroids, antihistamines, and immunosuppressants are often used to manage eczema flare-ups. Moisturizers are also recommended to maintain skin hydration.",
        "Treatment": "Treatment involves managing flare-ups with corticosteroids or other topical medications, avoiding triggers, and using moisturizers to prevent dryness."
    },
    "Eczema": {
        "Symptoms": "Dry, itchy, inflamed skin, rashes.",
        "Causes": "Genetic predisposition, environmental triggers.",
        "Protection": "Moisturize, avoid harsh soaps, manage stress.",
        "Medicines": "Emollients, topical corticosteroids, antihistamines."
    },
      "Epidermolysis Bullosa": {
        "Symptoms": "Epidermolysis bullosa causes fragile skin that blisters easily. Blisters may form after mild friction or trauma, and they can cause significant pain and scarring.",
        "Causes": "This condition is caused by mutations in the genes that provide instructions for producing proteins necessary for skin integrity. It is inherited in a genetic pattern, often autosomal recessive or dominant.",
        "Protection": "People with epidermolysis bullosa should avoid activities that cause friction or trauma to the skin and wear protective clothing to minimize blister formation.",
        "Medicines": "There is no cure for epidermolysis bullosa, but treatment focuses on wound care, pain management, and preventing infections. Bandages and topical medications may be used to protect the skin.",
        "Treatment": "Treatment involves managing blisters and wounds, preventing infection, and providing pain relief. In severe cases, skin grafts or other surgical interventions may be necessary."
    },
    "Erysipelas": {
        "Symptoms": "Erysipelas presents with red, swollen, and painful skin, often with a raised border. The affected area is warm to the touch and may be accompanied by fever and chills.",
        "Causes": "Erysipelas is a bacterial infection, usually caused by *Streptococcus* bacteria, which enters through a break in the skin. It often affects the face, legs, and arms.",
        "Protection": "Maintaining proper wound hygiene and treating any cuts or skin injuries promptly can help prevent erysipelas. People with weakened immune systems should take extra precautions.",
        "Medicines": "Erysipelas is typically treated with antibiotics such as penicillin or erythromycin. Severe cases may require intravenous antibiotics.",
        "Treatment": "The primary treatment for erysipelas is antibiotics. Mild cases can be treated orally, while severe cases may require hospitalization for intravenous antibiotics."
    },
    "Erysipeloid": {
        "Symptoms": "Erysipeloid causes a red, swollen, and painful area of skin, typically on the hands or fingers, which may develop into ulcers. It is often associated with a history of handling infected animals or animal products.",
        "Causes": "Erysipeloid is caused by the *Erysipelothrix rhusiopathiae* bacterium, commonly found in animals such as pigs, sheep, and fish.",
        "Protection": "Proper hygiene when handling animals or animal products and wearing protective gloves can help prevent erysipeloid.",
        "Medicines": "The condition is treated with antibiotics, such as penicillin, which is effective against the *Erysipelothrix rhusiopathiae* bacterium.",
        "Treatment": "Treatment typically includes antibiotics. Most people recover after a few days of treatment, although some may require longer courses for more severe infections."
    },
    "Exanthems and Drug Eruptions": {
        "Symptoms": "Exanthems are rashes or eruptions that can appear in response to an infection or drug reaction. Symptoms include fever, red or pink rash, and sometimes blistering or peeling skin.",
        "Causes": "Exanthems can be caused by viral infections, bacterial infections, or drug reactions. Common viral causes include measles, rubella, and chickenpox. Drug eruptions can occur due to an allergic reaction to medications.",
        "Protection": "Vaccination can help prevent some viral causes of exanthems. For drug eruptions, avoiding known allergens and following medication instructions carefully can help prevent reactions.",
        "Medicines": "Treatment for exanthems and drug eruptions depends on the underlying cause. Antiviral medications may be used for viral infections, while corticosteroids and antihistamines are often prescribed for drug eruptions.",
        "Treatment": "Treatment involves addressing the underlying cause, such as using antiviral drugs or discontinuing the offending medication. Symptomatic relief with antihistamines and corticosteroids may also be provided."
    },
     "Fat Necrosis": {
        "Causes": "Fat necrosis occurs due to trauma, surgery, or radiation therapy that damages fat cells. It is most common in breast tissue but can occur elsewhere in the body.",
        "Protection": "Avoiding trauma and seeking medical attention for any suspicious lumps or swelling can help in early detection and management.",
        "Medicines": "No specific medication is needed unless there is an infection, in which case antibiotics may be prescribed.",
        "Treatment": "Most cases resolve on their own. If a lump persists or causes discomfort, surgical removal may be an option."
    },
    "Folliculitis": {
        "Causes": "Folliculitis is caused by bacterial, fungal, or viral infections that inflame hair follicles. Common causes include *Staphylococcus aureus* and improper shaving techniques.",
        "Protection": "Good hygiene, using clean razors, and avoiding tight clothing can help prevent folliculitis.",
        "Medicines": "Topical or oral antibiotics, antifungal creams, and antiseptic washes may be used depending on the cause.",
        "Treatment": "Warm compresses, topical treatments, and, in severe cases, antibiotics or antifungal medications are used to manage folliculitis."
    },
    "Genital Herpes (HSV-2)": {
        "Causes": "Genital herpes is caused by the herpes simplex virus type 2 (HSV-2), primarily transmitted through sexual contact.",
        "Protection": "Using condoms, limiting sexual partners, and avoiding contact during outbreaks can reduce the risk.",
        "Medicines": "Antiviral medications such as acyclovir, valacyclovir, and famciclovir are commonly prescribed.",
        "Treatment": "There is no cure, but antiviral medications help reduce symptoms, frequency, and severity of outbreaks."
    },
    "Genital Scabies & Pubic Lice": {
        "Causes": "Genital scabies is caused by *Sarcoptes scabiei* mites, while pubic lice (*Pthirus pubis*) infest pubic hair and spread through close contact.",
        "Protection": "Avoiding close contact with infected individuals and maintaining good hygiene can help prevent infestations.",
        "Medicines": "Topical treatments such as permethrin, lindane, or ivermectin are used to eliminate parasites.",
        "Treatment": "Medicated lotions and shampoos effectively treat both conditions. Washing clothes and bedding at high temperatures is also necessary."
    },
    "Genital Disease": {
        "Causes": "Genital diseases include infections such as herpes, gonorrhea, and syphilis, usually spread through sexual contact.",
        "Protection": "Safe sexual practices, regular check-ups, and vaccinations (such as HPV vaccines) help reduce risks.",
        "Medicines": "Depending on the disease, treatments may include antibiotics, antivirals, or antifungal medications.",
        "Treatment": "Early diagnosis and appropriate treatment can prevent complications. Regular medical check-ups are advised."
    },
    "Gonorrhea": {
        "Causes": "Gonorrhea is a sexually transmitted bacterial infection caused by *Neisseria gonorrhoeae*.",
        "Protection": "Using condoms, regular STD screenings, and limiting sexual partners help prevent transmission.",
        "Medicines": "Ceftriaxone is the primary antibiotic used to treat gonorrhea, sometimes combined with azithromycin.",
        "Treatment": "Antibiotics are highly effective, but reinfection is possible if exposure occurs again."
    },
    "Hair Diseases": {
        "Causes": "Hair diseases such as alopecia, dandruff, and fungal infections arise due to genetic, hormonal, or microbial factors.",
        "Protection": "Maintaining scalp hygiene, using mild shampoos, and avoiding excessive heat styling can help prevent hair diseases.",
        "Medicines": "Medications may include antifungal shampoos, corticosteroids, or minoxidil for hair regrowth.",
        "Treatment": "Treatments vary depending on the condition but can involve medication, dietary changes, and sometimes surgical interventions like hair transplants."
    },
    "Harlequin Ichthyosis": {
        "Causes": "A rare genetic disorder caused by mutations in the *ABCA12* gene, leading to thick, scaly skin at birth.",
        "Protection": "There is no known prevention, but prenatal genetic counseling can help assess risks in families with a history of the disorder.",
        "Medicines": "Moisturizers, retinoids like acitretin, and antibiotics for secondary infections are commonly used.",
        "Treatment": "Intensive skincare with emollients, early intervention in neonatal care, and monitoring for infections are critical for managing the condition."
    },
    "Head Lice (Pediculosis Capitis)": {
        "Causes": "Head lice are tiny insects that infest the scalp and spread through direct head-to-head contact.",
        "Protection": "Avoid sharing combs, hats, and personal items. Regular hair checks help in early detection.",
        "Medicines": "Over-the-counter treatments include permethrin and pyrethrin. Prescription options include ivermectin and malathion.",
        "Treatment": "Medicated shampoos, thorough combing with a fine-toothed comb, and washing bedding and clothing at high temperatures are necessary."
    },
    "Herpes Simplex": {
        "Causes": "Caused by herpes simplex virus types 1 and 2 (HSV-1 and HSV-2). HSV-1 usually affects the mouth, while HSV-2 affects the genital area.",
        "Protection": "Avoiding direct contact with sores, using condoms, and maintaining a strong immune system can help reduce risk.",
        "Medicines": "Antiviral medications like acyclovir, valacyclovir, and famciclovir are commonly used.",
        "Treatment": "While there is no cure, antiviral therapy helps control outbreaks and reduces the risk of transmission."
    },  "Hidradenitis Suppurativa": {
        "Symptoms": "Painful lumps under the skin, abscesses, scarring, foul-smelling drainage.",
        "Causes": "Blocked hair follicles, hormonal imbalance, immune system overactivity.",
        "Protection": "Maintain hygiene, avoid tight clothing, manage weight and hormones.",
        "Medicines": "Antibiotics, corticosteroids, immunosuppressants.",
        "Treatment": "Topical treatments, laser therapy, surgery for severe cases."
    },
    "Hives (Urticaria)": {
        "Symptoms": "Red, raised, itchy welts on the skin, swelling, burning sensation.",
        "Causes": "Allergic reactions, stress, heat, infections, certain medications.",
        "Protection": "Avoid allergens, manage stress, wear loose clothing.",
        "Medicines": "Antihistamines (Cetirizine, Loratadine), corticosteroids for severe cases.",
        "Treatment": "Cool compresses, anti-itch creams, avoiding known triggers."
    },
    "Human Papillomavirus (HPV - Genital Warts)": {
        "Symptoms": "Flesh-colored or gray growths on genitals, itching, discomfort.",
        "Causes": "HPV infection, sexual transmission, weakened immune system.",
        "Protection": "HPV vaccine, safe sex practices, regular screenings.",
        "Medicines": "Topical treatments (Imiquimod, Podophyllin), antiviral drugs.",
        "Treatment": "Cryotherapy, laser treatment, surgical removal."
    },
    "Hyperpigmentation": {
        "Symptoms": "Dark patches on the skin, uneven skin tone, melasma, freckles.",
        "Causes": "Sun exposure, hormonal changes, skin inflammation, medications.",
        "Protection": "Use sunscreen daily, avoid harsh skincare products.",
        "Medicines": "Hydroquinone, retinoids, vitamin C serums.",
        "Treatment": "Chemical peels, laser therapy, microdermabrasion."
    },
    "Hypopigmentation": {
        "Symptoms": "Lighter patches of skin, loss of skin color, uneven pigmentation.",
        "Causes": "Vitiligo, skin damage, fungal infections, genetic factors.",
        "Protection": "Use sunscreen, avoid harsh chemicals on the skin.",
        "Medicines": "Topical corticosteroids, calcineurin inhibitors.",
        "Treatment": "Light therapy, skin grafting for severe cases, repigmentation treatments."
    },
    "Ichthyosis": {
        "Symptoms": "Dry, scaly, thickened skin, rough patches, itching.",
        "Causes": "Genetic mutations, environmental factors, underlying health conditions.",
        "Protection": "Moisturize regularly, avoid hot showers, stay hydrated.",
        "Medicines": "Emollients, retinoids, keratolytic agents.",
        "Treatment": "Hydrating treatments, specialized skincare, prescription creams."
    },
    "Impetigo": {
        "Symptoms": "Red sores, honey-colored crusts, blisters, itching, swelling.",
        "Causes": "Bacterial infection (Staphylococcus, Streptococcus), skin injury.",
        "Protection": "Maintain hygiene, avoid sharing personal items, clean wounds properly.",
        "Medicines": "Antibiotic ointments (Mupirocin), oral antibiotics for severe cases.",
        "Treatment": "Topical and oral antibiotics, good skin hygiene."
    },
    "Keratosis Pilaris": {
        "Symptoms": "Rough, bumpy skin, dry patches, redness, irritation.",
        "Causes": "Keratin buildup, genetic predisposition, dry skin.",
        "Protection": "Regular exfoliation, use of gentle skincare products.",
        "Medicines": "Moisturizers with urea, lactic acid, or salicylic acid.",
        "Treatment": "Exfoliation, hydrating creams, avoiding harsh soaps."
    },
    "Leishmaniasis": {
        "Symptoms": "Skin sores, ulcers, swelling, fever, weight loss.",
        "Causes": "Parasitic infection from sandfly bites, weakened immunity.",
        "Protection": "Use insect repellent, wear protective clothing, avoid sandfly-prone areas.",
        "Medicines": "Antiparasitic drugs (Miltefosine, Amphotericin B).",
        "Treatment": "Oral or IV antiparasitics, wound care, supportive therapy."
    },
    "Leprosy (Hansen's Disease)": {
        "Symptoms": "Skin lesions, numbness, muscle weakness, nerve damage.",
        "Causes": "Mycobacterium leprae infection, prolonged close contact with infected individuals.",
        "Protection": "Early detection, proper hygiene, avoiding prolonged exposure.",
        "Medicines": "Antibiotics (Dapsone, Rifampin, Clofazimine).",
        "Treatment": "Long-term antibiotic therapy, nerve damage management, reconstructive surgery if needed."
    }, "Lichen Sclerosus": {
        "Causes": "The exact cause is unknown, but it is thought to be an autoimmune disorder. Hormonal imbalances and genetic factors may also contribute.",
        "Protection": "While it cannot be prevented, avoiding skin irritation, using gentle skincare products, and maintaining hygiene can help manage symptoms.",
        "Medicines": "Topical corticosteroids such as clobetasol are commonly used. In severe cases, immune-modulating creams like tacrolimus may be prescribed.",
        "Treatment": "Treatment focuses on reducing inflammation and preventing scarring. Long-term monitoring and lifestyle adjustments are essential."
    },
    "Lichen Disease": {
        "Causes": "Lichen diseases, such as lichen planus, are caused by immune system dysfunction. They can also be triggered by infections, medications, or allergens.",
        "Protection": "Avoiding known triggers, reducing stress, and maintaining good skin hygiene can help prevent flare-ups.",
        "Medicines": "Corticosteroids, antihistamines, and immunosuppressants are commonly used to manage symptoms.",
        "Treatment": "Treatment includes topical and oral medications, phototherapy, and lifestyle modifications to reduce irritation."
    },
    "Light Diseases and Disorders of Pigmentation": {
        "Causes": "Caused by excessive or reduced melanin production due to genetic factors, sun exposure, or underlying medical conditions.",
        "Protection": "Using sunscreen, avoiding excessive sun exposure, and wearing protective clothing can help prevent pigmentation disorders.",
        "Medicines": "Treatment may include topical retinoids, hydroquinone, corticosteroids, and laser therapy.",
        "Treatment": "Managing pigmentation disorders involves sun protection, prescription creams, and, in some cases, cosmetic treatments like chemical peels or laser therapy."
    },
    "Lupus (Cutaneous Lupus Erythematosus)": {
        "Causes": "An autoimmune disease where the immune system attacks the skin, leading to rashes and lesions. It may be triggered by sunlight, infections, or stress.",
        "Protection": "Avoiding UV exposure, using sunscreen, and managing stress can help reduce flare-ups.",
        "Medicines": "Treatment includes corticosteroids, hydroxychloroquine, and immunosuppressants to manage symptoms.",
        "Treatment": "Managing lupus involves lifestyle changes, medications, and regular check-ups to monitor the disease's progression."
    },
    "Lupus and Other Connective Tissue Diseases": {
        "Causes": "Caused by autoimmune reactions leading to chronic inflammation that affects connective tissues in the skin, joints, and organs.",
        "Protection": "Preventative measures include stress management, a balanced diet, and avoiding known triggers such as sun exposure.",
        "Medicines": "Corticosteroids, immunosuppressants, and antimalarial drugs like hydroxychloroquine are commonly used.",
        "Treatment": "Treatment focuses on managing inflammation, preventing complications, and improving the patient's quality of life through lifestyle changes and medications."
    },
    "Malignant Lesions": {
        "Causes": "Malignant lesions develop due to uncontrolled cell growth, often triggered by genetic mutations, UV exposure, or carcinogens.",
        "Protection": "Regular skin screenings, avoiding prolonged sun exposure, and using sunscreen can help prevent skin cancer.",
        "Medicines": "Depending on the type of cancer, chemotherapy, targeted therapy, or immunotherapy may be used.",
        "Treatment": "Treatment options include surgical removal, radiation therapy, and systemic treatments like chemotherapy or immunotherapy."
    },
    "Measles": {
        "Causes": "Caused by the measles virus (*Morbillivirus*), which spreads through respiratory droplets.",
        "Protection": "Vaccination with the MMR (measles, mumps, and rubella) vaccine is the best prevention.",
        "Medicines": "No specific antiviral treatment exists, but supportive care includes fever reducers and vitamin A supplements.",
        "Treatment": "Managing measles involves hydration, fever management, and monitoring for complications like pneumonia or encephalitis."
    },
    "Melanoma": {
        "Causes": "Caused by uncontrolled growth of melanocytes due to UV exposure, genetic mutations, or a family history of skin cancer.",
        "Protection": "Using sunscreen, avoiding tanning beds, and conducting regular skin checks can reduce the risk.",
        "Medicines": "Treatment may involve immunotherapy, targeted therapy, or chemotherapy, depending on the stage.",
        "Treatment": "Early-stage melanoma is treated with surgical excision, while advanced cases may require additional systemic therapies."
    },
    "Melasma": {
        "Causes": "Melasma is caused by hormonal changes, sun exposure, and genetic predisposition. It is common during pregnancy and in individuals using hormonal contraceptives.",
        "Protection": "Using broad-spectrum sunscreen daily and avoiding direct sun exposure can help prevent melasma flare-ups.",
        "Medicines": "Topical treatments include hydroquinone, tretinoin, and azelaic acid. Chemical peels and laser therapy may also be used.",
        "Treatment": "Treatment focuses on lightening hyperpigmentation and preventing further darkening through sun protection and prescribed creams."
    },
    "Miliaria (Heat Rash)": {
        "Causes": "Caused by blocked sweat ducts, leading to trapped sweat under the skin. It occurs in hot, humid conditions.",
        "Protection": "Wearing loose, breathable clothing, staying cool, and keeping the skin dry can help prevent miliaria.",
        "Medicines": "Calamine lotion, antihistamines, and mild corticosteroids can help relieve itching and irritation.",
        "Treatment": "Managing heat rash involves keeping the affected area dry, using soothing treatments, and avoiding excessive sweating."
    }, "Moles": {
        "Causes": "Moles are caused by the clustering of melanocytes, the pigment-producing cells in the skin. Genetic factors, hormonal changes, and sun exposure play key roles in their formation. Some moles develop due to excessive sun exposure, while others appear naturally with age.",
        "Protection": "To protect against moles, limit sun exposure, wear sunscreen, and avoid tanning beds. Regular skin checks help in detecting abnormal moles early.",
        "Medicines": "No specific medication is needed for benign moles. However, if a mole shows abnormal changes, topical treatments or removal procedures may be recommended.",
        "Treatment": "Treatment includes laser removal, surgical excision, and cryotherapy. Dermatologists may remove suspicious moles to prevent potential malignancy."
    },
    "Molluscum": {
        "Causes": "Molluscum is caused by the Molluscum contagiosum virus, a poxvirus that spreads through direct contact, contaminated objects, and sexual contact.",
        "Protection": "Avoid skin-to-skin contact with infected individuals. Maintain good hygiene and avoid sharing personal items like towels.",
        "Medicines": "Topical treatments such as imiquimod and retinoids can help. Cryotherapy and curettage are also options.",
        "Treatment": "Treatment includes physical removal methods like cryotherapy, laser therapy, and topical antiviral creams. Most cases resolve on their own within 6-12 months."
    },
    "Molluscum Contagiosum": {
        "Causes": "This condition results from infection with the Molluscum contagiosum virus. It spreads through skin contact, shared items, and sexual transmission.",
        "Protection": "Preventive measures include avoiding direct contact with infected skin, maintaining personal hygiene, and not sharing personal items.",
        "Medicines": "Podophyllotoxin cream, imiquimod, and potassium hydroxide solutions are commonly used.",
        "Treatment": "Cryotherapy, laser therapy, or curettage can be used for removal. In many cases, the condition resolves without treatment."
    },
    "Morphea": {
        "Causes": "Morphea is a localized form of scleroderma, believed to result from autoimmune reactions, genetic factors, and environmental triggers.",
        "Protection": "Avoid skin trauma and excessive sun exposure. Maintaining skin hydration can also be beneficial.",
        "Medicines": "Topical corticosteroids, calcineurin inhibitors, and systemic immunosuppressants may be used.",
        "Treatment": "Treatment includes phototherapy, systemic immunosuppressants, and physical therapy to maintain skin flexibility."
    },
    "Nail Disease": {
        "Causes": "Fungal infections, psoriasis, trauma, and systemic diseases like diabetes can contribute to nail diseases.",
        "Protection": "Maintain proper nail hygiene, avoid prolonged moisture exposure, and use antifungal powders if prone to infections.",
        "Medicines": "Oral antifungals (terbinafine, itraconazole), topical antifungals, and corticosteroids for inflammatory conditions.",
        "Treatment": "Treatment includes antifungal medications, nail debridement, and in severe cases, surgical removal of the affected nail."
    },
    "Pemphigus": {
        "Causes": "Pemphigus is an autoimmune disease where antibodies attack skin cells, causing blister formation. Genetic predisposition and environmental factors contribute to its onset.",
        "Protection": "There is no definite way to prevent pemphigus, but avoiding triggers like certain medications and infections can help.",
        "Medicines": "Corticosteroids, immunosuppressants (azathioprine, mycophenolate mofetil), and biologics like rituximab are used.",
        "Treatment": "Treatment involves systemic corticosteroids, immunosuppressive therapy, and wound care to prevent secondary infections."
    },
    "Perianal Cellulitis": {
        "Causes": "Caused by group A Streptococcus bacteria, often spreading from the throat or skin infections.",
        "Protection": "Proper hygiene, avoiding skin injuries, and prompt treatment of streptococcal infections can help prevent perianal cellulitis.",
        "Medicines": "Oral antibiotics such as penicillin or amoxicillin are the primary treatments.",
        "Treatment": "Treatment includes antibiotics, proper hygiene, and warm compresses to ease discomfort."
    },
    "Pseudomonas-Folliculitis-0018": {
        "Causes": "Pseudomonas folliculitis is caused by infection with Pseudomonas aeruginosa bacteria, often contracted from contaminated water sources like hot tubs and pools.",
        "Protection": "Avoid poorly maintained hot tubs and pools. Shower immediately after swimming and maintain good personal hygiene.",
        "Medicines": "Topical antiseptics, oral ciprofloxacin in severe cases, and anti-itch lotions.",
        "Treatment": "Most cases resolve without treatment. For persistent cases, antibiotics and topical antiseptics are used."
    },
    "Psoriasis": {
        "Causes": "Psoriasis is an autoimmune condition triggered by genetic factors, stress, infections, and certain medications.",
        "Protection": "Avoid known triggers, maintain skin hydration, and follow a healthy lifestyle to minimize flare-ups.",
        "Medicines": "Topical corticosteroids, vitamin D analogs, systemic immunosuppressants, and biologic therapies.",
        "Treatment": "Treatment includes topical therapies, phototherapy, systemic medications, and biologic agents to manage symptoms."
    },
    "Psoriasis-Guttate": {
        "Causes": "Guttate psoriasis is often triggered by streptococcal infections, stress, and genetic predisposition.",
        "Protection": "Prevent infections, avoid stress, and maintain good skin hydration.",
        "Medicines": "Topical corticosteroids, vitamin D analogs, and systemic immunosuppressants are commonly used.",
        "Treatment": "Phototherapy, systemic medications, and treating underlying infections help manage guttate psoriasis."
    },
    "Rosacea": {
        "Symptoms": "Facial redness, visible blood vessels, swelling, acne-like breakouts, eye irritation.",
        "Causes": "Genetic factors, immune system overactivity, environmental triggers (spicy food, alcohol, sun).",
        "Protection": "Use gentle skincare, avoid triggers, apply sunscreen regularly.",
        "Medicines": "Topical creams (Metronidazole, Azelaic Acid), oral antibiotics (Doxycycline).",
        "Treatment": "Laser therapy, IPL (intense pulsed light), lifestyle management."
    },
    "STDs (Sexually Transmitted Diseases)": {
        "Symptoms": "Varies by disease; common signs include genital sores, itching, discharge, painful urination.",
        "Causes": "Bacterial, viral, or parasitic infections transmitted through sexual contact.",
        "Protection": "Use protection (condoms), get vaccinated (HPV, Hepatitis B), regular STD screenings.",
        "Medicines": "Antibiotics (for bacterial STDs), antivirals (for viral STDs).",
        "Treatment": "Medication-based treatment depending on the type (penicillin for syphilis, antivirals for herpes)."
    },
    "Scabies (Scalp Scabies)": {
        "Symptoms": "Intense itching, red bumps, burrow lines on scalp and body.",
        "Causes": "Sarcoptes scabiei mite infestation.",
        "Protection": "Avoid direct skin contact, wash bedding and clothes in hot water.",
        "Medicines": "Permethrin cream, Ivermectin (oral).",
        "Treatment": "Topical medications, thorough cleaning of personal items."
    },
    "Scalp Fungal Diseases": {
        "Symptoms": "Itchy scalp, flaking, hair loss, redness, inflammation.",
        "Causes": "Fungal infections (Tinea capitis, Malassezia).",
        "Protection": "Maintain scalp hygiene, avoid sharing combs or hats.",
        "Medicines": "Antifungal shampoos (Ketoconazole), oral antifungal medications.",
        "Treatment": "Oral and topical antifungals, medicated shampoos."
    },
    "Scleroderma": {
        "Symptoms": "Hardened, tight skin, joint pain, Raynaud's phenomenon, internal organ damage in severe cases.",
        "Causes": "Autoimmune disease causing excess collagen production.",
        "Protection": "Avoid cold exposure, moisturize skin, manage stress.",
        "Medicines": "Immunosuppressants, corticosteroids.",
        "Treatment": "Physical therapy, medications to manage symptoms, in severe cases, organ-specific treatments."
    },
    "Sebaceous Cyst": {
        "Symptoms": "Painless lump under the skin, inflammation if infected, cheesy discharge.",
        "Causes": "Blocked sebaceous glands, genetic factors.",
        "Protection": "Maintain skin hygiene, avoid squeezing cysts.",
        "Medicines": "Antibiotics for infected cysts.",
        "Treatment": "Surgical removal if necessary, drainage procedures."
    },
    "Seborrheic Dermatitis": {
        "Symptoms": "Flaky, itchy skin, dandruff, redness, greasy patches, scaling.",
        "Causes": "Overgrowth of Malassezia yeast, genetic predisposition, stress.",
        "Protection": "Use medicated shampoos, maintain scalp hygiene.",
        "Medicines": "Antifungal creams, corticosteroids, salicylic acid-based shampoos.",
        "Treatment": "Topical antifungals, medicated shampoos, light therapy."
    },
    "Shingles (Herpes Zoster)": {
        "Symptoms": "Painful rash, blisters, burning sensation, fever, nerve pain.",
        "Causes": "Reactivation of the varicella-zoster virus (chickenpox virus).",
        "Protection": "Get vaccinated (Shingrix), boost immune health.",
        "Medicines": "Antivirals (Acyclovir, Valacyclovir), pain relievers.",
        "Treatment": "Antiviral therapy, pain management, skin soothing remedies."
    },
    "Staphylococcal Folliculitis": {
        "Symptoms": "Red, pus-filled bumps, itching, pain, inflammation.",
        "Causes": "Staphylococcus bacteria infecting hair follicles.",
        "Protection": "Maintain hygiene, avoid sharing personal care items.",
        "Medicines": "Topical or oral antibiotics (Mupirocin, Clindamycin).",
        "Treatment": "Antibiotic treatment, proper hygiene, warm compresses."
    },
    "Sun Damage": {
        "Symptoms": "Wrinkles, sunburn, hyperpigmentation, premature aging, increased skin cancer risk.",
        "Causes": "UV radiation exposure, prolonged sun exposure without protection.",
        "Protection": "Wear sunscreen, use protective clothing, avoid peak sun hours.",
        "Medicines": "Topical antioxidants (Vitamin C, retinoids), anti-inflammatory creams.",
        "Treatment": "Laser therapy, chemical peels, prescription skin treatments."
    },
    "Systemic Disease": {
        "Causes": "Systemic diseases affect multiple organs and body systems. Common causes include autoimmune disorders, infections, and genetic conditions.",
        "Protection": "Maintaining a healthy lifestyle, managing stress, and regular medical check-ups can help in early detection and prevention.",
        "Medicines": "Treatment depends on the specific systemic disease and may include immunosuppressants, steroids, or targeted therapies.",
        "Treatment": "Management often requires a combination of medications, lifestyle modifications, and regular monitoring to prevent complications."
    },
    "Tinea Ringworm Candidiasis and Fungal Infections": {
        "Causes": "These infections are caused by fungi such as *Trichophyton*, *Microsporum*, and *Candida*, which thrive in warm, moist environments.",
        "Protection": "Keeping the skin dry, avoiding shared personal items, and maintaining good hygiene can help prevent infections.",
        "Medicines": "Antifungal creams (clotrimazole, terbinafine), oral antifungals (fluconazole, itraconazole), and medicated shampoos are used for treatment.",
        "Treatment": "Mild cases can be treated with topical antifungals, while severe infections may require oral medications."
    },
    "Tinea Corporis (Body Ringworm)": {
        "Causes": "Caused by dermatophyte fungi, primarily *Trichophyton rubrum* and *Microsporum canis*.",
        "Protection": "Avoiding direct skin contact with infected individuals or animals and keeping the skin dry can reduce the risk.",
        "Medicines": "Topical antifungals like terbinafine and clotrimazole are first-line treatments. Oral antifungals may be needed for widespread infections.",
        "Treatment": "Treatment includes antifungal medications, good hygiene, and avoiding irritants that can worsen the condition."
    },
    "Traction Alopecia": {
        "Causes": "Caused by repeated tension on the hair follicles due to tight hairstyles, braiding, and excessive use of hair extensions.",
        "Protection": "Avoiding tight hairstyles, using gentle hair care techniques, and allowing the scalp to rest can prevent hair loss.",
        "Medicines": "Minoxidil may be used to promote regrowth. In severe cases, corticosteroids or platelet-rich plasma therapy might be recommended.",
        "Treatment": "Early intervention by changing hairstyles and using hair growth treatments can help reverse hair loss. Advanced cases may require hair transplants."
    },
    "Urticaria (Hives)": {
        "Causes": "Triggered by allergens, stress, infections, or underlying medical conditions such as autoimmune disorders.",
        "Protection": "Avoiding known triggers and managing stress can help prevent outbreaks.",
        "Medicines": "Antihistamines like cetirizine, diphenhydramine, and corticosteroids are commonly used.",
        "Treatment": "Treatment focuses on relieving itching and inflammation with antihistamines, avoiding triggers, and in severe cases, using immunosuppressive therapy."
    },
    "Vaginal Melanoma": {
        "Causes": "A rare form of melanoma occurring in the vaginal region, often linked to genetic mutations and prolonged UV exposure.",
        "Protection": "Regular gynecological check-ups and early detection improve outcomes, though no specific prevention exists.",
        "Medicines": "Immunotherapy, targeted therapy, and chemotherapy are commonly used for treatment.",
        "Treatment": "Surgical removal is the primary treatment, followed by radiation or immunotherapy for advanced cases."
    },
    "Vascular Tumors": {
        "Causes": "Caused by abnormal blood vessel growth, these tumors can be benign (hemangiomas) or malignant (angiosarcomas).",
        "Protection": "There is no known prevention, but early detection through regular medical exams can help manage progression.",
        "Medicines": "Treatment may include corticosteroids, beta-blockers, or targeted therapies depending on the type of tumor.",
        "Treatment": "Management involves observation for benign tumors, while malignant cases may require surgery, radiation, or chemotherapy."
    },
    "Vasculitis": {
        "Causes": "Inflammation of blood vessels due to autoimmune disorders, infections, or drug reactions.",
        "Protection": "Managing underlying conditions and avoiding known triggers can help prevent vasculitis flare-ups.",
        "Medicines": "Corticosteroids, immunosuppressants, and biologic drugs like rituximab are used for treatment.",
        "Treatment": "Treatment depends on severity and may include medication, lifestyle modifications, and monitoring for complications."
    },
    "Vitiligo": {
        "Causes": "An autoimmune disorder that destroys melanocytes, leading to loss of skin pigmentation.",
        "Protection": "Avoiding excessive sun exposure and using sunscreen can help protect depigmented areas.",
        "Medicines": "Treatment includes topical corticosteroids, calcineurin inhibitors, and phototherapy.",
        "Treatment": "Treatment aims to slow progression and restore pigmentation using medical therapies, laser treatments, or skin grafting."
    },
    "Warts, Molluscum, and Other Viral Infections": {
        "Causes": "Caused by viruses such as *Human Papillomavirus (HPV)* and *Molluscum contagiosum virus*.",
        "Protection": "Avoiding direct contact with infected skin, practicing good hygiene, and using protective measures in public places can help prevent infections.",
        "Medicines": "Salicylic acid, cryotherapy, and antiviral treatments may be used for warts and molluscum.",
        "Treatment": "Treatment includes topical treatments, laser therapy, or cryotherapy to remove lesions. Some cases resolve on their own over time."
    },
    "Xeroderma Pigmentosum": {
        "Symptoms": "Extreme sensitivity to sunlight, freckling, dry skin, eye irritation, increased skin cancer risk.",
        "Causes": "Genetic disorder affecting DNA repair mechanisms.",
        "Protection": "Avoid sunlight, use UV-protective clothing and glasses.",
        "Medicines": "No cure; symptom management with antioxidants and retinoids.",
        "Treatment": "Strict sun protection, frequent skin checks, surgical removal of precancerous growths."
    },
    "Yeast Infections": {
        "Symptoms": "Itching, redness, white discharge (in vaginal yeast infections), rash in skin folds.",
        "Causes": "Overgrowth of Candida yeast due to moisture, weakened immune system, antibiotics.",
        "Protection": "Keep skin dry, wear breathable fabrics, avoid excessive antibiotic use.",
        "Medicines": "Antifungal creams (Clotrimazole, Miconazole), oral antifungals (Fluconazole).",
        "Treatment": "Topical and oral antifungal medications, proper hygiene."
    },
    "Acne Keloidalis (Acne Keloidalis Nuchae)": {
        "Symptoms": "Painful, itchy bumps on the back of the scalp, keloid-like scars, hair loss.",
        "Causes": "Chronic inflammation of hair follicles, often linked to tight hairstyles and shaving.",
        "Protection": "Avoid tight hats, reduce scalp irritation, maintain scalp hygiene.",
        "Medicines": "Topical corticosteroids, antibiotics, retinoids.",
        "Treatment": "Laser therapy, corticosteroid injections, surgical removal for severe cases."
    },
    "Actinic Keratosis": {
        "Symptoms": "Rough, scaly patches on sun-exposed skin, sometimes itchy or tender.",
        "Causes": "Prolonged sun exposure causing precancerous skin changes.",
        "Protection": "Use sunscreen, wear protective clothing, avoid excessive sun exposure.",
        "Medicines": "Topical treatments (5-fluorouracil, Imiquimod), cryotherapy.",
        "Treatment": "Cryotherapy, laser therapy, photodynamic therapy to remove lesions."
    },
    "Allergic Contact Dermatitis": {
        "Symptoms": "Red, itchy rash, swelling, blistering, dry or cracked skin after contact with allergens.",
        "Causes": "Allergic reaction to substances like nickel, fragrances, latex, poison ivy.",
        "Protection": "Avoid known allergens, use barrier creams, wear gloves if needed.",
        "Medicines": "Antihistamines, corticosteroid creams, moisturizers.",
        "Treatment": "Topical steroids, cold compresses, antihistamines for severe reactions."
    },
    "Alopecia Areata": {
        "Symptoms": "Sudden hair loss in round patches on scalp or body, nail changes in some cases.",
        "Causes": "Autoimmune condition where the immune system attacks hair follicles.",
        "Protection": "Reduce stress, maintain scalp care, manage immune health.",
        "Medicines": "Corticosteroids, Minoxidil, JAK inhibitors.",
        "Treatment": "Topical and injectable steroids, immunotherapy, PRP (platelet-rich plasma) therapy."
    },
    "Atypical Nevi (Atypical Moles)": {
        "Symptoms": "Irregularly shaped moles, varying colors, larger than common moles, sometimes itchy.",
        "Causes": "Genetic predisposition, sun exposure, increased melanoma risk.",
        "Protection": "Regular skin checks, avoid sun exposure, wear sunscreen.",
        "Medicines": "No medication needed unless atypical mole changes.",
        "Treatment": "Surgical removal if changes are suspicious, biopsy for potential melanoma."
    },
    "Basal Cell Carcinoma": {
        "Symptoms": "Pearly or waxy bump, non-healing sore, red patch, sometimes bleeding.",
        "Causes": "UV exposure, fair skin, genetic predisposition.",
        "Protection": "Wear sunscreen, avoid tanning beds, regular skin screenings.",
        "Medicines": "Topical chemotherapy (5-fluorouracil), Imiquimod.",
        "Treatment": "Surgical removal, Mohs surgery, cryotherapy, radiation therapy."
    },
    "Dermatofibroma": {
        "Symptoms": "Firm, small, raised bump on skin, sometimes itchy or tender.",
        "Causes": "Reaction to minor trauma, insect bites, or unknown triggers.",
        "Protection": "Avoid skin trauma, proper wound care.",
        "Medicines": "Usually not needed; corticosteroids for inflammation.",
        "Treatment": "Surgical excision if symptomatic or for cosmetic reasons."
    },
    "Dissecting Cellulitis": {
        "Symptoms": "Painful scalp nodules, pus-filled abscesses, scarring, hair loss.",
        "Causes": "Chronic follicular inflammation, possible bacterial involvement.",
        "Protection": "Maintain scalp hygiene, avoid excessive irritation.",
        "Medicines": "Antibiotics, corticosteroids, isotretinoin.",
        "Treatment": "Antibiotic therapy, steroid injections, laser therapy, surgery for severe cases."
    },"Halo Nevus": {
        "Causes": "A benign mole surrounded by a depigmented ring, caused by an autoimmune reaction targeting melanocytes.",
        "Protection": "Sun protection is essential to prevent skin damage in the depigmented area.",
        "Medicines": "No specific treatment is required, but corticosteroids may be used if inflammation occurs.",
        "Treatment": "Typically, no treatment is needed as it resolves on its own. In rare cases, surgical removal may be considered if changes occur."
    },
    "Herpes Disease": {
        "Causes": "Caused by the Herpes Simplex Virus (HSV-1 for oral herpes, HSV-2 for genital herpes).",
        "Protection": "Avoid direct contact with infected individuals, use protective measures, and maintain a strong immune system.",
        "Medicines": "Antiviral medications like acyclovir, valacyclovir, and famciclovir help control outbreaks.",
        "Treatment": "Treatment includes antiviral therapy, pain management, and lifestyle modifications to reduce flare-ups."
    },
    "Insect Bites": {
        "Causes": "Caused by insects such as mosquitoes, fleas, bedbugs, and ticks injecting saliva or venom into the skin.",
        "Protection": "Using insect repellents, wearing protective clothing, and avoiding infested areas can prevent bites.",
        "Medicines": "Antihistamines, corticosteroid creams, and pain relievers can help manage symptoms.",
        "Treatment": "Cleaning the bite, applying cold compresses, and using topical medications can reduce swelling and itching."
    },
    "Lentigo (Adults)": {
        "Causes": "Age-related pigmented spots caused by prolonged sun exposure and melanin accumulation.",
        "Protection": "Wearing sunscreen, avoiding excessive UV exposure, and using protective clothing can help prevent new lesions.",
        "Medicines": "Topical retinoids, hydroquinone, and laser therapy can be used for cosmetic treatment.",
        "Treatment": "Treatment includes cryotherapy, chemical peels, and laser therapy for lightening or removal."
    },
    "Lichen Planus": {
        "Causes": "An autoimmune inflammatory condition affecting the skin, mucous membranes, nails, and scalp.",
        "Protection": "Avoiding stress, certain medications, and allergens may help reduce flare-ups.",
        "Medicines": "Corticosteroids, antihistamines, and immunosuppressants are commonly used.",
        "Treatment": "Topical and systemic treatments aim to reduce inflammation and itching. Phototherapy may be used in severe cases."
    },
    "Malignant Melanoma": {
        "Causes": "A dangerous skin cancer caused by uncontrolled growth of melanocytes, often triggered by UV exposure and genetic factors.",
        "Protection": "Regular skin checks, sun protection, and early detection are crucial for prevention.",
        "Medicines": "Treatment includes immunotherapy, targeted therapy, and chemotherapy in advanced stages.",
        "Treatment": "Surgical excision is the primary treatment. In advanced cases, radiation or systemic therapy may be required."
    },
    "Milia": {
        "Causes": "Small cysts caused by trapped keratin under the skin, often seen in newborns but also in adults.",
        "Protection": "Regular exfoliation and avoiding heavy skincare products can help prevent milia.",
        "Medicines": "Topical retinoids and chemical peels may help reduce milia.",
        "Treatment": "Milia often resolve on their own, but dermatological extraction may be needed for persistent cases."
    },
    "Nevus": {
        "Causes": "A benign mole or birthmark caused by a cluster of melanocytes in the skin.",
        "Protection": "Monitoring changes in moles and using sun protection can prevent malignant transformation.",
        "Medicines": "No medication is required unless a nevus shows signs of malignancy.",
        "Treatment": "Surgical removal may be recommended if the nevus changes in size, shape, or color."
    },
    "Phototoxic Reactions": {
        "Causes": "Skin damage caused by sunlight exposure after taking certain medications or applying chemicals.",
        "Protection": "Avoiding sun exposure, using sunscreen, and wearing protective clothing can prevent reactions.",
        "Medicines": "Anti-inflammatory creams, antihistamines, and corticosteroids may be used for relief.",
        "Treatment": "Managing phototoxicity involves discontinuing the triggering substance and soothing affected skin."
    },
    "Pigmented Benign Keratosis": {
        "Causes": "Non-cancerous skin growths caused by aging and sun exposure, commonly known as seborrheic keratosis.",
        "Protection": "Using sunscreen and avoiding excessive UV exposure can help reduce the risk.",
        "Medicines": "No medications are needed unless removal is requested for cosmetic reasons.",
        "Treatment": "Treatment includes cryotherapy, laser removal, or electrocautery for cosmetic concerns."
    }, "Pityriasis Rosea": {
        "Symptoms": "Herald patch followed by a widespread rash, mild itching, fatigue.",
        "Causes": "Unknown, possibly viral (HHV-6, HHV-7).",
        "Protection": "Maintain good hygiene, avoid skin irritants.",
        "Medicines": "Antihistamines, corticosteroids for itching.",
        "Treatment": "Self-limiting, moisturizers, light therapy for severe cases."
    },
    "Porphyrias": {
        "Symptoms": "Blistering skin lesions, sensitivity to sunlight, dark urine, neurological issues.",
        "Causes": "Genetic enzyme deficiency affecting heme production.",
        "Protection": "Avoid sun exposure, alcohol, and triggering medications.",
        "Medicines": "Hemin injections, beta-carotene supplements.",
        "Treatment": "Avoid triggers, IV glucose, hemin therapy."
    },
    "Psoriasis (Digits)": {
        "Symptoms": "Thickened, scaly patches on fingers/toes, nail pitting, joint pain.",
        "Causes": "Autoimmune reaction causing rapid skin cell turnover.",
        "Protection": "Moisturize, avoid triggers like stress, alcohol, and smoking.",
        "Medicines": "Topical steroids, Vitamin D analogs, biologics.",
        "Treatment": "Phototherapy, systemic immunosuppressants."
    },
    "Rhus Dermatitis (Poison Ivy Rash)": {
        "Symptoms": "Red, itchy, blistering rash after contact with poison ivy/oak.",
        "Causes": "Allergic reaction to urushiol oil from plants.",
        "Protection": "Wear protective clothing, wash skin after exposure.",
        "Medicines": "Antihistamines, corticosteroid creams, calamine lotion.",
        "Treatment": "Cool compresses, steroid shots for severe cases."
    },
    "Scabies": {
        "Symptoms": "Intense itching, burrows in skin, red rash, worsens at night.",
        "Causes": "Infestation by the Sarcoptes scabiei mite.",
        "Protection": "Avoid direct skin contact with infected individuals, wash bedding.",
        "Medicines": "Permethrin cream, Ivermectin for severe cases.",
        "Treatment": "Topical scabicides, thorough cleaning of personal items."
    },
    "Seborrheic Keratosis": {
        "Symptoms": "Waxy, wart-like, brown or black growths on skin, usually painless.",
        "Causes": "Aging, genetic factors, sun exposure.",
        "Protection": "General skin care, avoid excessive sun exposure.",
        "Medicines": "No specific medicine; cryotherapy if removal needed.",
        "Treatment": "Cryotherapy, laser therapy, surgical removal for cosmetic reasons."
    },
    "Seborrheic Dermatitis": {
        "Symptoms": "Flaky, scaly patches, greasy skin, redness, itching (common on scalp, face, ears).",
        "Causes": "Overgrowth of Malassezia yeast, genetic factors, stress.",
        "Protection": "Use gentle shampoos, maintain scalp hygiene.",
        "Medicines": "Antifungal shampoos (Ketoconazole), corticosteroids, sulfur-based treatments.",
        "Treatment": "Medicated shampoos, topical antifungals, phototherapy."
    },
    "Syphilis": {
        "Symptoms": "Painless sores, rashes on palms/soles, fever, swollen lymph nodes.",
        "Causes": "Bacterial infection (Treponema pallidum) transmitted sexually.",
        "Protection": "Safe sex practices, routine STI screening.",
        "Medicines": "Penicillin G (primary treatment).",
        "Treatment": "Single-dose penicillin for early syphilis, multiple doses for late stages."
    },
    "Squamous Cell Carcinoma": {
        "Symptoms": "Scaly red patches, open sores, thickened wart-like skin, may bleed.",
        "Causes": "Chronic sun exposure, HPV, weakened immune system.",
        "Protection": "Wear sunscreen, avoid tanning beds, regular skin checks.",
        "Medicines": "Topical chemotherapy (5-fluorouracil, Imiquimod).",
        "Treatment": "Surgical excision, Mohs surgery, radiation therapy for advanced cases."
    },
    "Trichotillomania": {
        "Symptoms": "Compulsive hair pulling, patchy hair loss, anxiety relief from pulling.",
        "Causes": "Psychological disorder, often linked to OCD and anxiety.",
        "Protection": "Behavioral therapy, stress management.",
        "Medicines": "SSRIs, N-acetylcysteine (NAC) for impulse control.",
        "Treatment": "Cognitive behavioral therapy (CBT), habit-reversal training."
    },
    "Vascular Lesion": {
        "Symptoms": "Red, purple, or blue skin discolorations, swelling, visible blood vessels.",
        "Causes": "Congenital conditions, trauma, blood vessel malformations.",
        "Protection": "Avoid trauma, maintain good skin care.",
        "Medicines": "Topical treatments for inflammation.",
        "Treatment": "Laser therapy, sclerotherapy, surgical removal for severe cases."
    }
}

# Function to preprocess the image
def preprocess_image(image):
    img = image.resize((224,224))  # Resize to the input size expected by the model
    img = np.array(img)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Function to make predictions
def predict(image):
    img = preprocess_image(image)
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions, axis=1)
    return class_labels[predicted_class[0]]

# Function to generate a PDF report
def generate_pdf(disease, info):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Skin Disease Classification Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Diagnosis: {disease}", ln=True)
    pdf.cell(200, 10, f"Symptoms: {info['Symptoms']}", ln=True)
    pdf.cell(200, 10, f"Causes: {info['Causes']}", ln=True)
    pdf.cell(200, 10, f"Protection: {info['Protection']}", ln=True)
    pdf.cell(200, 10, f"Recommended Medicines: {info['Medicines']}", ln=True)
    pdf.cell(200, 10, f"Treatment: {info['Treatment']}", ln=True)
    pdf.output("diagnosis_report.pdf")

# Function to find nearby clinics
def find_nearby_hospitals():
    webbrowser.open("https://www.google.com/maps/search/dermatology+clinic+near+me")

# Streamlit app
st.set_page_config(page_title="Caresyn", page_icon="🩺", layout="centered")
st.title("🩺 Caresyn")


uploaded_file = st.file_uploader("📤 Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    label = predict(image)
    
    st.image(image, caption='Uploaded Image', use_container_width=True)
    st.markdown(f"<h2 style='color: #FF4B4B; text-align: center;'>Diagnosis: {label}</h2>", unsafe_allow_html=True)
    
    if label in disease_info:
        info = disease_info[label]
        st.markdown(f"""
            <div style='background-color: #222831; padding: 20px; border-radius: 10px; text-align: center; color: white;'>
            <h3 style='color: #FFA500;'>📝 Disease Details</h3>
            <p><strong>🩸 Symptoms:</strong> {info['Symptoms']}</p>
            <p><strong>⚠️ Causes:</strong> {info['Causes']}</p>
            <p><strong>🛡 Protection:</strong> {info['Protection']}</p>
            <p><strong>💊 Recommended Medicines:</strong> {info['Medicines']}</p>
            <p><strong>⚠️ Treatment:</strong> {info['Treatment']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        generate_pdf(label, info)

        
        
        with open("diagnosis_report.pdf", "rb") as file:
            st.download_button("📥 Download Report", file, file_name="diagnosis_report.pdf", mime="application/pdf")
    
    if st.button("🔍 Find Nearby Clinics & Hospitals"):
        find_nearby_hospitals()

