# Implementation Plan - UI/UX Overhaul

This plan outlines the steps to implement the UI/UX recommendations for the e-Kost website, focusing on mobile responsiveness, consistency, and a modern aesthetic.

## User Review Required
> [!IMPORTANT]
> The Navbar redesign will significantly change the look of the site header from a dark gradient to a clean white/light style.

## Proposed Changes

### Core UI (`base.html` & `script.js`)
#### [MODIFY] [base.html](file:///c:/Users/azmia/e_kost/templates/base.html)
- **Mobile Navigation**: Add a hamburger menu button and a hidden mobile menu container.
- **Navbar Redesign**: Switch from dark gradient background to a clean white background with subtle shadow. Update text colors to be dark for contrast.
- **Footer**: Keep dark for contrast, but refine spacing.

#### [MODIFY] [script.js](file:///c:/Users/azmia/e_kost/static/js/script.js)
- **Mobile Toggle Logic**: Add JavaScript to handle the click event on the hamburger button to show/hide the mobile menu.

### Page Specific - Rooms (`rooms.html`)
#### [MODIFY] [rooms.html](file:///c:/Users/azmia/e_kost/templates/rooms.html)
- **Standardize Cards**: Update "Room Card 2" to use the same classes as Card 1 and 3 (`rounded-3xl`, `shadow-xl`, gradient buttons).
- **Filter Section**: Ensure the sticky filter looks good with the new lighter theme.

### Page Specific - Home (`index.html`)
#### [MODIFY] [index.html](file:///c:/Users/azmia/e_kost/templates/index.html)
- **Hero Section**: Refine the gradient to be more subtle or "glass-like" to match the new clean navbar.
- **Buttons**: Ensure all CTA buttons match the new consistent style.

## Verification Plan

### Manual Verification
- **Mobile Menu**: Shrink browser window to mobile width, click hamburger menu, verify it opens/closes.
- **Card Consistency**: Check `rooms.html` to ensure all 3 cards look identical in style.
- **Visual Check**: Verify the new Navbar looks professional and scrolling is smooth.
