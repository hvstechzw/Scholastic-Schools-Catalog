# Scholastic Services SchoolFinder Website

Generated on: 2025-12-22 16:30:20
Total Schools: 2
Database: school_manager.db
Developer: High Voltage Software Technologies
Established: 2025

## Files Generated:
- index.html - Main homepage with all schools
- schools.json - Basic school data for index page
- schools-full.json - Complete school data for detail pages
- [school-name].html - Individual school detail pages (clean URLs)
- .nojekyll - Disables Jekyll processing on GitHub Pages
- logo_light.png - Main logo for light theme
- logo_dark.png - Main logo for dark theme
- manufacturer_light.png - Developer logo for light theme
- manufacturer_dark.png - Developer logo for dark theme

## Key Features:
- Mobile-first responsive design
- Google Maps integration for school locations
- Online ratings and reviews system
- Dark/Light theme switcher
- Search and filter functionality
- Clean URL structure (school-name.html)
- GitHub Pages compatible
- All data fetched from JSON files

## How to Use:
1. Upload ALL files to GitHub Pages
2. Make sure your logo files (logo_light.png, logo_dark.png, manufacturer_light.png, manufacturer_dark.png) are in the same folder
3. Open index.html in any web browser
4. Browse schools using search and filters
5. Click on any school to view detailed information
6. Use the theme switcher button (bottom right) to toggle between light/dark modes

## GitHub Pages Deployment:
1. Create a repository on GitHub
2. Upload all files from the output folder
3. Go to Settings > Pages
4. Set source to "main" branch and "/ (root)" folder
5. Your site will be available at: https://[username].github.io/[repository]/

## Theme Support:
The website supports both light and dark themes with:
- Automatic detection of system preference
- Manual theme switching
- Theme persistence using localStorage
- Separate logos for each theme

## Statistics:
- Total Schools: 2
- Total Students: 497
- Total Teachers: 23
- Schools with Logos: 2
- Schools with Coordinates: 2
- Schools with Reviews: 0

## Notes:
- All school logos are embedded as base64 in the JSON files
- Google Maps uses a demo API key (replace with your own in production)
- The website is fully static and works without any server-side processing
- All functionality works offline after initial load
