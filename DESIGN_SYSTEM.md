## 1) Design Principles

- **Clarity first**: readable typography, high-contrast text, predictable layouts.
- **Soft surfaces**: light gradients, subtle borders, and low-elevation shadows.
- **Rounded geometry**: generous radii on containers and controls.
- **Consistent interaction**: smooth transitions (`0.15s`–`0.3s`) and focus rings.

## 2) System Configuration (How styles are applied)

- **Tailwind CSS**: loaded via CDN
&nbsp; - `https://cdn.jsdelivr.net/npm/tailwindcss@3.4.15/dist/tailwind.min.css`
- **Tailwind Browser Runtime**:
&nbsp; - `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4`
- **Icons**: Iconify Solar Icons
&nbsp; - `https://code.iconify.design/3/3.1.1/iconify.min.js`
- **No local Tailwind config detected** (`tailwind.config.*` not present). The project relies on Tailwind defaults + template-level styles.

**Source-of-truth templates for design tokens**

- `templates/base.html` (Student app shell + “Minimal” component styles)
- `templates/admin_base.html` (Admin component styles)
- `templates/login.html`, `templates/admin_login.html` (Splash screen + auth card)
- `templates/register.html` (Wizard + auth card)

## 3) Color System

This project primarily uses Tailwind’s **Slate** scale for neutrals and **Indigo/Purple** as the main brand accent.

### 3.1 Neutrals (Slate)

Used heavily via Tailwind classes:

- `bg-gradient-to-br from-slate-50 to-slate-100` (page background)
- `text-slate-800` (default text)
- `text-slate-900` (headings)
- `text-slate-500` / `text-slate-400` (secondary text)
- `border-slate-200` / `border-slate-300` (borders & dividers)
- `bg-slate-50` / `bg-slate-100` / `bg-slate-200` (soft surfaces)
- `bg-slate-900` / `to-slate-800` (dark surfaces)

Additional neutral hex values used in inline styles:

- `#f8fafc` (table header background)
- `#e2e8f0` (borders, soft button backgrounds, rings, etc.)
- `#cbd5e1` (hover border, soft button border)
- `#64748b` (muted text)
- `#334155` (hover text / focus border)
- `#0f172a` / `#020617` (dark primary/admin)

### 3.2 Brand Accent (Indigo / Purple)

Used for primary actions and highlights:

- **Primary gradient**: `linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)`
- **Primary hover gradient**: `linear-gradient(135deg, #4f46e5 0%, #4338ca 100%)`
- Tailwind usage:
&nbsp; - `bg-indigo-50`, `text-indigo-600`, `text-indigo-700`
&nbsp; - `from-indigo-500 to-purple-600`

### 3.3 Status / Semantic Colors

- **Success (Emerald)**
&nbsp; - Tailwind: `bg-emerald-50`, `text-emerald-700`, `border-emerald-200`
&nbsp; - Primary success CTA: `from-emerald-500 to-emerald-600`
- **Danger (Rose)**
&nbsp; - Tailwind: `bg-rose-50`, `text-rose-700`, `border-rose-200`
&nbsp; - Admin danger button hex:
&nbsp;   - `#fff1f2` (bg)
&nbsp;   - `#be123c` (text)
&nbsp;   - `#ffe4e6` (hover bg)
- **Info (Blue / Sky)**
&nbsp; - Progress bar gradient: `linear-gradient(90deg, #3b82f6, #8b5cf6)`
&nbsp; - Attendance ring uses: `#0ea5e9`

### 3.4 Data Visualization (Attendance “heat”)

Inline palette in `templates/base.html`:

- `level-0`: `#ebedf0`
- `level-1`: `#9be9a8`
- `level-2`: `#40c463`
- `level-3`: `#30a14e`
- `level-4`: `#216e39`

## 4) Typography

The project uses **Tailwind defaults** (system-ui stack). No custom font-family was found.

### 4.1 Type Scale (observed)

Common Tailwind sizes used:

- `text-xs` (labels, metadata)
- `text-sm` (body, buttons)
- `text-lg` (section titles)
- `text-xl` (page header title)

Custom sizes used:

- `text-[11px]` (mobile nav label)

### 4.2 Font Weights

- `font-medium` (buttons, labels)
- `font-semibold` (headers, card titles)
- `font-bold`/`700` (splash branding)

