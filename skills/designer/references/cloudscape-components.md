# Cloudscape Design System — Component Reference

Source: cloudscape.design (AWS's open-source design system)

## When to Use
Always use Cloudscape components for any CloudWatch APM prototype. This is the standard AWS console component library.

## Core Layout Components

| Component | Use For | Notes |
|-----------|---------|-------|
| **App Layout** | Page shell with nav, breadcrumbs, tools panel | Always the outermost wrapper |
| **Content Layout** | Page-level content organization | Header + body with overlap support |
| **Split Panel** | Detail pane (bottom or side) | Use for "click row → see details" pattern |
| **Drawer** | Side panels for tools, help, preferences | Slides in from right |
| **Grid** | Responsive column layout | Use for dashboard-style layouts |
| **Column Layout** | Multi-column within a page | Simpler than Grid for basic layouts |
| **Space Between** | Consistent spacing between elements | Use instead of manual margins |
| **Container** | Content grouping with header | Every logical section gets a Container |

## Data Display Components

| Component | Use For | Notes |
|-----------|---------|-------|
| **Table** | Tabular data with sort/filter/pagination | Most-used component in APM consoles |
| **Cards** | Grid of summary items | Use for service cards, metric summaries |
| **Key Value Pairs** | Label-value display | Use in detail panels for metadata |
| **Property Filter** | Advanced query builder | Boolean AND/OR filters on table data |
| **Collection Preferences** | Column visibility, page size, display mode | Pair with Table for user preferences |
| **Attribute Editor** | Editable key-value pairs | Use for tag editing, config |
| **Token Group** | Tag/chip display | Use for filter tokens, labels |

## Navigation Components

| Component | Use For | Notes |
|-----------|---------|-------|
| **Breadcrumb Group** | Hierarchical navigation | Always present in App Layout |
| **Side Navigation** | Left nav menu | Service-level navigation |
| **Tabs** | In-page section switching | Max 7 tabs |
| **Link** | Inline navigation | Cross-references between entities |
| **Pagination** | Table/list pagination | Always use with Table |

## Feedback & Status Components

| Component | Use For | Notes |
|-----------|---------|-------|
| **Flashbar** | Page-level notifications | Success, error, warning, info |
| **Alert** | Inline warnings/info | Within content sections |
| **Status Indicator** | Health/status badges | Healthy, Warning, Error, Stopped |
| **Progress Bar** | Operation progress | Loading, processing states |
| **Spinner** | Loading states | Use sparingly — prefer skeleton loading |
| **Badge** | Count indicators | Unread, pending items |

## Input Components

| Component | Use For | Notes |
|-----------|---------|-------|
| **Button** | Primary actions | Primary (blue), Normal (white), Link style |
| **Button Dropdown** | Grouped actions | "Actions" menu pattern |
| **Date Range Picker** | Time range selection | Critical for APM — always present |
| **Select** | Dropdown selection | Single value |
| **Multiselect** | Multi-value selection | Tags, services, operations |
| **Autosuggest** | Type-ahead search | Use for service/operation search |
| **Toggle** | On/off settings | Binary switches |
| **Segmented Control** | View mode switching | Table/cards, absolute/relative time |

## Visualization Components

| Component | Use For | Notes |
|-----------|---------|-------|
| **Line Chart** | Time series metrics | Latency, error rate, throughput over time |
| **Bar Chart** | Categorical comparisons | Top N operations, error distribution |
| **Area Chart** | Volume over time | Request volume, stacked service breakdown |
| **Mixed Line Bar Chart** | Dual-axis visualization | Latency + request count |
| **Pie Chart** | Proportional breakdown | Use sparingly — bar charts usually better |

## Key Patterns for APM

### Hub-and-Spoke Navigation
Services page (hub) → Service detail (spoke) → Operation detail (sub-spoke)
Components: Side Navigation → Table → Split Panel

### Filterable Data Table
Property Filter + Table + Collection Preferences + Pagination
This is the most common pattern in CloudWatch APM consoles.

### Time-Range-Aware Dashboard
Date Range Picker (global) → Grid of Containers with charts + tables
All charts and tables respond to the same time range.

### Detail-on-Select
Table with selectable rows + Split Panel (bottom or side)
Click a row → details appear in the split panel without navigating away.

### Drill-Down Chain
Table → click row → new Table scoped to that row → click row → detail view
Breadcrumbs track the drill-down path.

## Design Tokens
- Spacing scale: 4px, 8px, 12px, 16px, 20px, 24px, 32px, 40px
- Font: Noto Sans (Amazon Ember for internal tools)
- Border radius: 8px (containers), 4px (inputs)
- Color: Use semantic tokens (awsui-color-*) not hex values
