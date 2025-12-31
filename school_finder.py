import sqlite3
import json
from datetime import datetime
import os
import base64

class ScholasticForumWebsiteGenerator:
    def __init__(self, db_path="school_manager.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect_database(self):
        """Connect to SQLite database"""
        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            print("Database connected successfully")
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def get_schools_data(self):
        """Get all schools with public information"""
        query = """
        SELECT 
            school_id, name, short_name, motto, mission, vision, description,
            school_type, gender_focus, level, category, establishment_year,
            address, city, province, district, country, postal_code,
            google_maps_link,
            email, phone, phone_primary, website,
            facebook_page, twitter_handle, instagram_handle, linkedin_page,
            principal_name, principal_email,
            curriculum, total_students, total_teachers,
            total_classrooms, science_labs, computer_labs, library_rooms,
            playground_area, sports_facilities,
            has_library, has_science_lab, has_computer_lab, has_playground,
            has_sports_field, has_swimming_pool, has_auditorium, has_cafeteria,
            has_health_clinic, has_wifi, has_smart_classes,
            hostel_facilities, transport_services,
            fee_range, scholarships_available, scholarship_details,
            overall_rating, total_reviews, academic_rating, facility_rating,
            discipline_rating,
            logo_blob, banner_blob,
            latitude, longitude,
            created_at
        FROM schools 
        WHERE is_active = 1 AND is_verified = 1
        ORDER BY name
        """
        
        try:
            self.cursor.execute(query)
            columns = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            
            schools = []
            for row in rows:
                school_dict = dict(zip(columns, row))
                
                if school_dict.get('logo_blob'):
                    school_dict['logo_base64'] = self.blob_to_base64(school_dict['logo_blob'])
                if school_dict.get('banner_blob'):
                    school_dict['banner_base64'] = self.blob_to_base64(school_dict['banner_blob'])
                
                if school_dict.get('establishment_year'):
                    school_dict['age_years'] = datetime.now().year - school_dict['establishment_year']
                
                school_dict['full_address'] = self.format_address(school_dict)
                school_dict['amenities'] = self.get_amenities_list(school_dict)
                school_dict['social_links'] = self.get_social_links(school_dict)
                
                schools.append(school_dict)
            
            return schools
        except sqlite3.Error as e:
            print(f"Error fetching schools: {e}")
            return []
    
    def blob_to_base64(self, blob_data):
        """Convert BLOB to base64 string for HTML"""
        try:
            return base64.b64encode(blob_data).decode('utf-8')
        except:
            return None
    
    def format_address(self, school):
        """Format complete address string"""
        parts = []
        if school.get('address'):
            parts.append(school['address'])
        if school.get('district'):
            parts.append(school['district'])
        if school.get('city'):
            parts.append(school['city'])
        if school.get('province'):
            parts.append(school['province'])
        if school.get('postal_code'):
            parts.append(school['postal_code'])
        if school.get('country'):
            parts.append(school['country'])
        return ", ".join(parts)
    
    def get_amenities_list(self, school):
        """Extract list of available amenities"""
        amenities = []
        
        amenities_map = {
            'has_library': '📚 Library',
            'has_science_lab': '🔬 Science Lab',
            'has_computer_lab': '💻 Computer Lab',
            'has_playground': '⚽ Playground',
            'has_sports_field': '🏅 Sports Field',
            'has_swimming_pool': '🏊 Swimming Pool',
            'has_auditorium': '🎭 Auditorium',
            'has_cafeteria': '🍽️ Cafeteria',
            'has_health_clinic': '🏥 Health Clinic',
            'has_wifi': '📡 WiFi',
            'has_smart_classes': '💡 Smart Classes',
            'hostel_facilities': '🏠 Boarding',
            'transport_services': '🚌 Transport'
        }
        
        for key, label in amenities_map.items():
            if school.get(key):
                amenities.append(label)
        
        return amenities
    
    def get_social_links(self, school):
        """Extract social media links"""
        social = {}
        
        if school.get('website'):
            social['website'] = school['website']
        if school.get('facebook_page'):
            social['facebook'] = school['facebook_page']
        if school.get('twitter_handle'):
            social['twitter'] = f"https://twitter.com/{school['twitter_handle']}"
        if school.get('instagram_handle'):
            social['instagram'] = f"https://instagram.com/{school['instagram_handle']}"
        if school.get('linkedin_page'):
            social['linkedin'] = school['linkedin_page']
        if school.get('google_maps_link'):
            social['maps'] = school['google_maps_link']
        
        return social
    
    def generate_homepage(self, schools):
        """Generate the main homepage"""
        total_schools = len(schools)
        html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Advanced SEO Meta Tags -->
    <title>Scholastic Forum - Discover Educational Institutions & Schools Directory</title>
    <meta name="description" content="Comprehensive school directory with detailed profiles of educational institutions. Find schools by location, curriculum, facilities, and ratings. Part of Scholastic Services.">
    <meta name="keywords" content="schools directory, educational institutions, find schools, school profiles, education database, Scholastic Services">
    <meta name="author" content="Scholastic Services">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://hvstechzw.github.io/Scholastic-Schools-Catalog/">
    <meta property="og:title" content="Scholastic Forum - School Directory & Educational Institutions">
    <meta property="og:description" content="Discover and compare schools with our comprehensive educational directory. Part of Scholastic Services suite.">
    <meta property="og:image" content="https://hvstechzw.github.io/Scholastic-Schools-Catalog/assets/images/og-image.jpg">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://hvstechzw.github.io/Scholastic-Schools-Catalog/">
    <meta property="twitter:title" content="Scholastic Forum - School Directory & Educational Institutions">
    <meta property="twitter:description" content="Discover and compare schools with our comprehensive educational directory. Part of Scholastic Services suite.">
    <meta property="twitter:image" content="https://hvstechzw.github.io/Scholastic-Schools-Catalog/assets/images/og-image.jpg">
    
    <!-- Structured Data for Schools Directory -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Scholastic Forum",
        "description": "Comprehensive directory of educational institutions and schools",
        "url": "https://hvstechzw.github.io/Scholastic-Schools-Catalog/",
        "potentialAction": {{
            "@type": "SearchAction",
            "target": "https://hvstechzw.github.io/Scholastic-Schools-Catalog/?search={{search_term_string}}",
            "query-input": "required name=search_term_string"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "Scholastic Services",
            "url": "https://hvstechzw.github.io/Scholastic-Services-Web-Portal/"
        }}
    }}
    </script>
    
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Schools Directory",
        "description": "List of educational institutions",
        "url": "https://hvstechzw.github.io/Scholastic-Schools-Catalog/",
        "numberOfItems": {total_schools},
        "itemListElement": [
            {self.generate_school_schema_data(schools)}
        ]
    }}
    </script>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="canonical" href="https://hvstechzw.github.io/Scholastic-Schools-Catalog/">
    <link rel="sitemap" type="application/xml" href="https://hvstechzw.github.io/Scholastic-Schools-Catalog/sitemap.xml">
    <style>
        :root {{
            --primary: #ffffff;
            --primary-dark: #f0f0f0;
            --secondary: #6c757d;
            --accent: #6c757d;
            --dark: #212529;
            --light: #f8f9fa;
            --gray: #adb5bd;
            --gray-light: #e9ecef;
            --gray-dark: #495057;
            --white: #ffffff;
            --silver: #c0c0c0;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.05), 0 5px 10px rgba(0, 0, 0, 0.05);
            --radius: 12px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            min-height: 100vh;
        }}
        
        .container {{
            width: 100%;
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        /* Header & Navigation */
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow);
            position: sticky;
            top: 0;
            z-index: 1000;
            border-bottom: 1px solid var(--gray-light);
        }}
        
        .nav-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }}
        
        .logo-section {{
            display: flex;
            align-items: center;
            gap: 15px;
            text-decoration: none;
        }}
        
        .logo-wrapper {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .main-logo {{
            width: 100px;
            height: 100px;
            background: transparent;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--white);
            font-size: 2.5rem;
            box-shadow: var(--shadow);
            border: 2px solid var(--white);
            overflow: hidden;
        }}
        
        .main-logo img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: 10px;
        }}
        
        .logo-text {{
            display: flex;
            flex-direction: column;
        }}
        
        .main-title {{
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            font-size: 1.8rem;
            background: linear-gradient(135deg, var(--gray-dark) 0%, var(--dark) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .subtitle {{
            font-size: 0.75rem;
            color: var(--gray);
            font-weight: 500;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-top: -2px;
        }}
        
        .nav-links {{
            display: flex;
            gap: 2rem;
            align-items: center;
        }}
        
        .nav-link {{
            text-decoration: none;
            color: var(--dark);
            font-weight: 500;
            transition: var(--transition);
            padding: 0.5rem 1rem;
            border-radius: var(--radius);
            position: relative;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .nav-link:hover {{
            background: var(--gray-light);
            color: var(--dark);
            transform: translateY(-1px);
        }}
        
        .nav-link.active {{
            background: var(--white);
            color: var(--accent);
            box-shadow: var(--shadow);
        }}
        
        .nav-link.active::before {{
            content: '';
            position: absolute;
            bottom: -1px;
            left: 50%;
            transform: translateX(-50%);
            width: 20px;
            height: 3px;
            background: var(--accent);
            border-radius: 2px;
        }}
        
        .portal-link {{
            background: linear-gradient(135deg, var(--silver) 0%, var(--gray) 100%);
            color: var(--dark);
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius);
            text-decoration: none;
            font-weight: 600;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .portal-link:hover {{
            background: linear-gradient(135deg, var(--gray) 0%, var(--gray-dark) 100%);
            color: var(--white);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(108, 117, 125, 0.3);
        }}
        
        .mobile-menu-btn {{
            display: none;
            background: none;
            border: none;
            font-size: 1.5rem;
            color: var(--dark);
            cursor: pointer;
            width: 44px;
            height: 44px;
            border-radius: var(--radius);
            transition: var(--transition);
        }}
        
        .mobile-menu-btn:hover {{
            background: var(--gray-light);
        }}
        
        /* Hero Banner */
        .hero-banner {{
            position: relative;
            height: auto;
            min-height: 400px;
            max-height: 600px;
            margin: 2rem 0;
            border-radius: var(--radius);
            overflow: hidden;
            box-shadow: var(--shadow-lg);
        }}
        
        .banner-background {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(240,240,240,0.9) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }}
        
        .banner-content {{
            position: relative;
            z-index: 2;
            text-align: center;
            max-width: 800px;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(10px);
            border-radius: var(--radius);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
            margin: 1rem;
            width: calc(100% - 2rem);
        }}
        
        .banner-title {{
            font-family: 'Poppins', sans-serif;
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--gray-dark) 0%, var(--dark) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.2;
        }}
        
        .banner-subtitle {{
            font-size: clamp(1rem, 3vw, 1.2rem);
            color: var(--gray-dark);
            margin-bottom: 2rem;
            line-height: 1.6;
        }}
        
        .cta-button {{
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            padding: 1rem 2rem;
            background: linear-gradient(135deg, var(--silver) 0%, var(--gray) 100%);
            color: var(--dark);
            text-decoration: none;
            border-radius: var(--radius);
            font-weight: 600;
            font-size: 1.1rem;
            transition: var(--transition);
            box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
        }}
        
        .cta-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(108, 117, 125, 0.4);
            background: linear-gradient(135deg, var(--gray) 0%, var(--gray-dark) 100%);
            color: var(--white);
        }}
        
        /* Search & Filters */
        .search-section {{
            background: var(--white);
            padding: 2.5rem;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            margin-bottom: 3rem;
            border: 1px solid var(--gray-light);
            transition: var(--transition);
        }}
        
        .search-section:hover {{
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }}
        
        .search-box {{
            position: relative;
            margin-bottom: 2rem;
        }}
        
        .search-input {{
            width: 100%;
            padding: 1.25rem 1.25rem 1.25rem 3.5rem;
            border: 2px solid var(--gray-light);
            border-radius: var(--radius);
            font-size: 1rem;
            transition: var(--transition);
            background: var(--light);
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(108, 117, 125, 0.1);
            background: var(--white);
        }}
        
        .search-icon {{
            position: absolute;
            left: 1.25rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--gray);
            font-size: 1.2rem;
        }}
        
        .filter-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
        }}
        
        .filter-group {{
            margin-bottom: 0.5rem;
        }}
        
        .filter-label {{
            display: block;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: var(--dark);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .filter-select {{
            width: 100%;
            padding: 0.875rem;
            border: 2px solid var(--gray-light);
            border-radius: var(--radius);
            font-size: 0.95rem;
            background: var(--light);
            cursor: pointer;
            transition: var(--transition);
            appearance: none;
            background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
            background-repeat: no-repeat;
            background-position: right 1rem center;
            background-size: 1em;
        }}
        
        .filter-select:focus {{
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(108, 117, 125, 0.1);
            background: var(--white);
        }}
        
        /* Featured Schools */
        .featured-schools {{
            margin-bottom: 5rem;
        }}
        
        .featured-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 2rem;
        }}
        
        .featured-card {{
            background: var(--white);
            border-radius: var(--radius);
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: var(--transition);
            cursor: pointer;
            border: 1px solid var(--gray-light);
            position: relative;
        }}
        
        .featured-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(to right, var(--silver), var(--gray));
            z-index: 1;
        }}
        
        .featured-card:hover {{
            transform: translateY(-8px);
            box-shadow: var(--shadow-lg);
            border-color: var(--accent);
        }}
        
        .featured-card-header {{
            height: 160px;
            position: relative;
            padding: 1.5rem;
            color: var(--dark);
            overflow: hidden;
        }}
        
        .featured-banner {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.1;
        }}
        
        .featured-logo-container {{
            position: absolute;
            top: 1rem;
            left: 1rem;
            width: 80px;
            height: 80px;
            background: var(--white);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow);
            border: 3px solid var(--white);
            overflow: hidden;
            z-index: 2;
        }}
        
        .featured-logo {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: 10px;
        }}
        
        .featured-type-badge {{
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(5px);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--dark);
            border: 1px solid var(--gray-light);
            z-index: 2;
        }}
        
        .featured-card-body {{
            padding: 1.75rem;
        }}
        
        .featured-school-name {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            color: var(--dark);
            line-height: 1.3;
        }}
        
        .featured-location {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: var(--gray-dark);
            font-size: 0.9rem;
            margin-bottom: 1.25rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--gray-light);
        }}
        
        .featured-info-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        
        .featured-info-item {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 0.85rem;
            color: var(--dark);
        }}
        
        .featured-info-item i {{
            color: var(--accent);
            width: 16px;
            font-size: 1rem;
        }}
        
        .featured-rating {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
            padding: 0.75rem;
            background: var(--light);
            border-radius: var(--radius);
        }}
        
        .featured-stars {{
            color: #ffc107;
            font-size: 1.1rem;
            letter-spacing: 2px;
        }}
        
        .featured-rating-text {{
            font-size: 0.9rem;
            color: var(--gray-dark);
            font-weight: 600;
        }}
        
        .featured-view-btn {{
            display: block;
            width: 100%;
            padding: 1rem;
            background: linear-gradient(135deg, var(--white) 0%, var(--gray-light) 100%);
            color: var(--dark);
            border: 2px solid var(--gray-light);
            border-radius: var(--radius);
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            text-align: center;
            text-decoration: none;
            position: relative;
            overflow: hidden;
        }}
        
        .featured-view-btn::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: 0.5s;
        }}
        
        .featured-view-btn:hover {{
            background: linear-gradient(135deg, var(--silver) 0%, var(--gray) 100%);
            color: var(--dark);
            border-color: var(--accent);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(108, 117, 125, 0.3);
        }}
        
        .featured-view-btn:hover::before {{
            left: 100%;
        }}
        
        /* Section Header */
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .section-title {{
            font-family: 'Poppins', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: var(--dark);
            position: relative;
            padding-bottom: 0.75rem;
        }}
        
        .section-title::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 60px;
            height: 4px;
            background: linear-gradient(to right, var(--silver), transparent);
            border-radius: 2px;
        }}
        
        .schools-count {{
            color: var(--gray-dark);
            font-size: 1rem;
            font-weight: 500;
            background: var(--gray-light);
            padding: 0.5rem 1rem;
            border-radius: 20px;
        }}
        
        /* View All Section */
        .view-all-section {{
            text-align: center;
            margin: 3rem 0;
            padding: 3rem;
            background: linear-gradient(135deg, var(--white) 0%, var(--light) 100%);
            border-radius: var(--radius);
            border: 2px dashed var(--gray-light);
        }}
        
        .view-all-btn {{
            display: inline-flex;
            align-items: center;
            gap: 1rem;
            padding: 1.25rem 2.5rem;
            background: linear-gradient(135deg, var(--white) 0%, var(--gray-light) 100%);
            color: var(--dark);
            text-decoration: none;
            border-radius: var(--radius);
            font-weight: 600;
            font-size: 1.1rem;
            transition: var(--transition);
            border: 2px solid var(--gray-light);
            position: relative;
            overflow: hidden;
        }}
        
        .view-all-btn:hover {{
            background: linear-gradient(135deg, var(--dark) 0%, var(--gray-dark) 100%);
            color: var(--white);
            border-color: var(--dark);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }}
        
        .view-all-btn i {{
            transition: var(--transition);
        }}
        
        .view-all-btn:hover i {{
            transform: translateX(5px);
        }}
        
        /* Footer */
        .footer {{
            background: linear-gradient(135deg, var(--dark) 0%, #343a40 100%);
            color: var(--white);
            padding: 4rem 0 2rem;
            margin-top: 6rem;
        }}
        
        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 3rem;
            margin-bottom: 3rem;
        }}
        
        .footer-section h3 {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.3rem;
            margin-bottom: 1.5rem;
            color: var(--white);
            position: relative;
            padding-bottom: 0.75rem;
        }}
        
        .footer-section h3::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 40px;
            height: 3px;
            background: var(--silver);
            border-radius: 2px;
        }}
        
        .footer-links {{
            list-style: none;
        }}
        
        .footer-links li {{
            margin-bottom: 0.875rem;
        }}
        
        .footer-links a {{
            color: var(--gray);
            text-decoration: none;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        
        .footer-links a:hover {{
            color: var(--silver);
            padding-left: 5px;
        }}
        
        .footer-links a i {{
            width: 20px;
            font-size: 0.9rem;
        }}
        
        .social-links {{
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
        }}
        
        .social-link {{
            width: 44px;
            height: 44px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--white);
            text-decoration: none;
            transition: var(--transition);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .social-link:hover {{
            background: var(--silver);
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(192, 192, 192, 0.3);
        }}
        
        .company-info {{
            color: var(--gray);
            font-size: 0.9rem;
            line-height: 1.6;
        }}
        
        .manufacturer-logo {{
            margin-top: 1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .manufacturer-logo img {{
            height: 48px;
            width: auto;
            filter: brightness(0) invert(1);
            opacity: 0.9;
        }}
        
        .footer-bottom {{
            text-align: center;
            padding-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--gray);
            font-size: 0.9rem;
        }}
        
        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.6s ease-out forwards;
        }}
        
        /* Loading State */
        .loading {{
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 3rem;
            color: var(--gray);
        }}
        
        .spinner {{
            width: 40px;
            height: 40px;
            border: 3px solid var(--gray-light);
            border-top-color: var(--accent);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 1rem;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        /* Mobile Responsive */
        @media (max-width: 1024px) {{
            .featured-grid {{
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            }}
            
            .banner-title {{
                font-size: 2.5rem;
            }}
        }}
        
        @media (max-width: 768px) {{
            .nav-links {{
                display: none;
                position: fixed;
                top: 80px;
                left: 0;
                right: 0;
                background: var(--white);
                padding: 1rem;
                flex-direction: column;
                box-shadow: var(--shadow);
                border-radius: var(--radius);
                margin: 0 20px;
                z-index: 999;
            }}
            
            .nav-links.active {{
                display: flex;
                animation: fadeIn 0.3s ease-out;
            }}
            
            .mobile-menu-btn {{
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .hero-banner {{
                height: auto;
                min-height: 300px;
                margin: 1rem 0;
            }}
            
            .banner-title {{
                font-size: clamp(1.8rem, 4vw, 2.5rem);
                line-height: 1.2;
            }}
            
            .banner-subtitle {{
                font-size: clamp(0.9rem, 2vw, 1.1rem);
            }}
            
            .banner-content {{
                padding: 1.5rem;
                margin: 0.5rem;
                width: calc(100% - 1rem);
            }}
            
            .section-title {{
                font-size: 1.75rem;
            }}
            
            .filter-grid {{
                grid-template-columns: 1fr;
            }}
            
            .search-section {{
                padding: 1.75rem;
            }}
            
            .footer-content {{
                grid-template-columns: 1fr;
                gap: 2rem;
            }}
            
            .logo-wrapper {{
                flex-direction: column;
                align-items: flex-start;
                gap: 5px;
            }}
            
            .main-logo {{
                width: 80px;
                height: 80px;
            }}
        }}
        
        @media (max-width: 480px) {{
            .container {{
                padding: 0 15px;
            }}
            
            .banner-title {{
                font-size: 1.8rem;
            }}
            
            .section-title {{
                font-size: 1.5rem;
            }}
            
            .featured-grid {{
                grid-template-columns: 1fr;
            }}
            
            .nav-container {{
                padding: 0.75rem 0;
            }}
            
            .main-title {{
                font-size: 1.4rem;
            }}
            
            .main-logo {{
                width: 70px;
                height: 70px;
            }}
            
            .footer {{
                padding: 3rem 0 1.5rem;
            }}
            
            .view-all-btn {{
                padding: 1rem 1.5rem;
                font-size: 1rem;
            }}
            
            .featured-logo-container {{
                width: 70px;
                height: 70px;
            }}
            
            .manufacturer-logo img {{
                height: 40px;
            }}
        }}
        
        /* Interactive Elements */
        .interactive-card {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .interactive-card:hover {{
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }}
        
        .pulse {{
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        
        /* Scroll to Top */
        .scroll-top {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 50px;
            height: 50px;
            background: var(--silver);
            color: var(--dark);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
            z-index: 1000;
            box-shadow: 0 4px 15px rgba(192, 192, 192, 0.3);
        }}
        
        .scroll-top.visible {{
            opacity: 1;
            visibility: visible;
        }}
        
        .scroll-top:hover {{
            background: var(--gray);
            transform: translateY(-3px);
        }}
    </style>
</head>
<body itemscope itemtype="https://schema.org/WebPage">
    <!-- Header -->
    <header class="header">
        <div class="container">
            <nav class="nav-container">
                <div class="logo-wrapper">
                    <a href="index.html" class="logo-section" itemprop="url">
                        <div class="main-logo" style="background: transparent;">
                            <img id="theme-logo" src="assets/images/logo_light.png" alt="Scholastic Forum" itemprop="logo">
                        </div>
                        <div class="logo-text">
                            <div class="main-title" itemprop="name">Scholastic Forum</div>
                            <div class="subtitle">Academic Elegance and Efficiency</div>
                        </div>
                    </a>
                </div>
                
                <div class="nav-links" id="navLinks">
                    <a href="index.html" class="nav-link active">
                        <i class="fas fa-home"></i> Home
                    </a>
                    <a href="#schools" class="nav-link">
                        <i class="fas fa-school"></i> Schools
                    </a>
                    <a href="#about" class="nav-link">
                        <i class="fas fa-info-circle"></i> About
                    </a>
                    <a href="#contact" class="nav-link">
                        <i class="fas fa-envelope"></i> Contact
                    </a>
                    <a href="schools/all.html" class="nav-link" style="background: var(--silver); color: var(--dark);">
                        <i class="fas fa-eye"></i> View All
                    </a>
                    <a href="https://hvstechzw.github.io/Scholastic-Services-Web-Portal/" class="portal-link" target="_blank">
                        <i class="fas fa-external-link-alt"></i> Portal
                    </a>
                </div>
                
                <button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="Toggle navigation menu">
                    <i class="fas fa-bars"></i>
                </button>
            </nav>
        </div>
    </header>

    <!-- Hero Banner -->
    <section class="hero-banner" itemprop="mainContentOfPage">
        <div class="banner-background">
            <div class="banner-content">
                <h1 class="banner-title" itemprop="headline">Discover Excellence in Education</h1>
                <p class="banner-subtitle" itemprop="description">
                    Scholastic Forum brings you comprehensive insights into educational institutions. 
                    Explore detailed profiles, compare facilities, and make informed decisions for your educational journey.
                </p>
                <a href="#schools" class="cta-button pulse" itemprop="significantLink">
                    <i class="fas fa-search"></i> Explore Schools
                </a>
            </div>
        </div>
    </section>

    <!-- Main Content -->
    <main class="container">
        <!-- Search & Filters -->
        <section class="search-section fade-in" id="search">
            <div class="search-box">
                <i class="fas fa-search search-icon"></i>
                <input type="text" class="search-input" id="searchInput" 
                       placeholder="Search schools by name, location, curriculum, or type..."
                       aria-label="Search schools">
            </div>
            
            <div class="filter-grid">
                <div class="filter-group">
                    <label class="filter-label" for="levelFilter">Education Level</label>
                    <select class="filter-select" id="levelFilter">
                        <option value="all">All Levels</option>
                        <option value="Pre-School">Pre-School</option>
                        <option value="Primary">Primary</option>
                        <option value="Secondary">Secondary</option>
                        <option value="High School">High School</option>
                        <option value="College">College</option>
                        <option value="University">University</option>
                        <option value="Mixed">Mixed</option>
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label" for="typeFilter">School Type</label>
                    <select class="filter-select" id="typeFilter">
                        <option value="all">All Types</option>
                        <option value="Day">Day School</option>
                        <option value="Boarding">Boarding School</option>
                        <option value="Mixed">Mixed</option>
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label" for="genderFilter">Gender Focus</label>
                    <select class="filter-select" id="genderFilter">
                        <option value="all">All Genders</option>
                        <option value="Mixed">Mixed</option>
                        <option value="Boys Only">Boys Only</option>
                        <option value="Girls Only">Girls Only</option>
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label" for="curriculumFilter">Curriculum System</label>
                    <select class="filter-select" id="curriculumFilter">
                        <option value="all">All Curricula</option>
                        <option value="Competence-Based Learning">Competence-Based</option>
                        <option value="Heritage-Based Education">Heritage-Based</option>
                        <option value="STEM Bias">STEM Focus</option>
                        <option value="British">British Curriculum</option>
                        <option value="American">American Curriculum</option>
                        <option value="International Baccalaureate">IB Program</option>
                    </select>
                </div>
            </div>
        </section>

        <!-- Featured Schools -->
        <section class="featured-schools" id="schools" itemscope itemtype="https://schema.org/ItemList">
            <div class="section-header">
                <h2 class="section-title" itemprop="name">Featured Educational Institutions</h2>
                <div class="schools-count" id="schoolsCount">
                    Showing {min(12, total_schools)} of {total_schools} institutions
                </div>
            </div>
            
            <div class="featured-grid" id="schoolsGrid" itemprop="itemListElement">
"""
        
        for school in schools[:12]:
            amenities_sample = school.get('amenities', [])[:3]
            rating = school.get('overall_rating', 0)
            stars_html = self.generate_stars_html(rating)
            est_year = school.get('establishment_year', '2025')
            
            banner_html = ''
            if school.get('banner_base64'):
                banner_html = f'<img src="data:image/jpeg;base64,{school["banner_base64"]}" alt="{school["name"]} Banner" class="featured-banner">'
            
            logo_html = ''
            if school.get('logo_base64'):
                logo_html = f'<img src="data:image/jpeg;base64,{school["logo_base64"]}" alt="{school["name"]} Logo" class="featured-logo">'
            
            html += f"""
                <div class="featured-card interactive-card" data-school-id="{school['school_id']}" 
                     data-level="{school.get('level', '')}"
                     data-type="{school.get('school_type', '')}"
                     data-gender="{school.get('gender_focus', '')}"
                     data-curriculum="{school.get('curriculum', '')}"
                     data-rating="{rating}"
                     data-search="{school['name'].lower()} {school.get('city', '').lower()} {school.get('province', '').lower()} {school.get('curriculum', '').lower()}"
                     itemprop="itemListElement" itemscope itemtype="https://schema.org/EducationalOrganization">
                    <div class="featured-card-header">
                        {banner_html}
                        <div class="featured-logo-container">
                            {logo_html if school.get('logo_base64') else '<i class="fas fa-school"></i>'}
                        </div>
                        <div class="featured-type-badge">{school.get('school_type', '')}</div>
                    </div>
                    <div class="featured-card-body">
                        <h3 class="featured-school-name" itemprop="name">{school['name']}</h3>
                        <div class="featured-location" itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">
                            <i class="fas fa-map-marker-alt"></i>
                            <span itemprop="addressLocality">{school.get('city', '')}</span>, 
                            <span itemprop="addressRegion">{school.get('province', '')}</span>
                        </div>
                        
                        <div class="featured-info-grid">
                            <div class="featured-info-item">
                                <i class="fas fa-graduation-cap"></i>
                                <span itemprop="educationalLevel">{school.get('level', 'N/A')}</span>
                            </div>
                            <div class="featured-info-item">
                                <i class="fas fa-users"></i>
                                <span itemprop="numberOfStudents">{school.get('total_students', 0):,} Students</span>
                            </div>
                            <div class="featured-info-item">
                                <i class="fas fa-chalkboard-teacher"></i>
                                <span itemprop="numberOfEmployees">{school.get('total_teachers', 0):,} Staff</span>
                            </div>
                            <div class="featured-info-item">
                                <i class="fas fa-calendar-star"></i>
                                <span itemprop="foundingDate">Est. {est_year}</span>
                            </div>
                        </div>
                        
                        {f'<div class="featured-rating" itemprop="aggregateRating" itemscope itemtype="https://schema.org/AggregateRating"><meta itemprop="ratingValue" content="{rating:.1f}"><meta itemprop="reviewCount" content="{school.get('total_reviews', 0)}"><div class="featured-stars">{stars_html}</div><span class="featured-rating-text">{rating:.1f}/5.0</span></div>' if rating > 0 else ''}
                        
                        <a href="schools/{school['school_id']}.html" class="featured-view-btn" itemprop="url">
                            <i class="fas fa-external-link-alt"></i> View Complete Profile
                        </a>
                    </div>
                </div>
"""
        
        html += f"""
            </div>
            
            <div class="view-all-section fade-in">
                <h3 style="margin-bottom: 1.5rem; color: var(--dark); font-size: 1.5rem;">Explore Complete School Directory</h3>
                <p style="color: var(--gray-dark); margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                    Browse through our comprehensive database of {total_schools} educational institutions with detailed profiles, facilities information, and reviews.
                </p>
                <a href="schools/all.html" class="view-all-btn">
                    <i class="fas fa-list-alt"></i> View All Schools ({total_schools} Total)
                    <i class="fas fa-arrow-right"></i>
                </a>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="footer" itemprop="publisher" itemscope itemtype="https://schema.org/Organization">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Scholastic Forum</h3>
                    <p class="company-info">
                        Part of the <span style="color: var(--silver);">Scholastic Services</span> suite by 
                        <span style="color: var(--silver);">High Voltage Software Technologies</span>. 
                        Empowering educational institutions with comprehensive management solutions.
                    </p>
                    <div class="manufacturer-logo">
                        <img src="assets/images/manufacturer_dark.png" alt="High Voltage Software Technologies" itemprop="logo">
                    </div>
                    <div class="social-links">
                        <a href="#" class="social-link" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                        <a href="#" class="social-link" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="social-link" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                        <a href="#" class="social-link" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                        <a href="#" class="social-link" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
                    </div>
                </div>
                
                <div class="footer-section">
                    <h3>Quick Access</h3>
                    <ul class="footer-links">
                        <li><a href="index.html"><i class="fas fa-home"></i> Home</a></li>
                        <li><a href="schools/all.html"><i class="fas fa-school"></i> Schools Directory</a></li>
                        <li><a href="https://hvstechzw.github.io/Scholastic-Services-Web-Portal/" target="_blank"><i class="fas fa-info-circle"></i> About Scholastic Services</a></li>
                        <li><a href="#contact"><i class="fas fa-envelope"></i> Contact Support</a></li>
                        <li><a href="#faq"><i class="fas fa-question-circle"></i> Help & FAQ</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h3>Contact Information</h3>
                    <ul class="footer-links">
                        <li><a href="mailto:support@scholasticforum.org"><i class="fas fa-envelope"></i> support@scholasticforum.org</a></li>
                        <li><a href="tel:+263123456789"><i class="fas fa-phone"></i> +263 123 456 789</a></li>
                        <li><a href="#" itemprop="address" itemscope itemtype="https://schema.org/PostalAddress"><i class="fas fa-map-marker-alt"></i> Harare, Zimbabwe</a></li>
                        <li><a href="#" itemprop="name"><i class="fas fa-building"></i> High Voltage Software Technologies</a></li>
                        <li><a href="https://hvstechzw.github.io/Scholastic-Services-Web-Portal/" target="_blank"><i class="fas fa-globe"></i> Scholastic Services Portal</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; <span itemprop="copyrightYear">2025</span> Scholastic Forum | A Scholastic Services Product | Powered by High Voltage Software Technologies</p>
                <p style="margin-top: 0.5rem; font-size: 0.8rem;">Comprehensive School Directory & Management System</p>
            </div>
        </div>
    </footer>

    <!-- Scroll to Top -->
    <a href="#" class="scroll-top" id="scrollTop" aria-label="Scroll to top">
        <i class="fas fa-chevron-up"></i>
    </a>

    <!-- JavaScript -->
    <script>
        // Force light theme
        document.documentElement.setAttribute('data-theme', 'light');
        document.body.style.colorScheme = 'light';
        
        // Mobile Menu Toggle
        const mobileMenuBtn = document.getElementById('mobileMenuBtn');
        const navLinks = document.getElementById('navLinks');
        
        mobileMenuBtn.addEventListener('click', function(e) {{
            e.preventDefault();
            e.stopPropagation();
            navLinks.classList.toggle('active');
            this.setAttribute('aria-expanded', navLinks.classList.contains('active'));
            this.innerHTML = navLinks.classList.contains('active') 
                ? '<i class="fas fa-times"></i>' 
                : '<i class="fas fa-bars"></i>';
        }});
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {{
            if (!navLinks.contains(e.target) && !mobileMenuBtn.contains(e.target)) {{
                navLinks.classList.remove('active');
                mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
            }}
        }});
        
        // Close mobile menu when clicking a link
        document.querySelectorAll('.nav-link').forEach(link => {{
            link.addEventListener('click', function() {{
                navLinks.classList.remove('active');
                mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
            }});
        }});
        
        // Search and Filter Functionality
        const searchInput = document.getElementById('searchInput');
        const levelFilter = document.getElementById('levelFilter');
        const typeFilter = document.getElementById('typeFilter');
        const genderFilter = document.getElementById('genderFilter');
        const curriculumFilter = document.getElementById('curriculumFilter');
        const schoolCards = document.querySelectorAll('.featured-card');
        const schoolsCount = document.getElementById('schoolsCount');
        
        function filterSchools() {{
            const searchTerm = searchInput.value.toLowerCase().trim();
            const levelValue = levelFilter.value;
            const typeValue = typeFilter.value;
            const genderValue = genderFilter.value;
            const curriculumValue = curriculumFilter.value;
            
            let visibleCount = 0;
            
            schoolCards.forEach(card => {{
                const searchData = card.getAttribute('data-search');
                const level = card.getAttribute('data-level');
                const type = card.getAttribute('data-type');
                const gender = card.getAttribute('data-gender');
                const curriculum = card.getAttribute('data-curriculum');
                const rating = parseFloat(card.getAttribute('data-rating'));
                
                const matchesSearch = searchTerm === '' || searchData.includes(searchTerm);
                const matchesLevel = levelValue === 'all' || level === levelValue;
                const matchesType = typeValue === 'all' || type === typeValue;
                const matchesGender = genderValue === 'all' || gender === genderValue;
                const matchesCurriculum = curriculumValue === 'all' || curriculum === curriculumValue;
                
                if (matchesSearch && matchesLevel && matchesType && matchesGender && matchesCurriculum) {{
                    card.style.display = 'block';
                    card.classList.add('fade-in');
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                    card.classList.remove('fade-in');
                }}
            }});
            
            schoolsCount.textContent = `Showing ${{visibleCount}} of {total_schools} institutions`;
            
            if (visibleCount === 0 && searchTerm) {{
                schoolsCount.innerHTML = `<div class="loading"><div class="spinner"></div>No matching schools found</div>`;
            }}
        }}
        
        // Add event listeners with debouncing
        let searchTimeout;
        searchInput.addEventListener('input', function() {{
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(filterSchools, 300);
        }});
        
        levelFilter.addEventListener('change', filterSchools);
        typeFilter.addEventListener('change', filterSchools);
        genderFilter.addEventListener('change', filterSchools);
        curriculumFilter.addEventListener('change', filterSchools);
        
        // Clear filters
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape' && searchInput.value) {{
                searchInput.value = '';
                filterSchools();
            }}
        }});
        
        // School Card Click
        schoolCards.forEach(card => {{
            card.addEventListener('click', function(e) {{
                if (!e.target.classList.contains('featured-view-btn') && !e.target.closest('.featured-view-btn')) {{
                    const schoolId = this.getAttribute('data-school-id');
                    window.location.href = `schools/${{schoolId}}.html`;
                }}
            }});
            
            // Keyboard navigation for cards
            card.addEventListener('keydown', function(e) {{
                if (e.key === 'Enter' || e.key === ' ') {{
                    e.preventDefault();
                    const schoolId = this.getAttribute('data-school-id');
                    window.location.href = `schools/${{schoolId}}.html`;
                }}
            }});
            
            // Make cards focusable
            card.setAttribute('tabindex', '0');
        }});
        
        // Smooth Scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                if (this.getAttribute('href') === '#') return;
                
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});
        
        // Scroll to Top
        const scrollTop = document.getElementById('scrollTop');
        window.addEventListener('scroll', function() {{
            if (window.pageYOffset > 300) {{
                scrollTop.classList.add('visible');
            }} else {{
                scrollTop.classList.remove('visible');
            }}
        }});
        
        scrollTop.addEventListener('click', function(e) {{
            e.preventDefault();
            window.scrollTo({{
                top: 0,
                behavior: 'smooth'
            }});
        }});
        
        // Initialize filters
        document.addEventListener('DOMContentLoaded', function() {{
            filterSchools();
            
            // Add fade-in animation
            const elements = document.querySelectorAll('.fade-in');
            elements.forEach((el, index) => {{
                el.style.animationDelay = `${{index * 0.1}}s`;
            }});
            
            // Add keyboard navigation
            document.addEventListener('keydown', function(e) {{
                // Escape to close mobile menu
                if (e.key === 'Escape' && navLinks.classList.contains('active')) {{
                    navLinks.classList.remove('active');
                    mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
                    mobileMenuBtn.setAttribute('aria-expanded', 'false');
                }}
                
                // Focus search on Ctrl+K or /
                if ((e.ctrlKey || e.metaKey) && e.key === 'k') {{
                    e.preventDefault();
                    searchInput.focus();
                }}
                
                if (e.key === '/' && document.activeElement !== searchInput) {{
                    e.preventDefault();
                    searchInput.focus();
                }}
            }});
        }});
        
        // Add real-time search feedback
        searchInput.addEventListener('input', function() {{
            if (this.value.length > 0) {{
                this.style.background = 'var(--white)';
                this.style.borderColor = 'var(--accent)';
            }} else {{
                this.style.background = 'var(--light)';
                this.style.borderColor = 'var(--gray-light)';
            }}
        }});
    </script>
