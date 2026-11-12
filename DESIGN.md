---
name: Google Educational Material
colors:
  surface: '#faf9fd'
  surface-dim: '#dbd9dd'
  surface-bright: '#faf9fd'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f3f7'
  surface-container: '#efedf1'
  surface-container-high: '#e9e7eb'
  surface-container-highest: '#e3e2e6'
  on-surface: '#1a1b1e'
  on-surface-variant: '#414754'
  inverse-surface: '#2f3033'
  inverse-on-surface: '#f1f0f4'
  outline: '#727785'
  outline-variant: '#c1c6d6'
  surface-tint: '#005bc0'
  primary: '#005bbf'
  on-primary: '#ffffff'
  primary-container: '#1a73e8'
  on-primary-container: '#ffffff'
  inverse-primary: '#adc7ff'
  secondary: '#076d2e'
  on-secondary: '#ffffff'
  secondary-container: '#9cf7a7'
  on-secondary-container: '#147434'
  tertiary: '#944a00'
  on-tertiary: '#ffffff'
  tertiary-container: '#b95e00'
  on-tertiary-container: '#ffffff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc7ff'
  on-primary-fixed: '#001a41'
  on-primary-fixed-variant: '#004493'
  secondary-fixed: '#9cf7a7'
  secondary-fixed-dim: '#81da8d'
  on-secondary-fixed: '#002109'
  on-secondary-fixed-variant: '#005320'
  tertiary-fixed: '#ffdcc6'
  tertiary-fixed-dim: '#ffb785'
  on-tertiary-fixed: '#301400'
  on-tertiary-fixed-variant: '#713700'
  background: '#faf9fd'
  on-background: '#1a1b1e'
  surface-variant: '#e3e2e6'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Inter
    fontSize: 26px
    fontWeight: '600'
    lineHeight: 34px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  code-lg:
    fontFamily: JetBrains Mono
    fontSize: 16px
    fontWeight: '500'
    lineHeight: 24px
    letterSpacing: -0.01em
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: -0.01em
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  margin: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system delivers an approachable, focused, and systematic workspace for technical education in computer networking. Targeted at vocational high school instructors and networking students, the interface bridges foundational technical rigor with clarity. 

The aesthetic adheres to **Corporate / Modern Minimalism** inspired by modern Google Material design patterns. It prioritizes legibility, cognitive breathing room, and structured feedback over ornamental decoration. Pure white and warm tinted surfaces provide an uncluttered backdrop, while crisp micro-borders and soft ambient elevation delineate functional working zones. Monospaced notations for bitfields, subnet masks, and network addresses sit alongside friendly, humanized typography to reduce the intimidation factor of binary mathematics and Variable Length Subnet Masking (VLSM).

## Colors

The color system establishes functional hierarchy through accessible tonal contrast and familiar educational indicators:

- **Primary (`#1A73E8`)**: Google Educational Royal Blue serves as the key action and interactive focus color. Interactive hover states transition to `#1557B0`. Surface tint `#E8F0FE` is used for active pill selections, focused field backgrounds, and interactive subnet blocks.
- **Secondary (`#137333`)**: Emerald Green indicates valid CIDR allocations, non-overlapping subnet allocations, and verified student calculations. Paired with container tint `#E6F4EA`.
- **Tertiary (`#E37400`)**: Amber signals host waste warnings, edge-case broadcast boundaries, and instructional callouts. Paired with container tint `#FEF7E0`.
- **Error / Critical (`#D93025`)**: Crimson Red communicates validation failures (e.g., prefix overflow, invalid octets, overlapping ranges). Paired with container tint `#FCE8E6`.
- **Neutral Core**:
  - Surface Background: `#FFFFFF` (pure canvas) and `#F8FAFC` (workspace canvas).
  - Borders & Dividers: `#E2E8F0` and `#E8EAED`.
  - Content Text: `#202124` (primary text, high contrast) and `#5F6368` (secondary metadata, units, and structural labels).

## Typography

The type system blends **Inter** for UI controls, instruction copy, and tabular headers with **JetBrains Mono** for technical networking data:

- **Inter**: Selected for clean geometry, high legibility across small sizes, and open aperture. Used across structural headers, tooltips, instructional steps, and interactive input labels.
- **JetBrains Mono**: Assigned to every octet representation, network address, subnet mask, CIDR prefix, wildcard mask, and 32-bit binary breakdown. Fixed-width character sizing prevents misalignment when rendering stacked IP addresses, network ranges, and subnet bit split charts.

## Layout & Spacing

The interface runs on an 8pt base modular rhythm using a fluid, responsive 12-column grid system capped at a maximum width of `1280px` to maintain optimal focus during calculation and lab walkthroughs.