### 4.3 Letter Spacing / Case

- “App brand” label: `uppercase tracking-[0.2em]`
- Form labels: `uppercase tracking-wider`
- Admin table headers:
&nbsp; - `font-size: 12px`
&nbsp; - `letter-spacing: 0.06em`
&nbsp; - `text-transform: uppercase`

## 5) Spacing (Padding, Margin, Layout)

Spacing is primarily Tailwind spacing scale.

### 5.1 Layout Containers

- **Page background**: `min-h-screen bg-gradient-to-br from-slate-50 to-slate-100`
- **App layout grid**: `grid grid-cols-1 md:grid-cols-[280px_1fr]`
- **Main padding**:
&nbsp; - Student content area: `p-6 md:p-8`
&nbsp; - Admin content area: `p-4 sm:p-6 md:p-8`
- **Sidebars**: `p-6` with `gap-6`

### 5.2 Form spacing

- Forms often use `space-y-4` or `space-y-6`
- Labels typically use `mb-2`

## 6) Radius (“Softness”)

The interface leans toward **rounded** components.

Observed radii:

- `rounded-xl` (controls, buttons, nav items)
- `rounded-2xl` (cards, avatar containers)
- `rounded-t-3xl` (bottom sheet)
- `rounded-full` / `999px` (pills, dots)

Inline radii:

- `12px` (buttons/inputs)
- `14px` (avatar)
- `16px` (cards)
- `20px` (badge)
- `24px` (splash logo)

## 7) Elevation (Shadows)

The project uses subtle shadows with Slate-based RGBA.

### 7.1 Key shadow tokens (observed)

- **App shell / Auth card shadow**
&nbsp; - `0 30px 80px rgba(15, 23, 42, 0.15), 0 2px 10px rgba(15, 23, 42, 0.06)`
- **Card base**
&nbsp; - `0 1px 3px rgba(15, 23, 42, 0.04)`
- **Card hover**
&nbsp; - `0 4px 12px rgba(15, 23, 42, 0.08)`
- **Avatar**
&nbsp; - `0 2px 8px rgba(15, 23, 42, 0.08)`
- **Admin soft button**
&nbsp; - `0 1px 2px rgba(15, 23, 42, 0.06)`
- **Splash logo**
&nbsp; - `0 20px 60px rgba(0, 0, 0, 0.3)`

## 8) Motion & Transitions

### 8.1 Transition timings

- `0.15s` (admin buttons)
- `0.2s` (minimal card/button/nav/input)
- `0.3s` (progress bar width/opacity; bottom-sheet transforms)

### 8.2 Animations

- **Fade-in content** (`templates/base.html`)
&nbsp; - `fadeIn`: `opacity` + `translateY(10px)`
- **Splash screen** (`templates/login.html`, `templates/admin_login.html`)
&nbsp; - `splash-pulse`: scale `1.00` → `1.05`
&nbsp; - `splash-fade-in`: `opacity` + `translateY(20px)`

## 9) Focus States & Accessibility

Focus patterns are consistent:

- Inputs use:
&nbsp; - `focus:outline-none`
&nbsp; - `focus:border-...`
&nbsp; - `focus:ring-4 focus:ring-.../10`
- Admin input focus (inline):
&nbsp; - `box-shadow: 0 0 0 4px rgba(15, 23, 42, 0.08)`

Guidelines:

- Use **ring + border** for focus visibility.
- Avoid removing focus state unless an alternative focus style is present.

## 10) Component System (Project Elements)

### 10.1 Student “Minimal” components (`templates/base.html`)

- **Card**: `.minimal-card`
&nbsp; - White background, `16px` radius, `1px` slate border, subtle shadow, hover elevation.
- **Button**: `.minimal-btn` + `.minimal-btn-primary`
&nbsp; - `12px` radius, gradient primary, hover lift + shadow.
- **Input**: `.minimal-input`
&nbsp; - `12px` radius, slate border, soft indigo ring on focus.
- **Navigation item**: `.minimal-nav-item` (+ `.active`)
&nbsp; - Rounded, padded, muted slate text; soft hover surface.
- **Badge**: `.minimal-badge`
&nbsp; - Pill-like rounded corners, small text.
- **Avatar**: `.minimal-avatar`
&nbsp; - Rounded, border + subtle shadow.

