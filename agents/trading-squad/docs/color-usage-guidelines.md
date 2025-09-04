# Trading Squad UI Color Usage Guidelines

## Overview
This document defines the unified color palette and usage guidelines for the Trading Squad Streamlit UI to ensure consistent visual branding and maintainable code.

## Unified Color Palette

### Primary Colors
- **`--primary-blue`** (#1f77b4): Main brand color for headers, primary buttons, and key UI elements
- **`--primary-blue-light`** (#4a9eff): Hover states and accent highlights
- **`--primary-blue-dark`** (#0d5aa7): Gradients and depth effects

### Secondary Colors
- **`--secondary-blue`** (#17a2b8): Running agent status indicators and secondary elements
- **`--accent-blue`** (#5a9fd4): Metric cards and decorative elements
- **`--accent-blue-dark`** (#3d7ba8): Accent gradients and depth

### Status Colors
- **`--success-green`** (#28a745): Completed states, success indicators
- **`--warning-yellow`** (#ffc107): Pending states, warnings
- **`--danger-red`** (#dc3545): Error states, critical alerts

### Neutral Colors
- **`--white`** (#ffffff): Backgrounds, text on dark elements
- **`--light-gray`** (#f8f9fa): Container backgrounds, subtle separators
- **`--medium-gray`** (#e0e0e0): Borders, scrollbars, inactive elements
- **`--dark-gray`** (#333333): Text, active scrollbar elements

## Usage Guidelines

### Headers and Branding
```css
/* Main header with brand gradient */
background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);
```

### Buttons
```css
/* Primary buttons */
background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);

/* Hover states */
background: linear-gradient(135deg, var(--primary-blue-light) 0%, var(--primary-blue) 100%);

/* Status-specific buttons */
.agent-completed: var(--success-green)
.agent-error: var(--danger-red)
.agent-running: var(--primary-blue) with animation
```

### Status Indicators
```css
/* Agent status borders */
.agent-status-pending: var(--warning-yellow)
.agent-status-running: var(--secondary-blue)
.agent-status-complete: var(--success-green)
```

### Interactive Elements
```css
/* Metric cards */
background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-blue-dark) 100%);

/* Streaming messages */
border-left: 3px solid var(--primary-blue);

/* Activity indicators */
.activity-running: var(--primary-blue)
.activity-complete: var(--success-green)
.activity-pending: var(--warning-yellow)
```

## Best Practices

### DO
- ✅ Always use CSS custom properties instead of hardcoded hex values
- ✅ Use gradients for depth and visual interest: `linear-gradient(135deg, color1, color2)`
- ✅ Apply consistent hover states with lighter variants
- ✅ Use status colors semantically (green=success, yellow=pending, red=error)
- ✅ Maintain 135-degree gradient angle for consistency

### DON'T
- ❌ Use hardcoded hex colors like `#1f77b4` directly in styles
- ❌ Mix different gradient angles without purpose
- ❌ Use status colors for non-status elements
- ❌ Create new color variants without updating this palette

## Animation Integration
Colors work seamlessly with our optimized animations:
```css
/* Pulse animation uses primary blue variants */
@keyframes pulse {
    box-shadow: var(--shadow-glow); /* Uses primary-blue */
}

/* Glow animation transitions between primary variants */
@keyframes glow {
    border-color: var(--primary-blue) to var(--primary-blue-dark);
}
```

## Accessibility Considerations
- All color combinations meet WCAG contrast requirements
- Status colors are supplemented with visual indicators (borders, icons)
- Hover states provide clear visual feedback
- `prefers-reduced-motion` is respected for animations

## Maintenance
When adding new UI elements:
1. Check if existing palette covers your needs
2. Use semantic color names (primary, secondary, status)
3. Update this document if new colors are added
4. Test all interactive states (hover, active, focus)
5. Validate accessibility compliance

## Version History
- **v1.0** (August 2025): Initial unified color palette implementation
- Replaced inconsistent purple-blue gradients with cohesive blue-based system
- Simplified button styling with consistent color logic
- Added accent colors for metric cards and decorative elements