</body>
</html>
"""
        
        return html
    
    def generate_school_schema_data(self, schools):
        """Generate schema.org data for SEO"""
        schema_items = []
        for i, school in enumerate(schools[:5], 1):
            schema_item = f"""
            {{
                "@type": "ListItem",
                "position": {i},
                "item": {{
                    "@type": "EducationalOrganization",
                    "name": "{school['name']}",
                    "description": "{school.get('description', 'Educational institution').replace('"', '\\"')[:200]}",
                    "url": "https://hvstechzw.github.io/Scholastic-Schools-Catalog/schools/{school['school_id']}.html"
                }}
            }}"""
            schema_items.append(schema_item)
        
        return ',\n            '.join(schema_items)
    
    def generate_stars_html(self, rating):
        """Generate star rating HTML"""
        full_stars = int(rating)
        half_star = 1 if rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        
        stars = '★' * full_stars + '☆' * empty_stars
        if half_star:
            stars = '★' * full_stars + '⯪' + '☆' * empty_stars
        
        return stars
    
    def generate_school_pages(self, schools):
        """Generate individual school detail pages"""
        os.makedirs("schools", exist_ok=True)
        
        for school in schools:
            html = self.generate_school_page(school)
            filename = f"schools/{school['school_id']}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Generated: {filename}")
    
    def generate_school_page(self, school):
        """Generate a detailed school page with SEO"""
        rating = school.get('overall_rating', 0)
        stars_html = self.generate_stars_html(rating)
        amenities = school.get('amenities', [])
        social_links = school.get('social_links', {})
        est_year = school.get('establishment_year', '2025')
        total_schools = len(self.get_schools_data()) if hasattr(self, '_schools_cache') else 0
        
        html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO Meta Tags for School Page -->
    <title>{school['name']} - School Profile | Scholastic Forum</title>
    <meta name="description" content="{school.get('description', school.get('mission', 'Detailed profile of ' + school['name'] + ' educational institution. Find information about curriculum, facilities, location, and contact details.'))[:155]}">
    <meta name="keywords" content="{school['name']}, {school.get('city', '')} schools, {school.get('province', '')} education, {school.get('curriculum', '')} curriculum, {school.get('level', '')} school">
    <meta name="author" content="Scholastic Services">
    
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://hvstechzw.github.io/Scholastic-Schools-Catalog/schools/{school['school_id']}.html">
    <meta property="og:title" content="{school['name']} - School Profile">
    <meta property="og:description" content="{school.get('description', 'View complete school profile including facilities, curriculum, and contact information.')[:200]}">
    <meta property="og:image" content="https://hvstechzw.github.io/Scholastic-Schools-Catalog/assets/images/schools/{school['school_id']}.jpg">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "name": "{school['name']}",
        "description": "{school.get('description', 'Educational institution in ' + school.get('city', '') + ', ' + school.get('province', '')).replace('"', '\\"')}",
        "url": "https://hvstechzw.github.io/Scholastic-Schools-Catalog/schools/{school['school_id']}.html",
        "address": {{
            "@type": "PostalAddress",
            "streetAddress": "{school.get('address', '')}",
            "addressLocality": "{school.get('city', '')}",
            "addressRegion": "{school.get('province', '')}",
            "postalCode": "{school.get('postal_code', '')}",
            "addressCountry": "{school.get('country', 'ZW')}"
        }},
        "telephone": "{school.get('phone_primary', school.get('phone', ''))}",
        "email": "{school.get('email', '')}",
        "foundingDate": "{est_year}",
        "numberOfStudents": {school.get('total_students', 0)},
        "numberOfEmployees": {school.get('total_teachers', 0)},
        "educationalLevel": "{school.get('level', '')}",
        "curriculum": "{school.get('curriculum', '')}"
        {f', "aggregateRating": {{"@type": "AggregateRating", "ratingValue": "{rating}", "reviewCount": "{school.get('total_reviews', 0)}"}}' if rating > 0 else ''}
    }}
    </script>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="canonical" href="https://hvstechzw.github.io/Scholastic-Schools-Catalog/schools/{school['school_id']}.html">
    <style>
        :root {{
            --primary: #ffffff;
            --primary-dark: #f0f0f0;
            --secondary: #6c757d;
            --accent: #6c757d;
            --dark: #212529;
            --light: #f8f9fa;
            --gray: #adb5bd;
            --gray-light: #e9ecef;
            --gray-dark: #495057;
            --white: #ffffff;
            --silver: #c0c0c0;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.05), 0 5px 10px rgba(0, 0, 0, 0.05);
            --radius: 12px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            min-height: 100vh;
        }}
        
        .container {{
            width: 100%;
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        /* Header */
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow);
            position: sticky;
            top: 0;
            z-index: 1000;
            border-bottom: 1px solid var(--gray-light);
        }}
        
        .nav-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }}
        
        .logo-section {{
            display: flex;
            align-items: center;
            gap: 15px;
            text-decoration: none;
        }}
        
        .logo-wrapper {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .main-logo {{
            width: 100px;
            height: 100px;
            background: transparent;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--white);
            font-size: 2.5rem;
            box-shadow: var(--shadow);
            border: 2px solid var(--white);
        }}
        
        .main-logo img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: 5px;
        }}
        
        .logo-text {{
            display: flex;
            flex-direction: column;
        }}
        
        .main-title {{
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            font-size: 1.5rem;
            background: linear-gradient(135deg, var(--gray-dark) 0%, var(--dark) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .subtitle {{
            font-size: 0.75rem;
            color: var(--gray);
            font-weight: 500;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-top: -2px;
        }}
        
        .back-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, var(--white) 0%, var(--gray-light) 100%);
            border: 2px solid var(--gray-light);
            border-radius: var(--radius);
            color: var(--dark);
            text-decoration: none;
            font-weight: 600;
            transition: var(--transition);
        }}
        
        .back-btn:hover {{
            background: linear-gradient(135deg, var(--silver) 0%, var(--gray) 100%);
            color: var(--dark);
            border-color: var(--silver);
            transform: translateX(-5px);
            box-shadow: 0 5px 15px rgba(192, 192, 192, 0.3);
        }}
        
        /* School Header */
        .school-header {{
            background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(240,240,240,0.9) 100%);
            padding: 3rem 0;
            margin-bottom: 3rem;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
            border: 1px solid var(--gray-light);
        }}
        
        .school-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(to right, var(--silver), var(--gray));
        }}
        
        .school-basic-info {{
            display: flex;
            align-items: center;
            gap: 3rem;
            margin-bottom: 3rem;
            flex-wrap: wrap;
        }}
        
        .school-logo-container {{
            flex-shrink: 0;
            position: relative;
        }}
        
        .school-logo {{
            width: 150px;
            height: 150px;
            background: var(--white);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--silver);
            box-shadow: var(--shadow-lg);
            border: 3px solid var(--white);
            overflow: hidden;
            transition: var(--transition);
        }}
        
        .school-logo:hover {{
            transform: scale(1.05);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
        }}
        
        .school-logo img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: 15px;
        }}
        
        .logo-badge {{
            position: absolute;
            bottom: -10px;
            right: -10px;
            background: var(--silver);
            color: var(--dark);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            box-shadow: 0 4px 10px rgba(192, 192, 192, 0.3);
            border: 3px solid var(--white);
        }}
        
        .school-title-section {{
            flex: 1;
            min-width: 300px;
        }}
        
        .school-title-section h1 {{
            font-family: 'Poppins', sans-serif;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
            color: var(--dark);
            line-height: 1.2;
        }}
        
        .school-motto {{
            font-style: italic;
            font-size: 1.2rem;
            color: var(--accent);
            margin-bottom: 1.5rem;
            font-weight: 500;
            padding-left: 1rem;
            border-left: 3px solid var(--silver);
        }}
        
        .school-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-top: 1.5rem;
        }}
        
        .school-tag {{
            background: var(--white);
            padding: 0.5rem 1.25rem;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--dark);
            border: 2px solid var(--gray-light);
            transition: var(--transition);
        }}
        
        .school-tag:hover {{
            border-color: var(--silver);
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(192, 192, 192, 0.2);
        }}
        
        .school-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 2rem;
            background: rgba(255, 255, 255, 0.7);
            padding: 2rem;
            border-radius: var(--radius);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .stat-item {{
            text-align: center;
            padding: 1.5rem;
            background: var(--white);
            border-radius: var(--radius);
            transition: var(--transition);
            border: 1px solid var(--gray-light);
        }}
        
        .stat-item:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
            border-color: var(--silver);
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            color: var(--accent);
            background: linear-gradient(135deg, var(--silver), var(--gray));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: var(--gray-dark);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* Main Content */
        .main-content {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 3rem;
            margin-bottom: 5rem;
        }}
        
        @media (min-width: 1200px) {{
            .main-content {{
                grid-template-columns: 2fr 1fr;
            }}
        }}
        
        /* Sections */
        .section {{
            background: var(--white);
            border-radius: var(--radius);
            padding: 2.5rem;
            box-shadow: var(--shadow);
            border: 1px solid var(--gray-light);
            transition: var(--transition);
        }}
        
        .section:hover {{
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }}
        
        .section-title {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--silver);
            color: var(--dark);
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .section-title i {{
            color: var(--accent);
            background: linear-gradient(135deg, var(--silver), var(--gray));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        /* Info Grid */
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 2rem;
        }}
        
        .info-item {{
            margin-bottom: 1.5rem;
        }}
        
        .info-label {{
            font-weight: 700;
            color: var(--gray-dark);
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .info-label i {{
            color: var(--silver);
        }}
        
        .info-value {{
            font-size: 1.1rem;
            color: var(--dark);
            line-height: 1.6;
            padding-left: 1.5rem;
        }}
        
        /* Amenities */
        .amenities-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 1.5rem;
        }}
        
        .amenity {{
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1.25rem;
            background: var(--light);
            border-radius: var(--radius);
            transition: var(--transition);
            border: 1px solid var(--gray-light);
        }}
        
        .amenity:hover {{
            background: linear-gradient(135deg, var(--silver) 0%, var(--gray) 100%);
            color: var(--dark);
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(192, 192, 192, 0.3);
            border-color: var(--silver);
        }}
        
        .amenity i {{
            font-size: 1.5rem;
            width: 40px;
            height: 40px;
            background: var(--white);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: var(--transition);
        }}
        
        .amenity:hover i {{
            background: rgba(255, 255, 255, 0.2);
            color: var(--dark);
            transform: scale(1.1);
        }}
        
        /* Rating */
        .rating-container {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}
        
        .rating-main {{
            display: flex;
            align-items: center;
            gap: 2rem;
            padding: 2rem;
            background: linear-gradient(135deg, var(--light) 0%, var(--white) 100%);
            border-radius: var(--radius);
            border: 1px solid var(--gray-light);
        }}
        
        .rating-stars {{
            color: #ffc107;
            font-size: 2rem;
            letter-spacing: 3px;
        }}
        
        .rating-numbers {{
            flex: 1;
        }}
        
        .rating-value {{
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--dark);
            line-height: 1;
        }}
        
        .rating-count {{
            color: var(--gray-dark);
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }}
        
        .rating-breakdown {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        .rating-bar {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .rating-label {{
            width: 100px;
            font-size: 0.9rem;
            color: var(--gray-dark);
            font-weight: 600;
        }}
        
        .bar-container {{
            flex: 1;
            height: 8px;
            background: var(--gray-light);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .bar-fill {{
            height: 100%;
            background: linear-gradient(to right, var(--silver), var(--gray));
            border-radius: 4px;
            transition: width 1s ease-out;
        }}
        
        /* Contact */
        .contact-methods {{
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }}
        
        .contact-method {{
            display: flex;
            align-items: center;
            gap: 1.5rem;
            padding: 1.5rem;
            background: var(--light);
            border-radius: var(--radius);
            text-decoration: none;
            color: var(--dark);
            transition: var(--transition);
            border: 1px solid var(--gray-light);
        }}
        
        .contact-method:hover {{
            background: linear-gradient(135deg, var(--silver) 0%, var(--gray) 100%);
            color: var(--dark);
            transform: translateX(10px);
            box-shadow: 0 8px 20px rgba(192, 192, 192, 0.3);
            border-color: var(--silver);
        }}
        
        .contact-icon {{
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--white) 0%, var(--gray-light) 100%);
            color: var(--dark);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            transition: var(--transition);
            flex-shrink: 0;
        }}
        
        .contact-method:hover .contact-icon {{
            background: rgba(255, 255, 255, 0.2);
            color: var(--dark);
            transform: scale(1.1);
        }}
        
        .contact-details h4 {{
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }}
        
        .contact-details p {{
            font-size: 0.9rem;
            opacity: 0.8;
        }}
        
        /* Social Links */
        .social-links {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(60px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }}
        
        .social-link {{
            width: 60px;
            height: 60px;
            background: var(--light);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--dark);
            text-decoration: none;
            transition: var(--transition);
            border: 2px solid var(--gray-light);
            font-size: 1.5rem;
        }}
        
        .social-link:hover {{
            background: linear-gradient(135deg, var(--silver) 0%, var(--gray) 100%);
            color: var(--dark);
            transform: translateY(-5px) scale(1.1);
            box-shadow: 0 10px 25px rgba(192, 192, 192, 0.3);
            border-color: var(--silver);
        }}
        
        /* Location Frame */
        .location-frame {{
            background: linear-gradient(135deg, var(--light) 0%, var(--white) 100%);
            border-radius: var(--radius);
            overflow: hidden;
            margin-top: 1rem;
            border: 1px solid var(--gray-light);
            min-height: 250px;
            display: flex;
            flex-direction: column;
        }}
        
        .location-header {{
            padding: 1.5rem;
            background: var(--white);
            border-bottom: 1px solid var(--gray-light);
        }}
        
        .location-header h4 {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--dark);
            margin-bottom: 0.5rem;
        }}
        
        .location-address {{
            color: var(--gray-dark);
            font-size: 0.9rem;
        }}
        
        .map-placeholder {{
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, var(--silver) 0%, var(--gray) 100%);
            color: var(--dark);
            padding: 2rem;
            text-align: center;
            min-height: 200px;
        }}
        
        .map-placeholder i {{
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.9;
        }}
        
        .map-placeholder a {{
            color: var(--dark);
            text-decoration: none;
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50px;
            margin-top: 1rem;
            transition: var(--transition);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .map-placeholder a:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }}
        
        /* Quick Facts */
        .quick-facts {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1.5rem;
        }}
        
        .fact {{
            text-align: center;
            padding: 1.5rem;
            background: var(--light);
            border-radius: var(--radius);
            transition: var(--transition);
            border: 1px solid var(--gray-light);
        }}
        
        .fact:hover {{
            background: linear-gradient(135deg, var(--silver) 0%, var(--gray) 100%);
            color: var(--dark);
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(192, 192, 192, 0.3);
        }}
        
        .fact-icon {{
            font-size: 2rem;
            margin-bottom: 1rem;
            color: var(--silver);
            transition: var(--transition);
        }}
        
        .fact:hover .fact-icon {{
            color: var(--dark);
            transform: scale(1.1);
        }}
        
        .fact-text {{
            font-size: 0.9rem;
            font-weight: 600;
        }}
        
        /* Footer */
        .footer {{
            background: linear-gradient(135deg, var(--dark) 0%, #343a40 100%);
            color: var(--white);
            padding: 3rem 0 1.5rem;
            margin-top: 6rem;
        }}
        
        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        .footer-section h3 {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
            color: var(--white);
        }}
        
        .footer-links {{
            list-style: none;
        }}
        
        .footer-links li {{
            margin-bottom: 0.75rem;
        }}
        
        .footer-links a {{
            color: var(--gray);
            text-decoration: none;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        
        .footer-links a:hover {{
            color: var(--silver);
            padding-left: 5px;
        }}
        
        .footer-bottom {{
            text-align: center;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--gray);
            font-size: 0.9rem;
        }}
        
        .manufacturer-logo {{
            margin-top: 1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .manufacturer-logo img {{
            height: 48px;
            width: auto;
            filter: brightness(0) invert(1);
            opacity: 0.9;
        }}
        
        /* Responsive */
        @media (max-width: 992px) {{
            .school-basic-info {{
                flex-direction: column;
                text-align: center;
                gap: 2rem;
            }}
            
            .school-tags {{
                justify-content: center;
            }}
            
            .amenities-grid {{
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            }}
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 0 15px;
            }}
            
            .school-header {{
                padding: 2rem 0;
            }}
            
            .school-title-section h1 {{
                font-size: 2rem;
            }}
            
            .section {{
                padding: 1.75rem;
            }}
            
            .school-stats {{
                grid-template-columns: repeat(2, 1fr);
                gap: 1rem;
            }}
            
            .rating-main {{
                flex-direction: column;
                text-align: center;
                gap: 1rem;
            }}
            
            .info-grid {{
                grid-template-columns: 1fr;
            }}
            
            .location-frame {{
                min-height: 200px;
            }}
            
            .main-logo {{
                width: 80px;
                height: 80px;
            }}
        }}
        
        @media (max-width: 480px) {{
            .container {{
                padding: 0 10px;
            }}
            
            .school-title-section h1 {{
                font-size: 1.75rem;
            }}
            
            .section {{
                padding: 1.25rem;
            }}
            
            .school-stats {{
                grid-template-columns: 1fr;
            }}
            
            .amenities-grid {{
                grid-template-columns: 1fr;
            }}
            
            .school-logo {{
                width: 120px;
                height: 120px;
            }}
            
            .location-frame {{
                min-height: 180px;
            }}
            
            .main-logo {{
                width: 70px;
                height: 70px;
            }}
            
            .manufacturer-logo img {{
                height: 40px;
            }}
        }}
        
        /* Animations */
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateX(-20px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        .slide-in {{
            animation: slideIn 0.6s ease-out forwards;
        }}
        
        /* Interactive Elements */
        .interactive-stat {{
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .interactive-stat:hover {{
            transform: scale(1.05);
        }}
    </style>
</head>
<body itemscope itemtype="https://schema.org/WebPage">
    <!-- Force light theme -->
    <script>document.documentElement.setAttribute('data-theme', 'light');</script>
    
    <!-- Header -->
    <header class="header">
        <div class="container">
            <nav class="nav-container">
                <div class="logo-wrapper">
                    <a href="../index.html" class="logo-section">
                        <div class="main-logo" style="background: transparent;">
                            <img id="theme-logo" src="../assets/images/logo_light.png" alt="Scholastic Forum">
                        </div>
                        <div class="logo-text">
                            <div class="main-title">Scholastic Forum</div>
                            <div class="subtitle">School Profile</div>
                        </div>
                    </a>
                </div>
                <a href="../index.html" class="back-btn">
                    <i class="fas fa-arrow-left"></i>
                    Back to Directory
                </a>
            </nav>
        </div>
    </header>

    <!-- School Header -->
    <section class="school-header" itemprop="mainEntity" itemscope itemtype="https://schema.org/EducationalOrganization">
        <div class="container">
            <div class="school-basic-info slide-in">
                <div class="school-logo-container">
                    <div class="school-logo">
                        {'<img src="data:image/jpeg;base64,' + school['logo_base64'] + '" alt="' + school['name'] + ' Logo" itemprop="logo">' if school.get('logo_base64') else '<i class="fas fa-school"></i>'}
                    </div>
                    <div class="logo-badge">
                        <i class="fas fa-award"></i>
                    </div>
                </div>
                <div class="school-title-section">
                    <h1 itemprop="name">{school['name']}</h1>
                    {'<p class="school-motto" itemprop="slogan">"' + school['motto'] + '"</p>' if school.get('motto') else ''}
                    {'<p style="color: var(--gray-dark); margin-bottom: 1rem; font-size: 1.1rem;" itemprop="alternateName">' + school.get('short_name', '') + '</p>' if school.get('short_name') else ''}
                    <div class="school-tags">
                        <span class="school-tag" itemprop="educationalLevel">{school.get('school_type', '')} School</span>
                        <span class="school-tag" itemprop="gender">{school.get('gender_focus', '')}</span>
                        <span class="school-tag">{school.get('level', '')}</span>
                        {'<span class="school-tag" itemprop="curriculum">' + school.get('curriculum', '') + '</span>' if school.get('curriculum') else ''}
                        {'<span class="school-tag" itemprop="foundingDate">Est. ' + str(est_year) + '</span>' if est_year else ''}
                    </div>
                </div>
            </div>
            
            <div class="school-stats">
                <div class="stat-item interactive-stat">
                    <div class="stat-value">{est_year}</div>
                    <div class="stat-label">Established</div>
                </div>
                <div class="stat-item interactive-stat">
                    <div class="stat-value">{school.get('total_students', 0):,}</div>
                    <div class="stat-label">Students</div>
                </div>
                <div class="stat-item interactive-stat">
                    <div class="stat-value">{school.get('total_teachers', 0):,}</div>
                    <div class="stat-label">Teaching Staff</div>
                </div>
                <div class="stat-item interactive-stat">
                    <div class="stat-value">{school.get('total_classrooms', 0):,}</div>
                    <div class="stat-label">Classrooms</div>
                </div>
                {'<div class="stat-item interactive-stat"><div class="stat-value">' + str(school.get('science_labs', 0)) + '</div><div class="stat-label">Science Labs</div></div>' if school.get('science_labs') else ''}
                {'<div class="stat-item interactive-stat"><div class="stat-value">' + str(school.get('computer_labs', 0)) + '</div><div class="stat-label">Computer Labs</div></div>' if school.get('computer_labs') else ''}
            </div>
        </div>
    </section>

    <!-- Main Content -->
    <main class="container">
        <div class="main-content">
            <!-- Left Column -->
            <div class="left-column">
                <!-- About Section -->
                <section class="section" itemscope itemtype="https://schema.org/AboutPage">
                    <h2 class="section-title"><i class="fas fa-info-circle"></i> About {school['name']}</h2>
                    <div class="info-grid">
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-bullseye"></i> Mission</div><div class="info-value" itemprop="description">' + school['mission'] + '</div></div>' if school.get('mission') else ''}
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-eye"></i> Vision</div><div class="info-value">' + school['vision'] + '</div></div>' if school.get('vision') else ''}
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-align-left"></i> Description</div><div class="info-value">' + school.get('description', '') + '</div></div>' if school.get('description') else ''}
                    </div>
                </section>
                
                <!-- Academics -->
                <section class="section">
                    <h2 class="section-title"><i class="fas fa-graduation-cap"></i> Academic Program</h2>
                    <div class="info-grid">
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-book-open"></i> Curriculum System</div><div class="info-value" itemprop="curriculum">' + school['curriculum'] + '</div></div>' if school.get('curriculum') else ''}
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-user-graduate"></i> Student Capacity</div><div class="info-value">' + str(school.get('student_capacity', school.get('total_students', 'N/A'))) + '</div></div>' if school.get('student_capacity') or school.get('total_students') else ''}
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-chalkboard"></i> Average Class Size</div><div class="info-value">' + str(school.get('average_class_size', '25-30')) + ' students</div></div>' if school.get('average_class_size') else ''}
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-money-bill-wave"></i> Fee Structure</div><div class="info-value">' + school.get('fee_range', 'Contact administration for details') + '</div></div>' if school.get('fee_range') else ''}
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-award"></i> Scholarship Program</div><div class="info-value">' + ('Available: ' + school['scholarship_details'] if school.get('scholarships_available') and school.get('scholarship_details') else ('Available' if school.get('scholarships_available') else 'Not available')) + '</div></div>' if school.get('scholarships_available') or school.get('scholarship_details') else ''}
                    </div>
                </section>
                
                <!-- Facilities -->
                <section class="section" itemscope itemtype="https://schema.org/EducationalOrganization">
                    <h2 class="section-title"><i class="fas fa-building"></i> Campus Facilities</h2>
                    <div class="amenities-grid">
"""
        
        for amenity in amenities:
            html += f"""
                        <div class="amenity">
                            <i class="fas fa-check-circle"></i>
                            <span>{amenity}</span>
                        </div>
"""
        
        html += f"""
                    </div>
                    <div class="info-grid" style="margin-top: 2rem;">
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-flask"></i> Science Laboratories</div><div class="info-value">' + str(school.get('science_labs', 0)) + ' fully equipped labs</div></div>' if school.get('science_labs') else ''}
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-desktop"></i> Computer Laboratories</div><div class="info-value">' + str(school.get('computer_labs', 0)) + ' labs with modern equipment</div></div>' if school.get('computer_labs') else ''}
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-book"></i> Library Resources</div><div class="info-value">' + str(school.get('library_rooms', 0)) + ' library rooms with extensive collection</div></div>' if school.get('library_rooms') else ''}
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-running"></i> Sports Facilities</div><div class="info-value">' + school.get('sports_facilities', 'Comprehensive sports facilities') + '</div></div>' if school.get('sports_facilities') else ''}
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-bus"></i> Transport Services</div><div class="info-value">' + ('Available with extensive coverage' if school.get('transport_services') else 'Not available') + '</div></div>' if school.get('transport_services') else ''}
                        {'<div class="info-item"><div class="info-label"><i class="fas fa-bed"></i> Boarding Facilities</div><div class="info-value">' + ('Available with ' + str(school.get('boarding_capacity', '')) + ' capacity' if school.get('hostel_facilities') else 'Day school only') + '</div></div>' if school.get('hostel_facilities') or school.get('boarding_capacity') else ''}
                    </div>
                </section>
            </div>
            
            <!-- Right Column -->
            <div class="right-column">
                <!-- Rating -->
                <section class="section">
                    <h2 class="section-title"><i class="fas fa-star"></i> Institutional Rating</h2>
                    <div class="rating-container">
                        {'<div class="rating-main"><div class="rating-stars">' + stars_html + '</div><div class="rating-numbers"><div class="rating-value">' + str(rating) + '/5.0</div><div class="rating-count">Based on ' + str(school.get('total_reviews', 0)) + ' verified reviews</div></div></div>' if rating > 0 else '<div class="rating-main"><div class="rating-value">No ratings yet</div><div class="rating-count">Be the first to review this institution</div></div>'}
                        
                        {'<div class="rating-breakdown"><div class="rating-bar"><span class="rating-label">Academic</span><div class="bar-container"><div class="bar-fill" style="width: ' + str(school.get('academic_rating', 0) * 20) + '%"></div></div><span>' + str(school.get('academic_rating', 0)) + '</span></div><div class="rating-bar"><span class="rating-label">Facilities</span><div class="bar-container"><div class="bar-fill" style="width: ' + str(school.get('facility_rating', 0) * 20) + '%"></div></div><span>' + str(school.get('facility_rating', 0)) + '</span></div><div class="rating-bar"><span class="rating-label">Discipline</span><div class="bar-container"><div class="bar-fill" style="width: ' + str(school.get('discipline_rating', 0) * 20) + '%"></div></div><span>' + str(school.get('discipline_rating', 0)) + '</span></div></div>' if school.get('academic_rating') else ''}
                    </div>
                </section>
                
                <!-- Contact -->
                <section class="section">
                    <h2 class="section-title"><i class="fas fa-address-book"></i> Contact Information</h2>
                    <div class="contact-methods">
                        {'<a href="tel:' + school.get('phone_primary', '') + '" class="contact-method"><div class="contact-icon"><i class="fas fa-phone"></i></div><div class="contact-details"><h4>Primary Phone</h4><p itemprop="telephone">' + school.get('phone_primary', 'N/A') + '</p></div></a>' if school.get('phone_primary') else ''}
                        {'<a href="tel:' + school.get('phone', '') + '" class="contact-method"><div class="contact-icon"><i class="fas fa-phone-alt"></i></div><div class="contact-details"><h4>Alternative Phone</h4><p>' + school.get('phone', 'N/A') + '</p></div></a>' if school.get('phone') else ''}
                        {'<a href="mailto:' + school.get('email', '') + '" class="contact-method"><div class="contact-icon"><i class="fas fa-envelope"></i></div><div class="contact-details"><h4>Email Address</h4><p itemprop="email">' + school.get('email', 'N/A') + '</p></div></a>' if school.get('email') else ''}
                        <div class="contact-method">
                            <div class="contact-icon">
                                <i class="fas fa-map-marker-alt"></i>
                            </div>
                            <div class="contact-details">
                                <h4>Campus Address</h4>
                                <p itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">{school.get('full_address', 'Address not specified')}</p>
                            </div>
                        </div>
                        {'<div class="contact-method"><div class="contact-icon"><i class="fas fa-user-tie"></i></div><div class="contact-details"><h4>Principal / Director</h4><p>' + school.get('principal_name', 'N/A') + '</p></div></div>' if school.get('principal_name') else ''}
                        {'<a href="mailto:' + school.get('principal_email', '') + '" class="contact-method"><div class="contact-icon"><i class="fas fa-envelope-open-text"></i></div><div class="contact-details"><h4>Principal\'s Email</h4><p>' + school.get('principal_email', 'N/A') + '</p></div></a>' if school.get('principal_email') else ''}
                    </div>
                    
                    <!-- Social Links -->
                    <div class="social-links">
                        {'<a href="' + social_links['website'] + '" class="social-link" target="_blank" title="Official Website" itemprop="url"><i class="fas fa-globe"></i></a>' if 'website' in social_links else ''}
                        {'<a href="' + social_links['facebook'] + '" class="social-link" target="_blank" title="Facebook Page"><i class="fab fa-facebook-f"></i></a>' if 'facebook' in social_links else ''}
                        {'<a href="' + social_links['twitter'] + '" class="social-link" target="_blank" title="Twitter Profile"><i class="fab fa-twitter"></i></a>' if 'twitter' in social_links else ''}
                        {'<a href="' + social_links['instagram'] + '" class="social-link" target="_blank" title="Instagram"><i class="fab fa-instagram"></i></a>' if 'instagram' in social_links else ''}
                        {'<a href="' + social_links['linkedin'] + '" class="social-link" target="_blank" title="LinkedIn"><i class="fab fa-linkedin-in"></i></a>' if 'linkedin' in social_links else ''}
                        {'<a href="' + social_links['maps'] + '" class="social-link" target="_blank" title="Google Maps"><i class="fas fa-map-marked-alt"></i></a>' if 'maps' in social_links else ''}
                    </div>
                </section>
                
                <!-- Location -->
                <section class="section">
                    <h2 class="section-title"><i class="fas fa-map"></i> Location & Campus</h2>
                    <div class="location-frame">
                        <div class="location-header">
                            <h4>{school.get('city', '')}, {school.get('province', '')}</h4>
                            <p class="location-address">{school.get('full_address', '')}</p>
                        </div>
                        <div class="map-placeholder">
                            <i class="fas fa-map-marked-alt"></i>
                            <p style="margin-bottom: 1rem;">Interactive Map View</p>
                            {'<a href="' + social_links.get('maps', '#') + '" target="_blank">Open in Google Maps <i class="fas fa-external-link-alt"></i></a>' if 'maps' in social_links else '<p>Map location available upon request</p>'}
                        </div>
                    </div>
                </section>
                
                <!-- Quick Facts -->
                <section class="section">
                    <h2 class="section-title"><i class="fas fa-lightbulb"></i> Key Information</h2>
                    <div class="quick-facts">
                        <div class="fact">
                            <div class="fact-icon"><i class="fas fa-school"></i></div>
                            <div class="fact-text">{school.get('school_type', 'N/A')}</div>
                        </div>
                        <div class="fact">
                            <div class="fact-icon"><i class="fas fa-venus-mars"></i></div>
                            <div class="fact-text">{school.get('gender_focus', 'N/A')}</div>
                        </div>
                        <div class="fact">
                            <div class="fact-icon"><i class="fas fa-layer-group"></i></div>
                            <div class="fact-text">{school.get('category', 'N/A')}</div>
                        </div>
                        <div class="fact">
                            <div class="fact-icon"><i class="fas fa-calendar-star"></i></div>
                            <div class="fact-text">Est. {est_year}</div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Scholastic Forum</h3>
                    <p style="color: var(--gray); font-size: 0.9rem; line-height: 1.6;">
                        Part of the Scholastic Services suite by High Voltage Software Technologies.<br>
                        Comprehensive educational institution directory and management system.
                    </p>
                    <div class="manufacturer-logo">
                        <img src="../assets/images/manufacturer_dark.png" alt="High Voltage Software Technologies">
                    </div>
                    <div class="social-links">
                        <a href="https://hvstechzw.github.io/Scholastic-Services-Web-Portal/" class="social-link" target="_blank" title="Scholastic Services Portal"><i class="fas fa-external-link-alt"></i></a>
                    </div>
                </div>
                
                <div class="footer-section">
                    <h3>School Profile</h3>
                    <ul class="footer-links">
                        <li><a href="#academics"><i class="fas fa-graduation-cap"></i> Academic Program</a></li>
                        <li><a href="#facilities"><i class="fas fa-building"></i> Campus Facilities</a></li>
                        <li><a href="#contact"><i class="fas fa-address-book"></i> Contact Details</a></li>
                        <li><a href="#location"><i class="fas fa-map"></i> Location Info</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h3>Navigation</h3>
                    <ul class="footer-links">
                        <li><a href="../index.html"><i class="fas fa-home"></i> Home Directory</a></li>
                        <li><a href="../schools/all.html"><i class="fas fa-list"></i> All Schools ({total_schools})</a></li>
                        <li><a href="#top"><i class="fas fa-arrow-up"></i> Back to Top</a></li>
                        <li><a href="mailto:support@scholasticforum.org"><i class="fas fa-question-circle"></i> Report Issue</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2025 Scholastic Forum | Scholastic Services Product | High Voltage Software Technologies</p>
                <p style="margin-top: 0.5rem; font-size: 0.8rem;">Profile ID: {school['school_id']} | Last Updated: {datetime.now().strftime('%Y-%m-%d')}</p>
            </div>
        </div>
    </footer>

    <script>
        // Force light theme
        document.documentElement.setAttribute('data-theme', 'light');
        document.body.style.colorScheme = 'light';
        
        // Animate rating bars
        document.addEventListener('DOMContentLoaded', function() {{
            const bars = document.querySelectorAll('.bar-fill');
            bars.forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {{
                    bar.style.width = width;
                }}, 300);
            }});
        }});
        
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});
    </script>
</body>
</html>
"""
        
        return html
    
    def generate_all_schools_page(self, schools):
        """Generate a page listing all schools with enhanced styling"""
        total_schools = len(schools)
        
        html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete School Directory - {total_schools}+ Educational Institutions | Scholastic Forum</title>
    <meta name="description" content="Browse comprehensive directory of {total_schools} educational institutions. Find schools by location, curriculum, facilities, and ratings. Complete school profiles.">
    <meta name="keywords" content="schools directory, educational institutions database, find schools, school search, education directory">
    <meta name="author" content="Scholastic Services">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://hvstechzw.github.io/Scholastic-Schools-Catalog/schools/all.html">
    <meta property="og:title" content="Complete School Directory - {total_schools}+ Institutions">
    <meta property="og:description" content="Browse {total_schools} educational institutions with detailed profiles.">
    <meta property="og:image" content="https://hvstechzw.github.io/Scholastic-Schools-Catalog/assets/images/og-image.jpg">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://hvstechzw.github.io/Scholastic-Schools-Catalog/schools/all.html">
    <meta property="twitter:title" content="Complete School Directory - {total_schools}+ Institutions">
    <meta property="twitter:description" content="Browse {total_schools} educational institutions with detailed profiles.">
    <meta property="twitter:image" content="https://hvstechzw.github.io/Scholastic-Schools-Catalog/assets/images/og-image.jpg">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Complete School Directory",
        "description": "Directory of {total_schools} educational institutions",
        "url": "https://hvstechzw.github.io/Scholastic-Schools-Catalog/schools/all.html",
        "mainEntity": {{
            "@type": "ItemList",
            "numberOfItems": {total_schools},
            "itemListElement": [
                {self.generate_school_schema_data(schools[:10])}
            ]
        }}
    }}
    </script>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="canonical" href="https://hvstechzw.github.io/Scholastic-Schools-Catalog/schools/all.html">
    <style>
        :root {{
            --primary: #ffffff;
            --primary-dark: #f0f0f0;
            --secondary: #6c757d;
            --accent: #6c757d;
            --dark: #212529;
            --light: #f8f9fa;
            --gray: #adb5bd;
            --gray-light: #e9ecef;
            --gray-dark: #495057;
            --white: #ffffff;
            --silver: #c0c0c0;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.05), 0 5px 10px rgba(0, 0, 0, 0.05);
            --radius: 12px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            min-height: 100vh;
        }}
        
        .container {{
            width: 100%;
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        /* Header */
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow);
            position: sticky;
            top: 0;
            z-index: 1000;
            border-bottom: 1px solid var(--gray-light);
        }}
        
        .nav-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }}
        
        .logo-section {{
            display: flex;
            align-items: center;
            gap: 15px;
            text-decoration: none;
        }}
        
        .logo-wrapper {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .main-logo {{
            width: 100px;
            height: 100px;
            background: transparent;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--white);
            font-size: 2.5rem;
            box-shadow: var(--shadow);
            border: 2px solid var(--white);
        }}
        
        .main-logo img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: 5px;
        }}
        
        .logo-text {{
            display: flex;
            flex-direction: column;
        }}
        
        .main-title {{
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            font-size: 1.5rem;
            background: linear-gradient(135deg, var(--gray-dark) 0%, var(--dark) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .subtitle {{
            font-size: 0.75rem;
            color: var(--gray);
            font-weight: 500;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-top: -2px;
        }}
        
        .back-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, var(--white) 0%, var(--gray-light) 100%);
            border: 2px solid var(--gray-light);
            border-radius: var(--radius);
            color: var(--dark);
            text-decoration: none;
            font-weight: 600;
            transition: var(--transition);
        }}
        
        .back-btn:hover {{
            background: linear-gradient(135deg, var(--silver) 0%, var(--gray) 100%);
            color: var(--dark);
            border-color: var(--silver);
            transform: translateX(-5px);
            box-shadow: 0 5px 15px rgba(192, 192, 192, 0.3);
        }}
        
        /* Page Header */
        .page-header {{
            text-align: center;
            padding: 4rem 0 3rem;
        }}
        
        .page-title {{
            font-family: 'Poppins', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--gray-dark) 0%, var(--dark) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .page-subtitle {{
            font-size: 1.2rem;
            color: var(--gray-dark);
            max-width: 800px;
            margin: 0 auto 2rem;
            line-height: 1.6;
        }}
        
        /* Stats Overview */
        .stats-overview {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }}
        
        .stat-card {{
            background: var(--white);
            padding: 2rem;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            text-align: center;
            border: 1px solid var(--gray-light);
            transition: var(--transition);
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
            border-color: var(--silver);
        }}
        
        .stat-icon {{
            font-size: 2.5rem;
            color: var(--silver);
            margin-bottom: 1rem;
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--dark);
            margin-bottom: 0.5rem;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: var(--gray-dark);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }}
        
        /* Enhanced Search */
        .enhanced-search {{
            background: var(--white);
            padding: 2.5rem;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            margin-bottom: 3rem;
            border: 1px solid var(--gray-light);
        }}
        
        .search-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .search-title {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--dark);
        }}
        
        .search-actions {{
            display: flex;
            gap: 1rem;
            align-items: center;
        }}
        
        .search-box {{
            position: relative;
            margin-bottom: 1.5rem;
        }}
        
        .search-input {{
            width: 100%;
            padding: 1.25rem 1.25rem 1.25rem 3.5rem;
            border: 2px solid var(--gray-light);
            border-radius: var(--radius);
            font-size: 1rem;
            transition: var(--transition);
            background: var(--light);
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(108, 117, 125, 0.1);
            background: var(--white);
        }}
        
        .search-icon {{
            position: absolute;
            left: 1.25rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--gray);
            font-size: 1.2rem;
        }}
        
        .advanced-filters {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }}
        
        .filter-group {{
            margin-bottom: 0;
        }}
        
        .filter-label {{
            display: block;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: var(--dark);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .filter-select {{
            width: 100%;
            padding: 0.875rem;
            border: 2px solid var(--gray-light);
            border-radius: var(--radius);
            font-size: 0.95rem;
            background: var(--light);
            cursor: pointer;
            transition: var(--transition);
        }}
        
        .filter-select:focus {{
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(108, 117, 125, 0.1);
        }}
        
        .reset-btn {{
            padding: 0.875rem 1.5rem;
            background: linear-gradient(135deg, var(--white) 0%, var(--gray-light) 100%);
            border: 2px solid var(--gray-light);
            border-radius: var(--radius);
            color: var(--dark);
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
        }}
        
        .reset-btn:hover {{
            background: linear-gradient(135deg, var(--gray-dark) 0%, var(--dark) 100%);
            color: white;
            border-color: var(--dark);
        }}
        
        /* Schools Grid */
        .schools-grid-container {{
            margin-bottom: 4rem;
        }}
        
        .grid-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .grid-title {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--dark);
        }}
        
        .sort-controls {{
            display: flex;
            gap: 1rem;
            align-items: center;
        }}
        
        .sort-select {{
            padding: 0.75rem;
            border: 2px solid var(--gray-light);
            border-radius: var(--radius);
            background: var(--light);
            color: var(--dark);
            font-weight: 500;
            cursor: pointer;
        }}
        
        .schools-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
        }}
        
        .school-card {{
            background: var(--white);
            border-radius: var(--radius);
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: var(--transition);
            border: 1px solid var(--gray-light);
            position: relative;
        }}
        
        .school-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(to right, var(--silver), var(--gray));
            z-index: 1;
        }}
        
        .school-card:hover {{
            transform: translateY(-8px);
            box-shadow: var(--shadow-lg);
            border-color: var(--accent);
        }}
        
        .school-card-header {{
            height: 140px;
            position: relative;
            padding: 1.5rem;
            color: var(--dark);
            overflow: hidden;
        }}
        
        .school-banner {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.1;
        }}
        
        .school-type-badge {{
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(5px);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--dark);
            border: 1px solid var(--gray-light);
            z-index: 2;
        }}
        
        .school-logo-container {{
            position: absolute;
            top: 1rem;
            left: 1.5rem;
            width: 80px;
            height: 80px;
            background: var(--white);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow);
            border: 3px solid var(--white);
            overflow: hidden;
            z-index: 2;
        }}
        
        .school-logo {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: 10px;
        }}
        
        .school-card-body {{
            padding: 2rem 1.5rem 1.5rem;
            margin-top: 40px;
        }}
        
        .school-name {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--dark);
            line-height: 1.3;
        }}
        
        .school-location {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: var(--gray-dark);
            font-size: 0.9rem;
            margin-bottom: 1.25rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--gray-light);
        }}
        
        .school-details {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        
        .detail-item {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 0.85rem;
            color: var(--dark);
        }}
        
        .detail-item i {{
            color: var(--accent);
            width: 16px;
            font-size: 1rem;
        }}
        
        .school-rating {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
            padding: 0.75rem;
            background: var(--light);
            border-radius: var(--radius);
        }}
        
        .stars {{
            color: #ffc107;
            font-size: 1.1rem;
            letter-spacing: 2px;
        }}
        
        .rating-text {{
            font-size: 0.9rem;
            color: var(--gray-dark);
            font-weight: 600;
        }}
        
        .view-btn {{
            display: block;
            width: 100%;
            padding: 1rem;
            background: linear-gradient(135deg, var(--white) 0%, var(--gray-light) 100%);
            color: var(--dark);
            border: 2px solid var(--gray-light);
            border-radius: var(--radius);
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            text-align: center;
            text-decoration: none;
        }}
        
        .view-btn:hover {{
            background: linear-gradient(135deg, var(--silver) 0%, var(--gray) 100%);
            color: var(--dark);
            border-color: var(--silver);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(192, 192, 192, 0.3);
        }}
        
        /* Pagination */
        .pagination {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-top: 3rem;
            flex-wrap: wrap;
        }}
        
        .page-btn {{
            width: 45px;
            height: 45px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--white);
            border: 2px solid var(--gray-light);
            border-radius: var(--radius);
            color: var(--dark);
            text-decoration: none;
            font-weight: 600;
            transition: var(--transition);
        }}
        
        .page-btn:hover, .page-btn.active {{
            background: linear-gradient(135deg, var(--silver) 0%, var(--gray) 100%);
            color: var(--dark);
            border-color: var(--silver);
            transform: translateY(-2px);
        }}
        
        .page-btn.disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        /* Footer */
        .footer {{
            background: linear-gradient(135deg, var(--dark) 0%, #343a40 100%);
            color: var(--white);
            padding: 3rem 0 1.5rem;
            margin-top: 6rem;
        }}
        
        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        .footer-section h3 {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
            color: var(--white);
        }}
        
        .footer-links {{
            list-style: none;
        }}
        
        .footer-links li {{
            margin-bottom: 0.75rem;
        }}
        
        .footer-links a {{
            color: var(--gray);
            text-decoration: none;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        
        .footer-links a:hover {{
            color: var(--silver);
            padding-left: 5px;
        }}
        
        .footer-bottom {{
            text-align: center;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--gray);
            font-size: 0.9rem;
        }}
        
        .manufacturer-logo {{
            margin-top: 1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .manufacturer-logo img {{
            height: 48px;
            width: auto;
            filter: brightness(0) invert(1);
            opacity: 0.9;
        }}
        
        /* No Results */
        .no-results {{
            text-align: center;
            padding: 4rem 2rem;
            background: var(--white);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            border: 2px dashed var(--gray-light);
        }}
        
        .no-results-icon {{
            font-size: 4rem;
            color: var(--gray);
            margin-bottom: 1.5rem;
        }}
        
        /* Loading */
        .loading {{
            text-align: center;
            padding: 3rem;
            color: var(--gray);
        }}
        
        .spinner {{
            width: 50px;
            height: 50px;
            border: 4px solid var(--gray-light);
            border-top-color: var(--accent);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        /* Responsive */
        @media (max-width: 1200px) {{
            .schools-grid {{
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            }}
        }}
        
        @media (max-width: 768px) {{
            .page-title {{
                font-size: 2.5rem;
            }}
            
            .stats-overview {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .schools-grid {{
                grid-template-columns: 1fr;
            }}
            
            .advanced-filters {{
                grid-template-columns: 1fr;
            }}
            
            .search-header {{
                flex-direction: column;
                align-items: stretch;
            }}
            
            .sort-controls {{
                flex-direction: column;
                align-items: stretch;
            }}
            
            .school-logo-container {{
                width: 70px;
                height: 70px;
            }}
            
            .school-card-body {{
                margin-top: 35px;
            }}
            
            .main-logo {{
                width: 80px;
                height: 80px;
            }}
        }}
        
        @media (max-width: 480px) {{
            .container {{
                padding: 0 15px;
            }}
            
            .page-title {{
                font-size: 2rem;
            }}
            
            .stats-overview {{
                grid-template-columns: 1fr;
            }}
            
            .page-header {{
                padding: 3rem 0 2rem;
            }}
            
            .enhanced-search {{
                padding: 1.5rem;
            }}
            
            .school-logo-container {{
                width: 60px;
                height: 60px;
                top: 1rem;
                left: 1rem;
            }}
            
            .school-card-body {{
                margin-top: 30px;
            }}
            
            .main-logo {{
                width: 70px;
                height: 70px;
            }}
            
            .manufacturer-logo img {{
                height: 40px;
            }}
        }}
        
        /* Animations */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in-up {{
            animation: fadeInUp 0.6s ease-out forwards;
        }}
    </style>
</head>
<body itemscope itemtype="https://schema.org/WebPage">
    <!-- Force light theme -->
    <script>document.documentElement.setAttribute('data-theme', 'light');</script>
    
    <!-- Header -->
    <header class="header">
        <div class="container">
            <nav class="nav-container">
                <div class="logo-wrapper">
                    <a href="../index.html" class="logo-section">
                        <div class="main-logo" style="background: transparent;">
                            <img id="theme-logo" src="../assets/images/logo_light.png" alt="Scholastic Forum">
                        </div>
                        <div class="logo-text">
                            <div class="main-title">Scholastic Forum</div>
                            <div class="subtitle">Complete Directory</div>
                        </div>
                    </a>
                </div>
                <a href="../index.html" class="back-btn">
                    <i class="fas fa-arrow-left"></i>
                    Back to Home
                </a>
            </nav>
        </div>
    </header>

    <!-- Page Header -->
    <section class="page-header">
        <div class="container">
            <h1 class="page-title">Complete School Directory</h1>
            <p class="page-subtitle">
                Browse our comprehensive database of {total_schools} educational institutions. 
                Filter by location, curriculum, facilities, and more to find the perfect educational match.
            </p>
        </div>
    </section>

    <!-- Stats Overview -->
    <section class="container">
        <div class="stats-overview">
            <div class="stat-card fade-in-up">
                <div class="stat-icon">
                    <i class="fas fa-school"></i>
                </div>
                <div class="stat-number">{total_schools}</div>
                <div class="stat-label">Total Institutions</div>
            </div>
            <div class="stat-card fade-in-up" style="animation-delay: 0.1s;">
                <div class="stat-icon">
                    <i class="fas fa-graduation-cap"></i>
                </div>
                <div class="stat-number">{sum(s.get('total_students', 0) for s in schools):,}</div>
                <div class="stat-label">Total Students</div>
            </div>
            <div class="stat-card fade-in-up" style="animation-delay: 0.2s;">
                <div class="stat-icon">
                    <i class="fas fa-chalkboard-teacher"></i>
                </div>
                <div class="stat-number">{sum(s.get('total_teachers', 0) for s in schools):,}</div>
                <div class="stat-label">Teaching Staff</div>
            </div>
            <div class="stat-card fade-in-up" style="animation-delay: 0.3s;">
                <div class="stat-icon">
                    <i class="fas fa-calendar-star"></i>
                </div>
                <div class="stat-number">{min(s.get('establishment_year', 2025) for s in schools if s.get('establishment_year'))}</div>
                <div class="stat-label">Oldest Institution</div>
            </div>
        </div>
    </section>

    <!-- Enhanced Search -->
    <section class="container">
        <div class="enhanced-search">
            <div class="search-header">
                <h2 class="search-title">Find Schools</h2>
                <div class="search-actions">
                    <button class="reset-btn" id="resetFilters">
                        <i class="fas fa-redo"></i> Reset Filters
                    </button>
                </div>
            </div>
            
            <div class="search-box">
                <i class="fas fa-search search-icon"></i>
                <input type="text" class="search-input" id="allSearchInput" 
                       placeholder="Search by school name, location, curriculum, facilities, or keywords...">
            </div>
            
            <div class="advanced-filters">
                <div class="filter-group">
                    <label class="filter-label">Location</label>
                    <select class="filter-select" id="locationFilter">
                        <option value="all">All Locations</option>
                        {self.generate_location_options(schools)}
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">Education Level</label>
                    <select class="filter-select" id="levelFilter">
                        <option value="all">All Levels</option>
                        <option value="Pre-School">Pre-School</option>
                        <option value="Primary">Primary</option>
                        <option value="Secondary">Secondary</option>
                        <option value="High School">High School</option>
                        <option value="College">College</option>
                        <option value="University">University</option>
                        <option value="Mixed">Mixed</option>
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">School Type</label>
                    <select class="filter-select" id="typeFilter">
                        <option value="all">All Types</option>
                        <option value="Day">Day School</option>
                        <option value="Boarding">Boarding School</option>
                        <option value="Mixed">Mixed</option>
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">Minimum Rating</label>
                    <select class="filter-select" id="ratingFilter">
                        <option value="0">Any Rating</option>
                        <option value="3">3.0+ Stars</option>
                        <option value="4">4.0+ Stars</option>
                        <option value="4.5">4.5+ Stars</option>
                    </select>
                </div>
            </div>
        </div>
    </section>

    <!-- Schools Grid -->
    <section class="container">
        <div class="schools-grid-container">
            <div class="grid-header">
                <h2 class="grid-title">All Educational Institutions ({total_schools} Total)</h2>
                <div class="sort-controls">
                    <span style="color: var(--gray-dark); font-weight: 500;">Sort by:</span>
                    <select class="sort-select" id="sortSelect">
                        <option value="name">Name (A-Z)</option>
                        <option value="name-desc">Name (Z-A)</option>
                        <option value="rating">Highest Rating</option>
                        <option value="students">Most Students</option>
                        <option value="established">Newest First</option>
                        <option value="established-desc">Oldest First</option>
                    </select>
                </div>
            </div>
            
            <div class="schools-grid" id="allSchoolsGrid">
"""
        
        for school in schools:
            amenities_sample = school.get('amenities', [])[:2]
            rating = school.get('overall_rating', 0)
            stars_html = self.generate_stars_html(rating)
            est_year = school.get('establishment_year', '2025')
            
            banner_html = ''
            if school.get('banner_base64'):
                banner_html = f'<img src="data:image/jpeg;base64,{school["banner_base64"]}" alt="{school["name"]} Banner" class="school-banner">'
            
            logo_html = ''
            if school.get('logo_base64'):
                logo_html = f'<img src="data:image/jpeg;base64,{school["logo_base64"]}" alt="{school["name"]} Logo" class="school-logo">'
            
            html += f"""
                <div class="school-card fade-in-up" 
                     data-name="{school['name'].lower()}"
                     data-location="{school.get('city', '').lower()} {school.get('province', '').lower()}"
                     data-level="{school.get('level', '').lower()}"
                     data-type="{school.get('school_type', '').lower()}"
                     data-rating="{rating}"
                     data-students="{school.get('total_students', 0)}"
                     data-established="{est_year}"
                     data-search="{school['name'].lower()} {school.get('city', '').lower()} {school.get('province', '').lower()} {school.get('curriculum', '').lower()} {school.get('school_type', '').lower()} {' '.join(amenities_sample).lower()}">
                    <div class="school-card-header">
                        {banner_html}
                        <div class="school-logo-container">
                            {logo_html if school.get('logo_base64') else '<i class="fas fa-school"></i>'}
                        </div>
                        <div class="school-type-badge">{school.get('school_type', '')}</div>
                    </div>
                    <div class="school-card-body">
                        <h3 class="school-name">{school['name']}</h3>
                        <div class="school-location">
                            <i class="fas fa-map-marker-alt"></i>
                            <span>{school.get('city', '')}, {school.get('province', '')}</span>
                        </div>
                        
                        <div class="school-details">
                            <div class="detail-item">
                                <i class="fas fa-graduation-cap"></i>
                                <span>{school.get('level', 'N/A')}</span>
                            </div>
                            <div class="detail-item">
                                <i class="fas fa-users"></i>
                                <span>{school.get('total_students', 0):,} Students</span>
                            </div>
                            <div class="detail-item">
                                <i class="fas fa-calendar-star"></i>
                                <span>Est. {est_year}</span>
                            </div>
                            <div class="detail-item">
                                <i class="fas fa-book"></i>
                                <span>{school.get('curriculum', 'Various')}</span>
                            </div>
                        </div>
                        
                        {f'<div class="school-rating"><div class="stars">{stars_html}</div><span class="rating-text">{rating:.1f}/5.0</span></div>' if rating > 0 else ''}
                        
                        <a href="{school['school_id']}.html" class="view-btn">
                            <i class="fas fa-external-link-alt"></i> View Complete Profile
                        </a>
                    </div>
                </div>
"""
        
        html += f"""
            </div>
            
            <div class="pagination" id="pagination">
                <!-- Pagination will be generated by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Scholastic Forum</h3>
                    <p style="color: var(--gray); font-size: 0.9rem; line-height: 1.6;">
                        Comprehensive educational institution directory system.<br>
                        Part of Scholastic Services by High Voltage Software Technologies.
                    </p>
                    <div class="manufacturer-logo">
                        <img src="../assets/images/manufacturer_dark.png" alt="High Voltage Software Technologies">
                    </div>
                </div>
                
                <div class="footer-section">
                    <h3>Directory</h3>
                    <ul class="footer-links">
                        <li><a href="../index.html"><i class="fas fa-home"></i> Home Page</a></li>
                        <li><a href="#"><i class="fas fa-search"></i> Advanced Search</a></li>
                        <li><a href="#"><i class="fas fa-filter"></i> Filter Guide</a></li>
                        <li><a href="https://hvstechzw.github.io/Scholastic-Services-Web-Portal/" target="_blank"><i class="fas fa-question-circle"></i> Scholastic Services Portal</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h3>Contact</h3>
                    <ul class="footer-links">
                        <li><a href="mailto:support@scholasticforum.org"><i class="fas fa-envelope"></i> Email Support</a></li>
                        <li><a href="#"><i class="fas fa-phone"></i> +263 123 456 789</a></li>
                        <li><a href="#"><i class="fas fa-building"></i> High Voltage Software</a></li>
                        <li><a href="#"><i class="fas fa-globe"></i> Scholastic Services</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2025 Scholastic Forum | Complete School Directory | {total_schools} Institutions Listed</p>
                <p style="margin-top: 0.5rem; font-size: 0.8rem;">Data Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
        </div>
    </footer>

    <!-- JavaScript -->
    <script>
        // Force light theme
        document.documentElement.setAttribute('data-theme', 'light');
        document.body.style.colorScheme = 'light';
        
        // School data and pagination
        const allSchoolCards = document.querySelectorAll('#allSchoolsGrid .school-card');
        const schoolsPerPage = 12;
        let currentPage = 1;
        let filteredSchools = Array.from(allSchoolCards);
        
        // Filter and Search
        const allSearchInput = document.getElementById('allSearchInput');
        const locationFilter = document.getElementById('locationFilter');
        const levelFilter = document.getElementById('levelFilter');
        const typeFilter = document.getElementById('typeFilter');
        const ratingFilter = document.getElementById('ratingFilter');
        const sortSelect = document.getElementById('sortSelect');
        const resetFilters = document.getElementById('resetFilters');
        
        function filterAndSortSchools() {{
            const searchTerm = allSearchInput.value.toLowerCase().trim();
            const locationValue = locationFilter.value.toLowerCase();
            const levelValue = levelFilter.value.toLowerCase();
            const typeValue = typeFilter.value.toLowerCase();
            const minRating = parseFloat(ratingFilter.value);
            const sortBy = sortSelect.value;
            
            filteredSchools = Array.from(allSchoolCards).filter(card => {{
                const name = card.getAttribute('data-name');
                const location = card.getAttribute('data-location');
                const level = card.getAttribute('data-level');
                const type = card.getAttribute('data-type');
                const rating = parseFloat(card.getAttribute('data-rating'));
                const searchData = card.getAttribute('data-search');
                
                const matchesSearch = searchTerm === '' || searchData.includes(searchTerm);
                const matchesLocation = locationValue === 'all' || location.includes(locationValue);
                const matchesLevel = levelValue === 'all' || level === levelValue;
                const matchesType = typeValue === 'all' || type === typeValue;
                const matchesRating = minRating === 0 || rating >= minRating;
                
                return matchesSearch && matchesLocation && matchesLevel && matchesType && matchesRating;
            }});
            
            // Sort schools
            filteredSchools.sort((a, b) => {{
                switch(sortBy) {{
                    case 'name':
                        return a.getAttribute('data-name').localeCompare(b.getAttribute('data-name'));
                    case 'name-desc':
                        return b.getAttribute('data-name').localeCompare(a.getAttribute('data-name'));
                    case 'rating':
                        return parseFloat(b.getAttribute('data-rating')) - parseFloat(a.getAttribute('data-rating'));
                    case 'students':
                        return parseInt(b.getAttribute('data-students')) - parseInt(a.getAttribute('data-students'));
                    case 'established':
                        return parseInt(b.getAttribute('data-established')) - parseInt(a.getAttribute('data-established'));
                    case 'established-desc':
                        return parseInt(a.getAttribute('data-established')) - parseInt(b.getAttribute('data-established'));
                    default:
                        return 0;
                }}
            }});
            
            updateDisplay();
            updatePagination();
        }}
        
        function updateDisplay() {{
            const startIndex = (currentPage - 1) * schoolsPerPage;
            const endIndex = startIndex + schoolsPerPage;
            const schoolsToShow = filteredSchools.slice(startIndex, endIndex);
            
            // Hide all schools
            allSchoolCards.forEach(card => {{
                card.style.display = 'none';
                card.classList.remove('fade-in-up');
            }});
            
            // Show filtered schools with animation
            schoolsToShow.forEach((card, index) => {{
                card.style.display = 'block';
                card.style.animationDelay = `${{index * 0.05}}s`;
                card.classList.add('fade-in-up');
            }});
            
            // Update count
            const gridTitle = document.querySelector('.grid-title');
            gridTitle.textContent = `Educational Institutions (${{filteredSchools.length}} Found)`;
            
            // Show no results message
            const noResults = document.getElementById('noResults');
            if (filteredSchools.length === 0) {{
                if (!noResults) {{
                    const noResultsDiv = document.createElement('div');
                    noResultsDiv.id = 'noResults';
                    noResultsDiv.className = 'no-results';
                    noResultsDiv.innerHTML = `
                        <div class="no-results-icon">
                            <i class="fas fa-search"></i>
                        </div>
                        <h3 style="margin-bottom: 1rem; color: var(--dark);">No Schools Found</h3>
                        <p style="color: var(--gray-dark); margin-bottom: 1.5rem;">
                            Try adjusting your search or filter criteria to find what you're looking for.
                        </p>
                        <button class="reset-btn" onclick="resetAllFilters()" style="margin-top: 1rem;">
                            <i class="fas fa-redo"></i> Reset All Filters
                        </button>
                    `;
                    document.querySelector('.schools-grid-container').appendChild(noResultsDiv);
                }}
            }} else if (noResults) {{
                noResults.remove();
            }}
        }}
        
        function updatePagination() {{
            const totalPages = Math.ceil(filteredSchools.length / schoolsPerPage);
            const pagination = document.getElementById('pagination');
            
            if (totalPages <= 1) {{
                pagination.innerHTML = '';
                return;
            }}
            
            let paginationHTML = '';
            
            // Previous button
            paginationHTML += `
                <a href="#" class="page-btn ${{currentPage === 1 ? 'disabled' : ''}}" 
                   onclick="changePage(${{currentPage - 1}}); return false;">
                    <i class="fas fa-chevron-left"></i>
                </a>
            `;
            
            // Page numbers
            const maxVisiblePages = 5;
            let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
            let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
            
            if (endPage - startPage + 1 < maxVisiblePages) {{
                startPage = Math.max(1, endPage - maxVisiblePages + 1);
            }}
            
            for (let i = startPage; i <= endPage; i++) {{
                paginationHTML += `
                    <a href="#" class="page-btn ${{i === currentPage ? 'active' : ''}}" 
                       onclick="changePage(${{i}}); return false;">
                        ${{i}}
                    </a>
                `;
            }}
            
            // Next button
            paginationHTML += `
                <a href="#" class="page-btn ${{currentPage === totalPages ? 'disabled' : ''}}" 
                   onclick="changePage(${{currentPage + 1}}); return false;">
                    <i class="fas fa-chevron-right"></i>
                </a>
            `;
            
            pagination.innerHTML = paginationHTML;
        }}
        
        function changePage(page) {{
            currentPage = page;
            updateDisplay();
            updatePagination();
            window.scrollTo({{ top: document.querySelector('.schools-grid').offsetTop - 100, behavior: 'smooth' }});
        }}
        
        function resetAllFilters() {{
            allSearchInput.value = '';
            locationFilter.value = 'all';
            levelFilter.value = 'all';
            typeFilter.value = 'all';
            ratingFilter.value = '0';
            sortSelect.value = 'name';
            currentPage = 1;
            filterAndSortSchools();
        }}
        
        // Event listeners with debouncing
        let filterTimeout;
        function scheduleFilter() {{
            clearTimeout(filterTimeout);
            filterTimeout = setTimeout(filterAndSortSchools, 300);
        }}
        
        allSearchInput.addEventListener('input', scheduleFilter);
        locationFilter.addEventListener('change', scheduleFilter);
        levelFilter.addEventListener('change', scheduleFilter);
        typeFilter.addEventListener('change', scheduleFilter);
        ratingFilter.addEventListener('change', scheduleFilter);
        sortSelect.addEventListener('change', scheduleFilter);
        resetFilters.addEventListener('click', resetAllFilters);
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {{
            filterAndSortSchools();
            
            // Add click animation to cards
            allSchoolCards.forEach(card => {{
                card.addEventListener('click', function(e) {{
                    if (!e.target.classList.contains('view-btn') && !e.target.closest('.view-btn')) {{
                        this.style.transform = 'scale(0.98)';
                        setTimeout(() => {{
                            this.style.transform = '';
                        }}, 150);
                    }}
                }});
            }});
            
            // Add keyboard shortcuts
            document.addEventListener('keydown', function(e) {{
                // Focus search on /
                if (e.key === '/' && e.target !== allSearchInput) {{
                    e.preventDefault();
                    allSearchInput.focus();
                }}
                
                // Escape to clear search
                if (e.key === 'Escape' && document.activeElement === allSearchInput) {{
                    allSearchInput.value = '';
                    filterAndSortSchools();
                }}
                
                // Ctrl+F to focus search
                if ((e.ctrlKey || e.metaKey) && e.key === 'f') {{
                    e.preventDefault();
                    allSearchInput.focus();
                }}
            }});
            
            // Prevent form submission on Enter in search
            allSearchInput.addEventListener('keydown', function(e) {{
                if (e.key === 'Enter') {{
                    e.preventDefault();
                    filterAndSortSchools();
                }}
            }});
        }});
        
        // Expose functions to global scope for onclick handlers
        window.changePage = changePage;
        window.resetAllFilters = resetAllFilters;
    </script>
</body>
</html>
"""
        
        return html

    
    def generate_location_options(self, schools):
        """Generate unique location options for filter"""
        locations = set()
        for school in schools:
            city = school.get('city', '')
            province = school.get('province', '')
            if city and province:
                locations.add(f"{city}, {province}")
            elif city:
                locations.add(city)
            elif province:
                locations.add(province)
        
        options = []
        for location in sorted(locations):
            options.append(f'<option value="{location.lower()}">{location}</option>')
        
        return '\n'.join(options)
    
    def generate_css_file(self):
        """Generate main CSS file"""
        css = """
/* Main Stylesheet for Scholastic Forum */

:root {
    --primary: #ffffff;
    --primary-dark: #f0f0f0;
    --secondary: #6c757d;
    --accent: #6c757d;
    --dark: #212529;
    --light: #f8f9fa;
    --gray: #adb5bd;
    --gray-light: #e9ecef;
    --gray-dark: #495057;
    --white: #ffffff;
    --silver: #c0c0c0;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.05), 0 5px 10px rgba(0, 0, 0, 0.05);
    --radius: 12px;
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    color: var(--dark);
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    min-height: 100vh;
}

/* Common Components */
.school-card, .section, .stat-card {
    background: var(--white);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    transition: var(--transition);
    border: 1px solid var(--gray-light);
}

.school-card:hover, .section:hover, .stat-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-5px);
    border-color: var(--silver);
}

.btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 2rem;
    background: linear-gradient(135deg, var(--silver) 0%, var(--gray) 100%);
    color: var(--dark);
    text-decoration: none;
    border-radius: var(--radius);
    font-weight: 600;
    transition: var(--transition);
    border: none;
    cursor: pointer;
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(192, 192, 192, 0.3);
    background: linear-gradient(135deg, var(--gray) 0%, var(--gray-dark) 100%);
    color: var(--white);
}

.btn-secondary {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.875rem 1.5rem;
    background: linear-gradient(135deg, var(--white) 0%, var(--gray-light) 100%);
    color: var(--dark);
    text-decoration: none;
    border-radius: var(--radius);
    font-weight: 600;
    transition: var(--transition);
    border: 2px solid var(--gray-light);
}

.btn-secondary:hover {
    background: linear-gradient(135deg, var(--gray-dark) 0%, var(--dark) 100%);
    color: white;
    border-color: var(--dark);
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

.fade-in { animation: fadeIn 0.6s ease-out forwards; }
.slide-in { animation: slideIn 0.6s ease-out forwards; }

/* Loading States */
.loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    color: var(--gray);
}

.spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--gray-light);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Responsive Design */
@media (max-width: 768px) {
    .container {
        padding: 0 15px;
    }
    
    .schools-grid, .amenities-grid, .info-grid {
        grid-template-columns: 1fr !important;
    }
    
    .stats-overview {
        grid-template-columns: repeat(2, 1fr) !important;
    }
}

@media (max-width: 480px) {
    .container {
        padding: 0 10px;
    }
    
    .stats-overview {
        grid-template-columns: 1fr !important;
    }
    
    .section {
        padding: 1.25rem !important;
    }
    
    .page-title {
        font-size: 2rem !important;
    }
}

/* Print Styles */
@media print {
    .header, .footer, .back-btn, .print-btn {
        display: none;
    }
    
    body {
        background: white;
        color: black;
    }
    
    .section {
        box-shadow: none;
        border: 1px solid #ddd;
        break-inside: avoid;
    }
}

/* Utility Classes */
.text-center { text-align: center; }
.text-accent { color: var(--accent); }
.bg-light { background: var(--light); }
.bg-white { background: var(--white); }
.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }
.p-1 { padding: 0.5rem; }
.p-2 { padding: 1rem; }
.p-3 { padding: 1.5rem; }
.p-4 { padding: 2rem; }
.d-flex { display: flex; }
.align-center { align-items: center; }
.justify-between { justify-content: space-between; }
.flex-wrap { flex-wrap: wrap; }
.gap-1 { gap: 0.5rem; }
.gap-2 { gap: 1rem; }
.gap-3 { gap: 1.5rem; }
.w-100 { width: 100%; }
.h-100 { height: 100%; }
"""
        
        with open("assets/style.css", "w", encoding="utf-8") as f:
            f.write(css)
        print("Generated: assets/style.css")
    
    def generate_schools_json(self, schools):
        """Generate JSON data file for filtering"""
        filtered_data = []
        for school in schools:
            filtered_data.append({
                'id': school['school_id'],
                'name': school['name'],
                'short_name': school.get('short_name', ''),
                'city': school.get('city', ''),
                'province': school.get('province', ''),
                'level': school.get('level', ''),
                'type': school.get('school_type', ''),
                'gender': school.get('gender_focus', ''),
                'curriculum': school.get('curriculum', ''),
                'students': school.get('total_students', 0),
                'teachers': school.get('total_teachers', 0),
                'rating': school.get('overall_rating', 0),
                'established': school.get('establishment_year', 2025),
                'amenities': school.get('amenities', [])[:5]
            })
        
        with open("assets/schools.json", "w", encoding="utf-8") as f:
            json.dump(filtered_data, f, indent=2)
        print("Generated: assets/schools.json")
    
    def generate_sitemap(self, schools):
        """Generate sitemap.xml for SEO"""
        sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://hvstechzw.github.io/Scholastic-Schools-Catalog/</loc>
        <lastmod>2025-01-01</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://hvstechzw.github.io/Scholastic-Schools-Catalog/schools/all.html</loc>
        <lastmod>2025-01-01</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>"""
        
        for school in schools:
            sitemap += f"""
    <url>
        <loc>https://hvstechzw.github.io/Scholastic-Schools-Catalog/schools/{school['school_id']}.html</loc>
        <lastmod>2025-01-01</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>"""
        
        sitemap += "\n</urlset>"
        
        with open("sitemap.xml", "w", encoding="utf-8") as f:
            f.write(sitemap)
        print("Generated: sitemap.xml for SEO")

    def generate_static_files(self):
        """Generate all static website files with all fixes"""
        print("Generating Scholastic Forum website...")
        
        if not self.connect_database():
            print("Failed to connect to database")
            return
        
        # Get schools data
        schools = self.get_schools_data()
        print(f"Loaded {len(schools)} schools from database")
        
        if not schools:
            print("No schools found in database")
            return
        
        # Create directories
        os.makedirs("schools", exist_ok=True)
        os.makedirs("assets", exist_ok=True)
        os.makedirs("assets/images", exist_ok=True)
        
        # Generate homepage
        homepage_html = self.generate_homepage(schools)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(homepage_html)
        print("Generated: index.html (Homepage)")
        
        # Generate all schools page
        all_schools_html = self.generate_all_schools_page(schools)
        with open("schools/all.html", "w", encoding="utf-8") as f:
            f.write(all_schools_html)
        print("Generated: schools/all.html (All Schools)")
        
        # Generate individual school pages
        self.generate_school_pages(schools)
        
        # Generate CSS file
        self.generate_css_file()
        
        # Generate school data JSON for filtering
        self.generate_schools_json(schools)
        
        # Generate sitemap for SEO
        self.generate_sitemap(schools)
        
        # Create placeholder logo files if they don't exist
        self.create_placeholder_logos()
        # Generate mobile app data file
        self.generate_mobile_data_file(schools) 
        
        print(f"\nWebsite generation complete!")
        print(f"- Homepage: index.html")
        print(f"- Schools directory: schools/")
        print(f"- Individual school pages: {len(schools)} pages")
        print(f"- All schools listing: schools/all.html")
        print(f"- Static assets: assets/")
        print(f"- SEO sitemap: sitemap.xml")
        print(f"\nKey Features Implemented:")
        print(f"✓ SEO directing to GitHub Pages: https://hvstechzw.github.io/Scholastic-Schools-Catalog/")
        print(f"✓ Theme locked to light theme (even on mobile)")
        print(f"✓ Search filters fully functional and immediately responsive")
        print(f"✓ Manufacturer logo enlarged in footer (48px height)")
        print(f"✓ All functionality maintained and production-ready")
        print(f"✓ Mobile-responsive design")
        print(f"✓ Advanced SEO meta tags")
        print(f"✓ Structured data for search engines")
        print(f"✓ Sitemap generated")
        print(f"✓ Accessibility improvements")
        print(f"✓ Performance optimizations")
        print(f"✓ Ready for future scalability")
        print(f"✓ Mobile App Data File:")
        print(f"✓ Ready to launch immediately")
        
    def create_placeholder_logos(self):
        """Create placeholder logo files if they don't exist"""
        # Create simple HTML for placeholder logos
        logos = [
            ("logo_light.png", "SF"),
            ("manufacturer_dark.png", "HVST"),
            ("og-image.jpg", "Scholastic Forum")
        ]
        
        for filename, text in logos:
            path = f"assets/images/{filename}"
            if not os.path.exists(path):
                try:
                    with open(path, 'w') as f:
                        f.write(f"<!-- Placeholder for {text} -->")
                    print(f"Created placeholder: {path}")
                except:
                    pass
    
    def generate_mobile_data_file(self, schools):
        """Generate JSON data file for mobile app consumption"""
        mobile_data = []
        
        for school in schools:
            school_data = {
                'school_id': school['school_id'],
                'name': school['name'],
                'short_name': school.get('short_name', ''),
                'motto': school.get('motto', ''),
                'mission': school.get('mission', ''),
                'vision': school.get('vision', ''),
                'description': school.get('description', ''),
                'school_type': school.get('school_type', ''),
                'gender_focus': school.get('gender_focus', ''),
                'level': school.get('level', ''),
                'category': school.get('category', ''),
                'establishment_year': school.get('establishment_year', 2025),
                'address': school.get('address', ''),
                'city': school.get('city', ''),
                'province': school.get('province', ''),
                'district': school.get('district', ''),
                'country': school.get('country', ''),
                'postal_code': school.get('postal_code', ''),
                'google_maps_link': school.get('google_maps_link', ''),
                'email': school.get('email', ''),
                'phone': school.get('phone', ''),
                'phone_primary': school.get('phone_primary', ''),
                'website': school.get('website', ''),
                'facebook_page': school.get('facebook_page', ''),
                'twitter_handle': school.get('twitter_handle', ''),
                'instagram_handle': school.get('instagram_handle', ''),
                'linkedin_page': school.get('linkedin_page', ''),
                'principal_name': school.get('principal_name', ''),
                'principal_email': school.get('principal_email', ''),
                'curriculum': school.get('curriculum', ''),
                'total_students': school.get('total_students', 0),
                'total_teachers': school.get('total_teachers', 0),
                'total_classrooms': school.get('total_classrooms', 0),
                'science_labs': school.get('science_labs', 0),
                'computer_labs': school.get('computer_labs', 0),
                'library_rooms': school.get('library_rooms', 0),
                'playground_area': school.get('playground_area', ''),
                'sports_facilities': school.get('sports_facilities', ''),
                'has_library': 1 if school.get('has_library') else 0,
                'has_science_lab': 1 if school.get('has_science_lab') else 0,
                'has_computer_lab': 1 if school.get('has_computer_lab') else 0,
                'has_playground': 1 if school.get('has_playground') else 0,
                'has_sports_field': 1 if school.get('has_sports_field') else 0,
                'has_swimming_pool': 1 if school.get('has_swimming_pool') else 0,
                'has_auditorium': 1 if school.get('has_auditorium') else 0,
                'has_cafeteria': 1 if school.get('has_cafeteria') else 0,
                'has_health_clinic': 1 if school.get('has_health_clinic') else 0,
                'has_wifi': 1 if school.get('has_wifi') else 0,
                'has_smart_classes': 1 if school.get('has_smart_classes') else 0,
                'hostel_facilities': 1 if school.get('hostel_facilities') else 0,
                'transport_services': 1 if school.get('transport_services') else 0,
                'fee_range': school.get('fee_range', ''),
                'scholarships_available': 1 if school.get('scholarships_available') else 0,
                'scholarship_details': school.get('scholarship_details', ''),
                'overall_rating': float(school.get('overall_rating', 0)),
                'total_reviews': school.get('total_reviews', 0),
                'academic_rating': float(school.get('academic_rating', 0)),
                'facility_rating': float(school.get('facility_rating', 0)),
                'discipline_rating': float(school.get('discipline_rating', 0)),
                'logo_url': f"https://hvstechzw.github.io/Scholastic-Schools-Catalog/assets/logos/{school['school_id']}.png" if school.get('logo_base64') else '',
                'banner_url': f"https://hvstechzw.github.io/Scholastic-Schools-Catalog/assets/banners/{school['school_id']}.jpg" if school.get('banner_base64') else '',
                'latitude': school.get('latitude'),
                'longitude': school.get('longitude'),
                'created_at': school.get('created_at', datetime.now().isoformat()),
                'amenities': school.get('amenities', []),
                'social_links': school.get('social_links', {})
            }
            mobile_data.append(school_data)
        
        with open("assets/schools_data.json", "w", encoding="utf-8") as f:
            json.dump(mobile_data, f, indent=2, default=str)
        print("Generated: assets/schools_data.json (for mobile app)")
        
        # Also create base64 version for immediate use
        schools_with_base64 = []
        for school in schools:
            school_copy = school.copy()
            school_copy['logo_url'] = f"data:image/jpeg;base64,{school_copy.get('logo_base64', '')}" if school_copy.get('logo_base64') else ''
            school_copy['banner_url'] = f"data:image/jpeg;base64,{school_copy.get('banner_base64', '')}" if school_copy.get('banner_base64') else ''
            schools_with_base64.append(school_copy)
        
        with open("assets/schools_data_base64.json", "w", encoding="utf-8") as f:
            json.dump(schools_with_base64, f, indent=2, default=str)
        print("Generated: assets/schools_data_base64.json (with base64 images)")
    # Main execution
if __name__ == "__main__":
    # Make sure to update the database path if needed
    db_path = "C:\\Users\\highv\\Desktop\\Scholastic Services\\SSMA01 - Schools Management\\Source Code\\V 0.0.1 BETA\\school_manager.db"  # Update this if your database is in a different location
    
    generator = ScholasticForumWebsiteGenerator(db_path)
    generator.generate_static_files()