- **Desktop (>= 1024px)**: 12 columns, `1.5rem` (`24px`) gutters, `2rem` (`32px`) margins. Two-pane layout with parameter configuration on the left (4–5 columns) and dynamic VLSM visualizer/table output on the right (7–8 columns).
- **Tablet (768px - 1023px)**: 8 columns, `1rem` (`16px`) gutters, `1.5rem` (`24px`) margins. Vertically stacked input blocks with horizontal scrolling for dense binary/subnet lookup tables.
- **Mobile (< 768px)**: 4 columns, `0.75rem` (`12px`) gutters, `1rem` (`16px`) margins. Form elements expand to full container width; tables convert into stacked card summaries per allocated subnet.

## Elevation & Depth

Visual hierarchy uses a hybrid of **tonal layering** and **low-contrast ambient drop shadows**, avoiding dark or harsh cast shadows:

- **Level 0 (Flat Canvas)**: Neutral surface `#F8FAFC`. Zero elevation.
- **Level 1 (Card & Section Containers)**: `#FFFFFF` fill with a `1px` crisp border `#E8EAED` and an ambient shadow `0 1px 3px 0 rgba(60, 64, 67, 0.08), 0 1px 2px 0 rgba(60, 64, 67, 0.04)`.
- **Level 2 (Active Cards / Floating Menus)**: `#FFFFFF` fill, `1px` border `#E2E8F0`, and shadow `0 4px 12px 0 rgba(60, 64, 67, 0.12), 0 1px 3px 0 rgba(60, 64, 67, 0.06)`. Used for active CIDR selector dropdowns and hover states on subnet allocation blocks.
- **Level 3 (Modals / Educational Popovers)**: `#FFFFFF` fill with `0 12px 24px 0 rgba(60, 64, 67, 0.16)`.

## Shapes

The design system employs **Rounded (Level 2)** geometry to evoke Google's approachable educational tool aesthetic:

- Standard controls (input fields, default buttons, selector pills) adopt an `8px` (`0.5rem`) radius.
- Cards, calculation result panels, and visual block containers use a softer `16px` (`1rem`, `rounded-lg` to `rounded-xl`) radius to separate mathematical modules visually.
- Status chips, step count badges, and CIDR shorthand tags use a pill radius (`9999px`) for quick visual identification.

## Components

### Buttons
- **Primary**: Solid `#1A73E8` fill, white `#FFFFFF` text, `0.5rem` radius, `0 1px 2px rgba(26, 115, 232, 0.2)` shadow. Hover `#1557B0`. Focused with a `2px` offset outline in `#1A73E8`.
- **Secondary / Outlined**: `#FFFFFF` background, `1px` border `#E2E8F0`, `#1A73E8` text. Hover brings `#E8F0FE` background with `#1557B0` border.
- **Text Button**: Borderless, `#1A73E8` font, soft `#E8F0FE` fill on hover.

### Form Inputs
- **Outlined Text Inputs**: Background `#FFFFFF`, border `1px` solid `#E8EAED`, text `#202124`. Radius `0.5rem`.
- **Focus State**: `2px` solid `#1A73E8` border with no clipping, label transitions to `#1A73E8`.
- **Error State**: Border shifts to `#D93025`; persistent helper text rendered in `code-sm` or `body-sm` using `#D93025`.
- **IP Octet Input Groups**: Segmented flex fields with monospace formatting, dots fixed in `#5F6368` text between octets.

### Tabs & Segmented Switchers
- Surface-encapsulated rounded tab container with `#F1F3F4` fill and `0.5rem` radius.
- Active tab pill has `#FFFFFF` fill, `#202124` text, and subtle elevation `0 1px 3px rgba(0,0,0,0.1)`. Inactive tabs render with `#5F6368` text.

### Result Cards & Visualizer
- **Cards**: Border `1px` `#E8EAED`, background `#FFFFFF`, radius `1rem`. Top border features an optional `3px` accent strip indicating subnet validity (`#137333` valid, `#D93025` error, `#1A73E8` primary).
- **Binary Bit Breakdown Component**: Horizontal flex container displaying Network Bits (`#E8F0FE` fill, `#1A73E8` text) against Host Bits (`#F1F3F4` fill, `#5F6368` text) separated by a dashed boundary line.

### Data Tables (Subnet Allocation Table)
- **Header**: `#F8FAFC` background, `1px` bottom border `#E2E8F0`, uppercase text styled in `label-sm` with `#5F6368`.
- **Rows**: Alternating background (`#FFFFFF` to `#FDFEFE`), border-bottom `1px` `#F1F3F4`. Hover row state uses `#F8FAFC`.
- **Cells**: Network address, usable range, and broadcast columns styled in `code-md`. Total host count right-aligned.

### Badges & Chips
- Rounded pill shape (`rounded-full`), `space-xs` vertical padding, `space-sm` horizontal padding.
- Success: Background `#E6F4EA`, text `#137333`.
- Warning: Background `#FEF7E0`, text `#B06000`.
- Error: Background `#FCE8E6`, text `#D93025`.
- Active CIDR: Background `#E8F0FE`, text `#1A73E8`.
