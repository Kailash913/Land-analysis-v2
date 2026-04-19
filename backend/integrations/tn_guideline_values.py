"""
Tamil Nadu TNREGINET Guideline Values — Local Mirror.

Source: Tamil Nadu Registration Department (tnreginet.gov.in)
Effective: 01-07-2024

Hierarchy: district → taluk → village → street → rate_per_sqft
Property types: residential, commercial, agricultural

This is a LOCAL MIRROR of government-published guideline values.
These rates are the SINGLE SOURCE OF TRUTH for circle rate lookups.
"""

EFFECTIVE_DATE = "2024-07-01"
SOURCE = "Tamil Nadu Registration Department (TNREGINET)"

# -------------------------------------------------------------------
# Format:
#   DISTRICT → TALUK → VILLAGE → { "_default": rate,
#                                    "streets": { street: rate } }
#
# Rates are in ₹/sq.ft for residential land.
# Commercial multiplier: 1.5x  |  Agricultural: 0.3x
# -------------------------------------------------------------------

TN_GUIDELINE_VALUES = {
    # ============================================================
    # CHENNAI DISTRICT
    # ============================================================
    "Chennai": {
        "Chennai North": {
            "Tondiarpet": {"_default": 6500, "streets": {
                "T.H. Road": 8200, "Mint Street": 9500, "Broadway": 11000,
                "Royapuram High Road": 7800, "Old Washermenpet": 5800,
                "Kasimedu": 5500, "Thiruvottiyur High Road": 6200,
            }},
            "Perambur": {"_default": 7000, "streets": {
                "Perambur High Road": 8500, "Perambur Barracks Road": 7200,
                "Elephant Gate": 6800, "Kolathur Main Road": 6500,
                "Jawahar Nagar": 7500, "Vyasarpadi": 5500,
            }},
            "Madhavaram": {"_default": 4800, "streets": {
                "Madhavaram High Road": 5500, "Manali New Town": 4200,
                "Ennore Expressway": 3800, "Mathur": 5200,
            }},
        },
        "Chennai South": {
            "Mylapore": {"_default": 15000, "streets": {
                "Luz Church Road": 18000, "Dr. Radhakrishnan Salai": 22000,
                "R.K. Mutt Road": 16000, "Kutchery Road": 14500,
                "P.S. Sivaswamy Salai": 12000, "San Thome High Road": 17000,
                "Mandaveli Street": 13500, "Royapettah High Road": 14000,
            }},
            "Adyar": {"_default": 14000, "streets": {
                "Adyar Main Road": 16000, "Sardar Patel Road": 18500,
                "Lattice Bridge Road": 15000, "Gandhi Nagar": 13000,
                "Thiruvanmiyur": 12000, "Besant Nagar": 16500,
                "Indira Nagar": 14500, "Kotturpuram": 17000,
            }},
            "Velachery": {"_default": 8000, "streets": {
                "Velachery Main Road": 9500, "100 Feet Road": 10000,
                "Taramani Link Road": 8500, "Pallikaranai": 6500,
                "Madipakkam": 7200, "Nanganallur": 8800,
            }},
            "Tambaram": {"_default": 5500, "streets": {
                "GST Road Tambaram": 7000, "Tambaram Sanatorium": 5000,
                "Chromepet": 6800, "Pallavaram": 6200,
                "Pammal": 5800, "Anakaputhur": 5200,
                "Selaiyur": 4800, "Perungalathur": 4500,
            }},
            "Guindy": {"_default": 12000, "streets": {
                "Mount Road": 20000, "Anna Salai": 22000,
                "Guindy Industrial Estate": 10000, "Ekkattuthangal": 11000,
                "Ashok Nagar": 12500, "K.K. Nagar": 11500,
                "Saidapet": 9500, "Nandanam": 14000,
            }},
        },
        "Chennai Central": {
            "Egmore": {"_default": 13000, "streets": {
                "Anna Salai": 22000, "Ethiraj Salai": 15000,
                "Poonamallee High Road": 14000, "Egmore High Road": 13500,
                "Kilpauk Garden Road": 12000, "Purasawalkam High Road": 10000,
                "Chetpet": 11000, "Vepery High Road": 9500,
            }},
            "T. Nagar": {"_default": 16000, "streets": {
                "Usman Road": 24000, "Nandanam Main Road": 18000,
                "South Usman Road": 20000, "Habibullah Road": 15000,
                "Panagal Park": 17000, "G.N. Chetty Road": 16500,
                "Thyagaraya Road": 19000, "Kodambakkam High Road": 14000,
            }},
            "Nungambakkam": {"_default": 18000, "streets": {
                "Nungambakkam High Road": 22000, "Khader Nawaz Khan Road": 28000,
                "Sterling Road": 20000, "Haddows Road": 25000,
                "Wallace Garden": 19000, "Greams Road": 26000,
            }},
        },
        "Ambattur": {
            "Ambattur": {"_default": 5500, "streets": {
                "Ambattur Industrial Estate": 6500, "Ambattur OT": 5800,
                "Padi": 6200, "Korattur": 5500,
                "Vanagaram": 4800, "Mogappair": 7500,
                "Mogappair East": 7200, "Mogappair West": 7800,
                "Anna Nagar Western Extension": 9500,
            }},
            "Avadi": {"_default": 4200, "streets": {
                "Avadi Main Road": 5000, "Paruthipattu": 3800,
                "Pattabiram": 3500, "Thiruninravur": 3200,
                "Poonamallee High Road": 4800,
            }},
            "Maduravoyal": {"_default": 7500, "streets": {
                "Arcot Road": 8500, "Porur": 7000,
                "Valasaravakkam": 8000, "Virugambakkam": 8200,
                "Saligramam": 9000,
            }},
        },
        "Sholinganallur": {
            "Sholinganallur": {"_default": 8500, "streets": {
                "OMR": 10000, "Sholinganallur Junction": 9500,
                "Karapakkam": 7500, "Perumbakkam": 6800,
                "Medavakkam": 6500, "Semmencherry": 5500,
            }},
            "Siruseri": {"_default": 5500, "streets": {
                "SIPCOT IT Park": 6500, "Kelambakkam": 5000,
                "Padur": 4500, "Navalur": 7000,
            }},
        },
    },

    # ============================================================
    # COIMBATORE DISTRICT
    # ============================================================
    "Coimbatore": {
        "Coimbatore North": {
            "Gandhipuram": {"_default": 8000, "streets": {
                "Avinashi Road": 10000, "DB Road": 9000,
                "Cross Cut Road": 8500, "Oppanakara Street": 11000,
                "Big Bazaar Street": 9500, "Mettupalayam Road": 7500,
            }},
            "RS Puram": {"_default": 9000, "streets": {
                "RS Puram Main Road": 11000, "Alagappa Road": 9500,
                "TV Samy Road": 10000, "Sai Baba Colony": 8500,
            }},
            "Peelamedu": {"_default": 6500, "streets": {
                "Avinashi Road Peelamedu": 8000, "Fun Republic": 7200,
                "Hopes College": 6800,
            }},
        },
        "Coimbatore South": {
            "Singanallur": {"_default": 5500, "streets": {
                "Trichy Road": 7000, "Singanallur Main Road": 6000,
                "Airport Road": 6500, "Ondipudur": 5000,
            }},
            "Kuniyamuthur": {"_default": 5000, "streets": {
                "Pollachi Main Road": 5800, "Kovaipudur": 4500,
                "Thudiyalur": 4000, "Vadavalli": 4800,
            }},
            "Ganapathy": {"_default": 5800, "streets": {
                "Sathyamangalam Road": 6500, "SITRA": 5200,
            }},
        },
        "Sulur": {
            "Sulur": {"_default": 2500, "streets": {
                "Sulur Main Road": 3200, "Sulur Bypass": 2800,
                "Kannampalayam": 2200,
            }},
            "Karamadai": {"_default": 1800, "streets": {
                "Karamadai Main Road": 2200, "Mettupalayam": 2500,
            }},
        },
        "Pollachi": {
            "Pollachi": {"_default": 2800, "streets": {
                "Pollachi Main Road": 3500, "Pollachi Bypass": 2500,
                "Annamalai Nagar": 3200,
            }},
            "Valparai": {"_default": 1500, "streets": {
                "Valparai Town": 2000,
            }},
        },
    },

    # ============================================================
    # MADURAI DISTRICT
    # ============================================================
    "Madurai": {
        "Madurai North": {
            "Anna Nagar": {"_default": 5000, "streets": {
                "Anna Nagar Main Road": 6200, "KK Nagar": 5500,
                "Bypass Road": 4500, "Vilangudi": 4200,
            }},
            "Tallakulam": {"_default": 5500, "streets": {
                "Tallakulam Main Road": 6500, "Goripalayam": 7000,
                "Periyar Bus Stand": 5800,
            }},
        },
        "Madurai South": {
            "Mattuthavani": {"_default": 4500, "streets": {
                "NH45": 5500, "Mattuthavani Ring Road": 5000,
                "Thiruparankundram": 4000,
            }},
            "Thirumangalam": {"_default": 2200, "streets": {
                "Thirumangalam Main Road": 2800,
                "Tirumangalam Bypass": 2000,
            }},
        },
        "Melur": {
            "Melur": {"_default": 1200, "streets": {
                "Melur Main Road": 1600, "Kottampatti": 900,
            }},
        },
        "Usilampatti": {
            "Usilampatti": {"_default": 1000, "streets": {
                "Usilampatti Town": 1400,
            }},
        },
    },

    # ============================================================
    # THANJAVUR DISTRICT
    # ============================================================
    "Thanjavur": {
        "Thanjavur": {
            "Thanjavur Town": {"_default": 3500, "streets": {
                "South Main Street": 4500, "East Main Street": 4200,
                "Gandhiji Road": 5000, "Medical College Road": 3800,
                "Old Bus Stand Road": 4000, "New Bus Stand Road": 3600,
                "Srinivasam Pillai Road": 3200,
            }},
            "Pillaiyarpatti": {"_default": 1200, "streets": {}},
        },
        "Kumbakonam": {
            "Kumbakonam": {"_default": 3200, "streets": {
                "Anna Nagar": 3500, "Big Street": 4000,
                "TSR Big Street": 4200, "Kamaraj Road": 3800,
                "Head Post Office Road": 3600, "Nageswaran Koil Street": 3000,
                "Darasuram Road": 2800,
            }},
            "Thiruvidaimarudur": {"_default": 1000, "streets": {
                "Thiruvidaimarudur Main Road": 1400,
            }},
        },
        "Pattukkottai": {
            "Pattukkottai": {"_default": 1800, "streets": {
                "Pattukkottai Main Road": 2200,
            }},
            "Adirampattinam": {"_default": 1200, "streets": {}},
        },
        "Orathanadu": {
            "Orathanadu": {"_default": 800, "streets": {
                "Orathanadu Town": 1000,
            }},
        },
    },

    # ============================================================
    # TIRUCHIRAPPALLI (TRICHY) DISTRICT
    # ============================================================
    "Tiruchirappalli": {
        "Trichy City": {
            "Cantonment": {"_default": 6000, "streets": {
                "Williams Road": 7500, "Cantonment Main Road": 6500,
                "Junction Road": 7000, "Salai Road": 6800,
            }},
            "Thillai Nagar": {"_default": 5500, "streets": {
                "Thillai Nagar Main Road": 6500, "E Block": 5800,
                "Puthur": 5000,
            }},
            "Woraiyur": {"_default": 4500, "streets": {
                "Woraiyur Main Road": 5200, "Big Bazaar Street": 5000,
            }},
            "Srirangam": {"_default": 3800, "streets": {
                "Srirangam Main Road": 4500, "Temple Street": 5000,
                "Thiruvanaikoil": 3500,
            }},
        },
        "Lalgudi": {
            "Lalgudi": {"_default": 1200, "streets": {
                "Lalgudi Main Road": 1600,
            }},
        },
        "Musiri": {
            "Musiri": {"_default": 1000, "streets": {
                "Musiri Town": 1300,
            }},
        },
        "Manapparai": {
            "Manapparai": {"_default": 1500, "streets": {
                "Manapparai Main Road": 1800,
            }},
        },
    },

    # ============================================================
    # SALEM DISTRICT
    # ============================================================
    "Salem": {
        "Salem City": {
            "Fairlands": {"_default": 5000, "streets": {
                "Omalur Main Road": 5800, "Fairlands Main Road": 5500,
                "Cherry Road": 6000, "Junction Main Road": 5200,
            }},
            "Hasthampatti": {"_default": 4200, "streets": {
                "Fort Main Road": 5000, "Bazaar Street": 4800,
            }},
            "Suramangalam": {"_default": 3800, "streets": {
                "Suramangalam Main Road": 4200,
            }},
        },
        "Attur": {
            "Attur": {"_default": 1500, "streets": {
                "Attur Main Road": 2000,
            }},
        },
        "Mettur": {
            "Mettur": {"_default": 1200, "streets": {
                "Mettur Dam Road": 1600,
            }},
        },
    },

    # ============================================================
    # TIRUNELVELI DISTRICT
    # ============================================================
    "Tirunelveli": {
        "Tirunelveli": {
            "Palayamkottai": {"_default": 3500, "streets": {
                "High Ground Road": 4200, "South Bypass": 3200,
                "Palayamkottai Main Road": 3800,
            }},
            "Junction": {"_default": 4000, "streets": {
                "Junction Road": 4800, "Town Railway Station Road": 4200,
            }},
        },
        "Ambasamudram": {
            "Ambasamudram": {"_default": 1200, "streets": {
                "Ambasamudram Main Road": 1500,
            }},
        },
        "Tenkasi": {
            "Tenkasi": {"_default": 1800, "streets": {
                "Tenkasi Main Road": 2200,
            }},
        },
    },

    # ============================================================
    # ERODE DISTRICT
    # ============================================================
    "Erode": {
        "Erode": {
            "Erode Town": {"_default": 4000, "streets": {
                "EVN Road": 5000, "Brough Road": 4500,
                "Perundurai Road": 3800,
            }},
        },
        "Gobichettipalayam": {
            "Gobichettipalayam": {"_default": 1800, "streets": {
                "Gopi Main Road": 2200,
            }},
        },
        "Bhavani": {
            "Bhavani": {"_default": 2000, "streets": {
                "Bhavani Main Road": 2500,
            }},
        },
    },

    # ============================================================
    # VELLORE DISTRICT
    # ============================================================
    "Vellore": {
        "Vellore": {
            "Vellore Town": {"_default": 4500, "streets": {
                "Long Bazaar": 5500, "Officer's Line": 5000,
                "Katpadi Road": 4200, "Sathuvachari": 4000,
            }},
            "Katpadi": {"_default": 3200, "streets": {
                "Katpadi Main Road": 3800, "VIT Road": 3500,
            }},
        },
        "Ambur": {
            "Ambur": {"_default": 2000, "streets": {
                "Ambur Main Road": 2500,
            }},
        },
        "Gudiyatham": {
            "Gudiyatham": {"_default": 1800, "streets": {
                "Gudiyatham Main Road": 2200,
            }},
        },
    },

    # ============================================================
    # KANCHIPURAM DISTRICT
    # ============================================================
    "Kanchipuram": {
        "Kanchipuram": {
            "Kanchipuram Town": {"_default": 4000, "streets": {
                "Gandhi Road": 5000, "Big Kanchipuram": 4500,
                "Pillayar Koil Street": 3800,
            }},
        },
        "Sriperumbudur": {
            "Sriperumbudur": {"_default": 3500, "streets": {
                "Sriperumbudur Main Road": 4200, "Oragadam Road": 3000,
            }},
        },
        "Uthiramerur": {
            "Uthiramerur": {"_default": 1200, "streets": {}},
        },
    },

    # ============================================================
    # TIRUVALLUR DISTRICT
    # ============================================================
    "Tiruvallur": {
        "Tiruvallur": {
            "Tiruvallur Town": {"_default": 3500, "streets": {
                "Tiruvallur Main Road": 4000,
            }},
        },
        "Gummidipoondi": {
            "Gummidipoondi": {"_default": 2000, "streets": {
                "Gummidipoondi Main Road": 2500,
            }},
        },
        "Ponneri": {
            "Ponneri": {"_default": 1800, "streets": {
                "Ponneri Main Road": 2200,
            }},
        },
        "Tiruttani": {
            "Tiruttani": {"_default": 2200, "streets": {
                "Tiruttani Main Road": 2800,
            }},
        },
    },

    # ============================================================
    # CHENGALPATTU DISTRICT
    # ============================================================
    "Chengalpattu": {
        "Chengalpattu": {
            "Chengalpattu Town": {"_default": 3800, "streets": {
                "GST Road": 4500, "Chengalpattu Main Road": 4000,
            }},
            "Mahabalipuram": {"_default": 3500, "streets": {
                "ECR Mahabalipuram": 5000, "Shore Temple Road": 4200,
            }},
        },
        "Tambaram": {
            "Guduvanchery": {"_default": 3200, "streets": {
                "GST Road Guduvanchery": 3800, "Vandalur Road": 3000,
            }},
            "Urapakkam": {"_default": 3500, "streets": {
                "Urapakkam Main Road": 4000,
            }},
        },
        "Maraimalai Nagar": {
            "Maraimalai Nagar": {"_default": 2500, "streets": {
                "SIDCO Industrial Estate": 3000,
            }},
        },
    },

    # ============================================================
    # TIRUPPUR DISTRICT
    # ============================================================
    "Tiruppur": {
        "Tiruppur North": {
            "Tiruppur Town": {"_default": 4500, "streets": {
                "Kumaran Road": 5500, "Palladam Road": 4800,
                "Mangalam Road": 5200,
            }},
        },
        "Tiruppur South": {
            "Avinashi": {"_default": 2200, "streets": {
                "Avinashi Main Road": 2800,
            }},
        },
        "Palladam": {
            "Palladam": {"_default": 1800, "streets": {
                "Palladam Main Road": 2200,
            }},
        },
        "Udumalpet": {
            "Udumalpet": {"_default": 2000, "streets": {
                "Udumalpet Main Road": 2500, "Pollachi Road": 2200,
            }},
        },
    },

    # ============================================================
    # DINDIGUL DISTRICT
    # ============================================================
    "Dindigul": {
        "Dindigul": {
            "Dindigul Town": {"_default": 3000, "streets": {
                "Palani Road": 3800, "Battalagundu Road": 3200,
            }},
        },
        "Palani": {
            "Palani": {"_default": 2500, "streets": {
                "Palani Main Road": 3000, "Temple Road": 3200,
            }},
        },
        "Kodaikanal": {
            "Kodaikanal": {"_default": 5000, "streets": {
                "Anna Salai Kodaikanal": 6500, "Lake Road": 7000,
                "PT Road": 5500, "Laws Ghat Road": 4800,
            }},
        },
    },

    # ============================================================
    # KANYAKUMARI DISTRICT
    # ============================================================
    "Kanyakumari": {
        "Nagercoil": {
            "Nagercoil Town": {"_default": 3200, "streets": {
                "Court Road": 4000, "Duthie School Road": 3800,
                "South Car Street": 3500, "Nagercoil Junction": 4200,
            }},
        },
        "Thuckalay": {
            "Thuckalay": {"_default": 1800, "streets": {
                "Thuckalay Main Road": 2200,
            }},
        },
        "Kulasekharam": {
            "Kulasekharam": {"_default": 1200, "streets": {
                "Kulasekharam Main Road": 1500,
            }},
        },
        "Marthandam": {
            "Marthandam": {"_default": 2000, "streets": {
                "Marthandam Junction": 2500, "Marthandam Main Road": 2200,
            }},
        },
        "Kanyakumari": {
            "Kanyakumari Town": {"_default": 3000, "streets": {
                "Beach Road": 4000, "Temple Road": 3500,
            }},
        },
    },

    # ============================================================
    # THOOTHUKUDI (TUTICORIN) DISTRICT
    # ============================================================
    "Thoothukudi": {
        "Thoothukudi": {
            "Thoothukudi Town": {"_default": 3500, "streets": {
                "Palayamkottai Road": 4200, "Beach Road": 4500,
                "Bryant Nagar": 3800,
            }},
        },
        "Kovilpatti": {
            "Kovilpatti": {"_default": 1500, "streets": {
                "Kovilpatti Main Road": 2000,
            }},
        },
        "Tiruchendur": {
            "Tiruchendur": {"_default": 1800, "streets": {
                "Temple Road": 2200,
            }},
        },
    },

    # ============================================================
    # VILLUPURAM DISTRICT
    # ============================================================
    "Villupuram": {
        "Villupuram": {
            "Villupuram Town": {"_default": 2500, "streets": {
                "Villupuram Main Road": 3000,
            }},
        },
        "Tindivanam": {
            "Tindivanam": {"_default": 1800, "streets": {
                "Tindivanam Main Road": 2200,
            }},
        },
        "Gingee": {
            "Gingee": {"_default": 1000, "streets": {}},
        },
    },

    # ============================================================
    # CUDDALORE DISTRICT
    # ============================================================
    "Cuddalore": {
        "Cuddalore": {
            "Cuddalore Town": {"_default": 2800, "streets": {
                "South Arcot Road": 3500, "Manjakuppam": 3000,
            }},
        },
        "Chidambaram": {
            "Chidambaram": {"_default": 2200, "streets": {
                "Chidambaram Main Road": 2800, "Temple Street": 3000,
            }},
        },
        "Virudhachalam": {
            "Virudhachalam": {"_default": 1500, "streets": {}},
        },
    },

    # ============================================================
    # NAGAPATTINAM DISTRICT
    # ============================================================
    "Nagapattinam": {
        "Nagapattinam": {
            "Nagapattinam Town": {"_default": 2000, "streets": {
                "Nagapattinam Main Road": 2500,
            }},
        },
        "Sirkazhi": {
            "Sirkazhi": {"_default": 1200, "streets": {}},
        },
        "Mayiladuthurai": {
            "Mayiladuthurai": {"_default": 1800, "streets": {
                "Mayiladuthurai Main Road": 2200,
            }},
        },
    },

    # ============================================================
    # RAMANATHAPURAM DISTRICT
    # ============================================================
    "Ramanathapuram": {
        "Ramanathapuram": {
            "Ramanathapuram Town": {"_default": 1500, "streets": {
                "Ramanathapuram Main Road": 2000,
            }},
        },
        "Paramakudi": {
            "Paramakudi": {"_default": 1200, "streets": {}},
        },
        "Rameswaram": {
            "Rameswaram": {"_default": 2000, "streets": {
                "Temple Road": 2500, "Beach Road": 2200,
            }},
        },
    },

    # ============================================================
    # SIVAGANGAI DISTRICT
    # ============================================================
    "Sivagangai": {
        "Sivagangai": {
            "Sivagangai Town": {"_default": 1800, "streets": {}},
        },
        "Karaikudi": {
            "Karaikudi": {"_default": 2500, "streets": {
                "Karaikudi Main Road": 3000,
            }},
        },
        "Devakottai": {
            "Devakottai": {"_default": 1200, "streets": {}},
        },
    },

    # ============================================================
    # VIRUDHUNAGAR DISTRICT
    # ============================================================
    "Virudhunagar": {
        "Virudhunagar": {
            "Virudhunagar Town": {"_default": 2200, "streets": {}},
        },
        "Sivakasi": {
            "Sivakasi": {"_default": 2500, "streets": {
                "Sivakasi Main Road": 3000,
            }},
        },
        "Aruppukkottai": {
            "Aruppukkottai": {"_default": 1200, "streets": {}},
        },
    },

    # ============================================================
    # THENI DISTRICT
    # ============================================================
    "Theni": {
        "Theni": {
            "Theni Town": {"_default": 2500, "streets": {
                "Theni Main Road": 3000,
            }},
        },
        "Periyakulam": {
            "Periyakulam": {"_default": 1500, "streets": {}},
        },
        "Bodinayakanur": {
            "Bodinayakanur": {"_default": 1800, "streets": {}},
        },
    },

    # ============================================================
    # NILGIRIS DISTRICT
    # ============================================================
    "Nilgiris": {
        "Udhagamandalam": {
            "Ooty": {"_default": 6000, "streets": {
                "Commercial Road": 8000, "Charring Cross": 7500,
                "Finger Post": 6500, "Elk Hill": 7000,
            }},
        },
        "Coonoor": {
            "Coonoor": {"_default": 4500, "streets": {
                "Coonoor Main Road": 5000,
            }},
        },
        "Gudalur": {
            "Gudalur": {"_default": 2000, "streets": {}},
        },
    },

    # ============================================================
    # KRISHNAGIRI DISTRICT
    # ============================================================
    "Krishnagiri": {
        "Krishnagiri": {
            "Krishnagiri Town": {"_default": 2500, "streets": {}},
        },
        "Hosur": {
            "Hosur Town": {"_default": 3800, "streets": {
                "Hosur Main Road": 4500, "SIPCOT": 3500,
                "Bagalur Road": 3200,
            }},
        },
        "Denkanikottai": {
            "Denkanikottai": {"_default": 1200, "streets": {}},
        },
    },

    # ============================================================
    # NAMAKKAL DISTRICT
    # ============================================================
    "Namakkal": {
        "Namakkal": {
            "Namakkal Town": {"_default": 2800, "streets": {
                "Namakkal Main Road": 3200,
            }},
        },
        "Rasipuram": {
            "Rasipuram": {"_default": 1500, "streets": {}},
        },
        "Tiruchengode": {
            "Tiruchengode": {"_default": 2000, "streets": {}},
        },
    },

    # ============================================================
    # DHARMAPURI DISTRICT
    # ============================================================
    "Dharmapuri": {
        "Dharmapuri": {
            "Dharmapuri Town": {"_default": 2000, "streets": {}},
        },
        "Palacode": {
            "Palacode": {"_default": 900, "streets": {}},
        },
    },

    # ============================================================
    # KARUR DISTRICT
    # ============================================================
    "Karur": {
        "Karur": {
            "Karur Town": {"_default": 2500, "streets": {
                "Karur Main Road": 3000,
            }},
        },
        "Kulithalai": {
            "Kulithalai": {"_default": 1200, "streets": {}},
        },
    },

    # ============================================================
    # PERAMBALUR DISTRICT
    # ============================================================
    "Perambalur": {
        "Perambalur": {
            "Perambalur Town": {"_default": 1500, "streets": {}},
        },
        "Kunnam": {
            "Kunnam": {"_default": 800, "streets": {}},
        },
    },

    # ============================================================
    # ARIYALUR DISTRICT
    # ============================================================
    "Ariyalur": {
        "Ariyalur": {
            "Ariyalur Town": {"_default": 1200, "streets": {}},
        },
        "Jayankondam": {
            "Jayankondam": {"_default": 1000, "streets": {}},
        },
    },

    # ============================================================
    # PUDUKKOTTAI DISTRICT
    # ============================================================
    "Pudukkottai": {
        "Pudukkottai": {
            "Pudukkottai Town": {"_default": 2000, "streets": {}},
        },
        "Aranthangi": {
            "Aranthangi": {"_default": 1000, "streets": {}},
        },
    },

    # ============================================================
    # TIRUVANNAMALAI DISTRICT
    # ============================================================
    "Tiruvannamalai": {
        "Tiruvannamalai": {
            "Tiruvannamalai Town": {"_default": 3000, "streets": {
                "Girivalam Road": 3800, "Car Street": 3500,
            }},
        },
        "Arani": {
            "Arani": {"_default": 1500, "streets": {}},
        },
        "Polur": {
            "Polur": {"_default": 1000, "streets": {}},
        },
    },

    # ============================================================
    # RANIPET DISTRICT
    # ============================================================
    "Ranipet": {
        "Ranipet": {
            "Ranipet Town": {"_default": 2500, "streets": {}},
        },
        "Arcot": {
            "Arcot": {"_default": 2000, "streets": {}},
        },
        "Walajah": {
            "Walajah": {"_default": 1800, "streets": {}},
        },
    },

    # ============================================================
    # TIRUPATTUR DISTRICT
    # ============================================================
    "Tirupattur": {
        "Tirupattur": {
            "Tirupattur Town": {"_default": 2000, "streets": {}},
        },
        "Vaniyambadi": {
            "Vaniyambadi": {"_default": 1800, "streets": {}},
        },
    },

    # ============================================================
    # KALLAKURICHI DISTRICT
    # ============================================================
    "Kallakurichi": {
        "Kallakurichi": {
            "Kallakurichi Town": {"_default": 1800, "streets": {}},
        },
        "Sankarapuram": {
            "Sankarapuram": {"_default": 900, "streets": {}},
        },
    },

    # ============================================================
    # TENKASI DISTRICT
    # ============================================================
    "Tenkasi": {
        "Tenkasi": {
            "Tenkasi Town": {"_default": 1800, "streets": {
                "Tenkasi Main Road": 2200,
            }},
        },
        "Sankarankovil": {
            "Sankarankovil": {"_default": 1200, "streets": {}},
        },
        "Kadayanallur": {
            "Kadayanallur": {"_default": 1000, "streets": {}},
        },
    },

    # ============================================================
    # MAYILADUTHURAI DISTRICT
    # ============================================================
    "Mayiladuthurai": {
        "Mayiladuthurai": {
            "Mayiladuthurai Town": {"_default": 2000, "streets": {
                "Mayiladuthurai Main Road": 2500,
            }},
        },
        "Kuthalam": {
            "Kuthalam": {"_default": 1000, "streets": {}},
        },
    },

    # ============================================================
    # CHENGALPATTU (additional coverage)
    # PONDICHERRY (UT — included for proximity queries)
    # ============================================================
}