### 10.2 Admin components (`templates/admin_base.html`)

- **Card**: `.admin-card`
&nbsp; - Same surface language as minimal card.
- **Table header**: `.admin-table thead`, `.admin-table th`
- **Input**: `.admin-input`
&nbsp; - Slightly larger padding (`12px 16px`), dark/slate focus ring.
- **Buttons**:
&nbsp; - `.admin-btn` base (inline-flex, `12px` radius)
&nbsp; - `.admin-btn-primary` (dark slate)
&nbsp; - `.admin-btn-soft` (soft slate surface)
&nbsp; - `.admin-btn-danger` (rose)
- **Pill**: `.admin-pill` (fully rounded)

### 10.3 Auth cards (login/register)

- Shared auth card style:
&nbsp; - `bg-white border border-slate-200 rounded-2xl`
&nbsp; - shadow token: `shadow-[0_30px_80px_rgba(15,23,42,0.15),0_2px_10px_rgba(15,23,42,0.06)]`

## 11) Recommended Usage Rules

- Prefer **Tailwind utilities** for layout and spacing.
- Reuse existing component classes (`minimal-*`, `admin-*`) when matching existing UI.
- When introducing new colors or shadows, add them here first (this file stays authoritative).

## 12) Future Improvements (Optional)

If you want a stricter design system:

- Add a local `tailwind.config.js` and define `theme.extend` tokens.
- Move inline `<style>` blocks into a single `static/styles.css` and keep templates utility-only.
- Define CSS variables for tokens (`--color-*`, `--radius-*`, `--shadow-*`) to reduce repetition.
## ROOT DESIGN TOKENS (GLOBAL CONTRACT)
### Color Tokens — Light Theme (Default)
```css
:root {
  /* ====== SURFACE COLORS ====== */
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-tertiary: #f1f5f9;
  /* ====== TEXT COLORS ====== */
  --text-primary: #0f172a;
  --text-secondary: #334155;
  --text-muted: #64748b;
  /* ====== BORDER COLORS ====== */
  --border-primary: #e2e8f0;
  --border-secondary: #cbd5f5;
  /* ====== BRAND COLORS ====== */
  --brand-primary: #2563eb;
  --brand-secondary: #1e40af;
  --brand-soft: #dbeafe;
  /* ====== STATUS COLORS ====== */
  --success: #16a34a;
  --warning: #f59e0b;
  --danger: #dc2626;
  --info: #0284c7;
  /* ====== SHADOW COLORS ====== */
  --shadow-color: rgba(15, 23, 42, 0.08);
}
```
### Dark Theme Tokens
```css
[data-color-scheme="dark"] {
  /* ====== SURFACE COLORS ====== */
  --bg-primary: #020617;
  --bg-secondary: #020617;
  --bg-tertiary: #020617;
  /* ====== TEXT COLORS ====== */
  --text-primary: #e5e7eb;
  --text-secondary: #cbd5f5;
  --text-muted: #94a3b8;
  /* ====== BORDER COLORS ====== */
  --border-primary: #020617;
  --border-secondary: #020617;
  /* ====== BRAND COLORS ====== */
  --brand-primary: #3b82f6;
  --brand-secondary: #1d4ed8;
  --brand-soft: #020617;
  /* ====== STATUS COLORS ====== */
  --success: #22c55e;
  --warning: #facc15;
  --danger: #ef4444;
  --info: #38bdf8;
  /* ====== SHADOW COLORS ====== */
  --shadow-color: rgba(0, 0, 0, 0.65);
}
```
## SPACING & RHYTHM SYSTEM
### Spacing Scale (Symmetry-Enforced)
```css
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
}
```
## TYPOGRAPHY SYSTEM
```css
:root {
  --font-sans: "Public-Sans", sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, monospace;
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
}
```
## RADIUS & ELEVATION (VISUAL HARMONY)
### Border Radius Tokens
```css
:root {
  --radius-sm: 0.375rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --radius-xl: 1.5rem;
  --radius-2xl: 2rem;
}
```
### Elevation Tokens
```css
:root {
  --shadow-xs: 0 1px 2px var(--shadow-color);
  --shadow-sm: 0 2px 4px var(--shadow-color);
  --shadow-md: 0 6px 16px var(--shadow-color);
  --shadow-lg: 0 12px 32px var(--shadow-color);
}
```