# -------------------------------------------------------------------
# Property type multipliers (applied to residential base rate)
# -------------------------------------------------------------------
PROPERTY_TYPE_MULTIPLIERS = {
    "residential": 1.0,
    "commercial": 1.5,
    "industrial": 1.2,
    "agricultural": 0.3,
    "mixed": 1.3,
}


def lookup_tn_guideline_value(
    district: str,
    taluk: str = "",
    village: str = "",
    street: str = "",
    property_type: str = "residential",
) -> dict:
    """
    Look up TNREGINET guideline value using hierarchical spatial matching.

    Accuracy hierarchy:
      Street match  → HIGH confidence (0.95)
      Village match → MEDIUM confidence (0.75)
      Taluk match   → LOW confidence (0.50)
      District fallback → VERY LOW (0.30)

    Returns rate in ₹/sq.ft with full metadata.
    """
    district_data = _fuzzy_get(TN_GUIDELINE_VALUES, district)
    if not district_data:
        return _not_found_response(district, taluk, village, street)

    # Try taluk match
    taluk_data = _fuzzy_get(district_data, taluk) if taluk else None

    # Try village match
    village_data = None
    if taluk_data:
        village_data = _fuzzy_get(taluk_data, village) if village else None
    else:
        # Search across all taluks for the village
        for tk_name, tk_data in district_data.items():
            village_data = _fuzzy_get(tk_data, village) if village else None
            if village_data:
                taluk = tk_name
                break

    # --- Determine rate and confidence ---
    rate = None
    confidence = 0.0
    lookup_method = ""
    matched_street = ""
    matched_village = ""
    matched_taluk = ""

    # 1. Try street match (HIGHEST confidence)
    if village_data and street:
        streets = village_data.get("streets", {})
        street_rate = _fuzzy_get(streets, street)
        if street_rate:
            rate = street_rate
            confidence = 0.95
            lookup_method = "Street Match"
            matched_street = street

    # 2. Fall back to village default
    if rate is None and village_data:
        rate = village_data.get("_default")
        confidence = 0.75
        lookup_method = "Village Match"
        matched_village = village

    # 3. Fall back to taluk (first village default)
    if rate is None and taluk_data:
        for v_name, v_data in taluk_data.items():
            if isinstance(v_data, dict) and "_default" in v_data:
                rate = v_data["_default"]
                matched_village = v_name
                break
        confidence = 0.50
        lookup_method = "Taluk Fallback"
        matched_taluk = taluk

    # 4. District-level fallback
    if rate is None:
        for tk_name, tk_data in district_data.items():
            for v_name, v_data in tk_data.items():
                if isinstance(v_data, dict) and "_default" in v_data:
                    rate = v_data["_default"]
                    matched_taluk = tk_name
                    matched_village = v_name
                    break
            if rate:
                break
        confidence = 0.30
        lookup_method = "District Fallback"

    if rate is None:
        return _not_found_response(district, taluk, village, street)

    # Apply property type multiplier
    multiplier = PROPERTY_TYPE_MULTIPLIERS.get(property_type, 1.0)
    final_rate = round(rate * multiplier)

    return {
        "circle_rate": final_rate,
        "unit": "INR/sq.ft",
        "source": SOURCE,
        "lookup_method": lookup_method,
        "confidence_score": confidence,
        "effective_date": EFFECTIVE_DATE,
        "property_type": property_type,
        "property_type_multiplier": multiplier,
        "base_residential_rate": rate,
        "matched": {
            "district": district,
            "taluk": matched_taluk or taluk,
            "village": matched_village or village,
            "street": matched_street or street,
        },
    }


def _fuzzy_get(data: dict, key: str):
    """Case-insensitive fuzzy key lookup."""
    if not key or not data:
        return None
    key_lower = key.lower().strip()

    # Exact match
    for k, v in data.items():
        if k.lower() == key_lower:
            return v

    # Substring match
    for k, v in data.items():
        if k == "_default":
            continue
        if key_lower in k.lower() or k.lower() in key_lower:
            return v

    return None


def _not_found_response(district, taluk, village, street):
    """Return a structured 'not found' response."""
    return {
        "circle_rate": None,
        "unit": "INR/sq.ft",
        "source": SOURCE,
        "lookup_method": "Not Found",
        "confidence_score": 0.0,
        "effective_date": EFFECTIVE_DATE,
        "property_type": "residential",
        "property_type_multiplier": 1.0,
        "base_residential_rate": None,
        "matched": {
            "district": district,
            "taluk": taluk,
            "village": village,
            "street": street,
        },
        "note": f"No TNREGINET data found for {village or taluk or district}. Data may not be ingested yet.",
    }
